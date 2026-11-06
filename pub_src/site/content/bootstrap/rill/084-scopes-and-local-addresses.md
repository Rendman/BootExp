+++
title = "Scopes and local addresses"
weight = 84
description = "A nested block may shadow a name from an outer block. Leaving it restores the earlier binding. The address operator produces a byte-addressed pointer to a live local; a pointer must not outlive its call frame."
download = "ESCOPE.RIL"
download_group = "toolchain"
+++

A nested block may shadow a name from an outer block. Leaving it restores the earlier binding. The address operator produces a byte-addressed pointer to a live local; a pointer must not outlive its call frame.

Save ESCOPE.RIL:

```rill
fn main() {
    let mut x=65;
    { let mut x=66; putc(x); }
    store16(&x,67);
    putc(x);
    return 0;
}
```

```dos
COPY ESCOPE.RIL SOURCE.RIL
CHECK RILLBOOT
COPY RESULT.IR SOURCE.IR
CHECK IWKEEP
COPY RESULT.ASM SOURCE.ASM
CHECK ASMAKEEP
```

Require `OK RESULT.IR 0000000256`, translator `OK RESULT.ASM 0000005398 text bytes`, and assembler `OK RESULT.COM 01146 bytes`, each with PASS **before** the following copy. VIEW.BAS must show result length 1146 and these first thirty-two bytes:

```text
FC 81 FC FE FF 74 03 E9 27 04 E8 4F 00 B4 4C CD 21 55 8B EC 81 EC 20 00 81 FC 00 F0 73 03 E9 10
```

Copy RESULT.COM to ESCOPE.COM. CHECK ESCOPE displays "BC" and reports PASS. Here `\r\n` means carriage return and line feed.

For a separate source rejection, create BAD.RIL:

```rill
fn main(){let mut x=x;return x;}
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
