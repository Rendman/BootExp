+++
title = "31 \u00b7 Complete assembly programs"
weight = 31
description = "Strings, a stack frame, a distant conditional, and repeated byte movement."
download = "ASM86A.ZIP"
+++

Use the completed ASMAKEEP.COM. For each NAME.ASM below, copy it to SOURCE.ASM and run CHECK ASMAKEEP. Require OK and PASS before copying RESULT.COM to NAME.COM. Inspect it with VIEW.BAS before running CHECK NAME.

## HELLO

```asm
MOV BX,1
MOV CX,MSG_LEN
MOV DX,MESSAGE
MOV AH,40H
INT 21H
JAE COUNTED
MOV AX,4C01H
INT 21H
COUNTED:
CMP AX,MSG_LEN
JNE FAILED
MOV AX,4C00H
INT 21H
FAILED:
MOV AX,4C01H
INT 21H
MESSAGE:
DB "Hello",13,10
MSG_LEN EQU $-MESSAGE
```

DOS function 40H writes a counted string. Both carry and the returned count are checked. Quoted data preserves the mixed case; CR and LF are explicit bytes.

Require `OK RESULT.COM 00043 bytes` and PASS. VIEW.BAS must report length 43 and these first thirty-two bytes:

```text
BB 01 00 B9 07 00 BA 24 01 B4 40 CD 21 73 05 B8 01 4C CD 21 81 F8 07 00 75 05 B8 00 4C CD 21 B8
```

After saving RESULT.COM as HELLO.COM, CHECK HELLO displays "Hello\r\n" and reports PASS. Here `\r\n` means carriage return followed by line feed.

For a separate rejection, copy the source to BAD.ASM. Replace `DB "Hello",13,10` with `DB "Hello,13,10`. Copy BAD.ASM to SOURCE.ASM and run CHECK ASMAKEEP. Require `ERROR 0000000018 CODE 1` and FAIL. The accepted RESULT.COM must remain unchanged; an unexpected PASS fails the check. Restore the accepted source before rebuilding.

## FRAME

```asm
MOV AX,65
PUSH AX
CALL F
MOV DL,AL
MOV AH,2
INT 21H
MOV AX,4C00H
INT 21H
F:
PUSH BP
MOV BP,SP
SUB SP,2
MOV AX,[BP+4]
MOV [BP-2],AX
MOV AX,[BP-2]
MOV SP,BP
POP BP
RET 2
```

CALL pushes the return address; PUSH BP saves the caller frame. BP+4 addresses the word argument. BP-2 is a local word after SUB SP,2. Restoring SP and BP precedes RET 2, which releases the argument. BP-based memory defaults to SS.

Require `OK RESULT.COM 00043 bytes` and PASS. VIEW.BAS must report length 43 and these first thirty-two bytes:

```text
B8 41 00 50 E8 0B 00 8A D0 B4 02 CD 21 B8 00 4C CD 21 55 8B EC 81 EC 02 00 8B 86 04 00 89 86 FE
```

After saving RESULT.COM as FRAME.COM, CHECK FRAME displays "A" and reports PASS. Here `\r\n` means carriage return followed by line feed.

For a separate rejection, copy the source to BAD.ASM. Replace `[BP+4]` with `[SP+4]`. Copy BAD.ASM to SOURCE.ASM and run CHECK ASMAKEEP. Require `ERROR 0000000013 CODE 1` and FAIL. The accepted RESULT.COM must remain unchanged; an unexpected PASS fails the check. Restore the accepted source before rebuilding.

## BRIDGE

```asm
MOV AX,1
CMP AX,0
JNE NEAR SHOW
MOV AX,4C01H
INT 21H
RESB 300
SHOW:
MOV DL,66
MOV AH,2
INT 21H
MOV AX,4C00H
INT 21H
```

The nonzero word takes JNE NEAR across a zero-filled region. The opposite short branch skips E9 and its word displacement when the condition is false. The intervening bytes are never executed.

Require `OK RESULT.COM 00328 bytes` and PASS. VIEW.BAS must report length 328 and these first thirty-two bytes:

```text
B8 01 00 81 F8 00 00 74 03 E9 31 01 B8 01 4C CD 21 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
```

After saving RESULT.COM as BRIDGE.COM, CHECK BRIDGE displays "B" and reports PASS. Here `\r\n` means carriage return followed by line feed.

For a separate rejection, copy the source to BAD.ASM. Replace `JNE NEAR SHOW` with `JNE SHOW`. Copy BAD.ASM to SOURCE.ASM and run CHECK ASMAKEEP. Require `ERROR 0000000003 CODE 4` and FAIL. The accepted RESULT.COM must remain unchanged; an unexpected PASS fails the check. Restore the accepted source before rebuilding.

## COPYTEXT

```asm
CLD
MOV SI,TEXT
MOV DI,DEST
MOV CX,2
REP MOVSB
MOV SI,DEST
MOV CX,2
SHOW:
MOV DL,[SI]
MOV AH,2
INT 21H
INC SI
DEC CX
JNE SHOW
MOV AX,4C00H
INT 21H
TEXT:
DB "Hi"
DEST:
RESB 2
```

A COM program begins with DS and ES selecting the program segment. CLD makes movement advance. REP MOVSB copies two bytes, then the output loop prints the copy. REP consumes CX; the output loop loads its own count.

Require `OK RESULT.COM 00037 bytes` and PASS. VIEW.BAS must report length 37 and these first thirty-two bytes:

```text
FC BE 21 01 BF 23 01 B9 02 00 F3 A4 BE 23 01 B9 02 00 8A 14 B4 02 CD 21 46 49 75 F6 B8 00 4C CD
```

After saving RESULT.COM as COPYTEXT.COM, CHECK COPYTEXT displays "Hi" and reports PASS. Here `\r\n` means carriage return followed by line feed.

For a separate rejection, copy the source to BAD.ASM. Replace `REP MOVSB` with `REP RET`. Copy BAD.ASM to SOURCE.ASM and run CHECK ASMAKEEP. Require `ERROR 0000000005 CODE 1` and FAIL. The accepted RESULT.COM must remain unchanged; an unexpected PASS fails the check. Restore the accepted source before rebuilding.

