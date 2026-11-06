+++
title = "06 \u00b7 Recognizing Decimal Digits"
weight = 6
description = "The decimal range is exactly ASCII 48 through 57."
download = "RC06.RIL"
download_group = "tools/rill"
aliases = ["/bootstrap/rill/094-rc-a-decimal-character-test/"]
reader_names = 1
+++

## The working parts

The decimal range is exactly ASCII 48 through 57. Punctuation next to a digit is not another numeric digit.

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
fn main(){return (letter(95))!=1;}
```

Replace it with:

```rill
fn main(){return (digit(57))!=1;}
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

Require `OK RESULT.IR 0000005405` and PASS. Copy RESULT.IR to SOURCE.IR.

```dos
CHECK IWKEEP
COPY RESULT.ASM SOURCE.ASM
CHECK ASMAKEEP
```

Require IR86 `OK RESULT.ASM 0000015177 text bytes` and PASS **before** the copy. Require assembler `OK RESULT.COM 11497 bytes` and PASS before saving:

```dos
COPY RESULT.COM RC06.COM
```

VIEW.BAS must report RC06.COM length 11497 bytes. Keep this executable and its source together.

## Acceptance check

```dos
CHECK RC06
```

The checker must report PASS. The driver compares the result with 1 and returns nonzero on a mismatch; it adds no display routine.

## If the result differs

Compare digit with the printed addition. Check its arguments and saved state across calls, then inspect the generated text or bytes.
