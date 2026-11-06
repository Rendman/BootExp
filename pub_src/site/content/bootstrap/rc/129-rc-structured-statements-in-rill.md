+++
title = "RC41 \u00b7 Structured statements in RILL"
weight = 41
description = "Keep assignment destinations, false targets, and loop targets in local slots."
download = "RC41.RIL"
download_group = "rc"
aliases = ["/bootstrap/rill/129-rc-structured-statements-in-rill/"]
+++

Keep assignment destinations, false targets, and loop targets in local slots.

## The working parts

Keep assignment destinations, false targets, and loop targets in local slots. An if/else join and a while back edge meet with no expression temporaries. Parse every statement even after an explicit return.

The entry diagnostic exercises the printed helper. Rejecting placeholders identify forms outside this stopping point. A diagnostic that emits only an IR fragment is inspected as text; it is not a complete compiler or output program.

## Enter the source

Copy RC40.RIL to RC41.RIL. Apply edits **from the bottom of the old file upward**. Physical positions refer to that unchanged old file; use the printed context to identify each place. Keep all other source.

### Edit 1

Unchanged source immediately before the edit:

```rill
    outstr("SETLOCAL "); outnum(slot); newline(); expect(59); return 0;
}
```

Remove this source at old physical positions 293–293 in RC40.RIL:

```rill
fn statement(){fail(2);return 0;}
```

Replace it with:

```rill
fn statement() {
    let mut p = 0; let mut kind = 0; let mut slot = 0;
    let mut a = 0; let mut b = 0; let mut bi = 0;
    if tok == 123 { return block(); }
    if isword("LET") { return declare(); }
    if isword("RETURN") {
        lex(); if tok == 59 { outstr("LIT 0\r\n"); } else { expr(1); }
        outstr("RETURN\r\n"); expect(59); return 0;
    }
    if isword("IF") {
        a = newlabel(); b = newlabel(); lex(); expr(1);
        outstr("JZ"); labeljump(a); block(); outstr("JMP"); labeljump(b); labeldef(a);
        if isword("ELSE") { lex(); block(); }
        labeldef(b); return 0;
    }
    if isword("WHILE") {
        a = newlabel(); b = newlabel(); labeldef(a); lex(); expr(1);
        outstr("JZ"); labeljump(b); block(); outstr("JMP"); labeljump(a); labeldef(b); return 0;
    }
    if tok != 1 { fail(2); }
    p = resolveoptional(); kind = rectype; slot = recval; bi = callbuiltin;
    lex();
    if tok == 40 { callargs(p,bi); expect(59); return 0; }
    if p == 65535 { fail(4); }
    if tok == 91 {
        if kind != 2 { fail(4); }
        outstr("ADDR V_"); outname(p); outstr("\r\nPUSH\r\n");
        lex(); expr(1); expect(93); outstr("ADD\r\n");
    }
    else {
        if kind == 1 { outstr("ADDR V_"); outname(p); newline(); }
        else {
            if kind == 5 { outstr("LADDR "); }
            else { if kind == 6 { outstr("PADDR "); } else { fail(4); } }
            outnum(slot); newline();
        }
    }
    outstr("PUSH\r\n"); expect(61); expr(1);
    if kind == 2 { outstr("PUTB\r\n"); } else { outstr("PUT\r\n"); }
    expect(59); return 0;
}
```

The following old source remains in place:

```rill

fn builtin() {
```

### Edit 2

Unchanged source immediately before the edit:

```rill
bytes ident[32];
bytes string[512];
```

Remove this source at old physical positions 35–35 in RC40.RIL:

```rill
fn main(){table=alloc(22000);output=create("RILL.TMP");own=1;input=open("SOURCE.RIL");if status(){fail(1);}next();lex();block();flush();close(output);output=0;own=0;print("OK RILL.TMP\r\n");return 0;}
```

Replace it with:

```rill
fn main(){table=alloc(22000);output=create("RILL.TMP");own=1;input=open("SOURCE.RIL");if status(){fail(1);}next();lex();outstr("PROC MAIN 0 16\r\n");block();outstr("LIT 0\r\nRETURN\r\n");flush();close(output);output=0;own=0;print("OK RILL.TMP\r\n");return 0;}
```

The following old source remains in place:

```rill

fn next() {
```

## Build this stopping point

```dos
COPY RC41.RIL SOURCE.RIL
CHECK RILLBOOT
```

Require `OK RESULT.IR 0000044238` and PASS. Copy RESULT.IR to SOURCE.IR.

```dos
CHECK IWKEEP
COPY RESULT.ASM SOURCE.ASM
CHECK ASMAKEEP
```

Require IR86 `OK RESULT.ASM 0000091929 text bytes` and PASS **before** the copy. Require assembler `OK RESULT.COM 24743 bytes` and PASS before saving:

```dos
COPY RESULT.COM RC41.COM
```

VIEW.BAS must report RC41.COM length 24743 bytes. Keep this executable and its source together.

## Acceptance check

Create TRC41.RIL with COPY CON or a plain-text editor. Finish COPY CON with Ctrl-Z and Enter:

```rill
{let mut x=65;while x<67{putc(x);x=x+1;}}
```

```dos
COPY TRC41.RIL SOURCE.RIL
```

```dos
CHECK RC41
```

Require, apart from command echo and the checker's separator:

```text
OK RILL.TMP
PASS
```

TYPE RILL.TMP. Its complete text is:

```ir
PROC MAIN 0 16
LIT 00065
SETLOCAL 00000
LABEL B_00001
LOCAL 00000
PUSH
LIT 00067
CULT
JZ B_00002
LOCAL 00000
PUSH
POP
PUTC
LADDR 00000
PUSH
LOCAL 00000
PUSH
LIT 00001
ADD
PUT
JMP B_00001
LABEL B_00002
LIT 0
RETURN
```

VIEW.BAS must show length 238 bytes. This is a complete program. Copy it to SOURCE.IR, run CHECK IWKEEP, copy the accepted RESULT.ASM to SOURCE.ASM, and run CHECK ASMAKEEP. Require OK and PASS at both steps. VIEW.BAS must report RESULT.COM length 1131. Copy that file to TRY.COM; CHECK TRY displays `AB` and reports PASS.

After inspection, delete this deliberately created RILL.TMP before another checkpoint. The file is diagnostic text, not an interrupted accepted compiler build.

## A rejection or boundary check

Create XRC41.RIL:

```rill
{putc();}
```

```dos
COPY XRC41.RIL SOURCE.RIL
CHECK RC41
```

Require:

```text
ERROR 0000000001 CODE 00004
FAIL
```

An unexpected PASS fails the rejection. The pre-existing RESULT.IR must remain unchanged; preserve a copy before the test.

## If the result differs

Check the saved pointer or slot, argument order, complete token spelling, and STATUS immediately after each service. A helper's local state must survive calls; an output count is independent of input position. Inspect text and file length before interpreting any bytes as a program.
