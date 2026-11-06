+++
title = "RC13 \u00b7 A byte in an opaque block"
weight = 13
description = "Use the same opaque block with a byte offset."
download = "RC13.RIL"
download_group = "rc"
aliases = ["/bootstrap/rill/101-rc-a-byte-in-an-opaque-block/"]
+++

Use the same opaque block with a byte offset.

## The working parts

Use the same opaque block with a byte offset. GET8 returns a zero-extended byte; it does not reveal a segment selector or native address.

The entry diagnostic exercises the printed helper. Rejecting placeholders identify forms outside this stopping point. A diagnostic that emits only an IR fragment is inspected as text; it is not a complete compiler or output program.

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
fn main(){table=alloc(22000);set16(table,100,4660);printnum(tword(100));return 0;}
```

Replace it with:

```rill
fn main(){table=alloc(22000);set16(table,100,4660);printnum(tbyte(100));return 0;}
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

Require `OK RESULT.IR 0000014718` and PASS. Copy RESULT.IR to SOURCE.IR.

```dos
CHECK IWKEEP
COPY RESULT.ASM SOURCE.ASM
CHECK ASMAKEEP
```

Require IR86 `OK RESULT.ASM 0000032091 text bytes` and PASS **before** the copy. Require assembler `OK RESULT.COM 14573 bytes` and PASS before saving:

```dos
COPY RESULT.COM RC13.COM
```

VIEW.BAS must report RC13.COM length 14573 bytes. Keep this executable and its source together.

## Acceptance check

```dos
CHECK RC13
```

Require, apart from command echo and the checker's separator:

```text
00052PASS
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
