+++
title = "22 \u00b7 Adding a Byte to the Output"
weight = 22
description = "Append one byte, advance the checked low/high output count, and flush a full 4096-byte block."
download = "RC22.RIL"
download_group = "tools/rill"
aliases = ["/bootstrap/rill/110-rc-append-an-output-byte/"]
reader_names = 1
+++

## The working parts

Append one byte, advance the checked low/high output count, and flush a full 4096-byte block. The output belongs to this assembly, not to the input refill buffer.

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
fn main(){output=create("RILL.TMP");own=1;outbuf[0]=65;outlen=1;flush();close(output);output=0;own=0;return 0;}
```

Replace it with:

```rill
fn main(){output=create("RILL.TMP");own=1;outchar(65);flush();close(output);output=0;own=0;return 0;}
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

Require `OK RESULT.IR 0000019525` and PASS. Copy RESULT.IR to SOURCE.IR.

```dos
CHECK IWKEEP
COPY RESULT.ASM SOURCE.ASM
CHECK ASMAKEEP
```

Require IR86 `OK RESULT.ASM 0000040995 text bytes` and PASS **before** the copy. Require assembler `OK RESULT.COM 16147 bytes` and PASS before saving:

```dos
COPY RESULT.COM RC22.COM
```

VIEW.BAS must report RC22.COM length 16147 bytes. Keep this executable and its source together.

## Acceptance check

```dos
CHECK RC22
```

The checker must report PASS. Inspect the emitted file below.

Use VIEW.BAS to inspect RILL.TMP. Require length 1 bytes. The complete bytes must be:

```text
41
```

This is an IR fragment for inspection. Do not translate it as a complete program or execute any file with its name.

After inspection, delete this deliberately created RILL.TMP before another checkpoint. The file is diagnostic text, not an interrupted accepted compiler build.

## If the result differs

Compare outchar with the printed addition. Check its arguments and saved state across calls, then inspect the generated text or bytes.
