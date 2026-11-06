+++
title = "Complete RILL programs"
weight = 32
description = "Byte output, a mutable counter, unsigned choice, and a checked byte-stream echo."
download = "RILL0.ZIP"
download_group = "tools/rill0"
reader_names = 1
+++

These programs use the completed compiler. For each NAME.RIL, copy it to SOURCE.RIL and run CHECK RLKEEP. Require the compiler count and PASS; copy RESULT.IR to NAME.IR. Run CHECK IRKEEP and CHECK ASMKEEP, entering NAME at each prompt, requiring both OK reports and PASS before executing NAME.COM.

## HELLO: Two output bytes

Save HELLO.RIL:

```rill
fn main() {
    putc(72);
    putc(73);
}
```

Each putc statement writes one ASCII byte. There are no string literals, so each character is explicit. The normal end returns zero.

Require compiler `OK RESULT.IR 00052`, IR86 `OK HELLO.ASM 02600 text bytes`, and ASM0 `OK 00480 bytes`, each followed by PASS.

CHECK HELLO displays `HI` and reports PASS.

For a separate rejection, copy the source to BAD.RIL. Change its first `putc` to `putcat`. Require ERROR 00002 CODE 00002 and FAIL. Copy that changed file to SOURCE.RIL and run CHECK RLKEEP. An unexpected PASS is a failed rejection. The older RESULT.IR must remain unchanged. Restore the accepted source before building again.

## COUNT: A mutable counter

Save COUNT.RIL:

```rill
fn main() {
    let mut x = 48;
    while x < 51 {
        putc(x);
        x = x + 1;
    }
}
```

The declaration reserves x before MAIN. The unsigned condition is false at 51, and addition wraps as a word. The displayed 012 shows three completed iterations.

Require compiler `OK RESULT.IR 00153`, IR86 `OK COUNT.ASM 02783 text bytes`, and ASM0 `OK 00511 bytes`, each followed by PASS.

CHECK COUNT displays `012` and reports PASS.

For a separate rejection, copy the source to BAD.RIL. Remove the declaration of x. Require ERROR 00002 CODE 00004 and FAIL. Copy that changed file to SOURCE.RIL and run CHECK RLKEEP. An unexpected PASS is a failed rejection. The older RESULT.IR must remain unchanged. Restore the accepted source before building again.

## CHOICE: Unsigned choice

Save CHOICE.RIL:

```rill
fn main() {
    let mut x = 65535;
    if x > 1 {
        putc(85);
    } else {
        putc(76);
    }
    if x == 65535 {
        putc(33);
    }
}
```

The word 65535 is greater than one in unsigned order. The first branch prints U; equality then prints an exclamation mark. There is no implicit signed interpretation.

Require compiler `OK RESULT.IR 00232`, IR86 `OK CHOICE.ASM 02891 text bytes`, and ASM0 `OK 00526 bytes`, each followed by PASS.

CHECK CHOICE displays `U!` and reports PASS.

For a separate rejection, copy the source to BAD.RIL. Change the initializer 65535 to 65536. Require ERROR 00002 CODE 00003 and FAIL. Copy that changed file to SOURCE.RIL and run CHECK RLKEEP. An unexpected PASS is a failed rejection. The older RESULT.IR must remain unchanged. Restore the accepted source before building again.

## RLECHO: A checked byte stream

Save RLECHO.RIL:

```rill
fn main() {
    let mut c = 0;
    let mut s = 0;
    c = getc();
    s = status();
    while s == 0 {
        if c == 65535 {
            exit(0);
        }
        putc(c);
        s = status();
        if s != 0 {
            exit(1);
        }
        c = getc();
        s = status();
    }
    exit(1);
}
```

c saves the input before status() is read. EOF is 65535 with success status; it exits zero. Every ordinary byte, including 255, is written and output status checked. A failed input or output exits one.

Require compiler `OK RESULT.IR 00397`, IR86 `OK RLECHO.ASM 03236 text bytes`, and ASM0 `OK 00595 bytes`, each followed by PASS.

Create KEY.TXT with `ECHO RILL echo.>KEY.TXT`. Run `CHECK RLECHO <KEY.TXT`; it displays `RILL echo.` with CR/LF and reports PASS. An empty input file produces no text and still reports PASS. The compiler source reader's Control-Z convention does not apply to this program's byte input.

For a separate rejection, copy the source to BAD.RIL. Change `getc()` to `getc(1)`. Require ERROR 00004 CODE 00002 and FAIL. Copy that changed file to SOURCE.RIL and run CHECK RLKEEP. An unexpected PASS is a failed rejection. The older RESULT.IR must remain unchanged. Restore the accepted source before building again.

