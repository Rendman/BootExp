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
    outstr("JE NEAR R_ARGDONE\r\nADD BX,13\r\nJMP R_ARGNEXT\r\nR_ARGDONE:\r\nMOV AX,BX\r\nJMP R_OK\r\nR_ARGBAD:\r\nMOV AX,0\r\nJMP R_ERROR\r\nCMDCOUNT:\r\nDW 0\r\nCMDPTR:\r\nDW 0\r\nCMDBUF:\r\nDB 0,0,0,0,0,0,0,0,0,0,0,0,0\r\nDB 0,0,0,0,0,0,0,0,0,0,0,0,0\r\nDB 0,0,0,0,0,0,0,0,0,0,0,0,");
    outstr("0\r\n");
```

Insert after old physical line 352.

Insert:

```rill
    editorruntime(); return 0;
}
fn editorruntime() {
    let mut file=open(filearg(3,"EDITRT.ASM")); if status() { fail(6); }
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

Insert after old physical line 322.

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
    let mut count=argc();
    if count==0{return fallback;}
```

Remove old physical positions 249–249:

```rill
    if count!=2{exit(1);}
```

Replace with:

```rill
    if (count!=2)&(count!=3){exit(1);}
    if n==3{if count==2{return fallback;}}
    if count==3{if filesame(arg(3),arg(1))|filesame(arg(3),arg(2))|filesame(arg(3),"IRTX.TMP")|filesame(arg(3),"IRRES.BAK"){exit(1);}}
```

The following old source remains:

```rill
    if filesame(arg(1),arg(2))|filesame(arg(1),"IRTX.TMP")|filesame(arg(1),"IRRES.BAK")|filesame(arg(2),"IRTX.TMP")|filesame(arg(2),"IRRES.BAK"){exit(1);}
    return arg(n);
```

### Edit 4

Unchanged source immediately before the edit:

```rill
    if delta == 3 { if depth < 2 { fail(4); } depth = depth-2; }
    if delta == 4 { if depth { fail(4); } }
```

Insert after old physical line 169.

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
CHECK R0 IRED.RIL RESULT.IR
CHECK I0 RESULT.IR RESULT.ASM
CHECK A0 RESULT.ASM RESULT.COM
COPY RESULT.COM IRED.COM
```

Require compiler `OK RESULT.IR 0000047148`, translator `OK RESULT.ASM 0000163312 text bytes`, assembler `OK RESULT.COM 33598 bytes`, and each PASS before the following copy. VIEW.BAS must report IRED.COM length 33598 bytes, beginning with:

```text
FC 81 FC FE FF 74 03 E9 8D 81 E8 D3 81 81 F8 FF FF 75 03 E9 81 81 E8 D9 7D B4 4C CD 21 00 00 00
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
CHECK IRED Q02.IR RESULT.ASM EDITRT.ASM
```

Require FAIL with CODE 00004: BMOVE has no four saved arguments. Keep all binding files as ASCII assembly source. A missing EDITRT.ASM is an I/O error and cannot publish a new RESULT.ASM.

## If the check disagrees

Check the table spelling, argument counts and exact insertion points. Keep the earlier builder executable so a rejected source cannot strand the workbench.
