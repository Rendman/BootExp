+++
title = "20 \u00b7 Quoted literal data"
weight = 20
description = "Preserve case and escape bytes while branching around inline constant storage."
download = "IR20.ASM"
download_group = "tools/ir86"
reader_names = 1
aliases = ["/bootstrap/ir86/056-iw-quoted-literal-data/", "/bootstrap/ir86/20-an-unconditional-transfer/"]
+++

A filename or diagnostic is awkward to spell as a row of numeric bytes. I shall let IR source contain quoted text and return a pointer to its terminated bytes. The generated code must branch around that inline storage as it runs. Our first literal will be small enough to follow from its spelling to the displayed character.

**Starting source:** `IR19.ASM`. **Save as:** `IR20.ASM`. **Build with:** `ASMAKEEP.COM`.

## How it works

Preserve case and escape bytes while branching around inline constant storage.

## Enter the source

Copy IR19.ASM to IR20.ASM. Apply the following edits from the bottom of the old file upward, using the old physical positions and unchanged context. Keep all other source.

### Edit at old physical position 2044

Unchanged source before the edit:

```asm
DW T_CUGT
DB 67,85,71,69,0,0,0,0,0,0,0,2,0,0
DW T_CUGE
```

Insert in its place:

```asm
DB 76,73,84,83,0,0,0,0,0,0,6,0,0,0
DW T_LITS
```

The following old source remains:

```asm

CMDCOUNT:
```

### Edit at old physical position 1665

Unchanged source before the edit:

```asm
DB "DB 0,0,0,0,0,0,0,0,0,0,0,0,0",13,10
DB 0
```

Insert in its place:

```asm
T_LITS:
DB 77,79,86,32,65,88,44,83,95,63,13,10,74,77,80,32
DB 73,95,63,13,10,83,95,63,58,13,10,68,66,32,0

T_LITSEND:
DB "0",13,10
DB "I_?:",13,10
DB 0

T_STRINGNEXT:
DB 13,10,68,66,32,0
```

The following old source remains:

```asm
T_EXIT:
DB "MOV AH,4CH",13,10
```

### Edit at old physical position 1031

Unchanged source before the edit:

```asm
TABLEFULL:
MOV AX,5
JMP ERROR
```

Insert in its place:

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

The following old source remains:

```asm

CMDINIT:
```

### Edit at old physical position 933

Unchanged source before the edit:

```asm
ADD AX,AX
MOV [NUMV],AX
JMP STATFINISH
```

Insert in its place:

```asm
STATSTRING:
CALL STRINGOUT
RET
```

The following old source remains:

```asm
STATFINISH:
CALL FINISH
```

### Edit at old physical position 897

Unchanged source before the edit:

```asm
JE NEAR STATPROC
CMP AL,5
JE NEAR STATINVOKE
```

Insert in its place:

```asm
CMP AL,6
JE NEAR STATSTRING
```

The following old source remains:

```asm
JMP STATFINISH
STATNUMBER:
```

### Edit at old physical position 872

Unchanged source before the edit:

```asm
CMP AL,0
JE NEAR STATDONE
MOV BX,IRTAB
```

Remove:

```asm
MOV CX,51
```

Insert in its place:

```asm
MOV CX,52
```

The following old source remains:

```asm
MOV AX,16
CALL LOOK
```

## Build and check

```dos
CHECK ASMAKEEP IR20.ASM RESULT.COM
```

Require fresh OK and PASS reports before each following copy. The assembler must report `OK RESULT.COM 09714 bytes`. Save RESULT.COM as IR20.COM. VIEW.BAS must show length 9714.

Create T20.IR:

```ir
PROC MAIN 0 0
LITS "Hi"
FETCHB
PUTC
LIT 0
RETURN
```

```dos
CHECK IR20 T20.IR RESULT.ASM
```

Require:

```text
OK RESULT.ASM 0000004166 text bytes
PASS
```

```dos
CHECK ASMAKEEP RESULT.ASM RESULT.COM
```

Require OK and PASS. VIEW.BAS must show RESULT.COM length 891 and these leading bytes:

```text
FC 81 FC FE FF 74 03 E9 0E 02 E8 10 02 81 F8 FF FF 75 03 E9 02 02 E8 04 00 B4 4C CD 21 55 8B EC
```

Copy it to TRY.COM. CHECK TRY displays `H` and reports PASS.

The displayed `H` is the first byte fetched from the literal `Hi`. The literal keeps its case and supplies a terminated string pointer. I can use the same form for readable filenames and messages in the compiler source.

## Check the new boundary

Save this separate rejected source as X20.IR:

```ir
UNKNOWN
```

```dos
CHECK IR20 X20.IR RESULT.ASM
```

Require:

```text
IR ERROR 0000000001 CODE 1
FAIL
```

An unexpected PASS fails this check. Keep a copy of the accepted result before testing; it must remain unchanged.

