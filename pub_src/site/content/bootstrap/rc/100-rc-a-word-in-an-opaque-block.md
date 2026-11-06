+++
title = "12 \u00b7 Reading a Word from Allocated Storage"
weight = 12
description = "An offset is meaningful only together with the TABLE block handle."
download = "RC12.RIL"
download_group = "tools/rill"
aliases = ["/bootstrap/rill/100-rc-a-word-in-an-opaque-block/"]
reader_names = 1
+++

## The working parts

An offset is meaningful only together with the TABLE block handle. GET16 reads the canonical low-byte-first word after validating its extent.

## Enter the source

Copy RC11.RIL to RC12.RIL. Apply edits **from the bottom of the old file upward**. Physical positions refer to that unchanged old file; use the printed context to identify each place. Keep all other source.

### Edit 1

Unchanged source immediately before the edit:

```rill

fn setident(s) { let mut i = 0; while 1 { ident[i] = load8(s+i); if ident[i] == 0 { return 0; } i = i+1; } }
```

Insert after old physical line 146.

Insert:

```rill
fn tword(p) { return get16(table,p); }
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

Remove this source at old physical positions 35–35 in RC11.RIL:

```rill
fn main(){setident("ABC");tok=1;return isword("ABC")!=1;}
```

Replace it with:

```rill
fn main(){table=alloc(22000);set16(table,100,4660);return (tword(100))!=4660;}
```

The following old source remains in place:

```rill

fn next() {
```

## Build this stopping point

```dos
COPY RC12.RIL SOURCE.RIL
CHECK RILLBOOT
```

Require `OK RESULT.IR 0000014604` and PASS. Copy RESULT.IR to SOURCE.IR.

```dos
CHECK IWKEEP
COPY RESULT.ASM SOURCE.ASM
CHECK ASMAKEEP
```

Require IR86 `OK RESULT.ASM 0000031861 text bytes` and PASS **before** the copy. Require assembler `OK RESULT.COM 14530 bytes` and PASS before saving:

```dos
COPY RESULT.COM RC12.COM
```

VIEW.BAS must report RC12.COM length 14530 bytes. Keep this executable and its source together.

## Acceptance check

```dos
CHECK RC12
```

The checker must report PASS. The driver compares the result with 4660 and returns nonzero on a mismatch; it adds no display routine.

## If the result differs

Compare tword with the printed addition. Check its arguments and saved state across calls, then inspect the generated text or bytes.
