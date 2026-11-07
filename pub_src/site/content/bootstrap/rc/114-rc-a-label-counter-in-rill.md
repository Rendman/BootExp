+++
title = "26 \u00b7 Giving Each Branch a Unique Name"
weight = 26
description = "Advance a checked word counter."
download = "RC26.RIL"
download_group = "tools/rill"
aliases = ["/bootstrap/rill/114-rc-a-label-counter-in-rill/"]
reader_names = 1
+++

## The working parts

Advance a checked word counter. The counter supplies names, not physical code addresses.

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
fn main(){output=create("RILL.TMP");own=1;newline();flush();close(output);output=0;own=0;return 0;}
```

Replace it with:

```rill
fn main(){return (newlabel())!=1;}
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

Require `OK RESULT.IR 0000020859` and PASS. Copy RESULT.IR to SOURCE.IR.

```dos
CHECK IWKEEP
COPY RESULT.ASM SOURCE.ASM
CHECK ASMAKEEP
```

Require IR86 `OK RESULT.ASM 0000043282 text bytes` and PASS **before** the copy. Require assembler `OK RESULT.COM 16571 bytes` and PASS before saving:

```dos
COPY RESULT.COM RC26.COM
```

VIEW.BAS must report RC26.COM length 16571 bytes. Keep this executable and its source together.

## Acceptance check

```dos
CHECK RC26
```

The checker must report PASS. The driver compares the result with 1 and returns nonzero on a mismatch; it adds no display routine.

## If the result differs

Compare newlabel with the printed addition. Check its arguments and saved state across calls, then inspect the generated text or bytes.
