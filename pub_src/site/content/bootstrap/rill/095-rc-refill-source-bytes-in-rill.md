+++
title = "RC07 \u00b7 Refill source bytes in RILL"
weight = 95
description = "INPOS and INLEN describe an already-read block."
download = "RC07.RIL"
download_group = "toolchain"
+++

INPOS and INLEN describe an already-read block.

## The working parts

INPOS and INLEN describe an already-read block. Refill only after consuming it. A short positive read is data, not EOF. Check STATUS before using a count. Control-Z ends source text; the byte services used by a compiled program still preserve that value.

The entry diagnostic exercises the printed helper. Rejecting placeholders identify forms outside this stopping point. A diagnostic that emits only an IR fragment is inspected as text; it is not a complete compiler or output program.

## Enter the source

Copy RC06.RIL to RC07.RIL. Apply edits **from the bottom of the old file upward**. Physical positions refer to that unchanged old file; use the printed context to identify each place. Keep all other source.

### Edit 1

Unchanged source immediately before the edit:

```rill
bytes ident[32];
bytes string[512];
```

Remove this source at old physical positions 35–35 in RC06.RIL:

```rill
fn main(){printnum(digit(57));return 0;}
```

Replace it with:

```rill
fn main(){input=open("SOURCE.RIL");if status(){fail(1);}next();printnum(ch);return 0;}

fn next() {
    if ch == 10 {
        line = line+1;
        if line == 0 { linehi = linehi+1; if linehi == 0 { fail(5); } }
    }
    if ended { ch = 0; return 0; }
    if inpos == inlen {
        inlen = read(input,inbuf,4096);
        if status() != 0 { fail(1); }
        inpos = 0;
        if inlen == 0 { ended = 1; ch = 0; return 0; }
    }
    ch = inbuf[inpos]; inpos = inpos+1;
    if ch == 26 { ended = 1; ch = 0; return 0; }
    if ch == 0 { fail(2); }
    if ch >= 127 { fail(2); }
    if ch < 32 {
        if ch != 9 { if ch != 10 { if ch != 13 { fail(2); } } }
    }
    return 0;
}
```

The following old source remains in place:

```rill

fn letter(c) {
```

## Build this stopping point

```dos
COPY RC07.RIL SOURCE.RIL
CHECK RILLBOOT
```

Require `OK RESULT.IR 0000007622` and PASS. Copy RESULT.IR to SOURCE.IR.

```dos
CHECK IWKEEP
COPY RESULT.ASM SOURCE.ASM
CHECK ASMAKEEP
```

Require IR86 `OK RESULT.ASM 0000019243 text bytes` and PASS **before** the copy. Require assembler `OK RESULT.COM 12215 bytes` and PASS before saving:

```dos
COPY RESULT.COM RC07.COM
```

VIEW.BAS must report RC07.COM length 12215 bytes. Keep this executable and its source together.

## Acceptance check

Create TRC07.RIL with COPY CON or a plain-text editor. Finish COPY CON with Ctrl-Z and Enter:

```rill
A
```

```dos
COPY TRC07.RIL SOURCE.RIL
```

```dos
CHECK RC07
```

Require, apart from command echo and the checker's separator:

```text
00065PASS
```

## A rejection or boundary check

Rename SOURCE.RIL to an unused HOLD.RIL and run CHECK RC07. Restore the source afterward.

Require:

```text
ERROR 0000000001 CODE 00001
FAIL
```

An unexpected PASS fails the rejection. The pre-existing RESULT.IR must remain unchanged; preserve a copy before the test.

## If the result differs

Check the saved pointer or slot, argument order, complete token spelling, and STATUS immediately after each service. A helper's local state must survive calls; an output count is independent of input position. Inspect text and file length before interpreting any bytes as a program.
