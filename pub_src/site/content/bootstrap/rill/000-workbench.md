+++
title = "The RILL workbench"
weight = 0
description = "Use the verified RILLBOOT compiler seed to construct the compiler in RILL."
download = "RILL.ZIP"
download_group = "tools/rill"
reader_names = 1
url = "/bootstrap/rc/000-workbench/"
+++

Complete the RILLBOOT collection first, including each complete-compiler acceptance program. Preserve RB12.COM as RILLBOOT.COM and RB12.IR as RILLBOOT.IR. Keep IWKEEP.COM as the native streaming IR translator and ASMAKEEP.COM as the native ASM86. Use the same DOS 3.10, period BASIC, CHECK.BAT, and VIEW.BAS workbench.

## Command-line filenames

```dos
CHECK RILL INPUT.RIL OUTPUT.IR
```

DOS supplies the names in the PSP command tail. The native entry binding copies them into owned zero-terminated storage before file services; IR and RILL code use portable argument services. CHECK.BAT forwards the arguments and reports status immediately. No arguments select SOURCE.RIL and RESULT.IR. Use unquoted 8.3 disk names in the current directory: letters, digits, underscore and hyphen, with an optional extension. Paths, switches, excess arguments and overlong names are rejected. Keep selected files distinct from each other and from RILL.TMP and RILL.BAK. Those temporary/backup names remain reserved.

Success reports the selected result name. Rejected source preserves that accepted result; recovery rules apply to the selected name. Early diagnostic writers may deliberately retain a temporary file for inspection, as stated in their lesson.

## Start the RILL implementation

RC01.RIL starts a new source file in RILL; it is not an edit to RB12.IR. The procedures retain the seed implementation's jobs while expressing them in the language the seed accepts. Later articles copy the preceding RILL source and apply exact edits from the bottom upward. Keep the saved RCxx filenames as printed.

```dos
CHECK RILLBOOT RC01.RIL RESULT.IR
CHECK IWKEEP RESULT.IR RESULT.ASM
CHECK ASMAKEEP RESULT.ASM RESULT.COM
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

The storage and procedure lessons build the sixty-four-local capacity into RC43. After RC43 passes, save its source as RILL.RIL and its executable as RBOOT.COM. The seed-built compiler is 27614 bytes. RBOOT compiles that unchanged source to establish R0 with sixty-four-slot frames. The following two self-builds produce R1 and R2; both must match R0.

After both compiler comparisons match, continue with [Rebuilding Our Tools in RILL](../../toolchain/index.html). Its workbench uses R0 to construct IR86.RIL and ASM86.RIL, then lets the RILL-written trio rebuild all three tools through two matching generations. Keep RILLBOOT, IWKEEP, and ASMAKEEP as reproducible predecessors.
