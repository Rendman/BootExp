+++
title = "IW10 \u00b7 Calls and returns"
weight = 46
description = "Keep a return address separate from a procedure result in A."
download = "IW10.ASM"
download_group = "toolchain"
+++

Keep a return address separate from a procedure result in A.

## The working parts

Keep a return address separate from a procedure result in A. The assembly routines use the inherited bounded reader and owned-file cleanup. The operation table supplies argument class, stack action, and an authored target template. Native encodings belong to this backend; the IR operation retains its abstract meaning.

## Enter the source

Copy IW09.ASM to IW10.ASM. Apply edits **from the bottom of the old file upward**. Physical positions refer to that unchanged old file; use the printed context to identify each place. Keep all other source.

### Edit 1

Unchanged source immediately before the edit:

```asm
DW T_SGT
DB 83,71,69,0,0,0,0,0,0,0,2,2,0,0
DW T_SGE
```

Insert after old physical line 1313.

Insert:

```asm
DB 67,65,76,76,0,0,0,0,0,0,2,0,0,0
DW T_CALL
DB 82,69,84,0,0,0,0,0,0,0,0,4,0,0
DW T_RET
```

### Edit 2

Unchanged source immediately before the edit:

```asm
T_JMP:
DB 74,77,80,32,85,95,64,13,10,0
```

Insert after old physical line 1238.

Insert:

```asm
T_CALL:
DB 67,65,76,76,32,85,95,64,13,10,0

T_RET:
DB 82,69,84,13,10,0
```

The following old source remains in place:

```asm
IRTAB:
DB 76,73,84,0,0,0,0,0,0,0,1,0,0,0
```

### Edit 3

Unchanged source immediately before the edit:

```asm
CMP AL,0
JE NEAR STATDONE
MOV BX,IRTAB
```

Remove this source at old physical positions 834–834 in IW09.ASM:

```asm
MOV CX,37
```

Replace it with:

```asm
MOV CX,39
```

The following old source remains in place:

```asm
MOV AX,16
CALL LOOK
```

## Build this stopping point

```dos
COPY IW10.ASM SOURCE.ASM
CHECK ASMAKEEP
```

Require `OK RESULT.COM 04279 bytes` and PASS, then save it:

```dos
COPY RESULT.COM IW10.COM
```

VIEW.BAS must report IW10.COM length 4279 bytes. Keep this executable and its source together.

## Acceptance check

Create TIW10.IR with COPY CON or a plain-text editor. Finish COPY CON with Ctrl-Z and Enter:

```ir
LABEL MAIN
CALL VALUE
PUSH
LIT 65
EQ GOOD
LIT 1
EXIT
LABEL GOOD
HALT
LABEL VALUE
LIT 65
RET
```

```dos
COPY TIW10.IR SOURCE.IR
```

```dos
CHECK IW10
```

Require, apart from command echo and the checker's separator:

```text
OK RESULT.ASM 0000000295 text bytes
PASS
```

```dos
COPY RESULT.ASM SOURCE.ASM
CHECK ASMAKEEP
```

Require `OK RESULT.COM 00053 bytes` and PASS before copying it to TRY.COM. VIEW.BAS must show length 53 and these first thirty-two bytes:

```text
FC 81 FC FE FF 74 03 E9 26 00 E8 04 00 B4 4C CD 21 E8 18 00 50 B8 41 00 5B 3B D8 75 03 E9 07 00
```

Run CHECK TRY. It returns zero and the checker reports PASS.

## A rejection or boundary check

Create XIW10.IR:

```ir
UNKNOWN
```

```dos
COPY XIW10.IR SOURCE.IR
CHECK IW10
```

Require:

```text
IR ERROR 0000000001 CODE 1
FAIL
```

The accepted RESULT.ASM must remain unchanged. An unexpected PASS fails this check.

## If the result differs

Check the saved pointer or slot, argument order, complete token spelling, and STATUS immediately after each service. A helper's local state must survive calls; an output count is independent of input position. Inspect text and file length before interpreting any bytes as a program.
