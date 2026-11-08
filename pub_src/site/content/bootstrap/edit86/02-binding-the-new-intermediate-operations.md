+++
title = "02 \u00b7 Binding the new intermediate operations"
weight = 2
description = "Define screen positions, key events and bounded transfers in the intermediate language. Keep BIOS calls, native registers and segments inside an explicit target binding."
download = "IRED.RIL"
download_group = "tools/edit86"
reader_names = 1
+++

Define screen positions, key events and bounded transfers in the intermediate language. Keep BIOS calls, native registers and segments inside an explicit target binding.

The new operations have no physical-register operands. VPOS takes a cell number in A; VWRITE consumes one saved value and A. BLOAD and BREAD consume three saved values plus A; BMOVE consumes four plus A. Delta values 6 and 5 describe those latter stack effects. Check depth before subtracting it. `editorruntime` reads EDITRT.ASM after source translation has finished, so it may reuse inbuf. It copies every positive read through outchar; it neither assembles text nor supplies instruction bytes. A missing binding aborts publication.

## Enter the source

Copy the exact toolchain IR86.RIL to IRED.RIL.

Keep the unchanged source. Apply these edits from the bottom of the old file upward; physical positions locate text and are not source to type.

### Edit 1

Unchanged source immediately before the edit:

```rill
    outstr(" R_MEMDONE\r\nR_SETWORD:\r\nMOV ES:[BX],AX\r\nJMP R_MEMDONE\r\nR_FREEBLOCK:\r\nMOV BX,AX\r\nCMP BX,1\r\nJB NEAR R_DFAIL\r\nCMP BX,16\r\nJA NEAR R_DFAIL\r\nDEC BX\r\nSHL BX,1\r\nSHL BX,1\r\nADD BX,R_BLOCKS\r\nMOV SI,BX\r\nMOV AX,[SI]\r\nCMP AX,0\r\nJE NEAR R_DFAIL\r\nMOV ES,AX");
    outstr("\r\nMOV AH,49H\r\nINT 21H\r\nJC NEAR R_FREEBAD\r\nMOV WORD [SI],0\r\nMOV AX,CS\r\nMOV ES,AX\r\nMOV AX,0\r\nJMP R_OK\r\nR_FREEBAD:\r\nMOV AX,CS\r\nMOV ES,AX\r\nJMP R_FAIL\r\nR_STACKFAIL:\r\nMOV AX,4C02H\r\nINT 21H\r\nR_WANT:\r\nDW 0\r\nR_MEMVALUE:\r\nDW 0\r\nR_BLOCKS:\r\nRESW 32\r\n");
```

Insert after old physical line 327.

Insert:

```rill
    editorruntime(); return 0;
}
fn editorruntime() {
    let mut file=open("EDITRT.ASM"); if status() { fail(6); }
    while 1 {
        let mut count=read(file,inbuf,4096); if status() { close(file); fail(6); }
        if count==0 { close(file); if status() { fail(6); } return 0; }
        let mut i=0; while i<count { outchar(inbuf[i]); i=i+1; }
    }
```

The following old source remains:

```rill
    return 0;
}
```

### Edit 2

Unchanged source immediately before the edit:

```rill
    op("SET8",0,3,"POP DX\r\nPOP BX\r\nMOV CX,1\r\nCALL R_SETMEM\r\n");
    op("SET16",0,3,"POP DX\r\nPOP BX\r\nMOV CX,2\r\nCALL R_SETMEM\r\n");
```

Insert after old physical line 304.

Insert:

```rill
    op("VBEGIN",0,0,"CALL R_VBEGIN\r\n");
    op("VEND",0,0,"CALL R_VEND\r\n");
    op("VPOS",0,0,"CALL R_VPOS\r\n");
    op("VWRITE",0,2,"POP DX\r\nCALL R_VWRITE\r\n");
    op("KEY",0,0,"CALL R_KEY\r\n");
    op("BMOVE",0,5,"POP DI\r\nPOP DX\r\nPOP CX\r\nPOP BX\r\nCALL R_BMOVE\r\n");
    op("BLOAD",0,6,"POP DX\r\nPOP CX\r\nPOP BX\r\nCALL R_BLOAD\r\n");
    op("BREAD",0,6,"POP DX\r\nPOP CX\r\nPOP BX\r\nCALL R_BREAD\r\n");
```

The following old source remains:

```rill
    return 0;
}
```

### Edit 3

Unchanged source immediately before the edit:

```rill
    if delta == 3 { if depth < 2 { fail(4); } depth = depth-2; }
    if delta == 4 { if depth { fail(4); } }
```

Insert after old physical line 168.

Insert:

```rill
    if delta == 5 { if depth < 4 { fail(4); } depth = depth-4; }
    if delta == 6 { if depth < 3 { fail(4); } depth = depth-3; }
```

The following old source remains:

```rill
    expand(t); return 0;
}
```

## Build and preserve the builder

```dos
COPY IRED.RIL SOURCE.RIL
CHECK R0
COPY RESULT.IR SOURCE.IR
CHECK I0
COPY RESULT.ASM SOURCE.ASM
CHECK A0
COPY RESULT.COM IRED.COM
```

Require compiler `OK RESULT.IR 0000042343`, translator `OK RESULT.ASM 0000140146 text bytes`, assembler `OK RESULT.COM 30657 bytes`, and each PASS before the following copy. VIEW.BAS must report IRED.COM length 30657 bytes, beginning with:

```text
FC 81 FC FE FF 74 03 E9 6E 77 E8 C6 73 B4 4C CD 21 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
```

Create the empty S02.ASM binding with `COPY NUL S02.ASM`, then copy it to EDITRT.ASM. Create P02.RIL:

```rill
fn main(){
    return 0;
}
```

Build P02.RIL with RILLED, IRED and A0 using the workbench pattern, preserving P02.COM. `CHECK P02` must report PASS. This program uses only the established runtime, so the binding can be empty.

Create Q02.IR:

```text
PROC MAIN 0 0
BMOVE
RETURN
```

```dos
COPY Q02.IR SOURCE.IR
CHECK IRED
```

Require FAIL with CODE 00004: BMOVE has no four saved arguments. Keep all binding files as ASCII assembly source. A missing EDITRT.ASM is an I/O error and cannot publish a new RESULT.ASM.

## If the check disagrees

Check the table spelling, argument counts and exact insertion points. Keep the earlier builder executable so a rejected source cannot strand the workbench.
