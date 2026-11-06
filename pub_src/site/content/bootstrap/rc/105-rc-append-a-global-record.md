+++
title = "RC17 \u00b7 Append a global record"
weight = 17
description = "Append one global or procedure record, bounded by 512 entries."
download = "RC17.RIL"
download_group = "rc"
aliases = ["/bootstrap/rill/105-rc-append-a-global-record/"]
+++

Append one global or procedure record, bounded by 512 entries.

## The working parts

Append one global or procedure record, bounded by 512 entries. The record offset remains stable even after scanning changes IDENT.

The entry diagnostic exercises the printed helper. Rejecting placeholders identify forms outside this stopping point. A diagnostic that emits only an IR fragment is inspected as text; it is not a complete compiler or output program.

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
fn main(){table=alloc(22000);setident("ABC");rectype=1;recval=12345;reclevel=0;record(0);globals=1;printnum(tword(34));return 0;}
```

Replace it with:

```rill
fn main(){table=alloc(22000);setident("ABC");recval=12345;newglobal(1);printnum(tword(34));return 0;}
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

Require `OK RESULT.IR 0000017462` and PASS. Copy RESULT.IR to SOURCE.IR.

```dos
CHECK IWKEEP
COPY RESULT.ASM SOURCE.ASM
CHECK ASMAKEEP
```

Require IR86 `OK RESULT.ASM 0000037158 text bytes` and PASS **before** the copy. Require assembler `OK RESULT.COM 15470 bytes` and PASS before saving:

```dos
COPY RESULT.COM RC17.COM
```

VIEW.BAS must report RC17.COM length 15470 bytes. Keep this executable and its source together.

## Acceptance check

```dos
CHECK RC17
```

Require, apart from command echo and the checker's separator:

```text
12345PASS
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
