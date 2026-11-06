+++
title = "RC32 \u00b7 A precedence table in RILL"
weight = 120
description = "Return a precedence number, with zero for a nonoperator."
download = "RC32.RIL"
download_group = "toolchain"
+++

Return a precedence number, with zero for a nonoperator.

## The working parts

Return a precedence number, with zero for a nonoperator. Multiplication binds more tightly than addition; word comparisons and bit operators occupy explicitly defined lower levels.

The entry diagnostic exercises the printed helper. Rejecting placeholders identify forms outside this stopping point. A diagnostic that emits only an IR fragment is inspected as text; it is not a complete compiler or output program.

## Enter the source

Copy RC31.RIL to RC32.RIL. Apply edits **from the bottom of the old file upward**. Physical positions refer to that unchanged old file; use the printed context to identify each place. Keep all other source.

### Edit 1

Unchanged source immediately before the edit:

```rill
    recval = 65535; reclevel = 0; p = newglobal(4); rectype = 4; return p;
}
```

Insert after old physical line 276.

Insert:

```rill
fn prec() {
    if tok == 124 { return 1; } if tok == 94 { return 2; } if tok == 38 { return 3; }
    if tok == 256 { return 4; } if tok == 257 { return 4; }
    if tok == 258 { return 4; } if tok == 259 { return 4; }
    if tok == 60 { return 4; } if tok == 62 { return 4; }
    if tok == 260 { return 5; } if tok == 261 { return 5; }
    if tok == 43 { return 6; } if tok == 45 { return 6; }
    if tok == 42 { return 7; } if tok == 47 { return 7; } if tok == 37 { return 7; }
    return 0;
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

Remove this source at old physical positions 35–35 in RC31.RIL:

```rill
fn main(){table=alloc(22000);setident("ABC");rectype=1;recval=12345;reclevel=0;record(0);globals=1;resolveoptional();printnum(rectype);return 0;}
```

Replace it with:

```rill
fn main(){input=open("SOURCE.RIL");if status(){fail(1);}next();lex();printnum(prec());return 0;}
```

The following old source remains in place:

```rill

fn next() {
```

## Build this stopping point

```dos
COPY RC32.RIL SOURCE.RIL
CHECK RILLBOOT
```

Require `OK RESULT.IR 0000026234` and PASS. Copy RESULT.IR to SOURCE.IR.

```dos
CHECK IWKEEP
COPY RESULT.ASM SOURCE.ASM
CHECK ASMAKEEP
```

Require IR86 `OK RESULT.ASM 0000056627 text bytes` and PASS **before** the copy. Require assembler `OK RESULT.COM 18640 bytes` and PASS before saving:

```dos
COPY RESULT.COM RC32.COM
```

VIEW.BAS must report RC32.COM length 18640 bytes. Keep this executable and its source together.

## Acceptance check

Create TRC32.RIL with COPY CON or a plain-text editor. Finish COPY CON with Ctrl-Z and Enter:

```rill
*
```

```dos
COPY TRC32.RIL SOURCE.RIL
```

```dos
CHECK RC32
```

Require, apart from command echo and the checker's separator:

```text
00007PASS
```

## A rejection or boundary check

Rename SOURCE.RIL to an unused HOLD.RIL and run CHECK RC32. Restore the source afterward.

Require:

```text
ERROR 0000000001 CODE 00001
FAIL
```

An unexpected PASS fails the rejection. The pre-existing RESULT.IR must remain unchanged; preserve a copy before the test.

## If the result differs

Check the saved pointer or slot, argument order, complete token spelling, and STATUS immediately after each service. A helper's local state must survive calls; an output count is independent of input position. Inspect text and file length before interpreting any bytes as a program.
