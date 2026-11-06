+++
title = "RC06 \u00b7 A decimal character test"
weight = 6
description = "The decimal range is exactly ASCII 48 through 57."
download = "RC06.RIL"
download_group = "rc"
aliases = ["/bootstrap/rill/094-rc-a-decimal-character-test/"]
+++

The decimal range is exactly ASCII 48 through 57.

## The working parts

The decimal range is exactly ASCII 48 through 57. Punctuation next to a digit is not another numeric digit.

The entry diagnostic exercises the printed helper. Rejecting placeholders identify forms outside this stopping point. A diagnostic that emits only an IR fragment is inspected as text; it is not a complete compiler or output program.

## Enter the source

Copy RC05.RIL to RC06.RIL. Apply edits **from the bottom of the old file upward**. Physical positions refer to that unchanged old file; use the printed context to identify each place. Keep all other source.

### Edit 1

Unchanged source immediately before the edit:

```rill
    if c >= 97 { if c <= 122 { return 1; } }
    return 0;
}
```

Insert after old physical line 42.

Insert:

```rill

fn digit(c) { if c < 48 { return 0; } if c > 57 { return 0; } return 1; }
```

The following old source remains in place:

```rill

fn print(s) { let mut c = 0; while 1 { c = load8(s); if c == 0 { return 0; } putc(c); s = s+1; } }
```

### Edit 2

Unchanged source immediately before the edit:

```rill
bytes ident[32];
bytes string[512];
```

Remove this source at old physical positions 35–35 in RC05.RIL:

```rill
fn main(){printnum(letter(95));return 0;}
```

Replace it with:

```rill
fn main(){printnum(digit(57));return 0;}
```

The following old source remains in place:

```rill

fn letter(c) {
```

## Build this stopping point

```dos
COPY RC06.RIL SOURCE.RIL
CHECK RILLBOOT
```

Require `OK RESULT.IR 0000005425` and PASS. Copy RESULT.IR to SOURCE.IR.

```dos
CHECK IWKEEP
COPY RESULT.ASM SOURCE.ASM
CHECK ASMAKEEP
```

Require IR86 `OK RESULT.ASM 0000015165 text bytes` and PASS **before** the copy. Require assembler `OK RESULT.COM 11495 bytes` and PASS before saving:

```dos
COPY RESULT.COM RC06.COM
```

VIEW.BAS must report RC06.COM length 11495 bytes. Keep this executable and its source together.

## Acceptance check

```dos
CHECK RC06
```

Require, apart from command echo and the checker's separator:

```text
00001PASS
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
