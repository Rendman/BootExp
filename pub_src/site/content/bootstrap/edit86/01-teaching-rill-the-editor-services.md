+++
title = "01 \u00b7 Teaching RILL the editor services"
weight = 1
description = "Keep the established compiler and add only the service names needed by a screen editor. Share the built-in lookup instead of copying its scanner."
download = "RILLED.RIL"
download_group = "tools/edit86"
reader_names = 1
+++

Keep the established compiler and add only the service names needed by a screen editor. Share the built-in lookup instead of copying its scanner.

The old built-in table remains intact. `findbuiltin(p)` performs the same complete-token match and argument setup for either table. An unsuccessful first lookup leaves the current source token available for the editor table. Each record names a source spelling, an arity and an IR sequence. The POP before a multi-argument operation places the final argument in A; the preceding arguments remain on the expression stack. This changes neither ordinary user procedures nor the language's frame bounds.

## Enter the source

Copy the exact toolchain RILL.RIL to RILLED.RIL.

Keep the unchanged source. Apply these edits from the bottom of the old file upward; physical positions locate text and are not source to type.

### Edit 1

Unchanged source immediately before the edit:

```rill
fn builtin() {
    let mut p = "PUTC\01\0POP\nPUTC\0STATUS\00\0STATUS\0OPEN\01\0POP\nOPEN\0CREATE\01\0POP\nCREATE\0CLOSE\01\0POP\nCLOSE\0READ\03\0POP\nREAD\0WRITE\03\0POP\nWRITE\0EXISTS\01\0POP\nEXISTS\0DELETE\01\0POP\nDELETE\0RENAME\02\0POP\nRENAME\0ALLOC\01\0POP\nALLOC\0FREE\01\0POP\nFREEBLOCK\0GET8\02\0POP\nGET8\0GET16\02\0POP\nGET16\0SET8\03\0POP\nSET8\0SET16\03\0POP\nSET16\0LOAD8\01\0POP\nFETCHB\0LOAD16\01\0POP\nFETCH\0STORE8\02\0POP\nPUTB\0STORE16\02\0POP\nPUT\0EXIT\01\0POP\nEXIT\0\0";
```

Insert after old physical line 379.

Insert:

```rill
    let mut hit = findbuiltin(p); if hit { return hit; }
    return findbuiltin("VBEGIN\00\0VBEGIN\0VEND\00\0VEND\0VPOS\01\0POP\nVPOS\0VWRITE\02\0POP\nVWRITE\0KEY\00\0KEY\0BLOCKMOVE\05\0POP\nBMOVE\0BLOCKLOAD\04\0POP\nBLOAD\0BLOCKREAD\04\0POP\nBREAD\0\0");
}
fn findbuiltin(p) {
```

The following old source remains:

```rill
    let mut i = 0; let mut same = 0;
    while load8(p) {
```

## Build and preserve the builder

```dos
COPY RILLED.RIL SOURCE.RIL
CHECK R0
COPY RESULT.IR SOURCE.IR
CHECK I0
COPY RESULT.ASM SOURCE.ASM
CHECK A0
COPY RESULT.COM RILLED.COM
```

Require compiler `OK RESULT.IR 0000050410`, translator `OK RESULT.ASM 0000104969 text bytes`, assembler `OK RESULT.COM 26840 bytes`, and each PASS before the following copy. VIEW.BAS must report RILLED.COM length 26840 bytes, beginning with:

```text
FC 81 FC FE FF 74 03 E9 85 68 E8 DD 64 B4 4C CD 21 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
```

Create P01.RIL:

```rill
fn main(){
    vbegin();
    vend();
    return 0;
}
```

```dos
COPY P01.RIL SOURCE.RIL
CHECK RILLED
TYPE RESULT.IR
```

Require PASS and exactly this intermediate source:

```text
PROC F_MAIN 00000 64
VBEGIN
VEND
LIT 00000
RETURN
LIT 0
RETURN
PROC MAIN 0 0
INVOKE F_MAIN 0
RETURN
```

Create Q01.RIL for a wrong-arity check:

```rill
fn main(){
    vpos();
    return 0;
}
```

```dos
COPY Q01.RIL SOURCE.RIL
CHECK RILLED
```

Require FAIL; VPOS needs one argument. No native screen code is needed to inspect these compiler results.

## If the check disagrees

Check the table spelling, argument counts and exact insertion points. Keep the earlier builder executable so a rejected source cannot strand the workbench.
