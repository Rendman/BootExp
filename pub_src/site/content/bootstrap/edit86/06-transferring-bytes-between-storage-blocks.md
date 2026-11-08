+++
title = "06 \u00b7 Transferring bytes between storage blocks"
weight = 6
description = "Copy counted bytes between a near I/O buffer and an allocated block. Validate the complete source and destination extents before changing memory."
download = "S06.ASM"
download_group = "tools/edit86"
reader_names = 1
+++

Copy counted bytes between a near I/O buffer and an allocated block. Validate the complete source and destination extents before changing memory.

BLOAD copies from a near buffer into a checked block; BREAD copies in the other direction. The private words remember both segment/offset pairs and the count while R_BLOCKPTR validates the allocated extent. A near transfer that wraps its sixteen-bit address is rejected. R_COPY selects a backward copy only when a destination follows its source within the same overlapping block; otherwise it copies forward. Every exit restores the segment state expected by generated code. The probe checks actual recovered bytes and an invalid extent through status, without a display helper.

## Enter the source

Copy S05.ASM to S06.ASM.

Keep the unchanged source. Apply these edits from the bottom of the old file upward; physical positions locate text and are not source to type.

### Edit 1

Unchanged source immediately before the edit:

```asm
R_KEYMAP:
DB 75,77,72,80,71,79,73,81,83,60,68,62,61,63,64,65
```

Insert after old physical line 185.

Insert:

```asm
R_MC:
DW 0
R_MS:
DW 0
R_MO:
DW 0
R_DS:
DW 0
R_DO:
DW 0
```

The following old source remains:

```asm
R_EDOK:
PUSH AX
```

### Edit 2

Unchanged source immediately before the edit:

```asm
; BX source block, CX source offset, DX destination block,
; DI destination offset, AX count. Validate both before copying.
```

Insert after old physical line 169.

Insert:

```asm
R_BLOAD:
MOV [R_MC],AX
MOV [R_MO],DX
ADD DX,AX
JC NEAR R_EBAD
MOV AX,CS
MOV [R_MS],AX
MOV AX,CX
MOV CX,[R_MC]
CALL R_BLOCKPTR
CMP AX,0
JE NEAR R_EBAD
MOV AX,ES
MOV [R_DS],AX
MOV [R_DO],BX
JMP R_COPY
R_BREAD:
MOV [R_MC],AX
MOV [R_DO],DX
ADD DX,AX
JC NEAR R_EBAD
MOV AX,CS
MOV [R_DS],AX
MOV AX,CX
MOV CX,[R_MC]
CALL R_BLOCKPTR
CMP AX,0
JE NEAR R_EBAD
MOV AX,ES
MOV [R_MS],AX
MOV [R_MO],BX
R_COPY:
MOV AX,[R_MS]
MOV DX,[R_DS]
MOV SI,[R_MO]
MOV DI,[R_DO]
MOV CX,[R_MC]
CMP AX,DX
JNE NEAR R_COPYFORWARD
CMP DI,SI
JBE NEAR R_COPYFORWARD
MOV BX,DI
SUB BX,SI
CMP BX,CX
JAE NEAR R_COPYFORWARD
MOV DS,AX
MOV ES,DX
ADD SI,CX
ADD DI,CX
R_COPYBACK:
CMP CX,0
JE NEAR R_COPYDONE
DEC SI
DEC DI
MOV AL,[SI]
MOV ES:[DI],AL
DEC CX
JMP R_COPYBACK
R_COPYFORWARD:
MOV DS,AX
MOV ES,DX
R_COPYNEXT:
CMP CX,0
JE NEAR R_COPYDONE
MOV AL,[SI]
MOV ES:[DI],AL
INC SI
INC DI
DEC CX
JMP R_COPYNEXT
R_COPYDONE:
MOV AX,CS
MOV DS,AX
MOV ES,AX
MOV AX,0
JMP R_EDOK
```

The following old source remains:

```asm
R_VACTIVE:
DB 0
```

## The service probe

Create S06.RIL as plain text:

```rill
bytes data[6];
fn main(){
    let mut h=alloc(64);
    if status(){
        return 1;
    }
    blockload(h,10,"ABCDEF",6);
    let mut bad=status();
    blockread(h,10,data,6);
    bad=bad|status();
    let mut i=0;
    while i<6{
        if data[i]!=load8("ABCDEF"+i){
            bad=1;
        }
        i=i+1;
    }
    blockread(h,63,data,2);
    if status()==0{
        bad=1;
    }
    free(h);
    return bad|status();
}
```

```dos
COPY S06.ASM EDITRT.ASM
```

```dos
COPY S06.RIL SOURCE.RIL
CHECK RILLED
COPY RESULT.IR SOURCE.IR
CHECK IRED
COPY RESULT.ASM SOURCE.ASM
CHECK A0
COPY RESULT.COM S06.COM
```

Require compiler `OK RESULT.IR 0000001133`, translator `OK RESULT.ASM 0000010529 text bytes`, assembler `OK RESULT.COM 02106 bytes`, and each PASS before the following copy. VIEW.BAS must report S06.COM length 2106 bytes, beginning with:

```text
FC 81 FC FE FF 74 03 E9 21 05 E8 79 01 B4 4C CD 21 00 00 00 00 00 00 55 8B EC 81 EC 80 00 81 FC
```

Run `CHECK S06`. The exact copied bytes and the rejected extent are checked through status. CHECK must report PASS; no display helper is added.

The invalid transfer starts at offset 63 of a sixty-four-byte block and requests two bytes. It must fail before changing destination memory. Every allocated probe block is freed.

## If the check disagrees

Check the saved binding stage and the stated build reports first. A runtime-label error means the matching EDITRT.ASM was not beside the translator. Compare the registers and extent checks before changing the test.
