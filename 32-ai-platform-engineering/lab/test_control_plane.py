import hashlib
import unittest

from control_plane import ControlPlane, Denied, digest


class ControlPlaneTest(unittest.TestCase):
    def setUp(self) -> None:
        self.plane = ControlPlane()
        self.corpus = self.plane.publish_corpus(
            "tenant-a", "corpus-1", "support", "doc-1\ndoc-2"
        )["corpus_version"]

    def test_successful_lineage_and_byte_stable_replay(self) -> None:
        self.plane.publish_index(
            "tenant-a", "index-1", self.corpus, "support-v1", 2, 2
        )
        model = self.plane.register_model(
            "tenant-a", "model-1", "model-v1", self.corpus
        )["model_digest"]
        self.plane.evaluate("tenant-a", "eval-1", model, True)
        self.plane.deploy("tenant-a", "deploy-1", model, "staging")
        evidence = self.plane.normalized_events()
        self.assertEqual(
            hashlib.sha256(evidence.encode()).hexdigest(),
            "aad8e9e757e6baba7f28ffc3d6cf5ea35b622b540aaa5069dcb3ee18d61bc2ee",
        )

    def test_tenant_namespace_is_enforced_before_indexing(self) -> None:
        with self.assertRaisesRegex(Denied, "principal's namespace"):
            self.plane.publish_index(
                "tenant-b", "index-1", self.corpus, "stolen", 2, 2
            )

    def test_partial_index_cannot_promote(self) -> None:
        with self.assertRaisesRegex(Denied, "manifest count"):
            self.plane.publish_index(
                "tenant-a", "index-1", self.corpus, "partial", 2, 1
            )
        self.assertFalse(
            any(event["kind"] == "index.promoted" for event in self.plane.events)
        )

    def test_idempotent_command_has_one_effect(self) -> None:
        first = self.plane.register_model(
            "tenant-a", "model-1", "model-v1", self.corpus
        )
        again = self.plane.register_model(
            "tenant-a", "model-1", "different-bytes", self.corpus
        )
        self.assertIs(first, again)
        self.assertEqual(
            1,
            sum(event["kind"] == "model.registered" for event in self.plane.events),
        )

    def test_stale_evaluation_cannot_authorize_changed_digest(self) -> None:
        model = self.plane.register_model(
            "tenant-a", "model-1", "model-v1", self.corpus
        )["model_digest"]
        self.plane.evaluate("tenant-a", "eval-1", model, True)
        with self.assertRaisesRegex(Denied, "exact digest"):
            self.plane.deploy(
                "tenant-a", "deploy-1", digest("model-v2"), "staging"
            )

    def test_rollback_restores_previous_approved_digest(self) -> None:
        first = self.plane.register_model(
            "tenant-a", "model-1", "model-v1", self.corpus
        )["model_digest"]
        second = self.plane.register_model(
            "tenant-a", "model-2", "model-v2", self.corpus
        )["model_digest"]
        for number, model in enumerate((first, second), 1):
            self.plane.evaluate("tenant-a", f"eval-{number}", model, True)
            self.plane.deploy("tenant-a", f"deploy-{number}", model, "staging")
        rollback = self.plane.rollback("tenant-a", "rollback-1", "staging")
        self.assertEqual(first, rollback["model_digest"])
        self.assertEqual(second, rollback["replaced_digest"])


if __name__ == "__main__":
    unittest.main()
