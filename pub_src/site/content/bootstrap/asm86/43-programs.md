+++
title = "27 \u00b7 Complete assembly programs"
weight = 27
description = "Strings, a stack frame, a distant conditional, and explicit byte movement."
download = "ASM86.ZIP"
download_group = "tools/asm86"
reader_names = 1
url = "/bootstrap/asm86a/43-programs/"
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
ADD SP,2
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
RET
```

CALL pushes the return address; PUSH BP saves the caller frame. BP+4 addresses the word argument. BP-2 is a local word after SUB SP,2. Restoring SP and BP precedes RET. The caller releases its argument with ADD SP,2. BP-based memory defaults to SS.

Require `OK RESULT.COM 00045 bytes` and PASS. VIEW.BAS must report length 45 and these first thirty-two bytes:

```text
B8 41 00 50 E8 0F 00 81 C4 02 00 8A D0 B4 02 CD 21 B8 00 4C CD 21 55 8B EC 81 EC 02 00 8B 86 04
```

After saving RESULT.COM as FRAME.COM, CHECK FRAME displays "A" and reports PASS. Here `\r\n` means carriage return followed by line feed.

For a separate rejection, copy the source to BAD.ASM. Replace `[BP+4]` with `[SP+4]`. Copy BAD.ASM to SOURCE.ASM and run CHECK ASMAKEEP. Require `ERROR 0000000014 CODE 1` and FAIL. The accepted RESULT.COM must remain unchanged; an unexpected PASS fails the check. Restore the accepted source before rebuilding.

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
COPYLOOP:
LODSB
STOSB
DEC CX
JNE COPYLOOP
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

A COM program begins with DS and ES selecting the program segment. CLD makes movement advance. The LODSB/STOSB loop copies two bytes, then the output loop prints the copy. The copy loop consumes CX; the output loop loads its own count.

Require `OK RESULT.COM 00040 bytes` and PASS. VIEW.BAS must report length 40 and these first thirty-two bytes:

```text
FC BE 24 01 BF 26 01 B9 02 00 AC AA 49 75 FB BE 26 01 B9 02 00 8A 14 B4 02 CD 21 46 49 75 F6 B8
```

After saving RESULT.COM as COPYTEXT.COM, CHECK COPYTEXT displays "Hi" and reports PASS. Here `\r\n` means carriage return followed by line feed.

For a separate rejection, copy the source to BAD.ASM. Replace `LODSB` with `LODSB 1`. Copy BAD.ASM to SOURCE.ASM and run CHECK ASMAKEEP. Require `ERROR 0000000006 CODE 1` and FAIL. The accepted RESULT.COM must remain unchanged; an unexpected PASS fails the check. Restore the accepted source before rebuilding.

