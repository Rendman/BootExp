+++
title = "The RILL0 workbench"
weight = 0
description = "Keep the tested tools and follow each source file through the complete chain."
download = "RILL0.ZIP"
download_group = "tools/rill0"
reader_names = 1
+++

Begin with the completed BOOTASM, ASM0, and IR86 collections. Preserve the working native assembler and translator under separate names:

```dos
COPY ASM0.COM ASMKEEP.COM
COPY IR86.COM IRKEEP.COM
```

Keep their sources, BOOTASM.BAS, CHECK.BAT, and VIEW.BAS. The completed tools directly build every compiler checkpoint; their instruction vocabulary and limits are sufficient without a preparatory change.

## Build a compiler checkpoint

The compiler's implementation files have extension **.IR**. RILL programs supplied to that compiler have extension **.RIL**. Keep that distinction when entering names.

For example, save the first printed listing as R01.IR, run `CHECK IRKEEP`, and enter R01 at `IR source name:`. Require the printed assembly-text count and PASS. Run `CHECK ASMKEEP` and enter R01 at `Source name:`. Require its machine-byte count and PASS. R01.COM is then the program to run.

The articles print exact changes from the preceding saved IR file. Apply them from the bottom upward. Physical positions are locators; the nearby labels and old context identify the actual insertion points. Save both the IR source and its tested executable at every stop.

The early programs are diagnostics, not complete RILL compilers. Their articles state whether they read a byte stream, inspect SOURCE.RIL, recognize a program, or create a result. A file containing diagnostic test text is not thereby a valid RILL program.

## The compiler's two work files

The completed compiler reads **SOURCE.RIL** in the current directory and writes **RESULT.IR** there. These fixed names keep filename prompting out of the parser. COPY selects a saved program:

```dos
COPY HELLO.RIL SOURCE.RIL
CHECK RILL0
```

Success prints `OK RESULT.IR nnnnn`, followed by the checker's PASS. The number is the IR file length in bytes, including CR/LF. It is not an executable size. Copy the accepted result to the base name used for the program:

```dos
COPY RESULT.IR HELLO.IR
CHECK IRKEEP
```

Enter HELLO. Require IR86's own OK and PASS. Then run `CHECK ASMKEEP`, enter HELLO, and require the assembler's OK and PASS. Only then run `CHECK HELLO`.

Use ordinary disk files. SOURCE.RIL must be readable, and RESULT.IR may be replaced. Syntax and input errors leave an older result untouched because the compiler buffers all output and closes the accepted source before creating the result. A create, write, or final close failure may leave partial output. Require a fresh compiler OK; the existence of an old file is not evidence of success.

## Typing source text

Use an editor which saves plain ASCII, or `COPY CON NAME.RIL`. For COPY CON, finish the last line with Enter, then press Ctrl-Z and Enter. The Ctrl-Z keystroke ends console input. A zero byte is not a valid source character. Source files use DOS CR/LF; LF text is also accepted. The line report counts LF bytes, so a bare CR is whitespace rather than a new numbered line.

RILL is case-sensitive. Keywords and the single-letter variable names use lowercase letters. Numeric literals use unsigned decimal spelling. Whitespace and `//` comments separate tokens. There are no quoted strings or character constants: `putc(65);` writes A.

The first program in the collection is entered as IR text rather than RILL. In its IR source, case is ignored as specified by the IR86 reference. The RILL scanner itself does not fold case.

## Visible checks

CHECK.BAT runs a complete program and immediately prints PASS for zero status or FAIL for nonzero status. The deliberately nonzero exit exercise must report FAIL. An error test must print its expected diagnostic and FAIL; an unexpected PASS is a failed rejection test. DOS may echo the batch command before ECHO OFF takes effect.

TYPE displays RESULT.IR and generated assembly. VIEW.BAS reports machine-file length and hexadecimal bytes; enter the complete filename at its prompt and use SYSTEM to return to DOS. Inspect a file's stated full length even when an article prints only its leading bytes.

For byte input, create a small KEY.TXT and run the completed program with `<KEY.TXT`. This avoids terminal buffering and echo. A program's getc() preserves all redirected byte values, including Control-Z; the compiler's SOURCE.RIL reader treats Control-Z as text termination.

## Values, storage, and limits

RILL values are unsigned sixteen-bit words with wrapping arithmetic. The compiler uses the IR runtime's opaque file handles and pointers formed by ADDR. Neither its source nor the language requires a native register convention.

The first backend still has its documented DOS requirements: a normal full 64 KB program segment, entry SP=FFFEH, and the reserved native stack area. Those are requirements for this workbench, not RILL value semantics. The compiler image is 5,173 bytes. Its data includes the 1024-byte output buffer, a small explicit parser stack, and bounded variable marks.

The reference gives the complete grammar, helper interfaces, resource limits, and diagnostics. Preserve a tested final R29.COM as RILL0.COM, and then preserve RILL0.COM as RLKEEP.COM. Retain RILL0.IR and all preceding tools alongside them.
