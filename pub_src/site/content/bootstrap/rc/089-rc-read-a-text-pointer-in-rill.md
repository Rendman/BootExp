+++
title = "01 \u00b7 Printing a String"
weight = 1
description = "A is a pointer to terminated bytes."
download = "RC01.RIL"
download_group = "tools/rill"
aliases = ["/bootstrap/rill/089-rc-read-a-text-pointer-in-rill/"]
reader_names = 1
+++

## The working parts

The parameter s points to zero-terminated bytes. Read one byte, stop at zero, or print it and advance s. The parameter belongs to this call.

The workbench explains the shared build steps and how to inspect intermediate files. Each stopping point below exercises the new routine.

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

Require:

```text
HI
PASS
```

## If the result differs

Check the zero terminator and the pointer after each output call.
