+++
title = "28 \u00b7 Naming a Branch Destination"
weight = 28
description = "Emit a saved label number as an operand after the caller has selected the branch operation."
download = "RC28.RIL"
download_group = "tools/rill"
aliases = ["/bootstrap/rill/116-rc-emit-a-branch-operand/"]
reader_names = 1
url = "/bootstrap/rc/116-rc-emit-a-branch-operand/"
+++

## The working parts

Emit a saved label number as an operand after the caller has selected the branch operation. Preserve that target across formatting calls.

## Enter the source

Copy RC27.RIL to RC28.RIL. Apply edits **from the bottom of the old file upward**. Physical positions refer to that unchanged old file; use the printed context to identify each place. Keep all other source.

### Edit 1

Unchanged source immediately before the edit:

```rill

fn labeldef(n) { outstr("LABEL B_"); outnum(n); newline(); return 0; }
```

Insert after old physical line 241.

Insert:

```rill
fn labeljump(n) { outstr(" B_"); outnum(n); newline(); return 0; }
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

Remove this source at old physical positions 35–35 in RC27.RIL:

```rill
fn main(){filearg(1,"SOURCE.RIL");output=create(filearg(2,"RILL.TMP"));own=1;labeldef(7);flush();close(output);output=0;own=0;return 0;}
```

Replace it with:

```rill
fn main(){filearg(1,"SOURCE.RIL");output=create(filearg(2,"RILL.TMP"));own=1;labeljump(7);flush();close(output);output=0;own=0;return 0;}
```

The following old source remains in place:

```rill

fn next() {
```

## Build this stopping point

```dos
CHECK RILLBOOT RC28.RIL RESULT.IR
```

Require `OK RESULT.IR 0000022928` and PASS. Pass RESULT.IR directly to the translator.

```dos
CHECK IWKEEP SOURCE.IR RESULT.ASM
CHECK ASMAKEEP RESULT.ASM RESULT.COM
```

Require IR86 `OK RESULT.ASM 0000049270 text bytes` and PASS **before** the copy. Require assembler `OK RESULT.COM 17670 bytes` and PASS before saving:

```dos
COPY RESULT.COM RC28.COM
```

VIEW.BAS must report RC28.COM length 17670 bytes. Keep this executable and its source together.

## Acceptance check

```dos
CHECK RC28 RC28.RIL RESULT.IR
```

The checker must report PASS. Inspect the emitted file below.

Use VIEW.BAS to inspect RESULT.IR. Require length 10 bytes. The complete bytes must be:

```text
20 42 5F 30 30 30 30 37 0D 0A
```

This is an IR fragment for inspection. Do not translate it as a complete program or execute any file with its name.

## If the result differs

Compare labeljump with the printed addition. Check its arguments and saved state across calls, then inspect the generated text or bytes.
