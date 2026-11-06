+++
title = "13 \u00b7 Reading a Byte from Allocated Storage"
weight = 13
description = "Use the same opaque block with a byte offset."
download = "RC13.RIL"
download_group = "tools/rill"
aliases = ["/bootstrap/rill/101-rc-a-byte-in-an-opaque-block/"]
reader_names = 1
+++

## The working parts

Use the same opaque block with a byte offset. GET8 returns a zero-extended byte; it does not reveal a segment selector or native address.

## Enter the source

Copy RC12.RIL to RC13.RIL. Apply edits **from the bottom of the old file upward**. Physical positions refer to that unchanged old file; use the printed context to identify each place. Keep all other source.

### Edit 1

Unchanged source immediately before the edit:

```rill

fn tword(p) { return get16(table,p); }
```

Insert after old physical line 148.

Insert:

```rill
fn tbyte(p) { return get8(table,p); }
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

Remove this source at old physical positions 35–35 in RC12.RIL:

```rill
fn main(){table=alloc(22000);set16(table,100,4660);return (tword(100))!=4660;}
```

Replace it with:

```rill
fn main(){table=alloc(22000);set16(table,100,4660);return (tbyte(100))!=52;}
```

The following old source remains in place:

```rill

fn next() {
```

## Build this stopping point

```dos
COPY RC13.RIL SOURCE.RIL
CHECK RILLBOOT
```

Require `OK RESULT.IR 0000014698` and PASS. Copy RESULT.IR to SOURCE.IR.

```dos
CHECK IWKEEP
COPY RESULT.ASM SOURCE.ASM
CHECK ASMAKEEP
```

Require IR86 `OK RESULT.ASM 0000032103 text bytes` and PASS **before** the copy. Require assembler `OK RESULT.COM 14575 bytes` and PASS before saving:

```dos
COPY RESULT.COM RC13.COM
```

VIEW.BAS must report RC13.COM length 14575 bytes. Keep this executable and its source together.

## Acceptance check

```dos
CHECK RC13
```

The checker must report PASS. The driver compares the result with 52 and returns nonzero on a mismatch; it adds no display routine.

## If the result differs

Compare tbyte with the printed addition. Check its arguments and saved state across calls, then inspect the generated text or bytes.
