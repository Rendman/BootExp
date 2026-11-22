+++
title = "The IR86 workbench"
weight = 0
description = "Carry the tested ASM86 source and builder into one continuing native translator."
download = "IR86.ZIP"
download_group = "tools/ir86"
reader_names = 1
aliases = ["/bootstrap/ir86/00-workbench/"]
+++

I have a working assembler and a way to inspect its output. For the next tool I want another visible stopping point between the source I enter and the bytes DOS executes: an assembly file I can read. IR86 will write that file, and the preserved ASM86 will turn it into a program.

## Command-line filenames

```dos
CHECK IR86 INPUT.IR OUTPUT.ASM
```

DOS supplies the names in the PSP command tail. The native entry binding copies them into owned zero-terminated storage before file services. The language-level interface supplies argument counts and ordinary string pointers through portable services. CHECK.BAT forwards the arguments and reports status immediately. No arguments select SOURCE.IR and RESULT.ASM. Use unquoted 8.3 disk names in the current directory: letters, digits, underscore and hyphen, with an optional extension. Paths, switches, excess arguments and overlong names are rejected. Keep selected files distinct from each other and from IRTX.TMP and IRRES.BAK. Those temporary/backup names remain reserved.

Success reports the selected result name. Rejected source preserves that accepted result; recovery rules apply to the selected name. Early diagnostic writers may deliberately retain a temporary file for inspection, as stated in their lesson.

## Carry the tested assembler forward

Bring ASM86.ASM and ASMAKEEP.COM from the completed ASM86 workbench into the directory used for this collection. ASM86.ASM is the accepted A40 source; ASMAKEEP.COM is the 6,433-byte assembler preserved after its two self-build comparisons. Keep that source untouched. ASMKEEP.COM names the earlier ASM0 and is not the builder used here.

Before editing a copy, check the source and executable together:

```dos
CHECK ASMAKEEP ASM86.ASM ASTEST.COM
C:\DOS\FC.EXE /B ASMAKEEP.COM ASTEST.COM
```

Require OK ASTEST.COM 06433 bytes and PASS before the comparison. FC must report no differences. This checks the same preserved assembler and source that begin the construction.

## Building the translator

The first four checkpoints prepare the reader, scanner, writer, and operation records separately. The fifth joins them into a small translator. From there we keep extending the same source until it can support the compiler. I shall save each accepted translator with its source so there is a working place to return to.

ASM86 builds every saved source in this collection. Supply the translator input and output names after its program name; SOURCE.IR and RESULT.ASM remain the no-argument defaults. At the final checkpoint save IR86.ASM and IR86.COM, then preserve identical IRKEEP.COM and IWKEEP.COM working copies.

Keep VIEW.BAS and the argument-forwarding CHECK.BAT from ASM1. Work in an ordinary DOS hard-disk directory. Give each tool its input and output filenames on the command line. No arguments select the established defaults. Use unquoted 8.3 names in the current directory, without paths or switches; input, result and recovery names must be distinct. Require a fresh OK and PASS before using an output in the next stage.

After entering IR01.ASM from the first article:

```dos
CHECK ASMAKEEP IR01.ASM RESULT.COM
```

Require `OK RESULT.COM 02534 bytes` and PASS before saving the accepted reader:

```dos
COPY RESULT.COM IR01.COM
```

An early stopping point may produce a fragment rather than a complete program. Inspect its length and bytes with VIEW.BAS; execute it only when the article gives a complete program. Recovery names protect an interrupted publication: inspect them before trying again.
