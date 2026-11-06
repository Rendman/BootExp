+++
title = "RC05 \u00b7 Character classification"
weight = 5
description = "Accept an underscore or a letter in either ASCII case."
download = "RC05.RIL"
download_group = "rc"
aliases = ["/bootstrap/rill/093-rc-character-classification/"]
+++

Accept an underscore or a letter in either ASCII case.

## The working parts

Accept an underscore or a letter in either ASCII case. The scanner performs case folding when saving a name; character recognition alone does not modify the source byte.

The entry diagnostic exercises the printed helper. Rejecting placeholders identify forms outside this stopping point. A diagnostic that emits only an IR fragment is inspected as text; it is not a complete compiler or output program.

## Enter the source

Copy RC04.RIL to RC05.RIL. Apply edits **from the bottom of the old file upward**. Physical positions refer to that unchanged old file; use the printed context to identify each place. Keep all other source.

### Edit 1

Unchanged source immediately before the edit:

```rill
bytes ident[32];
bytes string[512];
```

Remove this source at old physical positions 35–35 in RC04.RIL:

```rill
fn main(){print("READY");return 0;}
```

Replace it with:

```rill
fn main(){printnum(letter(95));return 0;}

fn letter(c) {
    if c == 95 { return 1; }
    if c >= 65 { if c <= 90 { return 1; } }
    if c >= 97 { if c <= 122 { return 1; } }
    return 0;
}
```

The following old source remains in place:

```rill

fn print(s) { let mut c = 0; while 1 { c = load8(s); if c == 0 { return 0; } putc(c); s = s+1; } }
```

## Build this stopping point

```dos
COPY RC05.RIL SOURCE.RIL
CHECK RILLBOOT
```

Require `OK RESULT.IR 0000005149` and PASS. Copy RESULT.IR to SOURCE.IR.

```dos
CHECK IWKEEP
COPY RESULT.ASM SOURCE.ASM
CHECK ASMAKEEP
```

Require IR86 `OK RESULT.ASM 0000014610 text bytes` and PASS **before** the copy. Require assembler `OK RESULT.COM 11393 bytes` and PASS before saving:

```dos
COPY RESULT.COM RC05.COM
```

VIEW.BAS must report RC05.COM length 11393 bytes. Keep this executable and its source together.

## Acceptance check

```dos
CHECK RC05
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
