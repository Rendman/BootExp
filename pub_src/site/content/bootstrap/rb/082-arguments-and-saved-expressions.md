+++
title = "Arguments and saved expressions"
weight = 50
description = "Arguments are evaluated from left to right. A call consumes its own argument words and leaves older expression operands available to the caller. Parameters are private mutable word cells."
download = "EARGS.RIL"
download_group = "tools/rillboot"
aliases = ["/bootstrap/rill/082-arguments-and-saved-expressions/"]
reader_names = 1
+++

Arguments are evaluated from left to right. A call consumes its own argument words and leaves older expression operands available to the caller. Parameters are private mutable word cells.

Save EARGS.RIL:

```rill
let mut count = 0;
fn bump() { count=count+1; return count; }
fn pair(a,b) { return a*10+b; }
fn twice(n) { return n*2; }
fn main() {
    if pair(bump(),bump()) == 12 {
        if 7+twice(9) == 25 { putc(65); }
    }
    return 0;
}
```

```dos
COPY EARGS.RIL SOURCE.RIL
CHECK RILLBOOT
COPY RESULT.IR SOURCE.IR
CHECK IWKEEP
COPY RESULT.ASM SOURCE.ASM
CHECK ASMAKEEP
```

Require `OK RESULT.IR 0000000735`, translator `OK RESULT.ASM 0000006427 text bytes`, and assembler `OK RESULT.COM 01335 bytes`, each with PASS **before** the following copy. VIEW.BAS must show result length 1335 and these first thirty-two bytes:

```text
FC 81 FC FE FF 74 03 E9 E4 04 E8 0C 01 B4 4C CD 21 00 00 55 8B EC 81 EC 20 00 81 FC 00 F0 73 03
```

Copy RESULT.COM to EARGS.COM. CHECK EARGS displays "A" and reports PASS. Here `\r\n` means carriage return and line feed.

For a separate source rejection, create BAD.RIL:

```rill
fn main(){return pair(1);} fn pair(a,b){return a+b;}
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
