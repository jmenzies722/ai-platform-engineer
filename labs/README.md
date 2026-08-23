# Labs

Labs turn a conceptual model into observable evidence. Every lab follows predict → establish baseline → inspect → build → break → debug → recover → explain. Completion means you can account for behavior, not that commands exited successfully.

## Lab Index

| Lab | Domain | Status | Core evidence |
|---|---|---|---|
| [Inspect How a Python Process Executes](01-software-execution/README.md) | Software Foundations | Ready | Process identity, `/proc` state, memory map, descriptors, scheduler/resource observations |

## Working Rules

- Run unfamiliar commands in a disposable environment first.
- Read commands before execution; never paste secrets into evidence.
- Predict output and failure signatures before observing them.
- Preserve only relevant output, environment/version context, and timestamps.
- Stop when safety, cost, or blast-radius assumptions are invalid.
- Use [templates/LAB.md](../templates/LAB.md) for new labs.
