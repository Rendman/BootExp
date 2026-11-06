+++
title = "IW20 \u00b7 Quoted literal data"
weight = 56
description = "Preserve case and escape bytes while branching around inline constant storage."
download = "IW20.ASM"
download_group = "tools/toolchain"
reader_names = 1
+++

## The working parts

Preserve case and escape bytes while branching around inline constant storage.

## Enter the source

Copy IW19.ASM to IW20.ASM. Apply edits **from the bottom of the old file upward**. Physical positions refer to that unchanged old file; use the printed context to identify each place. Keep all other source.

### Edit 1

Unchanged source immediately before the edit:

```asm
DW T_CSGT
DB 67,83,71,69,0,0,0,0,0,0,0,2,0,0
DW T_CSGE
```

Insert after old physical line 1761.

Insert:

```asm
DB 76,73,84,83,0,0,0,0,0,0,6,0,0,0
DW T_LITS
```

### Edit 2

Unchanged source immediately before the edit:

```asm
DB 48,13,10,13,10,82,95,83,84,65,67,75,70,65,73,76
DB 58,13,10,77,79,86,32,65,88,44,52,67,48,50,72,13
DB 10,73,78,84,32,50,49,72,13,10,0
```

Insert after old physical line 1316.

Insert:

```asm

T_LITS:
DB 77,79,86,32,65,88,44,83,95,63,13,10,74,77,80,32
DB 73,95,63,13,10,83,95,63,58,13,10,68,66,32,0

T_LITSEND:
DB 48,13,10,73,95,63,58,13,10,0

T_STRINGNEXT:
DB 13,10,68,66,32,0
```

The following old source remains in place:

```asm

T_NOP:
```

### Edit 3

Unchanged source immediately before the edit:

```asm
TABLEFULL:
MOV AX,5
JMP ERROR
```

Insert after old physical line 994.

Insert:

```asm

STRINGOUT:
MOV AX,[STRID]
INC AX
CMP AX,0
JE NEAR TABLEFULL
MOV [STRID],AX
PUSH SI
MOV SI,T_LITS
CALL EXPAND
POP SI
STRINGSPACE:
LODSB
CMP AL,32
JE NEAR STRINGSPACE
CMP AL,9
JE NEAR STRINGSPACE
CMP AL,34
JNE NEAR SYNTAXBAD
STRINGCHAR:
LODSB
CMP AL,0
JE NEAR SYNTAXBAD
CMP AL,34
JE NEAR STRINGEND
CMP AL,92
JNE NEAR STRINGBYTE
LODSB
CMP AL,110
JNE NEAR NOTLF
MOV AL,10
JMP STRINGBYTE
NOTLF:
CMP AL,114
JNE NEAR NOTCR
MOV AL,13
JMP STRINGBYTE
NOTCR:
CMP AL,116
JNE NEAR NOTTAB
MOV AL,9
JMP STRINGBYTE
NOTTAB:
CMP AL,48
JNE NEAR NOTZERO
MOV AL,0
JMP STRINGBYTE
NOTZERO:
CMP AL,92
JE NEAR STRINGBYTE
CMP AL,34
JNE NEAR SYNTAXBAD
STRINGBYTE:
MOV AH,0
CALL OUTNUM
PUSH SI
MOV SI,T_STRINGNEXT
CALL OUTTEXT
POP SI
JMP STRINGCHAR
STRINGEND:
CALL FINISH
MOV SI,T_LITSEND
CALL EXPAND
RET
```

The following old source remains in place:

```asm

OKMSG:
```

### Edit 4

Unchanged source immediately before the edit:

```asm
ADD AX,AX
MOV [NUMV],AX
JMP STATFINISH
```

Insert after old physical line 894.

Insert:

```asm
STATSTRING:
CALL STRINGOUT
RET
```

The following old source remains in place:

```asm
STATFINISH:
CALL FINISH
```

### Edit 5

Unchanged source immediately before the edit:

```asm
JE NEAR STATPROC
CMP AL,5
JE NEAR STATINVOKE
```

Insert after old physical line 858.

Insert:

```asm
CMP AL,6
JE NEAR STATSTRING
```

The following old source remains in place:

```asm
JMP STATFINISH
STATNUMBER:
```

### Edit 6

Unchanged source immediately before the edit:

```asm
CMP AL,0
JE NEAR STATDONE
MOV BX,IRTAB
```

Remove this source at old physical positions 834–834 in IW19.ASM:

```asm
MOV CX,73
```

Replace it with:

```asm
MOV CX,74
```

The following old source remains in place:

```asm
MOV AX,16
CALL LOOK
```

## Build this stopping point

```dos
COPY IW20.ASM SOURCE.ASM
CHECK ASMAKEEP
```

Require `OK RESULT.COM 08932 bytes` and PASS, then save it:

```dos
COPY RESULT.COM IW20.COM
```

VIEW.BAS must report IW20.COM length 8932 bytes. Keep this executable and its source together.

## Acceptance check

Create TIW20.IR with COPY CON or a plain-text editor. Finish COPY CON with Ctrl-Z and Enter:

```ir
PROC MAIN 0 0
LITS "Hi"
FETCHB
PUTC
LIT 0
RETURN
```

```dos
COPY TIW20.IR SOURCE.IR
```

```dos
CHECK IW20
```

Require:

```text
OK RESULT.ASM 0000002901 text bytes
PASS
```

```dos
COPY RESULT.ASM SOURCE.ASM
CHECK ASMAKEEP
```

Require `OK RESULT.COM 00577 bytes` and PASS before copying it to TRY.COM. VIEW.BAS must show length 577 and these first thirty-two bytes:

```text
FC 81 FC FE FF 74 03 E9 32 02 E8 04 00 B4 4C CD 21 55 8B EC 81 EC 00 00 81 FC 00 F0 73 03 E9 1B
```

Run CHECK TRY. It displays `H` and reports PASS.

## A rejection or boundary check

Create XIW20.IR:

```ir
UNKNOWN
```

```dos
COPY XIW20.IR SOURCE.IR
CHECK IW20
```

Require:

```text
IR ERROR 0000000001 CODE 1
FAIL
```

The accepted RESULT.ASM must remain unchanged. An unexpected PASS fails this check.

## If the result differs

Compare the new routine with the printed addition. Check its arguments and saved state across calls, then inspect the generated text or bytes.
