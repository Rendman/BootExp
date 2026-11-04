+++
title = "The IR workbench"
weight = 0
description = "Keep the working assembler, reuse its reader, and distinguish translation from assembly."
download = "IR86.ZIP"
+++

Begin with the completed BOOTASM and ASM86 collections. Keep BOOTASM.BAS, ASM86.ASM, and the tested ASM86.COM together with CHECK.BAT and VIEW.BAS. ASM86 must already pass its published self-assembly check. The completed tools have the instruction forms and capacity required for this construction.

At DOS preserve the known working assembler:

```dos
COPY ASM86.COM ASMKEEP.COM
```

CHECK.BAT immediately observes the executed program's DOS status and prints PASS or FAIL. Run `CHECK ASMKEEP`, then enter a source base name at `Source name:`. A successful assembly reports its machine-byte count and returns zero. Do not execute an older .COM after a failed build.

## Start with a reader already on the disk

Retain AS07.ASM from the ASM86 collection. It contains the checked filename input, handle-based file reader, physical-line routine, error report, and diagnostic printer. The first installment begins with:

```dos
COPY AS07.ASM IR01.ASM
```

Its printed edits turn that source into the first IR workbench diagnostic. The same directory may contain the later ASM86 checkpoints when a familiar routine is useful to copy. Complete source links provide each saved stopping point, while the articles show exactly what to change in the preceding file.

All sources are plain ASCII with DOS CR/LF line endings. Use a text editor which saves no formatting codes. For a small fixture, `COPY CON T01.IR` accepts keyboard input; finish with Ctrl-Z and Enter. The keystroke ends input and is not a language instruction. TYPE displays a saved text file.

## Two translation steps

The completed path is:

```text
NAME.IR  ->  IR86  ->  NAME.ASM  ->  ASM86  ->  NAME.COM
```

IR86 asks for `NAME`, reads NAME.IR, and produces assembly text in NAME.ASM. It does not emit an executable. ASM86 then reads that assembly text and creates NAME.COM. Require an OK and PASS from each tool. The translator checks its language and resource rules; ASM86 owns address resolution and also rejects duplicate or undefined symbols.

An IR source name has one through eight letters, digits, or underscores. Supply no path or extension. Use ordinary disk filenames, excluding DOS devices such as CON, NUL, PRN, AUX, COM1, and LPT1 even with an extension. Input is .IR; output is .ASM with the same base name. Use the T-prefixed fixture names so that test output is separate from the translator's own assembly source.

## The translator's segment

The translator requires a complete 64 KB program segment with the normal entry SP=FFFEH. Its entry check reports IR error code 7 if that stack arrangement is absent. DS, ES, and SS retain the DOS entry segment. Fixed work areas are separate from the loaded program and its stack:

| Offsets | Use inside the translator |
|---|---|
| 0000H–00FFH | DOS program segment prefix |
| 0100H–20FFH | Reserved image area within ASM86's output bound |
| 2200H–2278H | Physical source line and zero terminator |
| 2300H–2310H | Current token and zero terminator |
| 2400H–240BH | DOS console line-input buffer |
| 2500H–2510H | Saved name token |
| 2520H–2530H | Saved numeric spelling |
| 6000H–DFFFH | Assembly-text output buffer |
| F000H–FFFFH | Kept clear for the high stack |

The native translator's calls are shallow and nonrecursive. It buffers only assembly text, not the input file or a machine-code image. Output is written after successful input validation; a source error leaves an older .ASM untouched. A create, write, or close failure can leave a partial file, so a fresh OK remains necessary.

Generated programs are separate DOS programs with their own segments. Their header checks the same full-segment entry arrangement and returns status seven if it fails. The translator's fixed work buffers are not runtime storage assigned to those programs. A program's BYTE, WORD, and BUFFER declarations provide initialized storage in its own image.

## Inspect before execution

TYPE checks assembly text. VIEW.BAS checks a machine file's length and hexadecimal bytes: run `GWBASIC VIEW.BAS`, enter the complete .COM filename, then use SYSTEM to return to DOS. Use the interpreter supplied with the period DOS workbench; substitute its actual executable name if it differs from GWBASIC.

The first diagnostics are tools, not complete translators. Follow each installment's stated test. A fixture expressly described as data belongs in the viewer. Run CHECK on an emitted .COM only when the installment identifies it as a complete executable.

After the completed translator passes the pipeline check, preserve IR86.COM as IRKEEP.COM and retain its assembly source. The source collection also contains the identical published BOOTASM.BAS and ASM86.ASM, so the means to rebuild the tools remain on the disk.
