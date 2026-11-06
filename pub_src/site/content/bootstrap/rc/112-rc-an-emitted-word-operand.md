+++
title = "RC24 \u00b7 An emitted word operand"
weight = 24
description = "Emit a fixed decimal word spelling through OUTCHAR."
download = "RC24.RIL"
download_group = "rc"
aliases = ["/bootstrap/rill/112-rc-an-emitted-word-operand/"]
+++

Emit a fixed decimal word spelling through OUTCHAR.

## The working parts

Emit a fixed decimal word spelling through OUTCHAR. It uses the same checked output path as instruction names and delimiters.

The entry diagnostic exercises the printed helper. Rejecting placeholders identify forms outside this stopping point. A diagnostic that emits only an IR fragment is inspected as text; it is not a complete compiler or output program.

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
fn main(){output=create("RILL.TMP");own=1;outstr("HI");flush();close(output);output=0;own=0;print("OK RILL.TMP\r\n");return 0;}
```

Replace it with:

```rill
fn main(){output=create("RILL.TMP");own=1;outnum(12345);flush();close(output);output=0;own=0;print("OK RILL.TMP\r\n");return 0;}
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

Require `OK RESULT.IR 0000020790` and PASS. Copy RESULT.IR to SOURCE.IR.

```dos
CHECK IWKEEP
COPY RESULT.ASM SOURCE.ASM
CHECK ASMAKEEP
```

Require IR86 `OK RESULT.ASM 0000043425 text bytes` and PASS **before** the copy. Require assembler `OK RESULT.COM 16581 bytes` and PASS before saving:

```dos
COPY RESULT.COM RC24.COM
```

VIEW.BAS must report RC24.COM length 16581 bytes. Keep this executable and its source together.

## Acceptance check

```dos
CHECK RC24
```

Require, apart from command echo and the checker's separator:

```text
OK RILL.TMP
PASS
```

TYPE RILL.TMP. Its complete text is:

```ir
12345
```

VIEW.BAS must show length 5 bytes. This is an IR fragment for inspection. Do not translate it as a complete program or execute any file with its name.

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
