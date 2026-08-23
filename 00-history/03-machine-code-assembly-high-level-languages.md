# Machine Code to Assembly to High-Level Languages

Programming languages let humans describe work at useful levels while translators produce instructions a machine can execute.

## Why it matters

**Prerequisite:** [Why Software Exists](./02-why-software-exists.md).

Numeric opcodes exposed every machine detail and made even small programs hard to inspect. Assembly gave instructions names, but programs remained tied to a processor and demanded careful bookkeeping.

High-level languages let programmers express formulas, data, and control while a compiler or runtime handles translation. LLVM, just-in-time compilers, CUDA toolchains, and model compilers continue the same bargain: easier expression in exchange for a translation layer that must be trusted.

## How it works

Each language is a contract translated into a lower-level contract. Higher levels compress intent; lower levels reveal layout, calling, and machine cost.

Lexing and parsing create syntax structures; semantic analysis checks meaning; lowering produces IR; optimization transforms equivalent programs; code generation selects instructions; linking resolves symbols; loading maps an executable and libraries into a process.

An ISA abstracts microarchitecture, while an ABI specifies calling conventions, binary layout, and system interfaces. Undefined behavior lets compilers optimize aggressively but invalidates reasoning based on accidental machine behavior. JITs trade startup work for runtime specialization.

## Vocabulary

- **Opcode:** The part of an instruction that identifies the operation.
- **Mnemonic:** A readable symbolic name for a machine operation.
- **Assembler:** A translator from assembly language to machine code.
- **Compiler:** A translator from one program representation to another.
- **Intermediate representation (IR):** A compiler's internal form between source and target code.
- **Object file:** Compiled machine code and metadata not yet fully linked into an executable.
- **Linker:** A tool that resolves symbols and combines object files and libraries.
- **Loader:** OS/runtime machinery that maps a program into a process for execution.
- **ISA:** The machine instructions, registers, and behavior software may rely on.
- **ABI:** Binary-level conventions for calls, data layout, executable formats, and system interfaces.
- **JIT:** Just-in-time compilation performed during execution.
- **Undefined behavior:** A source-language case for which the specification imposes no required result.

## See it yourself

```bash
printf 'int square(int x){return x*x;}\n' > /tmp/square.c
cc -S -O2 /tmp/square.c -o /tmp/square.s
cc -c /tmp/square.c -o /tmp/square.o
objdump -d /tmp/square.o
```

Predict whether the assembly and object disassembly will look identical before running the commands. Both should express the same multiplication, but labels and directives disappear or change once instructions are encoded. This supports the distinction among source, assembly, and machine code. One compiler invocation does not establish portability, correctness of every optimization, or the behavior of another ISA.

## Where it shows up

A Python model call may enter a framework graph, lower into an intermediate representation, select fused GPU kernels, and finally execute device instructions. An unsupported operation can break the graph and return work to the Python runtime. The source still produces a correct answer, but throughput collapses because the translation path changed. Compiler artifacts and profiles, not source appearance alone, reveal the boundary.

## When it breaks

A common symptom is code that works in a debug build but crashes or changes result when optimized. Undefined behavior, an ABI mismatch, architecture-specific code generation, or a JIT deoptimization are plausible mechanisms. First preserve both artifacts and compare compiler diagnostics, symbols, target triples, and the smallest generated representation where behavior diverges.

## Practice

### Observe

Compile one function at `-O0` and `-O2`; compare assembly, binary size, and output. Explain which source guarantees permit each transformation.

### Build

Write a tiny expression compiler that emits stack-machine instructions for constants, addition, multiplication, and variables.

### Break

Feed the compiler an unknown symbol, divide-by-zero expression, malformed syntax, and deep nesting. Add bounded, stage-specific errors.

### Say it out loud

Trace one function from source text to a loaded process.

**Success:** You should distinguish language semantics, ISA, ABI, linking, and loading without claiming that source maps directly to instructions.

## Check yourself

1. What differs among ISA, ABI, and language semantics?
2. Why use IR?
3. Why can optimization expose undefined behavior?

### Interview stretch

- Diagnose “works in debug, fails in release.”
- Why can a JIT outperform ahead-of-time code?
- What does an ABI make independently evolvable?

## Sources

### REQUIRED

- “The FORTRAN Automatic Coding System” — Backus et al. [Computer History Museum PDF](https://archive.computerhistory.org/resources/text/Fortran/102663113.05.01.acc.pdf). Shows the case for practical high-level compilation.

### RECOMMENDED

- “System V Application Binary Interface” — Linux Foundation. [ABI specification](https://refspecs.linuxfoundation.org/elf/x86_64-abi-0.99.pdf). Defines executable and calling conventions.

### DEEP DIVE

- “LLVM Language Reference Manual” — LLVM Project. [Official documentation](https://llvm.org/docs/LangRef.html). Demonstrates a modern compiler IR contract.

## Next

Continue with [./04-evolution-of-programming-languages.md](./04-evolution-of-programming-languages.md).
