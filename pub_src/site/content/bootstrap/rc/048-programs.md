+++
title = "Complete RILL programs"
weight = 46
description = "Recursion, checked allocated storage, and counted files through the RILL-written compiler."
download = "RILL.ZIP"
download_group = "tools/rill"
reader_names = 1
+++

Use R0.COM, the completed RILL compiler built by RILLBOOT. Keep IWKEEP and ASMAKEEP as the translator and assembler. These programs use the same language accepted by the RILLBOOT seed; their IR and executable bytes must agree through both compilers.

## Recursive procedures

Each call owns its parameters and local words. Recursion therefore saves the pending multiplication in the caller rather than sharing one global parameter cell.

Save ERECUR.RIL:

```rill
fn factorial(n) {
    if n == 0 { return 1; }
    return n*factorial(n-1);
}
fn main() {
    if factorial(5) == 120 { putc(82); }
    return 0;
}
```

```dos
COPY ERECUR.RIL SOURCE.RIL
CHECK R0
COPY RESULT.IR SOURCE.IR
CHECK IWKEEP
COPY RESULT.ASM SOURCE.ASM
CHECK ASMAKEEP
```

Require compiler `OK RESULT.IR 0000000494`, translator `OK RESULT.ASM 0000005672 text bytes`, and assembler `OK RESULT.COM 01189 bytes`, each with PASS **before** the following copy. VIEW.BAS must report length 1189 and these first thirty-two bytes:

```text
FC 81 FC FE FF 74 03 E9 52 04 E8 AA 00 B4 4C CD 21 55 8B EC 81 EC 20 00 81 FC 00 F0 73 03 E9 3B
```

```dos
COPY RESULT.COM ERECUR.COM
```

CHECK ERECUR displays "R" and reports PASS. 

For a separate rejection, save BAD.RIL:

```rill
fn main(){return missing(5);}
```

```dos
COPY BAD.RIL SOURCE.RIL
CHECK R0
```

Require `ERROR 0000000001 CODE 00004` and FAIL. The accepted RESULT.IR must remain unchanged. An unexpected PASS fails the check. Restore the accepted source before building again.

## Opaque memory blocks

An allocated block is identified by a handle, not an address. Offsets are byte counts. The last valid word in a 40960-byte block begins at 40958; starting it one byte later must fail without reading outside the block.

Save EHEAP.RIL:

```rill
fn main() {
    let mut h=alloc(40960);
    if status() { return 1; }
    set16(h,40958,4660);
    if status() { free(h); return 1; }
    let mut n=get16(h,40958);
    get16(h,40959);
    let mut rejected=status();
    free(h);
    if status() { return 1; }
    if n==4660 { if rejected==1 { putc(65); } }
    return 0;
}
```

```dos
COPY EHEAP.RIL SOURCE.RIL
CHECK R0
COPY RESULT.IR SOURCE.IR
CHECK IWKEEP
COPY RESULT.ASM SOURCE.ASM
CHECK ASMAKEEP
```

Require compiler `OK RESULT.IR 0000000866`, translator `OK RESULT.ASM 0000006215 text bytes`, and assembler `OK RESULT.COM 01286 bytes`, each with PASS **before** the following copy. VIEW.BAS must report length 1286 and these first thirty-two bytes:

```text
FC 81 FC FE FF 74 03 E9 B3 04 E8 0B 01 B4 4C CD 21 55 8B EC 81 EC 20 00 81 FC 00 F0 73 03 E9 9C
```

```dos
COPY RESULT.COM EHEAP.COM
```

CHECK EHEAP displays "A" and reports PASS. 

For a separate rejection, save BAD.RIL:

```rill
fn main(){return get16(1);}
```

```dos
COPY BAD.RIL SOURCE.RIL
CHECK R0
```

Require `ERROR 0000000001 CODE 00004` and FAIL. The accepted RESULT.IR must remain unchanged. An unexpected PASS fails the check. Restore the accepted source before building again.

## Counted file transfer

File handles carry access modes and remain opaque. Read returns actual progress, with zero for EOF. Check status and the exact write count before reusing the buffer. File data preserves every byte, including Control-Z.

Save ECOPY.RIL:

```rill
bytes block[256];
fn main() {
    let mut input=open("IN.TXT");
    if status() { return 1; }
    let mut output=create("OUT.TXT");
    if status() { close(input); return 1; }
    let mut n=read(input,block,256);
    while n {
        if status() { close(input); close(output); return 1; }
        let mut written=write(output,block,n);
        if status() | (written!=n) { close(input); close(output); return 1; }
        n=read(input,block,256);
    }
    if status() { close(input); close(output); return 1; }
    close(input); if status() { close(output); return 1; }
    close(output); if status() { return 1; }
    return 0;
}
```

```dos
COPY ECOPY.RIL SOURCE.RIL
CHECK R0
COPY RESULT.IR SOURCE.IR
CHECK IWKEEP
COPY RESULT.ASM SOURCE.ASM
CHECK ASMAKEEP
```

Require compiler `OK RESULT.IR 0000001476`, translator `OK RESULT.ASM 0000007346 text bytes`, and assembler `OK RESULT.COM 01717 bytes`, each with PASS **before** the following copy. VIEW.BAS must report length 1717 and these first thirty-two bytes:

```text
FC 81 FC FE FF 74 03 E9 62 06 E8 BA 02 B4 4C CD 21 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
```

```dos
COPY RESULT.COM ECOPY.COM
```

Create IN.TXT with `ECHO A short copy.>IN.TXT`. CHECK ECOPY reports PASS. COMP IN.TXT OUT.TXT must report no differences; answer N to the compare-more-files question. An empty input and every possible byte value must also copy unchanged. 

For a separate rejection, save BAD.RIL:

```rill
fn main(){return read(1,2);}
```

```dos
COPY BAD.RIL SOURCE.RIL
CHECK R0
```

Require `ERROR 0000000001 CODE 00004` and FAIL. The accepted RESULT.IR must remain unchanged. An unexpected PASS fails the check. Restore the accepted source before building again.

