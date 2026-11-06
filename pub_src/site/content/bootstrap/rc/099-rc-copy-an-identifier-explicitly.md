+++
title = "RC11 \u00b7 Copy an identifier explicitly"
weight = 11
description = "Copy an explicit terminated spelling into IDENT."
download = "RC11.RIL"
download_group = "rc"
aliases = ["/bootstrap/rill/099-rc-copy-an-identifier-explicitly/"]
+++

Copy an explicit terminated spelling into IDENT.

## The working parts

Copy an explicit terminated spelling into IDENT. This is a table-test helper as well as a way to ask for a required entry without depending on the current source token.

The entry diagnostic exercises the printed helper. Rejecting placeholders identify forms outside this stopping point. A diagnostic that emits only an IR fragment is inspected as text; it is not a complete compiler or output program.

## Enter the source

Copy RC10.RIL to RC11.RIL. Apply edits **from the bottom of the old file upward**. Physical positions refer to that unchanged old file; use the printed context to identify each place. Keep all other source.

### Edit 1

Unchanged source immediately before the edit:

```rill
    return 0;
}
```

Insert after old physical line 144.

Insert:

```rill
fn setident(s) { let mut i = 0; while 1 { ident[i] = load8(s+i); if ident[i] == 0 { return 0; } i = i+1; } }
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

Remove this source at old physical positions 35–35 in RC10.RIL:

```rill
fn main(){input=open("SOURCE.RIL");if status(){fail(1);}next();lex();printnum(isword("FN"));return 0;}
```

Replace it with:

```rill
fn main(){setident("ABC");print(ident);return 0;}
```

The following old source remains in place:

```rill

fn next() {
```

## Build this stopping point

```dos
COPY RC11.RIL SOURCE.RIL
CHECK RILLBOOT
```

Require `OK RESULT.IR 0000014426` and PASS. Copy RESULT.IR to SOURCE.IR.

```dos
CHECK IWKEEP
COPY RESULT.ASM SOURCE.ASM
CHECK ASMAKEEP
```

Require IR86 `OK RESULT.ASM 0000031479 text bytes` and PASS **before** the copy. Require assembler `OK RESULT.COM 14456 bytes` and PASS before saving:

```dos
COPY RESULT.COM RC11.COM
```

VIEW.BAS must report RC11.COM length 14456 bytes. Keep this executable and its source together.

## Acceptance check

```dos
CHECK RC11
```

Require, apart from command echo and the checker's separator:

```text
ABCPASS
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
