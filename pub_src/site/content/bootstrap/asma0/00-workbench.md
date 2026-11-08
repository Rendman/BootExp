+++
title = "The streaming seed workbench"
weight = 0
description = "Preserve ASM0 and construct a streaming assembler inside its published bounds."
download = "ASM1.ZIP"
download_group = "tools/asm1"
reader_names = 1
+++

Begin with the completed BOOTASM and ASM0 collections. Keep BOOTASM.BAS, ASM0.ASM, VIEW.BAS, CHECK.BAT, and the tested ASM0.COM. Use the same DOS 3.10 and period GW-BASIC workbench. GWBASIC in these instructions means the interpreter's actual disk name; note its startup banner.

## Preserve the builder

```dos
COPY ASM0.COM ASMKEEP.COM
```

ASMKEEP is the original ASM0 and uses fixed SOURCE.ASM and RESULT.COM. It accepts an 8192-byte image, 256 definitions, 4000 physical lines, and 120 characters per line. Every A01 through A12 source fits that builder. Copy the checkpoint to SOURCE.ASM, run CHECK ASMKEEP, require the stated OK count and PASS, then copy RESULT.COM to the checkpoint executable name.

Each article copies the preceding source under the next filename and gives exact edits from the bottom upward. Preserve both the source and executable after each stopping test. The article number and saved source name are separate locators; keep the printed disk filenames exactly as given.

## Fixed work files

The new checkpoints select their source with COPY:

```dos
COPY T01.ASM SOURCE.ASM
CHECK A01
```

A01.COM is the diagnostic or assembler being tested. RESULT.COM is its output, which must be saved under a separate name before another assembly. The byte-copy exercises explicitly inspect their output as data; execute an output only when its article identifies a complete program.

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

A12.ASM is ASM1.ASM. ASMKEEP builds the 3302-byte executable; ASM1 must then reproduce it through both self-assembly comparisons. Save that tested ASM1.COM separately. The ASM86 workbench begins by copying this completed source, so the seed's routines need not be typed again.
