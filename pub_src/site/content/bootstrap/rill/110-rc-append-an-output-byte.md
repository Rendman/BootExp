+++
title = "22 \u00b7 Adding a Byte to the Output"
weight = 22
description = "Append one byte, advance the checked low/high output count, and flush a full 4096-byte block."
download = "RC22.RIL"
download_group = "tools/rill"
aliases = ["/bootstrap/rill/110-rc-append-an-output-byte/"]
reader_names = 1
url = "/bootstrap/rc/110-rc-append-an-output-byte/"
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
fn main(){filearg(1,"SOURCE.RIL");output=create(filearg(2,"RILL.TMP"));own=1;outbuf[0]=65;outlen=1;flush();close(output);output=0;own=0;return 0;}
```

Replace it with:

```rill
fn main(){filearg(1,"SOURCE.RIL");output=create(filearg(2,"RILL.TMP"));own=1;outchar(65);flush();close(output);output=0;own=0;return 0;}
```

The following old source remains in place:

```rill

fn next() {
```

## Build this stopping point

```dos
CHECK RILLBOOT RC22.RIL RESULT.IR
```

Require `OK RESULT.IR 0000021027` and PASS. Pass RESULT.IR directly to the translator.

```dos
CHECK IWKEEP SOURCE.IR RESULT.ASM
CHECK ASMAKEEP RESULT.ASM RESULT.COM
```

Require IR86 `OK RESULT.ASM 0000045496 text bytes` and PASS **before** the copy. Require assembler `OK RESULT.COM 16992 bytes` and PASS before saving:

```dos
COPY RESULT.COM RC22.COM
```

VIEW.BAS must report RC22.COM length 16992 bytes. Keep this executable and its source together.

## Acceptance check

```dos
CHECK RC22 RC22.RIL RESULT.IR
```

The checker must report PASS. Inspect the emitted file below.

Use VIEW.BAS to inspect RESULT.IR. Require length 1 bytes. The complete bytes must be:

```text
41
```

This is an IR fragment for inspection. Do not translate it as a complete program or execute any file with its name.

## If the result differs

Compare outchar with the printed addition. Check its arguments and saved state across calls, then inspect the generated text or bytes.
