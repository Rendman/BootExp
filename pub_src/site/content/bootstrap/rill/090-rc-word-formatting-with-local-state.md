+++
title = "RC02 \u00b7 Word formatting with local state"
weight = 90
description = "Save the value, current decimal place, and output digit separately."
download = "RC02.RIL"
download_group = "toolchain"
+++

Save the value, current decimal place, and output digit separately.

## The working parts

Save the value, current decimal place, and output digit separately. Repeated subtraction chooses one digit at each place. Formatting cannot borrow a parser work cell that remains live across a call.

The entry diagnostic exercises the printed helper. Rejecting placeholders identify forms outside this stopping point. A diagnostic that emits only an IR fragment is inspected as text; it is not a complete compiler or output program.

## Enter the source

Copy RC01.RIL to RC02.RIL. Apply edits **from the bottom of the old file upward**. Physical positions refer to that unchanged old file; use the printed context to identify each place. Keep all other source.

### Edit 1

Unchanged source immediately before the edit:

```rill
fn main(){print("HI");return 0;}

fn print(s) { let mut c = 0; while 1 { c = load8(s); if c == 0 { return 0; } putc(c); s = s+1; } }
```

Insert after old physical line 37.

Insert:

```rill

fn printnum(n) {
    let mut place = 10000; let mut c = 0;
    while place { c = 48; while n >= place { n = n-place; c = c+1; } putc(c); place = place/10; }
    return 0;
}
```

### Edit 2

Unchanged source immediately before the edit:

```rill
bytes ident[32];
bytes string[512];
```

Remove this source at old physical positions 35–35 in RC01.RIL:

```rill
fn main(){print("HI");return 0;}
```

Replace it with:

```rill
fn main(){printnum(65535);return 0;}
```

The following old source remains in place:

```rill

fn print(s) { let mut c = 0; while 1 { c = load8(s); if c == 0 { return 0; } putc(c); s = s+1; } }
```

## Build this stopping point

```dos
COPY RC02.RIL SOURCE.RIL
CHECK RILLBOOT
```

Require `OK RESULT.IR 0000001723` and PASS. Copy RESULT.IR to SOURCE.IR.

```dos
CHECK IWKEEP
COPY RESULT.ASM SOURCE.ASM
CHECK ASMAKEEP
```

Require IR86 `OK RESULT.ASM 0000007664 text bytes` and PASS **before** the copy. Require assembler `OK RESULT.COM 10224 bytes` and PASS before saving:

```dos
COPY RESULT.COM RC02.COM
```

VIEW.BAS must report RC02.COM length 10224 bytes. Keep this executable and its source together.

## Acceptance check

```dos
CHECK RC02
```

Require, apart from command echo and the checker's separator:

```text
65535PASS
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
