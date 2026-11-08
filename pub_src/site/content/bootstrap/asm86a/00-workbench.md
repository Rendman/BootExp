+++
title = "The larger assembler workbench"
weight = 0
description = "Begin with the verified ASM1 source and preserve its executable as the builder."
download = "ASM86.ZIP"
download_group = "tools/asm86"
reader_names = 1
+++

Begin with the completed ASM1 collection and its two matching self-assembly generations. Keep ASM1.ASM, ASM1.COM, VIEW.BAS, and CHECK.BAT. ASM1 is the fixed-file streaming seed; ASMKEEP.COM remains the earlier fixed-file ASM0.

## Begin with the seed source

The first construction article uses A13.ASM. Start from the completed seed:

```dos
COPY ASM1.ASM A13.ASM
```

Apply the printed edits from the bottom upward. Their old physical positions refer to the unchanged ASM1 source. The article numbering starts at one in this collection; saved checkpoint names continue from A13 through A40 so the disk handoff stays explicit.

Build the edited source with the preserved seed:

```dos
COPY A13.ASM SOURCE.ASM
CHECK ASM1
COPY RESULT.COM A13.COM
```

Require the stated OK count and PASS **before** copying the result. ASM1 writes RESULT.COM; save the checkpoint executable as A13.COM before using it to process a test. Every construction checkpoint in this collection is built by ASM1. Its source uses only the seed's language, even while implementing richer accepted forms.

## Files and memory

| Name | Role |
|---|---|
| SOURCE.ASM | Disk input reopened for each pass |
| RESULT.COM | Last published result |
| ASMA.TMP | Owned temporary output |
| RESULT.BAK | Previous result during publication |

Keep sources and preserved tools in an ordinary hard-disk directory, with room for both the temporary file and backup. Inspect any existing recovery file before another run. A source rejection must leave RESULT.COM unchanged; a publication failure can require recovery from the named temporary or backup.

The first additions retain the seed buffers while allocated-record helpers are tested. The complete assembler retains a 64 KB main segment and allocates eight 40 KiB symbol pages plus an 8 KiB lookup block: 392 KiB before DOS, environment, and allocation overhead. Allocation failure must report FAIL before replacing a result. Code remains near code in the main segment; allocated workspace does not enlarge the target COM image.

## Read, inspect, and preserve

Use DOS 3.10 and the same period BASIC interpreter as the preceding collections. Plain ASCII sources use DOS CR/LF and 8.3 names. Keep the source unchanged through both passes. Console devices and pipes are not substitutes for the reopenable source file.

VIEW.BAS reports file length and hexadecimal bytes; SYSTEM returns from BASIC to DOS. CHECK.BAT immediately reports executable status. Encoding fixtures are inspected as data unless an article explicitly identifies a complete program. Do not execute an empty output file.

The final checkpoint is A40.ASM, saved as ASM86.ASM. Preserve its seed-built executable and compare both self-assembly generations. Then copy the tested ASM86.COM to ASMAKEEP.COM. ASM1.COM remains the seed builder, and ASMKEEP.COM remains the original ASM0. Keep all three separately named.
