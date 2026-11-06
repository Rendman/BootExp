+++
title = "RC35 \u00b7 Values, addresses, and names"
weight = 35
description = "A primary can emit a literal, string pointer, binding, addressed slot, indexed byte, or call."
download = "RC35.RIL"
download_group = "rc"
aliases = ["/bootstrap/rill/123-rc-values-addresses-and-names/"]
+++

A primary can emit a literal, string pointer, binding, addressed slot, indexed byte, or call.

## The working parts

A primary can emit a literal, string pointer, binding, addressed slot, indexed byte, or call. Parentheses recurse through EXPR. Save binding metadata before scanning a nested expression, which can change the shared search fields.

The entry diagnostic exercises the printed helper. Rejecting placeholders identify forms outside this stopping point. A diagnostic that emits only an IR fragment is inspected as text; it is not a complete compiler or output program.

## Enter the source

Copy RC34.RIL to RC35.RIL. Apply edits **from the bottom of the old file upward**. Physical positions refer to that unchanged old file; use the printed context to identify each place. Keep all other source.

### Edit 1

Unchanged source immediately before the edit:

```rill
    return outstr("CUGT\r\n");
}
```

Remove this source at old physical positions 318–318 in RC34.RIL:

```rill
fn primary(){if tok!=2{fail(2);}outstr("LIT ");outnum(value);newline();lex();return 0;}
```

Replace it with:

```rill
fn primary() {
    let mut p = 0; let mut kind = 0; let mut slot = 0; let mut bi = 0;
    if tok == 2 { outstr("LIT "); outnum(value); newline(); lex(); return 0; }
    if tok == 3 { outstr("LITS "); outstr(string); newline(); lex(); return 0; }
    if tok == 40 { lex(); expr(1); expect(41); return 0; }
    if tok == 45 { lex(); expr(8); return outstr("NEG\r\n"); }
    if tok == 126 { lex(); expr(8); return outstr("NOT\r\n"); }
    if tok == 33 { lex(); expr(8); return outstr("PUSH\r\nLIT 0\r\nCEQ\r\n"); }
    if tok == 38 {
        lex(); if tok != 1 { fail(2); } resolve();
        if rectype <= 2 { outstr("ADDR V_"); outname(found); }
        else {
            if rectype == 5 { outstr("LADDR "); }
            else { if rectype == 6 { outstr("PADDR "); } else { fail(4); } }
            outnum(recval);
        }
        newline(); lex(); return 0;
    }
    if tok != 1 { fail(2); }
    p = resolveoptional(); kind = rectype; slot = recval; bi = callbuiltin; lex();
    if tok == 40 { return callargs(p,bi); }
    if kind == 1 { outstr("LD V_"); outname(p); newline(); return 0; }
    if kind == 5 { outstr("LOCAL "); outnum(slot); newline(); return 0; }
    if kind == 6 { outstr("PARAM "); outnum(slot); newline(); return 0; }
    if kind != 2 { fail(4); }
    outstr("ADDR V_"); outname(p); newline();
    if tok == 91 { outstr("PUSH\r\n"); lex(); expr(1); expect(93); outstr("ADD\r\nFETCHB\r\n"); }
    return 0;
}
```

The following old source remains in place:

```rill

fn fail(code) {
```

### Edit 2

Unchanged source immediately before the edit:

```rill
    recval = 65535; reclevel = 0; p = newglobal(4); rectype = 4; return p;
}
```

Insert after old physical line 276.

Insert:

```rill
fn callargs(p,bi){fail(2);return 0;}
```

The following old source remains in place:

```rill
fn prec() {
    if tok == 124 { return 1; } if tok == 94 { return 2; } if tok == 38 { return 3; }
```

## Build this stopping point

```dos
COPY RC35.RIL SOURCE.RIL
CHECK RILLBOOT
```

Require `OK RESULT.IR 0000034166` and PASS. Copy RESULT.IR to SOURCE.IR.

```dos
CHECK IWKEEP
COPY RESULT.ASM SOURCE.ASM
CHECK ASMAKEEP
```

Require IR86 `OK RESULT.ASM 0000073165 text bytes` and PASS **before** the copy. Require assembler `OK RESULT.COM 21427 bytes` and PASS before saving:

```dos
COPY RESULT.COM RC35.COM
```

VIEW.BAS must report RC35.COM length 21427 bytes. Keep this executable and its source together.

## Acceptance check

Create TRC35.RIL with COPY CON or a plain-text editor. Finish COPY CON with Ctrl-Z and Enter:

```rill
ABC+1
```

```dos
COPY TRC35.RIL SOURCE.RIL
```

```dos
CHECK RC35
```

Require, apart from command echo and the checker's separator:

```text
OK RILL.TMP
PASS
```

TYPE RILL.TMP. Its complete text is:

```ir
LD V_ABC
PUSH
LIT 00001
ADD
```

VIEW.BAS must show length 32 bytes. This is an IR fragment for inspection. Do not translate it as a complete program or execute any file with its name.

After inspection, delete this deliberately created RILL.TMP before another checkpoint. The file is diagnostic text, not an interrupted accepted compiler build.

## A rejection or boundary check

Create XRC35.RIL:

```rill
UNKNOWN
```

```dos
COPY XRC35.RIL SOURCE.RIL
CHECK RC35
```

Require:

```text
ERROR 0000000001 CODE 00004
FAIL
```

An unexpected PASS fails the rejection. The pre-existing RESULT.IR must remain unchanged; preserve a copy before the test.

## If the result differs

Check the saved pointer or slot, argument order, complete token spelling, and STATUS immediately after each service. A helper's local state must survive calls; an output count is independent of input position. Inspect text and file length before interpreting any bytes as a program.
