+++
title = "The streaming seed workbench"
weight = 0
description = "Preserve ASM0 and construct a streaming assembler inside its published bounds."
download = "ASM1.ZIP"
download_group = "tools/asm1"
reader_names = 1
url = "/bootstrap/asma0/00-workbench/"
+++

I put the tested ASM0 copy aside before opening its source again. Beside the routine notes I draw a map of its memory: code, working values, buffers, names and stack. As I move those boundaries, I want to be able to find both the bytes and the source that made my last working assembler.

## Command-line filenames

```dos
CHECK ASM1 INPUT.ASM OUTPUT.COM
```

DOS supplies the names in the PSP command tail. The native entry binding copies them into owned zero-terminated storage before file services. CHECK.BAT forwards the arguments and reports status immediately. No arguments select SOURCE.ASM and RESULT.COM. Use unquoted 8.3 disk names in the current directory: letters, digits, underscore and hyphen, with an optional extension. Paths, switches, excess arguments and overlong names are rejected. Keep selected files distinct from each other and from ASMA.TMP and RESULT.BAK. Those temporary/backup names remain reserved.

Success reports the selected result name. Rejected source preserves that accepted result; recovery rules apply to the selected name. Early diagnostic writers may deliberately retain a temporary file for inspection, as stated in their lesson.

Begin with the completed BOOTASM and ASM0 collections. Keep BOOTASM.BAS, ASM0.ASM, VIEW.BAS, CHECK.BAT, and the tested ASM0.COM. Use the same DOS 3.10 and period GW-BASIC workbench. GWBASIC in these instructions means the interpreter's actual disk name; note its startup banner.

## Preserve the builder

```dos
COPY ASM0.COM ASMKEEP.COM
```

ASMKEEP is the original ASM0 and uses fixed SOURCE.ASM and RESULT.COM. It accepts an 8192-byte image, 256 definitions, 4000 physical lines, and 120 characters per line. The six opening A01A through A01F sources and every A01 through A12 source fit that builder. Copy the checkpoint to SOURCE.ASM, run CHECK ASMKEEP, require the stated OK count and PASS, then copy RESULT.COM to the checkpoint executable name.

Each article copies the preceding source under the next filename and gives edits in the order they should be applied. Find the named label, including its colon, and confirm the complete definition on its own source line. Follow the unchanged locator block to the edit point; type only the insertion or replacement. No physical line numbers are needed, and blank lines or comment-only notes may differ in your copy. Preserve both the source and executable after each stopping test. The article number and saved source name are separate locators; keep the printed disk filenames exactly as given.

## The opening checkpoints

Begin with A01A, then A01B, A01C, A01D, A01E and A01F, before A01. Each is a separate article and saved source. A01A and A01B retain fixed SOURCE.ASM/RESULT.COM work names. A01C is a command-reader probe: it expects two names, opens no files and reports only status. A01D restores the assembly driver and accepts either no arguments or two names. A01E adds the result spelling to its report; A01F adds input-handle state. A01 then introduces XOR.

ASMKEEP always uses its fixed work names to build these checkpoints. COPY the selected source to SOURCE.ASM before CHECK ASMKEEP, and save the accepted RESULT.COM under the printed checkpoint name.

## Select work files

From A01D onward, pass filenames directly:

```dos
CHECK A01 T01.ASM RESULT.COM
```

The checkpoint executable is the diagnostic or assembler being tested. RESULT.COM is its output, which must be saved under a separate name before another assembly. The byte-copy exercises explicitly inspect their output as data; execute an output only when its article identifies a complete program.

| Name | Role |
|---|---|
| SOURCE.ASM | Disk source reopened for both passes |
| RESULT.COM | Published result |
| ASMA.TMP | Temporary output owned by the current run |
| RESULT.BAK | Previous result during publication |

Reserved-name protection refuses a completed seed run when a temporary or backup name already exists. Inspect or rename a recovery file before proceeding. The copy diagnostics state when their own deliberately created temporary file should be deleted.

## Memory and inspection

The completed seed requires a full 64 KB DOS segment and entry SP=FFFEH. Its source, scalar state, bounded buffers, 2048 symbol records, and high stack occupy that segment. It requests no extra DOS memory blocks. It reads and writes 1024-byte blocks, rather than retaining a whole input or target image.

Use plain ASCII, DOS CR/LF endings, and 8.3 disk names. A text editor must not insert word-processor formatting. COPY CON finishes with Ctrl-Z and Enter. Keep the source unchanged throughout both passes. The input must be a reopenable disk file.

Run GWBASIC VIEW.BAS and enter the full filename to check both length and hexadecimal bytes; SYSTEM returns to DOS. CHECK.BAT immediately prints PASS or FAIL from an executable's status. It does not judge the BASIC interpreter. Empty output is valid for inspection only.

## The seed handoff

A12.ASM is ASM1.ASM. ASMKEEP builds the 3740-byte executable; ASM1 must then reproduce it through both self-assembly comparisons. Save that tested ASM1.COM separately. The ASM86 workbench begins by copying this completed source, so the seed's routines need not be typed again.
