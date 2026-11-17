+++
title = "The linker workbench"
weight = 0
description = "Keep the RILL-built trio and preserve each linker before testing its output."
download = "LINK86.ZIP"
download_group = "tools/link86"
reader_names = 1
+++

Begin after Rebuilding Our Tools in RILL and its matching generations. Preserve the RILL compiler as R0.COM, its translator as I0.COM and its assembler as A0.COM. Use the same DOS 3.10 hard-disk work directory, plain ASCII editor, VIEW.BAS and CHECK.BAT. Keep the preceding source collections so each builder can be recovered.

## Command-line filenames

```dos
CHECK LINK86 FIRST.OBJ SECOND.OBJ OUTPUT.COM
```

DOS supplies the names in the PSP command tail. The native entry binding copies them into owned zero-terminated storage before file services. The language-level interface supplies argument counts and ordinary string pointers through portable services. CHECK.BAT forwards the arguments and reports status immediately. No arguments select MAIN.OBJ, UTIL.OBJ and RESULT.COM. Use unquoted 8.3 disk names in the current directory: letters, digits, underscore and hyphen, with an optional extension. Paths, switches, excess arguments and overlong names are rejected. Keep selected files distinct from each other and from LINK.TMP and LINK.BAK. Those temporary/backup names remain reserved.

Success reports the selected result name. Rejected source preserves that accepted result; recovery rules apply to the selected name. Early diagnostic writers may deliberately retain a temporary file for inspection, as stated in their lesson.

## Build a stopping point

Every Lnn.RIL is compiled through the same three tools:

```dos
CHECK R0 L01.RIL RESULT.IR
CHECK I0 RESULT.IR RESULT.ASM
CHECK A0 RESULT.ASM RESULT.COM
COPY RESULT.COM L01.COM
```

Require the stated fresh OK and PASS before every following copy. RESULT.COM is also the linker output name, so preserve L01.COM before testing it. Use the same pattern for each later source. The complete source is L10.RIL, also saved as LINK86.RIL.

## Module and result names

Use `CHECK LINK86 FIRST.OBJ SECOND.OBJ OUTPUT.COM`. The portable argc()/arg(n) services supply those names from the saved PSP tail. No arguments select MAIN.OBJ, UTIL.OBJ and RESULT.COM. Early one-module readers accept the same three-name interface but open only the first module. File names must be distinct unquoted 8.3 names in the current directory; LINK.TMP and LINK.BAK remain reserved recovery names. filearg checks the count and collisions before opening files, and filesame compares complete spellings. The linker itself contains no PSP offsets.

| Default file | Use |
|---|---|
| MAIN.OBJ | First module; its first emitted byte loads at 0100H |
| UTIL.OBJ | Second module, placed immediately after the first |
| RESULT.COM | Accepted linked image |
| LINK.TMP | Owned streamed output before publication |
| LINK.BAK | Previous accepted image during publication |

The .OBJ extension names our own ASCII format. Mnn.OBJ and Unn.OBJ are passed directly as the acceptance inputs; Xnn.OBJ replaces the first argument for rejection. Keep both inputs unchanged throughout a run.

Early reader checkpoints use only MAIN.OBJ and report success through CHECK.BAT. L04 recognizes the OBJ1/END envelope. L05 deliberately leaves LINK.TMP for byte inspection; delete that exercise file before another run. L06 publishes RESULT.COM. L07 and later read both modules in two passes. Unknown record types are rejected at every stopping point.

## Inspect and preserve results

VIEW.BAS reports file lengths and hexadecimal bytes. Encoding fixtures are data for inspection; execute only the complete L09 and L10 linked programs. A zero-byte result is valid for inspection and is never a runnable program.

Use C:\DOS\FC.EXE /B for complete byte comparisons and require no differences encountered. The full C:\DOS path finds the utility independently of PATH. Each rejection check preserves the accepted RESULT.COM as HOLD.COM and compares it afterward. CHECK must report FAIL for that input. An older output is never evidence of a new successful link. Inspect pre-existing LINK.TMP or LINK.BAK before running a publishing checkpoint; failed publication can retain recovery files.
