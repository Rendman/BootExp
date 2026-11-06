+++
title = "RC22 \u00b7 Append an output byte"
weight = 110
description = "Append one byte, advance the checked low/high output count, and flush a full 4096-byte block."
download = "RC22.RIL"
download_group = "toolchain"
+++

Append one byte, advance the checked low/high output count, and flush a full 4096-byte block.

## The working parts

Append one byte, advance the checked low/high output count, and flush a full 4096-byte block. The output belongs to this assembly, not to the input refill buffer.

The entry diagnostic exercises the printed helper. Rejecting placeholders identify forms outside this stopping point. A diagnostic that emits only an IR fragment is inspected as text; it is not a complete compiler or output program.

## Enter the source

Copy RC21.RIL to RC22.RIL. Apply edits **from the bottom of the old file upward**. Physical positions refer to that unchanged old file; use the printed context to identify each place. Keep all other source.

### Edit 1

Unchanged source immediately before the edit:

```rill
    return found;
}
```

Insert after old physical line 203.

Insert:

```rill
fn outchar(c) {
    outbuf[outlen] = c; outlen = outlen+1; total = total+1;
    if total == 0 { totalhi = totalhi+1; if totalhi == 0 { fail(5); } }
    if outlen == 4096 { flush(); }
    return 0;
}
```

The following old source remains in place:

```rill
fn flush() {
    if outlen {
```

### Edit 2

Unchanged source immediately before the edit:

```rill
bytes ident[32];
bytes string[512];
```

Remove this source at old physical positions 35–35 in RC21.RIL:

```rill
fn main(){output=create("RILL.TMP");own=1;outbuf[0]=65;outlen=1;flush();close(output);output=0;own=0;print("OK RILL.TMP\r\n");return 0;}
```

Replace it with:

```rill
fn main(){output=create("RILL.TMP");own=1;outchar(65);flush();close(output);output=0;own=0;print("OK RILL.TMP\r\n");return 0;}
```

The following old source remains in place:

```rill

fn next() {
```

## Build this stopping point

```dos
COPY RC22.RIL SOURCE.RIL
CHECK RILLBOOT
```

Require `OK RESULT.IR 0000019577` and PASS. Copy RESULT.IR to SOURCE.IR.

```dos
CHECK IWKEEP
COPY RESULT.ASM SOURCE.ASM
CHECK ASMAKEEP
```

Require IR86 `OK RESULT.ASM 0000041219 text bytes` and PASS **before** the copy. Require assembler `OK RESULT.COM 16175 bytes` and PASS before saving:

```dos
COPY RESULT.COM RC22.COM
```

VIEW.BAS must report RC22.COM length 16175 bytes. Keep this executable and its source together.

## Acceptance check

```dos
CHECK RC22
```

Require, apart from command echo and the checker's separator:

```text
OK RILL.TMP
PASS
```

TYPE RILL.TMP. Its complete text is:

```ir
A
```

VIEW.BAS must show length 1 bytes. This is an IR fragment for inspection. Do not translate it as a complete program or execute any file with its name.

After inspection, delete this deliberately created RILL.TMP before another checkpoint. The file is diagnostic text, not an interrupted accepted compiler build.

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
