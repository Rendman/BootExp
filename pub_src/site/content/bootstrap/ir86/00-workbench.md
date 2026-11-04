+++
title = "The IR workbench"
weight = 0
description = "Keep the working assembler and distinguish the virtual language from its first backend."
download = "IR86.ZIP"
+++

Begin with the completed BOOTASM and ASM86 collections. Keep BOOTASM.BAS, ASM86.ASM, the tested ASM86.COM, CHECK.BAT, and VIEW.BAS together. ASM86 must pass its published self-assembly check. At DOS preserve it:

```dos
COPY ASM86.COM ASMKEEP.COM
```

Run CHECK ASMKEEP and enter a source base name at its prompt. Require the assembler's OK and the checker's PASS. The completed ASM86 has the vocabulary and capacity to build every translator checkpoint directly.

## The language and the binding

IR source describes the virtual accumulator A and operations on declared storage. It does not name CPU registers or arrange operating-system calls. A runtime service returns a language value and updates a normalized status word. Ordinary arithmetic and comparisons do not replace that status.

The translator, backend, and runtime implementation in this collection are written for our 8086/8088 DOS workbench. Their assembly listings necessarily show target instructions. Those choices implement the language; they are not instructions an IR program must reproduce. The language reference separates the portable contract from this target profile.

The current build path is:

```text
NAME.IR -> IR86 with the 8086/DOS binding -> NAME.ASM -> ASM86 -> NAME.COM
```

IR86 emits assembly text. ASM86 encodes it. A successful translation cannot substitute for a successful assembly: require a fresh OK and PASS at both steps. ASM86 owns final address resolution and rejects duplicate or undefined names.

## Reuse the published reader

The first installment begins with the saved AS07.ASM from ASM86:

```dos
COPY AS07.ASM IR01.ASM
```

Its checked filename input, file reader, physical-line reader, and diagnostic printer are already working components. Follow each installment's exact edits and preserve the preceding source. Sources and expected outputs use ASCII, DOS CR/LF endings, and short disk names. A text editor must save no word-processor formatting codes.

For a small source, COPY CON T01.IR accepts keyboard input. Finish with Ctrl-Z and Enter. That keystroke ends input; it is not an instruction token. TYPE displays a saved text file.

## This DOS tool's filenames

At the translator prompt enter a base name of one through eight letters, digits, or underscores without path or extension. It reads NAME.IR and writes NAME.ASM. Use ordinary disk names, excluding DOS devices such as CON or NUL even with an extension. Use T-prefixed test names so their output is separate from the translator's own source.

These prompt and disk-name restrictions belong to the DOS tool. A file name passed to an IR runtime service is data in declared storage, interpreted by its environment binding. The examples use ordinary names supported by this binding.

## Translator memory on the DOS workbench

The native translator requires a full 64 KB segment and the normal entry SP=FFFEH. A failed check reports IR error 7. Its segment registers retain their DOS entry values. Fixed buffers are clear of the loaded image and high stack:

| Offsets | Translator use |
|---|---|
| 0000H–00FFH | DOS program segment prefix |
| 0100H–20FFH | Reserved native image area |
| 2200H–2278H | Physical source line and zero |
| 2300H–2310H | Current token and zero |
| 2400H–240BH | Console input buffer |
| 2500H–2510H | Saved name token |
| 2520H–2530H | Saved numeric spelling |
| 6000H–DFFFH | Assembly-text buffer |
| F000H–FFFFH | Kept clear for native stack use |

Generated DOS programs have their own segments. This backend also checks their normal full-segment entry arrangement. Neither that check nor this memory map is part of the processor-independent IR machine. A different backend supplies its own storage arrangement and calling convention.

The binding appends its runtime procedures and private data after the program's terminating path. Its private status, byte buffer, and file-handle table are separate from declared IR storage. Programs use ADDR and valid byte offsets rather than depending on those locations.

## Visible results

CHECK.BAT immediately observes the executed program's status and prints PASS or FAIL. TYPE inspects assembly text. VIEW.BAS reports a machine file's length and bytes: run GWBASIC VIEW.BAS, enter the complete filename, and use SYSTEM to return to DOS. Substitute the actual name of the period BASIC interpreter on your disk.

The first diagnostics are not complete translators. Follow their stated result and do not execute an output described as data only. Byte-input tests use a redirected file, so terminal echoing and line buffering cannot obscure the test.

A source rejection leaves an older assembly file untouched. An I/O failure during final creation or writing may leave partial output. Require a fresh OK before trusting any file. After the complete pipeline passes, preserve IR86.COM as IRKEEP.COM and retain its assembly source and the bootstrap tools.
