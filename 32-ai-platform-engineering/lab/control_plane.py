"""Deterministic, standard-library AI control-plane simulator."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field


class Denied(ValueError):
    """The requested transition violates a platform invariant."""


def digest(value: str) -> str:
    return "sha256:" + hashlib.sha256(value.encode()).hexdigest()


@dataclass
class ControlPlane:
    events: list[dict] = field(default_factory=list)
    command_results: dict[tuple[str, str], dict] = field(default_factory=dict)

    def _record(self, principal: str, key: str, kind: str, **data: str) -> dict:
        identity = (principal, key)
        if identity in self.command_results:
            return self.command_results[identity]
        event = {
            "sequence": len(self.events) + 1,
            "principal": principal,
            "kind": kind,
            **data,
        }
        self.events.append(event)
        self.command_results[identity] = event
        return event

    def publish_corpus(
        self, principal: str, key: str, corpus: str, manifest: str
    ) -> dict:
        return self._record(
            principal,
            key,
            "corpus.published",
            tenant=principal,
            corpus=corpus,
            corpus_version=digest(manifest),
        )

    def publish_index(
        self,
        principal: str,
        key: str,
        corpus_version: str,
        index: str,
        expected_docs: int,
        indexed_docs: int,
    ) -> dict:
        corpus = self._latest(
            "corpus.published", principal, corpus_version=corpus_version
        )
        if corpus is None:
            raise Denied("corpus version is absent from the principal's namespace")
        if indexed_docs != expected_docs:
            raise Denied("index manifest count does not match expected corpus count")
        return self._record(
            principal,
            key,
            "index.promoted",
            tenant=principal,
            corpus_version=corpus_version,
            index=index,
            index_version=digest(f"{corpus_version}:{index}:{indexed_docs}"),
        )

    def register_model(
        self, principal: str, key: str, model_bytes: str, corpus_version: str
    ) -> dict:
        if self._latest(
            "corpus.published", principal, corpus_version=corpus_version
        ) is None:
            raise Denied("model lineage references an unavailable corpus")
        return self._record(
            principal,
            key,
            "model.registered",
            tenant=principal,
            model_digest=digest(model_bytes),
            corpus_version=corpus_version,
        )

    def evaluate(
        self, principal: str, key: str, model_digest: str, passed: bool
    ) -> dict:
        if self._latest(
            "model.registered", principal, model_digest=model_digest
        ) is None:
            raise Denied("evaluation subject is not registered to principal")
        return self._record(
            principal,
            key,
            "model.evaluated",
            tenant=principal,
            model_digest=model_digest,
            result="pass" if passed else "fail",
            suite_version="suite-v1",
        )

    def deploy(
        self, principal: str, key: str, model_digest: str, target: str
    ) -> dict:
        evaluation = self._latest(
            "model.evaluated", principal, model_digest=model_digest
        )
        if evaluation is None or evaluation["result"] != "pass":
            raise Denied("deployment requires passing evaluation for exact digest")
        previous = self._latest("deployment.promoted", principal, target=target)
        return self._record(
            principal,
            key,
            "deployment.promoted",
            tenant=principal,
            target=target,
            model_digest=model_digest,
            rollback_digest=previous["model_digest"] if previous else "",
        )

    def rollback(self, principal: str, key: str, target: str) -> dict:
        current = self._latest("deployment.promoted", principal, target=target)
        if current is None or not current["rollback_digest"]:
            raise Denied("no compatible rollback target is recorded")
        return self._record(
            principal,
            key,
            "deployment.rolled_back",
            tenant=principal,
            target=target,
            model_digest=current["rollback_digest"],
            replaced_digest=current["model_digest"],
        )

    def _latest(self, kind: str, principal: str, **fields: str) -> dict | None:
        for event in reversed(self.events):
            if (
                event["kind"] == kind
                and event["principal"] == principal
                and all(event.get(name) == value for name, value in fields.items())
            ):
                return event
        return None

    def normalized_events(self) -> str:
        return "\n".join(
            json.dumps(event, sort_keys=True, separators=(",", ":"))
            for event in self.events
        )
