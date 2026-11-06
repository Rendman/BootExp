+++
title = "RC18 \u00b7 A scoped local record"
weight = 18
description = "Append a record in the separate local-name region."
download = "RC18.RIL"
download_group = "rc"
aliases = ["/bootstrap/rill/106-rc-a-scoped-local-record/"]
+++

Append a record in the separate local-name region.

## The working parts

Append a record in the separate local-name region. Its slot number and lexical level are explicit fields. The region has room for parameters and live local bindings, not a second global namespace.

The entry diagnostic exercises the printed helper. Rejecting placeholders identify forms outside this stopping point. A diagnostic that emits only an IR fragment is inspected as text; it is not a complete compiler or output program.

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
    if localcount >= 32 { fail(5); }
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
fn main(){table=alloc(22000);setident("ABC");recval=12345;newglobal(1);printnum(tword(34));return 0;}
```

Replace it with:

```rill
fn main(){table=alloc(22000);setident("ABC");recval=7;newlocal(5);printnum(tword(20514));return 0;}
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

Require `OK RESULT.IR 0000017871` and PASS. Copy RESULT.IR to SOURCE.IR.

```dos
CHECK IWKEEP
COPY RESULT.ASM SOURCE.ASM
CHECK ASMAKEEP
```

Require IR86 `OK RESULT.ASM 0000037895 text bytes` and PASS **before** the copy. Require assembler `OK RESULT.COM 15600 bytes` and PASS before saving:

```dos
COPY RESULT.COM RC18.COM
```

VIEW.BAS must report RC18.COM length 15600 bytes. Keep this executable and its source together.

## Acceptance check

```dos
CHECK RC18
```

Require, apart from command echo and the checker's separator:

```text
00007PASS
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
