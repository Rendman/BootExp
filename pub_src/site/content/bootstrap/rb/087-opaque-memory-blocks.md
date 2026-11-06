+++
title = "Opaque memory blocks"
weight = 55
description = "An allocated block is identified by a handle, not an address. Offsets are byte counts. The last valid word in a 40960-byte block begins at 40958; starting it one byte later must fail without reading outside the block."
download = "EHEAP.RIL"
download_group = "tools/rillboot"
aliases = ["/bootstrap/rill/087-opaque-memory-blocks/"]
reader_names = 1
+++

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
CHECK RILLBOOT
COPY RESULT.IR SOURCE.IR
CHECK IWKEEP
COPY RESULT.ASM SOURCE.ASM
CHECK ASMAKEEP
```

Require `OK RESULT.IR 0000000866`, translator `OK RESULT.ASM 0000006446 text bytes`, and assembler `OK RESULT.COM 01334 bytes`, each with PASS **before** the following copy. VIEW.BAS must show result length 1334 and these first thirty-two bytes:

```text
FC 81 FC FE FF 74 03 E9 E3 04 E8 0B 01 B4 4C CD 21 55 8B EC 81 EC 20 00 81 FC 00 F0 73 03 E9 CC
```

Copy RESULT.COM to EHEAP.COM. CHECK EHEAP displays "A" and reports PASS. Here `\r\n` means carriage return and line feed.

For a separate source rejection, create BAD.RIL:

```rill
fn main(){return get16(1);}
```

```dos
COPY BAD.RIL SOURCE.RIL
CHECK RILLBOOT
```

Require:

```text
ERROR 0000000001 CODE 00004
FAIL
```

The older RESULT.IR must remain unchanged. An unexpected PASS fails the rejection check. Restore the accepted source before another build.
