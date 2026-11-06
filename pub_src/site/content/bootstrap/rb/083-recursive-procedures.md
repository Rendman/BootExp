+++
title = "Recursive procedures"
weight = 51
description = "Each call owns its parameters and local words. Recursion therefore saves the pending multiplication in the caller rather than sharing one global parameter cell."
download = "ERECUR.RIL"
download_group = "tools/rillboot"
aliases = ["/bootstrap/rill/083-recursive-procedures/"]
reader_names = 1
+++

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
CHECK RILLBOOT
COPY RESULT.IR SOURCE.IR
CHECK IWKEEP
COPY RESULT.ASM SOURCE.ASM
CHECK ASMAKEEP
```

Require `OK RESULT.IR 0000000494`, translator `OK RESULT.ASM 0000005903 text bytes`, and assembler `OK RESULT.COM 01237 bytes`, each with PASS **before** the following copy. VIEW.BAS must show result length 1237 and these first thirty-two bytes:

```text
FC 81 FC FE FF 74 03 E9 82 04 E8 AA 00 B4 4C CD 21 55 8B EC 81 EC 20 00 81 FC 00 F0 73 03 E9 6B
```

Copy RESULT.COM to ERECUR.COM. CHECK ERECUR displays "R" and reports PASS. Here `\r\n` means carriage return and line feed.

For a separate source rejection, create BAD.RIL:

```rill
fn main(){return missing(5);}
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
