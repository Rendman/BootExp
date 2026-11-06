+++
title = "RC01 \u00b7 Read a text pointer in RILL"
weight = 89
description = "A is a pointer to terminated bytes."
download = "RC01.RIL"
download_group = "toolchain"
+++

A is a pointer to terminated bytes.

## The working parts

A is a pointer to terminated bytes. Save the pointer in a local slot before PUTC changes A. A zero byte ends the walk; it is not written.

The entry diagnostic exercises the printed helper. Rejecting placeholders identify forms outside this stopping point. A diagnostic that emits only an IR fragment is inspected as text; it is not a complete compiler or output program.

## Enter the source

Create RC01.RIL as plain text. This is its complete source:

```rill
// A RILL compiler written with ordinary RILL procedures, words, and byte buffers.
let mut table = 0;
let mut globals = 0;
let mut localcount = 0;
let mut level = 0;
let mut nextlocal = 0;
let mut tok = 0;
let mut value = 0;
let mut ch = 0;
let mut line = 1;
let mut linehi = 0;
let mut input = 0;
let mut output = 0;
let mut inpos = 0;
let mut inlen = 0;
let mut outlen = 0;
let mut total = 0;
let mut totalhi = 0;
let mut labelno = 0;
let mut ended = 0;
let mut own = 0;
let mut backup = 0;
let mut found = 0;
let mut rectype = 0;
let mut recval = 0;
let mut reclevel = 0;
let mut callbuiltin = 0;
let mut exprdepth = 0;
bytes decimal[10];
bytes inbuf[4096];
bytes outbuf[4096];
bytes ident[32];
bytes string[512];

fn main(){print("HI");return 0;}

fn print(s) { let mut c = 0; while 1 { c = load8(s); if c == 0 { return 0; } putc(c); s = s+1; } }
```

## Build this stopping point

```dos
COPY RC01.RIL SOURCE.RIL
CHECK RILLBOOT
```

Require `OK RESULT.IR 0000001201` and PASS. Copy RESULT.IR to SOURCE.IR.

```dos
CHECK IWKEEP
COPY RESULT.ASM SOURCE.ASM
CHECK ASMAKEEP
```

Require IR86 `OK RESULT.ASM 0000006730 text bytes` and PASS **before** the copy. Require assembler `OK RESULT.COM 10047 bytes` and PASS before saving:

```dos
COPY RESULT.COM RC01.COM
```

VIEW.BAS must report RC01.COM length 10047 bytes. Keep this executable and its source together.

## Acceptance check

```dos
CHECK RC01
```

Require, apart from command echo and the checker's separator:

```text
HIPASS
```

## A rejection or boundary check

Check the same word boundary in the compiler seed. Create BAD.RIL:

```rill
fn main(){return 65536;}
```

```dos
COPY BAD.RIL SOURCE.RIL
CHECK RILLBOOT
```

Require `ERROR 0000000001 CODE 00003` and FAIL, preserving the accepted RESULT.IR. An unexpected PASS fails this check.

## If the result differs

Check the saved pointer or slot, argument order, complete token spelling, and STATUS immediately after each service. A helper's local state must survive calls; an output count is independent of input position. Inspect text and file length before interpreting any bytes as a program.
