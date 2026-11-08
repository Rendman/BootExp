+++
title = "The linker workbench"
weight = 0
description = "Keep the RILL-built trio and preserve each linker before testing its output."
download = "LINK86.ZIP"
download_group = "tools/link86"
reader_names = 1
+++

Begin after Rebuilding Our Tools in RILL and its matching generations. Preserve the RILL compiler as R0.COM, its translator as I0.COM and its assembler as A0.COM. Use the same DOS 3.10 hard-disk work directory, plain ASCII editor, VIEW.BAS and CHECK.BAT. Keep the preceding source collections so each builder can be recovered.

## Build a stopping point

Every Lnn.RIL is compiled through the same three tools:

```dos
COPY L01.RIL SOURCE.RIL
CHECK R0
COPY RESULT.IR SOURCE.IR
CHECK I0
COPY RESULT.ASM SOURCE.ASM
CHECK A0
COPY RESULT.COM L01.COM
```

Require the stated fresh OK and PASS before every following copy. RESULT.COM is also the linker output name, so preserve L01.COM before testing it. Use the same pattern for each later source. The complete source is L10.RIL, also saved as LINK86.RIL.

## Fixed object and output files

| File | Use |
|---|---|
| MAIN.OBJ | First module; its first emitted byte loads at 0100H |
| UTIL.OBJ | Second module, placed immediately after the first |
| RESULT.COM | Accepted linked image |
| LINK.TMP | Owned streamed output before publication |
| LINK.BAK | Previous accepted image during publication |

The .OBJ extension here names our own ASCII format, not a commercial assembler object format. Mnn.OBJ and Unn.OBJ are the exact input fixtures copied to the fixed work names. Xnn.OBJ is the rejection input for MAIN.OBJ. Keep both inputs unchanged throughout a run.

Early reader checkpoints use only MAIN.OBJ and report success through CHECK.BAT. L04 recognizes the OBJ1/END envelope. L05 deliberately leaves LINK.TMP for byte inspection; delete that exercise file before another run. L06 publishes RESULT.COM. L07 and later read both modules in two passes. Unknown record types are rejected at every stopping point.

## Inspect and preserve results

VIEW.BAS reports file lengths and hexadecimal bytes. Encoding fixtures are data for inspection; execute only the complete L09 and L10 linked programs. A zero-byte result is valid for inspection and is never a runnable program.

```dos
ECHO N>NO.TXT
```

NO.TXT answers N when COMP asks whether to compare more files. Each rejection check preserves the accepted RESULT.COM as HOLD.COM and compares it afterward. CHECK must report FAIL for that input. An older output is never evidence of a new successful link. Inspect pre-existing LINK.TMP or LINK.BAK before running a publishing checkpoint; failed publication can retain recovery files.
