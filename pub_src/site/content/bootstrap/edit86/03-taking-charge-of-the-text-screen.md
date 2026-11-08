+++
title = "03 \u00b7 Taking charge of the text screen"
weight = 3
description = "Enter and leave an existing 80-column text mode, preserving its cursor settings. A failed entry must return to DOS without leaving an active screen session."
download = "S03.ASM"
download_group = "tools/edit86"
reader_names = 1
+++

Enter and leave an existing 80-column text mode, preserving its cursor settings. A failed entry must return to DOS without leaving an active screen session.

R_VBEGIN queries the current BIOS mode and accepts only 80-column modes 3 and 7. It remembers the active display page, cursor position and cursor shape, clears the working screen and marks the session active. R_VEND clears that screen and restores the saved cursor state. It does not restore the old screen contents. The common success and failure exits restore DS and ES to the main segment. BIOS calls preserve BP explicitly because the generated procedure frames depend on it.

## Enter the source

Create S03.ASM as plain ASCII:

```asm
R_VBEGIN:
CMP BYTE [R_VACTIVE],0
JNE NEAR R_EBAD
MOV AH,0FH
PUSH BP
INT 10H
POP BP
CMP AH,80
JNE NEAR R_EBAD
CMP AL,3
JE NEAR R_VMODE
CMP AL,7
JNE NEAR R_EBAD
R_VMODE:
MOV DX,0B800H
CMP AL,7
JNE NEAR R_VSEGOK
MOV DX,0B000H
R_VSEGOK:
MOV [R_VSEG],DX
MOV AL,BH
MOV [R_VPAGE],AL
MOV BL,AL
MOV BH,0
MOV CL,12
SHL BX,CL
MOV [R_VBASE],BX
MOV BH,[R_VPAGE]
MOV AH,3
PUSH BP
INT 10H
POP BP
MOV [R_VOLDPOS],DX
MOV [R_VOLDSHAPE],CX
MOV BYTE [R_VACTIVE],1
MOV WORD [R_VCELL],0
MOV AX,600H
MOV BH,7
MOV CX,0
MOV DX,184FH
PUSH BP
INT 10H
POP BP
MOV AX,0
JMP R_EDOK
R_VEND:
CMP BYTE [R_VACTIVE],1
JNE NEAR R_EBAD
MOV AX,600H
MOV BH,7
MOV CX,0
MOV DX,184FH
PUSH BP
INT 10H
POP BP
MOV CX,[R_VOLDSHAPE]
MOV AH,1
PUSH BP
INT 10H
POP BP
MOV DX,[R_VOLDPOS]
MOV BH,[R_VPAGE]
MOV AH,2
PUSH BP
INT 10H
POP BP
MOV BYTE [R_VACTIVE],0
MOV AX,0
JMP R_EDOK
R_EBAD:
MOV AX,CS
MOV DS,AX
MOV ES,AX
JMP R_FAIL
R_VACTIVE:
DB 0
R_VPAGE:
DB 0
R_VOLDPOS:
DW 0
R_VOLDSHAPE:
DW 0
R_VCELL:
DW 0
R_VSEG:
DW 0
R_VBASE:
DW 0
R_EDOK:
PUSH AX
MOV AX,CS
MOV DS,AX
MOV ES,AX
POP AX
JMP R_OK
```

## The service probe

Create S03.RIL as plain text:

```rill
fn main(){
    vbegin();
    if status(){
        return 1;
    }
    vend();
    return status();
}
```

```dos
COPY S03.ASM EDITRT.ASM
```

```dos
COPY S03.RIL SOURCE.RIL
CHECK RILLED
COPY RESULT.IR SOURCE.IR
CHECK IRED
COPY RESULT.ASM SOURCE.ASM
CHECK A0
COPY RESULT.COM S03.COM
```

Require compiler `OK RESULT.IR 0000000189`, translator `OK RESULT.ASM 0000006225 text bytes`, assembler `OK RESULT.COM 01301 bytes`, and each PASS before the following copy. VIEW.BAS must report S03.COM length 1301 bytes, beginning with:

```text
FC 81 FC FE FF 74 03 E9 E8 03 E8 40 00 B4 4C CD 21 55 8B EC 81 EC 80 00 81 FC 00 F0 73 03 E9 D1
```

Run `CHECK S03`. The screen clears; the cursor state is restored and CHECK reports PASS.

An unsupported mode returns FAIL before the session becomes active. Use an 80-column mode 3 or monochrome mode 7 screen.

## If the check disagrees

Check the saved binding stage and the stated build reports first. A runtime-label error means the matching EDITRT.ASM was not beside the translator. Compare the registers and extent checks before changing the test.
