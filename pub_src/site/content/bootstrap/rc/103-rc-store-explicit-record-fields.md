+++
title = "15 \u00b7 Storing a Symbol's Meaning"
weight = 15
description = "Kind, value or slot, and lexical level are distinct word fields."
download = "RC15.RIL"
download_group = "tools/rill"
aliases = ["/bootstrap/rill/103-rc-store-explicit-record-fields/"]
reader_names = 1
+++

## The working parts

Kind, value or slot, and lexical level are distinct word fields. Store them explicitly after initializing a record rather than relying on new memory containing zeroes.

## Enter the source

Copy RC14.RIL to RC15.RIL. Apply edits **from the bottom of the old file upward**. Physical positions refer to that unchanged old file; use the printed context to identify each place. Keep all other source.

### Edit 1

Unchanged source immediately before the edit:

```rill
    return 65535;
}
```

Insert after old physical line 172.

Insert:

```rill
fn recordfields(p) { set16(table,p+32,rectype); set16(table,p+34,recval); set16(table,p+36,reclevel); return p; }
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

Remove this source at old physical positions 35–35 in RC14.RIL:

```rill
fn main(){table=alloc(22000);setident("ABC");return (find(0,0))!=65535;}
```

Replace it with:

```rill
fn main(){table=alloc(22000);rectype=1;recval=12345;reclevel=0;recordfields(0);return (tword(34))!=12345;}
```

The following old source remains in place:

```rill

fn next() {
```

## Build this stopping point

```dos
COPY RC15.RIL SOURCE.RIL
CHECK RILLBOOT
```

Require `OK RESULT.IR 0000016334` and PASS. Copy RESULT.IR to SOURCE.IR.

```dos
CHECK IWKEEP
COPY RESULT.ASM SOURCE.ASM
CHECK ASMAKEEP
```

Require IR86 `OK RESULT.ASM 0000034807 text bytes` and PASS **before** the copy. Require assembler `OK RESULT.COM 15046 bytes` and PASS before saving:

```dos
COPY RESULT.COM RC15.COM
```

VIEW.BAS must report RC15.COM length 15046 bytes. Keep this executable and its source together.

## Acceptance check

```dos
CHECK RC15
```

The checker must report PASS. The driver compares the result with 12345 and returns nonzero on a mismatch; it adds no display routine.

## If the result differs

Compare recordfields with the printed addition. Check its arguments and saved state across calls, then inspect the generated text or bytes.
