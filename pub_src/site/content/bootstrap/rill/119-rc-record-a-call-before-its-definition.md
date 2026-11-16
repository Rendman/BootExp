+++
title = "31 \u00b7 Remembering Calls Before Their Definitions"
weight = 31
description = "A call can precede its procedure definition."
download = "RC31.RIL"
download_group = "tools/rill"
aliases = ["/bootstrap/rill/119-rc-record-a-call-before-its-definition/"]
reader_names = 1
url = "/bootstrap/rc/119-rc-record-a-call-before-its-definition/"
+++

## The working parts

A call can precede its procedure definition. Record its name and required arity as a pending procedure; final acceptance rejects any definition that never arrives. Ordinary undeclared variable use remains an error.

## Enter the source

Copy RC30.RIL to RC31.RIL. Apply edits **from the bottom of the old file upward**. Physical positions refer to that unchanged old file; use the printed context to identify each place. Keep all other source.

### Edit 1

Unchanged source immediately before the edit:

```rill
    return 0;
}
```

Insert after old physical line 267.

Insert:

```rill
fn resolveoptional() {
    callbuiltin = builtin();
    if callbuiltin { rectype = 7; return 65535; }
    let mut p = find(20480,localcount);
    if p != 65535 { return p; }
    p = lookglobal(); if p != 65535 { return p; }
    recval = 65535; reclevel = 0; p = newglobal(4); rectype = 4; return p;
}
```

The following old source remains in place:

```rill
fn fail(code) {
    if input { close(input); }
```

### Edit 2

Unchanged source immediately before the edit:

```rill
bytes ident[32];
bytes string[512];
```

Remove this source at old physical positions 35–35 in RC30.RIL:

```rill
fn main(){filearg(1,"SOURCE.RIL");setident("PUTC");builtin();return (recval)!=1;}
```

Replace it with:

```rill
fn main(){filearg(1,"SOURCE.RIL");table=alloc(23680);setident("ABC");rectype=1;recval=12345;reclevel=0;record(0);globals=1;resolveoptional();return (rectype)!=1;}
```

The following old source remains in place:

```rill

fn next() {
```

## Build this stopping point

```dos
CHECK RILLBOOT RC31.RIL RESULT.IR
```

Require `OK RESULT.IR 0000026046` and PASS. Pass RESULT.IR directly to the translator.

```dos
CHECK IWKEEP SOURCE.IR RESULT.ASM
CHECK ASMAKEEP RESULT.ASM RESULT.COM
```

Require IR86 `OK RESULT.ASM 0000058020 text bytes` and PASS **before** the copy. Require assembler `OK RESULT.COM 18901 bytes` and PASS before saving:

```dos
COPY RESULT.COM RC31.COM
```

VIEW.BAS must report RC31.COM length 18901 bytes. Keep this executable and its source together.

## Acceptance check

```dos
CHECK RC31
```

The checker must report PASS. The driver compares the result with 1 and returns nonzero on a mismatch; it adds no display routine.

## If the result differs

Compare resolveoptional with the printed addition. Check its arguments and saved state across calls, then inspect the generated text or bytes.
