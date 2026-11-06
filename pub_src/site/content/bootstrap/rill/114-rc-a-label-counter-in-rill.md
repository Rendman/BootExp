+++
title = "RC26 \u00b7 A label counter in RILL"
weight = 114
description = "Advance a checked word counter."
download = "RC26.RIL"
download_group = "toolchain"
+++

Advance a checked word counter.

## The working parts

Advance a checked word counter. The counter supplies names, not physical code addresses.

The entry diagnostic exercises the printed helper. Rejecting placeholders identify forms outside this stopping point. A diagnostic that emits only an IR fragment is inspected as text; it is not a complete compiler or output program.

## Enter the source

Copy RC25.RIL to RC26.RIL. Apply edits **from the bottom of the old file upward**. Physical positions refer to that unchanged old file; use the printed context to identify each place. Keep all other source.

### Edit 1

Unchanged source immediately before the edit:

```rill

fn newline() { return outstr("\r\n"); }
```

Insert after old physical line 237.

Insert:

```rill
fn newlabel() { labelno = labelno+1; if labelno == 0 { fail(5); } return labelno; }
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

Remove this source at old physical positions 35–35 in RC25.RIL:

```rill
fn main(){output=create("RILL.TMP");own=1;newline();flush();close(output);output=0;own=0;print("OK RILL.TMP\r\n");return 0;}
```

Replace it with:

```rill
fn main(){printnum(newlabel());return 0;}
```

The following old source remains in place:

```rill

fn next() {
```

## Build this stopping point

```dos
COPY RC26.RIL SOURCE.RIL
CHECK RILLBOOT
```

Require `OK RESULT.IR 0000020879` and PASS. Copy RESULT.IR to SOURCE.IR.

```dos
CHECK IWKEEP
COPY RESULT.ASM SOURCE.ASM
CHECK ASMAKEEP
```

Require IR86 `OK RESULT.ASM 0000043501 text bytes` and PASS **before** the copy. Require assembler `OK RESULT.COM 16617 bytes` and PASS before saving:

```dos
COPY RESULT.COM RC26.COM
```

VIEW.BAS must report RC26.COM length 16617 bytes. Keep this executable and its source together.

## Acceptance check

```dos
CHECK RC26
```

Require, apart from command echo and the checker's separator:

```text
00001PASS
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
