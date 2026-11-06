+++
title = "The RC workbench"
weight = 0
description = "Use the verified RB compiler seed to construct the compiler in RILL."
download = "RC.ZIP"
download_group = "rc"
+++

Complete the RB collection first, including its language programs. Preserve RB47.COM as RILLBOOT.COM and RB47.IR as RILLBOOT.IR. Keep IWKEEP.COM as the native streaming IR translator and ASMAKEEP.COM as the native ASM86A. Use the same DOS 3.10, period BASIC, CHECK.BAT, and VIEW.BAS workbench.

## Start the RILL implementation

RC01.RIL starts a new source file in RILL; it is not an edit to RB47.IR. The procedures retain the seed implementation's jobs while expressing them in the language the seed accepts. Later articles copy the preceding RC source and apply exact edits from the bottom upward. Keep the saved RCxx filenames as printed.

```dos
COPY RC01.RIL SOURCE.RIL
CHECK RILLBOOT
COPY RESULT.IR SOURCE.IR
CHECK IWKEEP
COPY RESULT.ASM SOURCE.ASM
CHECK ASMAKEEP
COPY RESULT.COM RC01.COM
```

Require each stated OK and PASS **before** the following copy. An old result left after failure does not establish a successful new translation. Preserve every tested source and executable. Early helper diagnostics may emit only a text fragment; inspect it as text rather than passing it to an assembler or executing it.

## Fixed work files

| Tool | Input | Output | Temporary and recovery names |
|---|---|---|---|
| RILLBOOT or RC compiler | SOURCE.RIL | RESULT.IR | RILL.TMP, RILL.BAK |
| IWKEEP | SOURCE.IR | RESULT.ASM | IRTX.TMP, IRRES.BAK |
| ASMAKEEP | SOURCE.ASM | RESULT.COM | ASMA.TMP, RESULT.BAK |

Use plain ASCII, DOS CR/LF, and 8.3 filenames in a hard-disk work directory. Keep source text unchanged throughout a translation. Inspect pre-existing temporary or backup files before running a full compiler. Source rejection preserves an older accepted result; a failed publication can leave recovery files requiring inspection. Delete only a diagnostic temporary file that its article explicitly tells you to inspect and remove.

The complete compiler streams 4096-byte blocks. Symbol storage uses an opaque allocated block; native registers and segments remain outside the RILL language. The language reference gives exact symbol, name, frame, nesting, and target-image limits. Allocated workspace does not enlarge the COM code image.

## Preserve the self-build handoff

After RC43 passes, copy RC43.RIL to RILL.RIL and RC43.COM to R0.COM. The seed-built compiler is 26625 bytes. The self-build exercise uses R0, then R1, to compile the same source through the preserved native translator and assembler. Both resulting executables must match R0.

The complete toolchain exercise also builds IR86.RIL and ASM86A.RIL, then lets the RILL-written trio rebuild all three tools through two matching generations. Keep RILLBOOT, IWKEEP, and ASMAKEEP as reproducible predecessors.
