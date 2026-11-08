+++
title = "05 \u00b7 Reading navigation keys"
weight = 5
description = "Translate the keyboard into character values and named event numbers. The editor needs arrows and function keys without knowing BIOS scan codes."
download = "S05.ASM"
download_group = "tools/edit86"
reader_names = 1
+++

Translate the keyboard into character values and named event numbers. The editor needs arrows and function keys without knowing BIOS scan codes.

Normal characters retain their byte values. Extended keys are translated through R_KEYMAP into event values beginning at 256. Unrecognized extended keys return zero and do nothing. Control-S, Control-Q and Control-Z also select Save, Quit and Undo. Save, Find, Undo and Quit therefore reach the editor as ordinary word values; no BIOS scan number appears in the RILL source. KEY requires an active screen session and waits for one event.

## Enter the source

Copy S04.ASM to S05.ASM.

Keep the unchanged source. Apply these edits from the bottom of the old file upward; physical positions locate text and are not source to type.

### Edit 1

Unchanged source immediately before the edit:

```asm
R_VBASE:
DW 0
```

Insert after old physical line 135.

Insert:

```asm
R_KEYMAP:
DB 75,77,72,80,71,79,73,81,83,60,68,62,61,63,64,65
```

The following old source remains:

```asm
R_EDOK:
PUSH AX
```

### Edit 2

Unchanged source immediately before the edit:

```asm
MOV AX,0
JMP R_EDOK
```

Insert after old physical line 121.

Insert:

```asm
R_KEY:
CMP BYTE [R_VACTIVE],1
JNE NEAR R_EBAD
MOV AH,0
PUSH BP
INT 16H
POP BP
CMP AL,0
JE NEAR R_KEXT
CMP AL,224
JE NEAR R_KEXT
CMP AL,19
JE NEAR R_KSAVE
CMP AL,17
JE NEAR R_KQUIT
CMP AL,26
JE NEAR R_KUNDO
MOV AH,0
JMP R_EDOK
R_KEXT:
MOV AL,AH
MOV AH,0
MOV SI,R_KEYMAP
MOV CX,16
MOV BX,256
R_KFIND:
CMP AL,[SI]
JE NEAR R_KFOUND
INC SI
INC BX
DEC CX
JNE NEAR R_KFIND
MOV AX,0
JMP R_EDOK
R_KFOUND:
MOV AX,BX
JMP R_EDOK
R_KSAVE:
MOV AX,265
JMP R_EDOK
R_KQUIT:
MOV AX,266
JMP R_EDOK
R_KUNDO:
MOV AX,267
JMP R_EDOK
; BX source block, CX source offset, DX destination block,
; DI destination offset, AX count. Validate both before copying.
```

The following old source remains:

```asm
R_VACTIVE:
DB 0
```

## The service probe

Create S05.RIL as plain text:

```rill
fn main(){
    vbegin();
    if status(){
        return 1;
    }
    vpos(0);
    vwrite("Press F10",9);
    let mut k=key();
    vend();
    return (k!=266)|status();
}
```

```dos
COPY S05.ASM EDITRT.ASM
```

```dos
COPY S05.RIL SOURCE.RIL
CHECK RILLED
COPY RESULT.IR SOURCE.IR
CHECK IRED
COPY RESULT.ASM SOURCE.ASM
CHECK A0
COPY RESULT.COM S05.COM
```

Require compiler `OK RESULT.IR 0000000337`, translator `OK RESULT.ASM 0000007982 text bytes`, assembler `OK RESULT.COM 01635 bytes`, and each PASS before the following copy. VIEW.BAS must report S05.COM length 1635 bytes, beginning with:

```text
FC 81 FC FE FF 74 03 E9 26 04 E8 7E 00 B4 4C CD 21 55 8B EC 81 EC 80 00 81 FC 00 F0 73 03 E9 0F
```

Run `CHECK S05`. Press F10 at the prompt. CHECK must report PASS; a different key deliberately returns FAIL.

## If the check disagrees

Check the saved binding stage and the stated build reports first. A runtime-label error means the matching EDITRT.ASM was not beside the translator. Compare the registers and extent checks before changing the test.
