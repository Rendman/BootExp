+++
title = "18 \u00b7 Adding a Local Name"
weight = 18
description = "Append a record in the separate local-name region."
download = "RC18.RIL"
download_group = "tools/rill"
aliases = ["/bootstrap/rill/106-rc-a-scoped-local-record/"]
reader_names = 1
+++

## The working parts

Append a record in the separate local-name region. Its slot number and lexical level are explicit fields. Eighty records provide room for sixteen parameters and sixty-four live local bindings. Reject another entry before writing beyond byte 23679.

## Enter the source

Copy RC17.RIL to RC18.RIL. Apply edits **from the bottom of the old file upward**. Physical positions refer to that unchanged old file; use the printed context to identify each place. Keep all other source.

### Edit 1

Unchanged source immediately before the edit:

```rill
    return record(p);
}
```

Insert after old physical line 188.

Insert:

```rill
fn newlocal(kind) {
    if localcount >= 80 { fail(5); }
    rectype = kind;
    let mut p = 20480+localcount*40; localcount = localcount+1;
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

Remove this source at old physical positions 35–35 in RC17.RIL:

```rill
fn main(){table=alloc(23680);setident("ABC");recval=12345;newglobal(1);return (tword(34))!=12345;}
```

Replace it with:

```rill
fn main(){table=alloc(23680);setident("ABC");recval=7;newlocal(5);return (tword(20514))!=7;}
```

The following old source remains in place:

```rill

fn next() {
```

## Build this stopping point

```dos
COPY RC18.RIL SOURCE.RIL
CHECK RILLBOOT
```

Require `OK RESULT.IR 0000017851` and PASS. Copy RESULT.IR to SOURCE.IR.

```dos
CHECK IWKEEP
COPY RESULT.ASM SOURCE.ASM
CHECK ASMAKEEP
```

Require IR86 `OK RESULT.ASM 0000037676 text bytes` and PASS **before** the copy. Require assembler `OK RESULT.COM 15554 bytes` and PASS before saving:

```dos
COPY RESULT.COM RC18.COM
```

VIEW.BAS must report RC18.COM length 15554 bytes. Keep this executable and its source together.

## Acceptance check

```dos
CHECK RC18
```

The checker must report PASS. The driver compares the result with 7 and returns nonzero on a mismatch; it adds no display routine.

## If the result differs

Compare newlocal with the printed addition. Check its arguments and saved state across calls, then inspect the generated text or bytes.
