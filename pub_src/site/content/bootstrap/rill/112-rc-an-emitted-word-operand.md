+++
title = "24 \u00b7 Writing a Numeric Operand"
weight = 24
description = "Emit a fixed decimal word spelling through OUTCHAR."
download = "RC24.RIL"
download_group = "tools/rill"
aliases = ["/bootstrap/rill/112-rc-an-emitted-word-operand/"]
reader_names = 1
url = "/bootstrap/rc/112-rc-an-emitted-word-operand/"
+++

## The working parts

Emit a fixed decimal word spelling through OUTCHAR. It uses the same checked output path as instruction names and delimiters.

## Enter the source

Copy RC23.RIL to RC24.RIL. Apply edits **from the bottom of the old file upward**. Physical positions refer to that unchanged old file; use the printed context to identify each place. Keep all other source.

### Edit 1

Unchanged source immediately before the edit:

```rill
    }
}
```

Insert after old physical line 229.

Insert:

```rill
fn outnum(n) {
    let mut place = 10000; let mut c = 0;
    while place { c = 48; while n >= place { n = n-place; c = c+1; } outchar(c); place = place/10; }
    return 0;
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

Remove this source at old physical positions 35–35 in RC23.RIL:

```rill
fn main(){output=create("RILL.TMP");own=1;outstr("HI");flush();close(output);output=0;own=0;return 0;}
```

Replace it with:

```rill
fn main(){output=create("RILL.TMP");own=1;outnum(12345);flush();close(output);output=0;own=0;return 0;}
```

The following old source remains in place:

```rill

fn next() {
```

## Build this stopping point

```dos
COPY RC24.RIL SOURCE.RIL
CHECK RILLBOOT
```

Require `OK RESULT.IR 0000020738` and PASS. Copy RESULT.IR to SOURCE.IR.

```dos
CHECK IWKEEP
COPY RESULT.ASM SOURCE.ASM
CHECK ASMAKEEP
```

Require IR86 `OK RESULT.ASM 0000042970 text bytes` and PASS **before** the copy. Require assembler `OK RESULT.COM 16505 bytes` and PASS before saving:

```dos
COPY RESULT.COM RC24.COM
```

VIEW.BAS must report RC24.COM length 16505 bytes. Keep this executable and its source together.

## Acceptance check

```dos
CHECK RC24
```

The checker must report PASS. Inspect the emitted file below.

Use VIEW.BAS to inspect RILL.TMP. Require length 5 bytes. The complete bytes must be:

```text
31 32 33 34 35
```

This is an IR fragment for inspection. Do not translate it as a complete program or execute any file with its name.

After inspection, delete this deliberately created RILL.TMP before another checkpoint. The file is diagnostic text, not an interrupted accepted compiler build.

## If the result differs

Compare outnum with the printed addition. Check its arguments and saved state across calls, then inspect the generated text or bytes.
