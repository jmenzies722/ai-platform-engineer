# AI Platform Engineering from First Principles

This is a working engineering fieldbook from first program to Staff AI Platform Engineer. It teaches the systems beneath modern AI platforms: computation, software, operating systems, networks, data, cloud infrastructure, reliability, machine learning, accelerators, model serving, platform control planes, and agent execution.

The repository is intentionally more than a reading list. Lessons establish the mechanism. Labs make the mechanism observable. Incidents remove the answer key and ask you to recover from evidence. Projects combine several domains under production constraints. Interview practice tests whether you can explain and adapt what you have actually built.

## Begin

1. Follow [START-HERE.md](START-HERE.md).
2. Read [HOW-TO-LEARN.md](HOW-TO-LEARN.md).
3. Start [00-history/01-origins-of-computing.md](00-history/01-origins-of-computing.md).
4. Run the first demonstration before reading further.

If you already work in engineering, use the stage gates in [ROADMAP.md](ROADMAP.md). Do not skip a prerequisite because its title looks familiar. Skip it when you can produce the listed evidence.

## Learn by evidence

Reading introduces a subject. Competence means you can:

- explain the mechanism without borrowed wording;
- build a small working version;
- diagnose a controlled failure from evidence;
- define safe operation and recovery;
- defend a design under explicit constraints.

Record that evidence in [PROGRESS.md](PROGRESS.md). Use [TEACH-BACK.md](TEACH-BACK.md) when an idea feels familiar but is still hard to explain.

Major technologies are studied from nine practical viewpoints:

- the problem that made the technology necessary;
- the contract it exposes and the concepts needed to use it;
- the mechanism and internal state that make the contract work;
- a small build that proves the mechanism;
- controlled failures that expose its limits;
- diagnosis from logs, metrics, traces, state, and system tools;
- safe operation, recovery, security, and cost;
- design choices under explicit constraints.

These viewpoints are expressed in lessons and exercises, not as a memorized slogan. Some topics need more internals; others need more operational judgment.

## Navigate

- [CURRICULUM.md](CURRICULUM.md) lists the complete module path.
- [tracks/README.md](tracks/README.md) composes those modules into role paths.
- [ROADMAP.md](ROADMAP.md) groups modules by capability.
- [assessments/README.md](assessments/README.md) defines competency gates across Explain, Build, Debug, Operate, and Design.
- [CONCEPT-INDEX.md](CONCEPT-INDEX.md) finds the best entry point for a concept.
- [GLOSSARY.md](GLOSSARY.md) defines recurring terms.
- [labs/README.md](labs/README.md) indexes guided engineering labs.
- [incidents/README.md](incidents/README.md) contains production incident drills with separate solutions.
- [case-studies/README.md](case-studies/README.md) provides staged decisions from incomplete evidence.
- [projects/README.md](projects/README.md) contains portfolio-grade integration briefs.
- [interview/README.md](interview/README.md) turns demonstrated competence into interview practice.
- [certs/README.md](certs/README.md) contains optional certification overlays, not separate courses.
- [cheatsheets/README.md](cheatsheets/README.md) provides high-signal operator aids.
- [architecture/README.md](architecture/README.md) collects system views and design review prompts.
- [REFERENCES.md](REFERENCES.md) is the authoritative source shelf.
- [00-history/README.md](00-history/README.md) explains why the stack took its present shape.
- [01-software-foundations/01-how-software-actually-executes.md](01-software-foundations/01-how-software-actually-executes.md) traces code through a real machine.
- [labs/01-software-execution/README.md](labs/01-software-execution/README.md) turns that model into observable evidence.

## What complete means

A checked box is not the finish line. For a domain you intend to claim, you should be able to:

1. explain the useful abstraction and the machinery beneath it;
2. build a reduced but working version;
3. break an assumption safely and identify the resulting evidence;
4. recover or roll back without creating a second incident;
5. operate it with meaningful telemetry, limits, access controls, and cost awareness;
6. defend a design and name the conditions that would change your decision;
7. teach the model clearly to another engineer.

Start small. Make one claim observable, explain what the observation does not prove, and continue.
