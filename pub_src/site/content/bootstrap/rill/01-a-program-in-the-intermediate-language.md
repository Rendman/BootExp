+++
title = "01 \u00b7 A program in the intermediate language"
weight = 1
description = "Build and run the first IR-written program."
download = "R01.IR"
+++

An IR source can already make a complete DOS program. Start with an observable result before adding a source reader.

## The working parts

The driver loads virtual A with 72 and 73 and calls PUTC for each byte. These are H and I in ASCII. HALT returns status zero. Each service consumes an empty expression boundary.

IRKEEP translates the source to assembly, and ASMKEEP encodes that assembly. The source has no physical register, interrupt number, or operating-system descriptor. A successful translation and a successful assembly are separate checks.

## Enter the source

Create R01.IR as plain IR text. This is the complete new source:

```ir
; Driver
LABEL MAIN
LIT 72
PUTC
LIT 73
PUTC
HALT
```

## Build the stopping point

```dos
CHECK IRKEEP
```

Enter `R01` at `IR source name:`. Require `OK R01.ASM 02594 text bytes` and PASS. Then run `CHECK ASMKEEP`, enter `R01` at `Source name:`, and require `OK 00480 bytes` and PASS. Save the source and executable before testing.

## Acceptance check

Run `CHECK R01`. This checkpoint does not read SOURCE.RIL.

Apart from DOS command echo and the checker's separating blank line, require:

```text
HIPASS
```

This is a diagnostic stopping point. It does not create RESULT.IR.

## A rejection check

The program has no source-language reader at this stopping point. Check an IR transcription error independently: create BAD.IR with this text:

```ir
LABEL MAIN
PUTC EXTRA
```

Run CHECK IRKEEP and enter BAD. Require:

```text
IR ERROR 00002 CODE 1
FAIL
```

The unwanted operand must prevent BAD.ASM from being created. If an older BAD.ASM exists, it must remain unchanged.

An unexpected PASS is a failed rejection test.

## If the result differs

Check the IR literal values, operand order, and empty expression boundaries. Translate and assemble afresh; an older COM file can otherwise conceal a source error.
