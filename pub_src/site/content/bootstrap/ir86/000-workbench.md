+++
title = "The IR86 workbench"
weight = 0
description = "ASM86 builds every saved source in this collection. Supply the translator input and output names after its program name; SOURCE.IR and RESULT.ASM remain the no-argument defaults. Preserve the completed translator as IRKEEP.COM; make the identical IWKEEP.COM copy used by later workbenches."
download = "IR86.ZIP"
download_group = "tools/ir86"
reader_names = 1
aliases = ["/bootstrap/ir86/00-workbench/"]
+++

ASM86 builds every saved source in this collection. Supply the translator input and output names after its program name; SOURCE.IR and RESULT.ASM remain the no-argument defaults. Preserve the completed translator as IRKEEP.COM; make the identical IWKEEP.COM copy used by later workbenches.

## Command-line filenames

```dos
CHECK IR86 INPUT.IR OUTPUT.ASM
```

DOS supplies the names in the PSP command tail. The native entry binding copies them into owned zero-terminated storage before file services. The language-level interface supplies argument counts and ordinary string pointers through portable services. CHECK.BAT forwards the arguments and reports status immediately. No arguments select SOURCE.IR and RESULT.ASM. Use unquoted 8.3 disk names in the current directory: letters, digits, underscore and hyphen, with an optional extension. Paths, switches, excess arguments and overlong names are rejected. Keep selected files distinct from each other and from IRTX.TMP and IRRES.BAK. Those temporary/backup names remain reserved.

Success reports the selected result name. Rejected source preserves that accepted result; recovery rules apply to the selected name. Early diagnostic writers may deliberately retain a temporary file for inspection, as stated in their lesson.

Keep VIEW.BAS and the argument-forwarding CHECK.BAT from ASM1. Work in an ordinary DOS hard-disk directory. Give each tool its input and output filenames on the command line. No arguments select the established defaults. Use unquoted 8.3 names in the current directory, without paths or switches; input, result and recovery names must be distinct. Require a fresh OK and PASS before using an output in the next stage.

```dos
CHECK ASMAKEEP IR01.ASM RESULT.COM
COPY RESULT.COM IR01.COM
```

An early stopping point may produce a fragment rather than a complete program. Inspect its length and bytes with VIEW.BAS; execute it only when the article gives a complete program. Recovery names protect an interrupted publication: inspect them before trying again.
