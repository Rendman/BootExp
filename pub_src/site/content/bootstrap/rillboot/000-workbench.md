+++
title = "The RILLBOOT workbench"
weight = 0
description = "Begin with the completed RILL0. Copy RILL0.IR to RB01.IR and continue editing its working compiler. Use IRKEEP and ASMAKEEP for every build. Each saved compiler accepts the earlier language while gaining one capability."
download = "RILLBOOT.ZIP"
download_group = "tools/rillboot"
reader_names = 1
aliases = ["/bootstrap/rb/033-the-systems-workbench/", "/bootstrap/rill/033-the-systems-workbench/"]
url = "/bootstrap/rb/000-workbench/"
+++

Begin with the completed RILL0. Copy RILL0.IR to RB01.IR and continue editing its working compiler. Use IRKEEP and ASMAKEEP for every build. Each saved compiler accepts the earlier language while gaining one capability.

## Command-line filenames

```dos
CHECK RILLBOOT INPUT.RIL OUTPUT.IR
```

DOS supplies the names in the PSP command tail. The native entry binding copies them into owned zero-terminated storage before file services. The language-level interface supplies argument counts and ordinary string pointers through portable services. CHECK.BAT forwards the arguments and reports status immediately. No arguments select SOURCE.RIL and RESULT.IR. Use unquoted 8.3 disk names in the current directory: letters, digits, underscore and hyphen, with an optional extension. Paths, switches, excess arguments and overlong names are rejected. Keep selected files distinct from each other and from RILL.TMP and RILL.BAK. Those temporary/backup names remain reserved.

Success reports the selected result name. Rejected source preserves that accepted result; recovery rules apply to the selected name. Early diagnostic writers may deliberately retain a temporary file for inspection, as stated in their lesson.

Keep VIEW.BAS and the argument-forwarding CHECK.BAT from ASM1. Work in an ordinary DOS hard-disk directory. Give each tool its input and output filenames on the command line. No arguments select the established defaults. Use unquoted 8.3 names in the current directory, without paths or switches; input, result and recovery names must be distinct. Require a fresh OK and PASS before using an output in the next stage.

```dos
CHECK IRKEEP RB01.IR RESULT.ASM
CHECK ASMAKEEP RESULT.ASM RESULT.COM
COPY RESULT.COM RB01.COM
```

An early stopping point may produce a fragment rather than a complete program. Inspect its length and bytes with VIEW.BAS; execute it only when the article gives a complete program. Recovery names protect an interrupted publication: inspect them before trying again.
