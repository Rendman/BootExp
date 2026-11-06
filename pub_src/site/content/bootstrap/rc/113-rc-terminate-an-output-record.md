+++
title = "25 \u00b7 Ending a Line of Generated Code"
weight = 25
description = "End an emitted IR record with carriage return and line feed."
download = "RC25.RIL"
download_group = "tools/rill"
aliases = ["/bootstrap/rill/113-rc-terminate-an-output-record/"]
reader_names = 1
+++

## The working parts

End an emitted IR record with carriage return and line feed. A record terminator and a zero byte ending an in-memory string have different jobs.

## Enter the source

Copy RC24.RIL to RC25.RIL. Apply edits **from the bottom of the old file upward**. Physical positions refer to that unchanged old file; use the printed context to identify each place. Keep all other source.

### Edit 1

Unchanged source immediately before the edit:

```rill
    return 0;
}
```

Insert after old physical line 235.

Insert:

```rill
fn newline() { return outstr("\r\n"); }
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

Remove this source at old physical positions 35–35 in RC24.RIL:

```rill
fn main(){output=create("RILL.TMP");own=1;outnum(12345);flush();close(output);output=0;own=0;return 0;}
```

Replace it with:

```rill
fn main(){output=create("RILL.TMP");own=1;newline();flush();close(output);output=0;own=0;return 0;}
```

The following old source remains in place:

```rill

fn next() {
```

## Build this stopping point

```dos
COPY RC25.RIL SOURCE.RIL
CHECK RILLBOOT
```

Require `OK RESULT.IR 0000020812` and PASS. Copy RESULT.IR to SOURCE.IR.

```dos
CHECK IWKEEP
COPY RESULT.ASM SOURCE.ASM
CHECK ASMAKEEP
```

Require IR86 `OK RESULT.ASM 0000043440 text bytes` and PASS **before** the copy. Require assembler `OK RESULT.COM 16593 bytes` and PASS before saving:

```dos
COPY RESULT.COM RC25.COM
```

VIEW.BAS must report RC25.COM length 16593 bytes. Keep this executable and its source together.

## Acceptance check

```dos
CHECK RC25
```

The checker must report PASS. Inspect the emitted file below.

Use VIEW.BAS to inspect RILL.TMP. Require length 2 bytes. The complete bytes must be:

```text
0D 0A
```

This is an IR fragment for inspection. Do not translate it as a complete program or execute any file with its name.

After inspection, delete this deliberately created RILL.TMP before another checkpoint. The file is diagnostic text, not an interrupted accepted compiler build.

## If the result differs

Compare newline with the printed addition. Check its arguments and saved state across calls, then inspect the generated text or bytes.
