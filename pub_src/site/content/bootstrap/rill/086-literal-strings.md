+++
title = "Literal strings"
weight = 86
description = "A quoted literal produces a pointer to zero-terminated bytes. It is data, not a printing operation. The small print procedure reads one byte at a time; backslash escapes supply CR and LF explicitly."
download = "ESTRING.RIL"
download_group = "toolchain"
+++

A quoted literal produces a pointer to zero-terminated bytes. It is data, not a printing operation. The small print procedure reads one byte at a time; backslash escapes supply CR and LF explicitly.

Save ESTRING.RIL:

```rill
fn print(s) {
    while load8(s) { putc(load8(s)); s=s+1; }
    return 0;
}
fn main() {
    print("Hello; RILL\r\n");
    return 0;
}
```

```dos
COPY ESTRING.RIL SOURCE.RIL
CHECK RILLBOOT
COPY RESULT.IR SOURCE.IR
CHECK IWKEEP
COPY RESULT.ASM SOURCE.ASM
CHECK ASMAKEEP
```

Require `OK RESULT.IR 0000000400`, translator `OK RESULT.ASM 0000005889 text bytes`, and assembler `OK RESULT.COM 01219 bytes`, each with PASS **before** the following copy. VIEW.BAS must show result length 1219 and these first thirty-two bytes:

```text
FC 81 FC FE FF 74 03 E9 70 04 E8 98 00 B4 4C CD 21 55 8B EC 81 EC 20 00 81 FC 00 F0 73 03 E9 59
```

Copy RESULT.COM to ESTRING.COM. CHECK ESTRING displays "Hello; RILL\r\n" and reports PASS. Here `\r\n` means carriage return and line feed.

For a separate source rejection, create BAD.RIL:

```rill
fn main(){putc("open);}
```

```dos
COPY BAD.RIL SOURCE.RIL
CHECK RILLBOOT
```

Require:

```text
ERROR 0000000001 CODE 00002
FAIL
```

The older RESULT.IR must remain unchanged. An unexpected PASS fails the rejection check. Restore the accepted source before another build.
