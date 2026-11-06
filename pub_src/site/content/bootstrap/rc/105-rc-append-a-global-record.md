+++
title = "17 \u00b7 Adding a Global Name"
weight = 17
description = "Append one global or procedure record, bounded by 512 entries."
download = "RC17.RIL"
download_group = "tools/rill"
aliases = ["/bootstrap/rill/105-rc-append-a-global-record/"]
reader_names = 1
+++

## The working parts

Append one global or procedure record, bounded by 512 entries. The record offset remains stable even after scanning changes IDENT.

## Enter the source

Copy RC16.RIL to RC17.RIL. Apply edits **from the bottom of the old file upward**. Physical positions refer to that unchanged old file; use the printed context to identify each place. Keep all other source.

### Edit 1

Unchanged source immediately before the edit:

```rill

fn recordfields(p) { set16(table,p+32,rectype); set16(table,p+34,recval); set16(table,p+36,reclevel); return p; }
```

Insert after old physical line 181.

Insert:

```rill
fn newglobal(kind) {
    if globals >= 512 { fail(5); }
    rectype = kind;
    let mut p = globals*40; globals = globals+1;
    return record(p);
}
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

Remove this source at old physical positions 35–35 in RC16.RIL:

```rill
fn main(){table=alloc(22000);setident("ABC");rectype=1;recval=12345;reclevel=0;record(0);globals=1;return (tword(34))!=12345;}
```

Replace it with:

```rill
fn main(){table=alloc(22000);setident("ABC");recval=12345;newglobal(1);return (tword(34))!=12345;}
```

The following old source remains in place:

```rill

fn next() {
```

## Build this stopping point

```dos
COPY RC17.RIL SOURCE.RIL
CHECK RILLBOOT
```

Require `OK RESULT.IR 0000017442` and PASS. Copy RESULT.IR to SOURCE.IR.

```dos
CHECK IWKEEP
COPY RESULT.ASM SOURCE.ASM
CHECK ASMAKEEP
```

Require IR86 `OK RESULT.ASM 0000037170 text bytes` and PASS **before** the copy. Require assembler `OK RESULT.COM 15472 bytes` and PASS before saving:

```dos
COPY RESULT.COM RC17.COM
```

VIEW.BAS must report RC17.COM length 15472 bytes. Keep this executable and its source together.

## Acceptance check

```dos
CHECK RC17
```

The checker must report PASS. The driver compares the result with 12345 and returns nonzero on a mismatch; it adds no display routine.

## If the result differs

Compare newglobal with the printed addition. Check its arguments and saved state across calls, then inspect the generated text or bytes.
