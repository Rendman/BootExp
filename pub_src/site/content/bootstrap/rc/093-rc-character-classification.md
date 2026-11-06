+++
title = "05 \u00b7 Recognizing Identifier Characters"
weight = 5
description = "Accept an underscore or a letter in either ASCII case."
download = "RC05.RIL"
download_group = "tools/rill"
aliases = ["/bootstrap/rill/093-rc-character-classification/"]
reader_names = 1
+++

## The working parts

Accept an underscore or a letter in either ASCII case. The scanner performs case folding when saving a name; character recognition alone does not modify the source byte.

## Enter the source

Copy RC04.RIL to RC05.RIL. Apply edits **from the bottom of the old file upward**. Physical positions refer to that unchanged old file; use the printed context to identify each place. Keep all other source.

### Edit 1

Unchanged source immediately before the edit:

```rill
bytes ident[32];
bytes string[512];
```

Remove this source at old physical positions 35–35 in RC04.RIL:

```rill
fn main(){fail(2);return 0;}
```

Replace it with:

```rill
fn main(){return (letter(95))!=1;}

fn letter(c) {
    if c == 95 { return 1; }
    if c >= 65 { if c <= 90 { return 1; } }
    if c >= 97 { if c <= 122 { return 1; } }
    return 0;
}
```

The following old source remains in place:

```rill

fn print(s) { let mut c = 0; while 1 { c = load8(s); if c == 0 { return 0; } putc(c); s = s+1; } }
```

## Build this stopping point

```dos
COPY RC05.RIL SOURCE.RIL
CHECK RILLBOOT
```

Require `OK RESULT.IR 0000005129` and PASS. Copy RESULT.IR to SOURCE.IR.

```dos
CHECK IWKEEP
COPY RESULT.ASM SOURCE.ASM
CHECK ASMAKEEP
```

Require IR86 `OK RESULT.ASM 0000014622 text bytes` and PASS **before** the copy. Require assembler `OK RESULT.COM 11395 bytes` and PASS before saving:

```dos
COPY RESULT.COM RC05.COM
```

VIEW.BAS must report RC05.COM length 11395 bytes. Keep this executable and its source together.

## Acceptance check

```dos
CHECK RC05
```

The checker must report PASS. The driver compares the result with 1 and returns nonzero on a mismatch; it adds no display routine.

## If the result differs

Compare letter with the printed addition. Check its arguments and saved state across calls, then inspect the generated text or bytes.
