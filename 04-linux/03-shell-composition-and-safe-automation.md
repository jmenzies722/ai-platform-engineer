# Shell Composition and Safe Automation

A shell is most useful when small programs are connected with explicit data flow, quoting, and failure handling.

## Why it matters

An unquoted deployment path containing a space can turn one intended argument into two, while a failed command in the middle of a pipeline may still leave a success-looking final status. Those are not shell trivia: they decide whether automation changes the correct resources and whether CI reports failure. The safest script makes expansion, inputs, errors, and cleanup visible.

## How it works

The shell expands variables and globs before launching commands. Quotes control that expansion. Pipelines connect one command’s stdout to another’s stdin. Exit statuses communicate success or failure; scripts can branch on them. Temporary directories and traps make cleanup reliable.

The shell parses syntax, performs expansions, applies redirections, and launches built-ins or external commands. Parameter expansion yields text; outside quotes that text can undergo word splitting and pathname expansion, so `"$value"` is the normal way to preserve one argument. Pipelines connect descriptors, usually in separate processes, and the pipeline’s status policy determines which failures are visible. Conditional contexts deliberately test statuses and should not be confused with unexpected errors. `IFS= read -r` preserves lines without treating backslashes or surrounding whitespace as syntax. `--` ends option parsing for many tools when a filename might begin with a dash. A trap can centralize cleanup, but it runs in the shell contexts and signals the script actually receives. Once data becomes nested or requires complex recovery, a general-purpose language usually provides a clearer model.

## See it yourself

**Tiny Proof:** predict that `two words` remains one line inside angle brackets and that the `EXIT` trap removes the temporary directory on both normal completion and most shell-level errors. Quote removal should not appear in the printed data.

```bash
tmp=$(mktemp -d)
trap 'rm -rf "$tmp"' EXIT
printf '%s\n' alpha 'two words' beta > "$tmp/items"
while IFS= read -r line; do printf '<%s>\n' "$line"; done < "$tmp/items"
```

Expected observation: Quoting preserves the line containing a space, and the exit trap removes the temporary directory.

Limits of the shell composition and safe automation observation: The snippet does not make arbitrary filenames safe in every utility, prove that traps run after `SIGKILL`, or enable strict failure handling for a larger script. It demonstrates line-preserving input and scoped cleanup only.

## Where it shows up

A release script often composes artifact lookup, checksum verification, upload, and activation. If lookup fails but a pipeline reports only the last formatting command, the script can activate an old artifact. Capturing each boundary’s status, writing temporary output in one owned directory, and moving into place only after verification produces an all-or-nothing shape reviewers can reason about. Idempotent reruns then become a design goal rather than an accident.

## When it breaks

“No such file” with a visibly correct path often points to splitting, globbing, or a wrong working directory; a zero status with missing output suggests hidden pipeline failure; leftovers suggest cleanup did not cover the exit path. First rerun with controlled inputs and `printf '%q
'` or `set -x` in a non-secret test environment to inspect actual arguments and statuses. Never enable tracing where expansions contain credentials.

## Practice

**Build:** write a script that accepts exactly one directory, validates it, counts regular files, and removes its temporary workspace through a trap. **Break:** test a path with spaces, a filename beginning with `-`, a missing directory, and an injected failing pipeline stage. **Explain back:** describe parse, expansion, redirection, process launch, and exit status in order. Success means correct output and status for every case, no leaked temporary directory, and no unquoted data-bearing expansion.

## Check yourself

1. When does expansion occur?
2. Why is `for x in $(command)` unsafe for arbitrary lines?

## Sources

### REQUIRED

- [Bash manual](https://www.gnu.org/software/bash/manual/bash.html)

### RECOMMENDED

- [POSIX Shell Command Language](https://pubs.opengroup.org/onlinepubs/9799919799/utilities/V3_chap02.html)

### DEEP DIVE

- [ShellCheck wiki](https://www.shellcheck.net/wiki/)

## Next

Continue to [Users, Privilege, and Software Installation](./04-users-privilege-and-software-installation.md).
