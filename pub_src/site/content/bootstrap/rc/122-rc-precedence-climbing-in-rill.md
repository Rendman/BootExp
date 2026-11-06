+++
title = "34 \u00b7 Translating an Expression"
weight = 34
description = "Save the pending operator and precedence in local slots."
download = "RC34.RIL"
download_group = "tools/rill"
aliases = ["/bootstrap/rill/122-rc-precedence-climbing-in-rill/"]
reader_names = 1
+++

## The working parts

Save the pending operator and precedence in local slots. Emit PUSH for the left operand, recurse at one higher minimum precedence for the right, then emit the operation. A bounded recursion counter prevents uncontrolled nesting.

## Enter the source

Copy RC33.RIL to RC34.RIL. Apply edits **from the bottom of the old file upward**. Physical positions refer to that unchanged old file; use the printed context to identify each place. Keep all other source.

### Edit 1

Unchanged source immediately before the edit:

```rill
    if op == 60 { return outstr("CULT\r\n"); }
    return outstr("CUGT\r\n");
}
```

Insert after old physical line 305.

Insert:

```rill

fn primary(){if tok!=2{fail(2);}outstr("LIT ");outnum(value);newline();lex();return 0;}
```

The following old source remains in place:

```rill

fn fail(code) {
```

### Edit 2

Unchanged source immediately before the edit:

```rill
    return 0;
}
```

Insert after old physical line 287.

Insert:

```rill
fn expr(min) {
    let mut p = 0; let mut op = 0;
    exprdepth = exprdepth+1; if exprdepth > 16 { fail(5); }
    primary(); p = prec();
    while p != 0 {
        if p < min { exprdepth = exprdepth-1; return 0; }
        op = tok; outstr("PUSH\r\n"); lex(); expr(p+1); binary(op); p = prec();
    }
    exprdepth = exprdepth-1; return 0;
}
```

The following old source remains in place:

```rill
fn binary(op) {
    if op == 43 { return outstr("ADD\r\n"); }
```

### Edit 3

Unchanged source immediately before the edit:

```rill
bytes ident[32];
bytes string[512];
```

Remove this source at old physical positions 35–35 in RC33.RIL:

```rill
fn main(){output=create("RILL.TMP");own=1;binary(43);flush();close(output);output=0;own=0;return 0;}
```

Replace it with:

```rill
fn main(){table=alloc(22000);setident("ABC");rectype=1;recval=12345;reclevel=0;record(0);globals=1;output=create("RILL.TMP");own=1;input=open("SOURCE.RIL");if status(){fail(1);}next();lex();expr(1);if tok!=0{fail(2);}flush();close(output);output=0;own=0;return 0;}
```

The following old source remains in place:

```rill

fn next() {
```

## Build this stopping point

```dos
COPY RC34.RIL SOURCE.RIL
CHECK RILLBOOT
```

Require `OK RESULT.IR 0000030368` and PASS. Copy RESULT.IR to SOURCE.IR.

```dos
CHECK IWKEEP
COPY RESULT.ASM SOURCE.ASM
CHECK ASMAKEEP
```

Require IR86 `OK RESULT.ASM 0000065503 text bytes` and PASS **before** the copy. Require assembler `OK RESULT.COM 20109 bytes` and PASS before saving:

```dos
COPY RESULT.COM RC34.COM
```

VIEW.BAS must report RC34.COM length 20109 bytes. Keep this executable and its source together.

## Acceptance check

Create TRC34.RIL with COPY CON or a plain-text editor. Finish COPY CON with Ctrl-Z and Enter:

```rill
1+2*3
```

```dos
COPY TRC34.RIL SOURCE.RIL
```

```dos
CHECK RC34
```

The checker must report PASS. Inspect the emitted file below.

Use VIEW.BAS to inspect RILL.TMP. Require length 55 bytes. The complete bytes must be:

```text
4C 49 54 20 30 30 30 30 31 0D 0A 50 55 53 48 0D
0A 4C 49 54 20 30 30 30 30 32 0D 0A 50 55 53 48
0D 0A 4C 49 54 20 30 30 30 30 33 0D 0A 4D 55 4C
0D 0A 41 44 44 0D 0A
```

This is an IR fragment for inspection. Do not translate it as a complete program or execute any file with its name.

After inspection, delete this deliberately created RILL.TMP before another checkpoint. The file is diagnostic text, not an interrupted accepted compiler build.

## A rejection or boundary check

Create XRC34.RIL:

```rill
(1)
```

```dos
COPY XRC34.RIL SOURCE.RIL
CHECK RC34
```

Require:

```text
ERROR 0000000001 CODE 00002
FAIL
```

An unexpected PASS fails the rejection. The pre-existing RESULT.IR must remain unchanged; preserve a copy before the test.

## If the result differs

Compare expr with the printed addition. Check its arguments and saved state across calls, then inspect the generated text or bytes.
