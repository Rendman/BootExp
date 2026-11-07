+++
title = "29 \u00b7 Writing a Stored Name"
weight = 29
description = "Read the spelling from its stable symbol record."
download = "RC29.RIL"
download_group = "tools/rill"
aliases = ["/bootstrap/rill/117-rc-emit-the-stored-spelling/"]
reader_names = 1
+++

## The working parts

Read the spelling from its stable symbol record. Parsing another argument must not silently change the name being emitted.

## Enter the source

Copy RC28.RIL to RC29.RIL. Apply edits **from the bottom of the old file upward**. Physical positions refer to that unchanged old file; use the printed context to identify each place. Keep all other source.

### Edit 1

Unchanged source immediately before the edit:

```rill
    return found;
}
```

Insert after old physical line 203.

Insert:

```rill
fn outname(p) { let mut i = 0; let mut c = 0; while 1 { c = tbyte(p+i); if c == 0 { return 0; } outchar(c); i = i+1; } }
```

The following old source remains in place:

```rill
fn outchar(c) {
    outbuf[outlen] = c; outlen = outlen+1; total = total+1;
```

### Edit 2

Unchanged source immediately before the edit:

```rill
bytes ident[32];
bytes string[512];
```

Remove this source at old physical positions 35–35 in RC28.RIL:

```rill
fn main(){output=create("RILL.TMP");own=1;labeljump(7);flush();close(output);output=0;own=0;return 0;}
```

Replace it with:

```rill
fn main(){table=alloc(22000);setident("ABC");rectype=1;recval=12345;reclevel=0;record(0);globals=1;output=create("RILL.TMP");own=1;outname(0);flush();close(output);output=0;own=0;return 0;}
```

The following old source remains in place:

```rill

fn next() {
```

## Build this stopping point

```dos
COPY RC29.RIL SOURCE.RIL
CHECK RILLBOOT
```

Require `OK RESULT.IR 0000022173` and PASS. Copy RESULT.IR to SOURCE.IR.

```dos
CHECK IWKEEP
COPY RESULT.ASM SOURCE.ASM
CHECK ASMAKEEP
```

Require IR86 `OK RESULT.ASM 0000045864 text bytes` and PASS **before** the copy. Require assembler `OK RESULT.COM 17008 bytes` and PASS before saving:

```dos
COPY RESULT.COM RC29.COM
```

VIEW.BAS must report RC29.COM length 17008 bytes. Keep this executable and its source together.

## Acceptance check

```dos
CHECK RC29
```

The checker must report PASS. Inspect the emitted file below.

Use VIEW.BAS to inspect RILL.TMP. Require length 3 bytes. The complete bytes must be:

```text
41 42 43
```

This is an IR fragment for inspection. Do not translate it as a complete program or execute any file with its name.

After inspection, delete this deliberately created RILL.TMP before another checkpoint. The file is diagnostic text, not an interrupted accepted compiler build.

## If the result differs

Compare outname with the printed addition. Check its arguments and saved state across calls, then inspect the generated text or bytes.
