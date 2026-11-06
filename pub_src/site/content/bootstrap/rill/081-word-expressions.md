+++
title = "Word expressions"
weight = 81
description = "Products, quotients, remainders, shifts, and comparisons have fixed word results. A comparison is itself zero or one, so a condition needs no special comparison parser."
download = "EWORDS.RIL"
download_group = "toolchain"
+++

Products, quotients, remainders, shifts, and comparisons have fixed word results. A comparison is itself zero or one, so a condition needs no special comparison parser.

Save EWORDS.RIL:

```rill
fn main() {
    let mut n = (7+3)*4;
    if n == 40 {
        if 65535/255 == 257 {
            if (65535%256) == 255 {
                if ((1<<4)|(255&3)) == 19 { putc(65); }
            }
        }
    }
    return 0;
}
```

```dos
COPY EWORDS.RIL SOURCE.RIL
CHECK RILLBOOT
COPY RESULT.IR SOURCE.IR
CHECK IWKEEP
COPY RESULT.ASM SOURCE.ASM
CHECK ASMAKEEP
```

Require `OK RESULT.IR 0000000658`, translator `OK RESULT.ASM 0000006283 text bytes`, and assembler `OK RESULT.COM 01312 bytes`, each with PASS **before** the following copy. VIEW.BAS must show result length 1312 and these first thirty-two bytes:

```text
FC 81 FC FE FF 74 03 E9 CD 04 E8 F5 00 B4 4C CD 21 55 8B EC 81 EC 20 00 81 FC 00 F0 73 03 E9 B6
```

Copy RESULT.COM to EWORDS.COM. CHECK EWORDS displays "A" and reports PASS. Here `\r\n` means carriage return and line feed.

For a separate source rejection, create BAD.RIL:

```rill
fn main(){return 65536;}
```

```dos
COPY BAD.RIL SOURCE.RIL
CHECK RILLBOOT
```

Require:

```text
ERROR 0000000001 CODE 00003
FAIL
```

The older RESULT.IR must remain unchanged. An unexpected PASS fails the rejection check. Restore the accepted source before another build.
