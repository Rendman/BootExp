+++
title = "Indexed byte storage"
weight = 85
description = "A global byte buffer has a stable address. An indexed read returns one zero-extended byte; an indexed store writes the low byte. Ordinary pointers and indexing are unchecked, so the program must keep indices inside the declared buffer."
download = "EBYTES.RIL"
download_group = "toolchain"
+++

A global byte buffer has a stable address. An indexed read returns one zero-extended byte; an indexed store writes the low byte. Ordinary pointers and indexing are unchecked, so the program must keep indices inside the declared buffer.

Save EBYTES.RIL:

```rill
bytes message[4];
fn main() {
    message[0]=72; message[1]=73;
    let mut i=0;
    while i<2 { putc(message[i]); i=i+1; }
    return 0;
}
```

```dos
COPY EBYTES.RIL SOURCE.RIL
CHECK RILLBOOT
COPY RESULT.IR SOURCE.IR
CHECK IWKEEP
COPY RESULT.ASM SOURCE.ASM
CHECK ASMAKEEP
```

Require `OK RESULT.IR 0000000484`, translator `OK RESULT.ASM 0000005827 text bytes`, and assembler `OK RESULT.COM 01216 bytes`, each with PASS **before** the following copy. VIEW.BAS must show result length 1216 and these first thirty-two bytes:

```text
FC 81 FC FE FF 74 03 E9 6D 04 E8 95 00 B4 4C CD 21 00 00 00 00 55 8B EC 81 EC 20 00 81 FC 00 F0
```

Copy RESULT.COM to EBYTES.COM. CHECK EBYTES displays "HI" and reports PASS. Here `\r\n` means carriage return and line feed.

For a separate source rejection, create BAD.RIL:

```rill
bytes a[0]; fn main(){return 0;}
```

```dos
COPY BAD.RIL SOURCE.RIL
CHECK RILLBOOT
```

Require:

```text
ERROR 0000000001 CODE 00005
FAIL
```

The older RESULT.IR must remain unchanged. An unexpected PASS fails the rejection check. Restore the accepted source before another build.
