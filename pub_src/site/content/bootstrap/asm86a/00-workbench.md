+++
title = "The streaming assembler workbench"
weight = 0
description = "Preserve the preceding builder and keep fixed work files under control."
download = "ASM86A.ZIP"
+++

Begin with the completed BOOTASM and ASM86 collections. Keep their plain ASCII sources, the tested ASM86 executable, VIEW.BAS, and CHECK.BAT. Use the same DOS 3.10 and period GW-BASIC workbench. GWBASIC below means the interpreter's actual disk name; DOS and BASIC version numbers are independent.

## Preserve the preceding assembler

ASM86 was built with BOOTASM.BAS and proved by self-assembly. Preserve it:

```dos
COPY ASM86.COM ASMKEEP.COM
```

Run CHECK ASMKEEP and enter an ordinary source base name at its prompt. The executable accepts an 8,192-byte image, 256 definitions, and its published small language. Every A01 through A12 source is built by this unchanged assembler. Do not replace ASMKEEP.COM with an incomplete checkpoint.

Each article gives exact edits to a copy of the preceding source. Apply edits from the bottom upward so old physical positions remain useful. Keep the printed context and nearby labels as well as the numeric position in view. Save the complete source and executable after each successful check.

## Fixed names for the new tool

The new checkpoint does not ask for a filename. Select its input with COPY:

```dos
COPY T01.ASM SOURCE.ASM
CHECK A01
```

A successful assembly writes RESULT.COM. Save that file under its own name before another assembly. The checkpoint's own executable is A01.COM, not RESULT.COM. In particular, after ASMA0 builds A13 from SOURCE.ASM, copy RESULT.COM to A13.COM before using A13 to process a test.

| Name | Meaning |
|---|---|
| SOURCE.ASM | Disk input, reopened for each pass |
| RESULT.COM | Last published result |
| ASMA.TMP | Owned temporary output |
| RESULT.BAK | Previous result during publication |

The early byte-copy diagnostics explicitly inspect ASMA.TMP or RESULT.COM as data. They are executable diagnostics, but their copied output is not a program. Later encoding fixtures also remain data unless the article expressly calls them complete programs.

At the seed handoff preserve ASMA0.COM. It builds A13 through A40 with the fixed names above. At the final handoff preserve ASM86A.COM as ASMAKEEP.COM. ASMKEEP and ASMAKEEP are different tools with different filename interfaces.

## Disk, memory, and inspection

Use an ordinary working directory on the hard disk, with room for sources, preserved tools, and both a temporary result and its backup. Spread saved sources across labeled disks if necessary. The whole collection need not fit one floppy. The complete assembler retains a 64 KB main segment and allocates 328 KiB of symbol workspace, for 392 KiB before DOS, environment, and allocation overhead. Keep resident programs out of the workbench when memory is scarce. An allocation failure must return FAIL before replacing output.

Sources use ordinary ASCII, DOS CR/LF endings, and 8.3 disk names. Use COPY CON for small fixtures; Ctrl-Z and Enter finish the file. A text editor is useful for growing sources, but must not insert word-processor formatting. The source must remain unchanged during both assembly passes. Console devices and pipes are not a substitute for the reopenable source disk file.

Run GWBASIC VIEW.BAS, enter the complete disk filename, and check both length and hexadecimal bytes. SYSTEM returns to DOS. CHECK.BAT immediately reports PASS or FAIL from a complete COM program's DOS status; it is not a checker for the BASIC interpreter itself. An empty output file can be inspected but must not be executed.

## Recovery files

Once reserved-name protection is installed, a pre-existing ASMA.TMP or RESULT.BAK prevents a new run. TYPE text files or inspect binary files with VIEW.BAS; compare preserved executable copies before deciding what to keep. Rename a recovery file to an unused name rather than blindly deleting it. The articles identify the temporary files deliberately created by their tests.

Ordinary source rejection leaves the accepted RESULT.COM unchanged. Publication failures can require recovery from the temporary or backup names. A failure is never permission to execute an old result as if it were new. Require a fresh OK and PASS at each build step.
