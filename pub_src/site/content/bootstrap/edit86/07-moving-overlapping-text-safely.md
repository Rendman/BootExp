+++
title = "07 \u00b7 Moving overlapping text safely"
weight = 7
description = "Move bytes within or between allocated blocks, including overlap. A gap buffer must preserve text when either copy direction overlaps its source."
download = "S07.ASM"
download_group = "tools/edit86"
reader_names = 1
+++

Move bytes within or between allocated blocks, including overlap. A gap buffer must preserve text when either copy direction overlaps its source.

BMOVE receives source handle, source offset, destination handle, destination offset and count. Resolve both opaque handles with R_BLOCKPTR before touching the destination. The checked descriptor values are private to the binding; the source program keeps only handles. The shared copy handles both directions. The probe first produces AABCDE by moving five overlapping bytes to the right, then ABCDEE by moving them left. A rejected source extent must not turn into a partial copy.

## Enter the source

Copy S06.ASM to S07.ASM.

Keep the unchanged source. Apply these edits from the bottom of the old file upward; physical positions locate text and are not source to type.

### Edit 1

Unchanged source immediately before the edit:

```asm
R_DO:
DW 0
```

Insert after old physical line 271.

Insert:

```asm
R_MDH:
DW 0
R_MDO:
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
R_BMOVE:
MOV [R_MC],AX
MOV [R_MDH],DX
MOV [R_MDO],DI
MOV AX,CX
MOV CX,[R_MC]
CALL R_BLOCKPTR
CMP AX,0
JE NEAR R_EBAD
MOV AX,ES
MOV [R_MS],AX
MOV [R_MO],BX
MOV BX,[R_MDH]
MOV AX,[R_MDO]
MOV CX,[R_MC]
CALL R_BLOCKPTR
CMP AX,0
JE NEAR R_EBAD
MOV AX,ES
MOV [R_DS],AX
MOV [R_DO],BX
JMP R_COPY
; BX block, CX block offset, DX near pointer, AX count.
```

The following old source remains:

```asm
R_BLOAD:
MOV [R_MC],AX
```

## The service probe

Create S07.RIL as plain text:

```rill
bytes data[6];
fn main(){
    let mut h=alloc(64);
    if status(){
        return 1;
    }
    blockload(h,0,"ABCDEF",6);
    blockmove(h,0,h,1,5);
    let mut bad=status();
    blockread(h,0,data,6);
    bad=bad|status();
    let mut i=0;
    while i<6{
        if data[i]!=load8("AABCDE"+i){
            bad=1;
        }
        i=i+1;
    }
    blockmove(h,1,h,0,5);
    bad=bad|status();
    blockread(h,0,data,6);
    bad=bad|status();
    i=0;
    while i<6{
        if data[i]!=load8("ABCDEE"+i){
            bad=1;
        }
        i=i+1;
    }
    blockmove(h,63,h,0,2);
    if status()==0{
        bad=1;
    }
    free(h);
    return bad|status();
}
```

```dos
COPY S07.ASM EDITRT.ASM
```

```dos
COPY S07.RIL SOURCE.RIL
CHECK RILLED
COPY RESULT.IR SOURCE.IR
CHECK IRED
COPY RESULT.ASM SOURCE.ASM
CHECK A0
COPY RESULT.COM S07.COM
```

Require compiler `OK RESULT.IR 0000001935`, translator `OK RESULT.ASM 0000012524 text bytes`, assembler `OK RESULT.COM 02455 bytes`, and each PASS before the following copy. VIEW.BAS must report S07.COM length 2455 bytes, beginning with:

```text
FC 81 FC FE FF 74 03 E9 2D 06 E8 85 02 B4 4C CD 21 00 00 00 00 00 00 55 8B EC 81 EC 80 00 81 FC
```

Run `CHECK S07`. The exact copied bytes and the rejected extent are checked through status. CHECK must report PASS; no display helper is added.

The invalid transfer starts at offset 63 of a sixty-four-byte block and requests two bytes. It must fail before changing destination memory. Every allocated probe block is freed.

## If the check disagrees

Check the saved binding stage and the stated build reports first. A runtime-label error means the matching EDITRT.ASM was not beside the translator. Compare the registers and extent checks before changing the test.
