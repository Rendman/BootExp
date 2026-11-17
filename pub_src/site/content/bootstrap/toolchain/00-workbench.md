+++
title = "The Toolchain Workbench"
weight = 0
description = "Preserve the self-compiling compiler and native builders before replacing either native tool."
download = "TOOLCHN.ZIP"
download_group = "tools/toolchain"
reader_names = 1
+++

Complete the RILL compiler construction and its self-build comparisons first. R0.COM is the 27614-byte compiler built from RC43.RIL, saved as RILL.RIL. Keep the matching compiler copies and source on a separate labeled disk.

## Command-line filenames

```dos
CHECK RILL INPUT.RIL OUTPUT.IR
```

DOS supplies the names in the PSP command tail. The native entry binding copies them into owned zero-terminated storage before file services; IR and RILL code use portable argument services. CHECK.BAT forwards the arguments and reports status immediately. No arguments select SOURCE.RIL and RESULT.IR. Use unquoted 8.3 disk names in the current directory: letters, digits, underscore and hyphen, with an optional extension. Paths, switches, excess arguments and overlong names are rejected. Keep selected files distinct from each other and from RILL.TMP and RILL.BAK. Those temporary/backup names remain reserved.

Success reports the selected result name. Rejected source preserves that accepted result; recovery rules apply to the selected name. Early diagnostic writers may deliberately retain a temporary file for inspection, as stated in their lesson.

Use the same DOS 3.10 and period BASIC workbench. CHECK.BAT reports executable status immediately; VIEW.BAS shows exact file length and bytes. Use TYPE for generated assembly and IR text.

## Bring the working builders

| Preserved executable | Source | Job |
|---|---|---|
| R0.COM | RILL.RIL, identical to RC43.RIL | Compile the RILL tool sources into IR |
| IWKEEP.COM | IR86.ASM, identical to IR23.ASM; IRWIDE.ASM is the same source | Translate IR into assembly |
| ASMAKEEP.COM | Native ASM86.ASM, identical to A40.ASM | Assemble that text into a COM image |

These are the tools already proved by the preceding collections. Bring their tested executables to a fresh hard-disk working directory and copy the source collection there. Keep plain ASCII, DOS CR/LF, and 8.3 filenames. Allow room for generated text, complete executables, and recovery files.

The [RILL language reference](../../rc/044-reference/index.html), [streaming IR contract](../../ir86/900-language-reference/index.html), and [native ASM86 reference](../../asm86a/42-reference/index.html) define the interfaces used here. Native registers and DOS conventions remain inside the selected backend and runtime binding.

## Build one replacement at a time

The first two installments use R0, IWKEEP, and ASMAKEEP. Pass each tool source filename to R0 with RESULT.IR as its result. Pass RESULT.IR directly to IWKEEP with RESULT.ASM as its result, then RESULT.ASM to ASMAKEEP with RESULT.COM as its result. Require the stated OK and PASS at every boundary before using the next file.

Save the accepted IR86 replacement as I0.COM and the accepted ASM86 replacement as A0.COM. R0, I0, and A0 then form the first trio of tools written in RILL. Keep IWKEEP and ASMAKEEP separately named throughout this handoff.

## Fixed files and ownership

| Tool | Input | Accepted output | Temporary and backup |
|---|---|---|---|
| RILL compiler | SOURCE.RIL | RESULT.IR | RILL.TMP, RILL.BAK |
| IR86 translator | SOURCE.IR | RESULT.ASM | IRTX.TMP, IRRES.BAK |
| ASM86 assembler | SOURCE.ASM | RESULT.COM | ASMA.TMP, RESULT.BAK |

Inspect any pre-existing recovery names before a run. Source rejection preserves accepted output. A publication failure can leave files that require recovery. Require a fresh successful report; an older result is not evidence that a new translation succeeded.

## Observe the produced artifacts

Inspect the actual assembly, IR, or executable made by each tool. Use the stated file lengths and bytes for encoding checks, and `C:\DOS\FC.EXE /B` for complete executable comparisons. The commands name `C:\DOS\FC.EXE` directly so they also work when that directory is absent from PATH. Require `no differences encountered`. A fixture intended for inspection is data; run a generated program only when its article identifies a complete program.

TMAKE.BAT begins with the preserved native ASMAKEEP.COM. It rebuilds the native IR translator, RILL0, and RILLBOOT, then produces RILL-tool generations zero, one, and two. The BASIC and native assembler constructions remain its prerequisites. Its source is printed in the build installment. The following comparison installment checks all six executable comparisons and runs a short RILL program with generation two. Preserve each generation until all comparisons agree.
