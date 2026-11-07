+++
title = "20 \u00b7 Finding the Visible Binding"
weight = 20
description = "Search active local bindings first, then globals."
download = "RC20.RIL"
download_group = "tools/rill"
aliases = ["/bootstrap/rill/108-rc-choose-the-innermost-binding/"]
reader_names = 1
+++

## The working parts

Search active local bindings first, then globals. Save the found offset separately from kind and value fields; recursive parsing can replace the shared search result.

## Enter the source

Copy RC19.RIL to RC20.RIL. Apply edits **from the bottom of the old file upward**. Physical positions refer to that unchanged old file; use the printed context to identify each place. Keep all other source.

### Edit 1

Unchanged source immediately before the edit:

```rill

fn lookglobal() { return find(0,globals); }
```

Insert after old physical line 197.

Insert:

```rill
fn resolve() {
    found = find(20480,localcount);
    if found == 65535 { found = lookglobal(); if found == 65535 { fail(4); } }
    return found;
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

Remove this source at old physical positions 35–35 in RC19.RIL:

```rill
fn main(){table=alloc(23680);setident("ABC");rectype=1;recval=12345;reclevel=0;record(0);globals=1;lookglobal();return (recval)!=12345;}
```

Replace it with:

```rill
fn main(){table=alloc(23680);setident("ABC");rectype=1;recval=12345;reclevel=0;record(0);globals=1;resolve();return (recval)!=12345;}
```

The following old source remains in place:

```rill

fn next() {
```

## Build this stopping point

```dos
COPY RC20.RIL SOURCE.RIL
CHECK RILLBOOT
```

Require `OK RESULT.IR 0000018485` and PASS. Copy RESULT.IR to SOURCE.IR.

```dos
CHECK IWKEEP
COPY RESULT.ASM SOURCE.ASM
CHECK ASMAKEEP
```

Require IR86 `OK RESULT.ASM 0000038858 text bytes` and PASS **before** the copy. Require assembler `OK RESULT.COM 15764 bytes` and PASS before saving:

```dos
COPY RESULT.COM RC20.COM
```

VIEW.BAS must report RC20.COM length 15764 bytes. Keep this executable and its source together.

## Acceptance check

```dos
CHECK RC20
```

The checker must report PASS. The driver compares the result with 12345 and returns nonzero on a mismatch; it adds no display routine.

## If the result differs

Compare resolve with the printed addition. Check its arguments and saved state across calls, then inspect the generated text or bytes.
