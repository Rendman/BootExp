+++
title = "The RILL workbench"
weight = 0
description = "Use the verified RILLBOOT compiler seed to construct the compiler in RILL."
download = "RILL.ZIP"
download_group = "tools/rill"
reader_names = 1
+++

Complete the RILLBOOT collection first, including each complete-compiler acceptance program. Preserve RB12.COM as RILLBOOT.COM and RB12.IR as RILLBOOT.IR. Keep IWKEEP.COM as the native streaming IR translator and ASMAKEEP.COM as the native ASM86. Use the same DOS 3.10, period BASIC, CHECK.BAT, and VIEW.BAS workbench.

## Start the RILL implementation

RC01.RIL starts a new source file in RILL; it is not an edit to RB12.IR. The procedures retain the seed implementation's jobs while expressing them in the language the seed accepts. Later articles copy the preceding RILL source and apply exact edits from the bottom upward. Keep the saved RCxx filenames as printed.

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
| RILLBOOT or RILL compiler | SOURCE.RIL | RESULT.IR | RILL.TMP, RILL.BAK |
| IWKEEP | SOURCE.IR | RESULT.ASM | IRTX.TMP, IRRES.BAK |
| ASMAKEEP | SOURCE.ASM | RESULT.COM | ASMA.TMP, RESULT.BAK |

Use plain ASCII, DOS CR/LF, and 8.3 filenames in a hard-disk work directory. Keep source text unchanged throughout a translation. Inspect pre-existing temporary or backup files before running a full compiler. Source rejection preserves an older accepted result; a failed publication can leave recovery files requiring inspection. Delete only a diagnostic temporary file that its article explicitly tells you to inspect and remove.

The complete compiler streams 4096-byte blocks. Symbol storage uses an opaque allocated block; native registers and segments remain outside the RILL language. The language reference gives exact symbol, name, frame, nesting, and target-image limits. Allocated workspace does not enlarge the COM code image.

## Preserve the self-build handoff

After RC43 passes, preserve RC43.RIL unchanged and copy RC43.COM to R0.COM. The seed-built compiler is 26617 bytes. The self-build exercise uses R0, then R1, to compile the same source through the preserved native translator and assembler. Both resulting executables must match R0.

After both compiler comparisons match, complete [More Local Storage](../134-more-local-storage/index.html). It extends RILL to sixty-four live locals while retaining sixteen parameters. Save RC44.RIL as RILL.RIL and establish matching R0/R1/R2 copies as described there. Then continue with [Rebuilding Our Tools in RILL](../../toolchain/index.html). Its workbench uses R0 to construct IR86.RIL and ASM86.RIL, then lets the RILL-written trio rebuild all three tools through two matching generations. Keep RILLBOOT, IWKEEP, and ASMAKEEP as reproducible predecessors.
