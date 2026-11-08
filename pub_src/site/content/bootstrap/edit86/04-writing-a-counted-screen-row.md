+++
title = "04 \u00b7 Writing a counted screen row"
weight = 4
description = "Write a counted span of cells with a stable attribute. Position zero is the upper left; the last status row must not scroll the document."
download = "S04.ASM"
download_group = "tools/edit86"
reader_names = 1
+++

Write a counted span of cells with a stable attribute. Position zero is the upper left; the last status row must not scroll the document.

A cell number is row times 80 plus column. R_VPOS checks the range 0–1999, divides by 80 and asks the BIOS to position the hardware cursor. R_VWRITE treats bytes as literal cells, with attribute 7; it does not interpret carriage return, tab or line feed. Validate the near span and the complete cell extent before writing. The binding privately selects B800H for color text or B000H for monochrome and adds the active page base. Keeping these addresses here leaves them out of the editor language. Direct cell writes also avoid scrolling when the last cell is written.

## Enter the source

Copy S03.ASM to S04.ASM.

Keep the unchanged source. Apply these edits from the bottom of the old file upward; physical positions locate text and are not source to type.

### Edit 1

Unchanged source immediately before the edit:

```asm
MOV ES,AX
JMP R_FAIL
```

Insert after old physical line 74.

Insert:

```asm
R_VPOS:
CMP BYTE [R_VACTIVE],1
JNE NEAR R_EBAD
CMP AX,2000
JAE NEAR R_EBAD
MOV [R_VCELL],AX
XOR DX,DX
MOV BX,80
DIV BX
MOV DH,AL
MOV BH,[R_VPAGE]
MOV AH,2
PUSH BP
INT 10H
POP BP
MOV AX,0
JMP R_EDOK
R_VWRITE:
CMP BYTE [R_VACTIVE],1
JNE NEAR R_EBAD
MOV SI,DX
MOV CX,AX
ADD DX,CX
JC NEAR R_EBAD
ADD AX,[R_VCELL]
JC NEAR R_EBAD
CMP AX,2000
JA NEAR R_EBAD
MOV DX,[R_VCELL]
MOV [R_VCELL],AX
MOV DI,DX
SHL DI,1
ADD DI,[R_VBASE]
MOV AX,[R_VSEG]
MOV ES,AX
R_VLOOP:
CMP CX,0
JE NEAR R_VDONE
LODSB
MOV AH,7
MOV ES:[DI],AX
ADD DI,2
DEC CX
JMP R_VLOOP
R_VDONE:
MOV AX,0
JMP R_EDOK
```

The following old source remains:

```asm
R_VACTIVE:
DB 0
```

## The service probe

Create S04.RIL as plain text:

```rill
fn main(){
    vbegin();
    if status(){
        return 1;
    }
    vpos(0);
    vwrite("EDIT86",6);
    let mut bad=status();
    vpos(2000);
    if status()==0{
        bad=1;
    }
    vend();
    return bad|status();
}
```

```dos
COPY S04.ASM EDITRT.ASM
```

```dos
COPY S04.RIL SOURCE.RIL
CHECK RILLED
COPY RESULT.IR SOURCE.IR
CHECK IRED
COPY RESULT.ASM SOURCE.ASM
CHECK A0
COPY RESULT.COM S04.COM
```

Require compiler `OK RESULT.IR 0000000463`, translator `OK RESULT.ASM 0000007414 text bytes`, assembler `OK RESULT.COM 01534 bytes`, and each PASS before the following copy. VIEW.BAS must report S04.COM length 1534 bytes, beginning with:

```text
FC 81 FC FE FF 74 03 E9 47 04 E8 9F 00 B4 4C CD 21 55 8B EC 81 EC 80 00 81 FC 00 F0 73 03 E9 30
```

Run `CHECK S04`. EDIT86 appears in the upper left; the deliberately invalid position is detected, then CHECK reports PASS.

The request for cell 2000 must fail; the final valid cell is 1999. The probe remembers that status before VEND replaces it.

## If the check disagrees

Check the saved binding stage and the stated build reports first. A runtime-label error means the matching EDITRT.ASM was not beside the translator. Compare the registers and extent checks before changing the test.
