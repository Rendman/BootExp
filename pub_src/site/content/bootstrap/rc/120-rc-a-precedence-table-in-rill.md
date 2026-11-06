+++
title = "32 \u00b7 Making Multiplication Come First"
weight = 32
description = "Return a precedence number, with zero for a nonoperator."
download = "RC32.RIL"
download_group = "tools/rill"
aliases = ["/bootstrap/rill/120-rc-a-precedence-table-in-rill/"]
reader_names = 1
+++

## The working parts

Return a precedence number, with zero for a nonoperator. Multiplication binds more tightly than addition; word comparisons and bit operators occupy explicitly defined lower levels.

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
fn main(){table=alloc(22000);setident("ABC");rectype=1;recval=12345;reclevel=0;record(0);globals=1;resolveoptional();return (rectype)!=1;}
```

Replace it with:

```rill
fn main(){input=open("SOURCE.RIL");if status(){fail(1);}next();lex();return (prec())!=7;}
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

Require `OK RESULT.IR 0000026214` and PASS. Copy RESULT.IR to SOURCE.IR.

```dos
CHECK IWKEEP
COPY RESULT.ASM SOURCE.ASM
CHECK ASMAKEEP
```

Require IR86 `OK RESULT.ASM 0000056639 text bytes` and PASS **before** the copy. Require assembler `OK RESULT.COM 18642 bytes` and PASS before saving:

```dos
COPY RESULT.COM RC32.COM
```

VIEW.BAS must report RC32.COM length 18642 bytes. Keep this executable and its source together.

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

The checker must report PASS. The driver compares the result with 7 and returns nonzero on a mismatch; it adds no display routine.

## If the result differs

Check the token code against the returned precedence. Multiplication must rank above addition; a nonoperator returns zero.
