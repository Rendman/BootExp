+++
title = "The workbench"
weight = 0
description = "BASIC, plain text, and a place to keep the stopping points."
download = "BOOTASM.ZIP"
download_group = "tools/bootasm"
reader_names = 1
+++

The BASIC manual is open beside the keyboard, and I've made a work directory for the experiment. Before I start, I want a simple habit: save a working version before changing it. If tonight's idea goes wrong, I want to be able to get back to yesterday's program.

Use a DOS work directory containing GW-BASIC, or keep the interpreter on your DOS command path. The instructions call it `GWBASIC`; substitute the name on your own disk if it differs. Start it once without a filename and note its version banner. Use the period GW-BASIC supplied with your MS-DOS 3.10 distribution; DOS and BASIC have independent version numbers.

The listings use ordinary line-numbered GW-BASIC, sequential text input, and one-byte random records. They do not require a separate BASIC compiler. About 60 KB of BASIC program-and-data space is a suitable workbench; BOOTASM's byte array alone occupies 8,192 bytes. The collection's storage and recursion notes appear in the reference.

## Entering and keeping a program

At the BASIC `Ok` prompt, type `NEW` before entering a new program. Type every printed BASIC line number. A line with an existing number replaces that line; typing a line number alone deletes it. `LIST 100-200` displays a range for comparison. A long BASIC line may wrap onto a second screen row; press Enter only at the end of the complete numbered line. Save ASCII copies using the `,A` option:

```basic
SAVE "BYTE.BAS",A
```

`LOAD "BYTE.BAS"` loads without running; `RUN` starts the loaded program. `RUN "VIEW.BAS"` loads and runs the viewer, replacing the program in memory, so save your work first. `SYSTEM` returns to DOS. At DOS, `GWBASIC BA02.BAS` starts the interpreter and runs that file.

Each checkpoint builds on the preceding checkpoint, apart from the first disk-byte exercise. For example, load `BA02.BAS`, make the exact additions in installment 03, and save `BA03.BAS`. Do not type a complete downloaded listing over a partly edited program: use `NEW` or `LOAD` first.

## Plain source files

Use ASCII text with DOS carriage-return/line-feed endings and short filenames. At DOS:

```dos
COPY CON TRY.ASM
```

Type the source lines. Finish with Ctrl-Z and Enter. The Ctrl-Z is the end-of-input keystroke, not a token to include in the assembly source. TYPE TRY.ASM displays what was saved. Copy TRY.ASM to SOURCE.ASM, then run GWBASIC BOOTASM.BAS. The assembler reads that fixed source and writes RESULT.COM after acceptance. Preserve it with COPY RESULT.COM TRY.COM before assembling another program.

SOURCE.ASM and RESULT.COM are ordinary work files in the current directory. Their names are assigned in BASIC line 30; no filename input or validation routine is required.

A failed assembly does not replace an older output file. Use a new test name, and require the assembler's `OK` report before inspecting or running output. A BASIC file error during writing may leave an incomplete file, so that case also requires a fresh successful assembly.

## Checking a program's DOS return code

Some tests deliberately display no text. Type the following as `CHECK.BAT` using `COPY CON CHECK.BAT`, ending with Ctrl-Z and Enter. The labels beginning with colons are batch-file labels, not assembly labels.

```dos
ECHO OFF
IF "%1"=="" GOTO USAGE
IF NOT EXIST %1.COM GOTO MISSING
%1
IF ERRORLEVEL 1 GOTO FAIL
ECHO.
ECHO PASS
GOTO END
:FAIL
ECHO.
ECHO FAIL
GOTO END
:MISSING
ECHO Missing program
GOTO END
:USAGE
ECHO Use CHECK name
:END
```

Run `CHECK T10` to run `T10.COM`. Supply only a base name, not an extension, path, or argument list. The `IF ERRORLEVEL` immediately follows the program: launching another program first could replace the status we mean to check. The checker reports PASS for a zero return code and FAIL for any code from 1 through 255. A missing file produces `Missing program`. DOS may echo the first `ECHO OFF` command before command echoing is disabled.

Only use this checker with a fixture expressly described as a complete executable. Data and instruction-encoding fixtures belong in the viewer.

## Files for the disk

Keep the BASIC listings, checkpoint files, test sources, and complete examples together in the work directory. A copy of DOS and a copy of the BASIC interpreter are the starting tools; neither is part of our source listings.
