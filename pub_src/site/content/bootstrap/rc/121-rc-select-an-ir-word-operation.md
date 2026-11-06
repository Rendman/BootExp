+++
title = "33 \u00b7 Translating an Arithmetic Operation"
weight = 33
description = "Emit the selected IR operation after the right expression is complete."
download = "RC33.RIL"
download_group = "tools/rill"
aliases = ["/bootstrap/rill/121-rc-select-an-ir-word-operation/"]
reader_names = 1
+++

## The working parts

Emit the selected IR operation after the right expression is complete. This routine translates an operation; it does not evaluate the user program during compilation.

## Enter the source

Copy RC32.RIL to RC33.RIL. Apply edits **from the bottom of the old file upward**. Physical positions refer to that unchanged old file; use the printed context to identify each place. Keep all other source.

### Edit 1

Unchanged source immediately before the edit:

```rill
    return 0;
}
```

Insert after old physical line 287.

Insert:

```rill
fn binary(op) {
    if op == 43 { return outstr("ADD\r\n"); }
    if op == 45 { return outstr("SUB\r\n"); }
    if op == 42 { return outstr("MUL\r\n"); }
    if op == 47 { return outstr("DIV\r\n"); }
    if op == 37 { return outstr("MOD\r\n"); }
    if op == 124 { return outstr("OR\r\n"); }
    if op == 94 { return outstr("XOR\r\n"); }
    if op == 38 { return outstr("AND\r\n"); }
    if op == 260 { return outstr("SHL\r\n"); }
    if op == 261 { return outstr("SHR\r\n"); }
    if op == 256 { return outstr("CEQ\r\n"); }
    if op == 257 { return outstr("CNE\r\n"); }
    if op == 258 { return outstr("CULE\r\n"); }
    if op == 259 { return outstr("CUGE\r\n"); }
    if op == 60 { return outstr("CULT\r\n"); }
    return outstr("CUGT\r\n");
}
```

The following old source remains in place:

```rill
fn fail(code) {
    if input { close(input); }
```

### Edit 2

Unchanged source immediately before the edit:

```rill
bytes ident[32];
bytes string[512];
```

Remove this source at old physical positions 35–35 in RC32.RIL:

```rill
fn main(){input=open("SOURCE.RIL");if status(){fail(1);}next();lex();return (prec())!=7;}
```

Replace it with:

```rill
fn main(){output=create("RILL.TMP");own=1;binary(43);flush();close(output);output=0;own=0;return 0;}
```

The following old source remains in place:

```rill

fn next() {
```

## Build this stopping point

```dos
COPY RC33.RIL SOURCE.RIL
CHECK RILLBOOT
```

Require `OK RESULT.IR 0000028479` and PASS. Copy RESULT.IR to SOURCE.IR.

```dos
CHECK IWKEEP
COPY RESULT.ASM SOURCE.ASM
CHECK ASMAKEEP
```

Require IR86 `OK RESULT.ASM 0000061927 text bytes` and PASS **before** the copy. Require assembler `OK RESULT.COM 19484 bytes` and PASS before saving:

```dos
COPY RESULT.COM RC33.COM
```

VIEW.BAS must report RC33.COM length 19484 bytes. Keep this executable and its source together.

## Acceptance check

```dos
CHECK RC33
```

The checker must report PASS. Inspect the emitted file below.

Use VIEW.BAS to inspect RILL.TMP. Require length 5 bytes. The complete bytes must be:

```text
41 44 44 0D 0A
```

This is an IR fragment for inspection. Do not translate it as a complete program or execute any file with its name.

After inspection, delete this deliberately created RILL.TMP before another checkpoint. The file is diagnostic text, not an interrupted accepted compiler build.

## If the result differs

Compare binary with the printed addition. Check its arguments and saved state across calls, then inspect the generated text or bytes.
