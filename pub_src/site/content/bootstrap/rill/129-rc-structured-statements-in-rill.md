+++
title = "41 \u00b7 Compiling Assignments and Branches"
weight = 41
description = "Keep assignment destinations, false targets, and loop targets in local slots."
download = "RC41.RIL"
download_group = "tools/rill"
aliases = ["/bootstrap/rill/129-rc-structured-statements-in-rill/"]
reader_names = 1
url = "/bootstrap/rc/129-rc-structured-statements-in-rill/"
+++

## The working parts

Keep assignment destinations, false targets, and loop targets in local slots. An if/else join and a while back edge meet with no expression temporaries. Parse every statement even after an explicit return.

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
fn main(){filearg(1,"SOURCE.RIL");table=alloc(23680);output=create(filearg(2,"RILL.TMP"));own=1;input=open(filearg(1,"SOURCE.RIL"));if status(){fail(1);}next();lex();block();flush();close(output);output=0;own=0;return 0;}
```

Replace it with:

```rill
fn main(){filearg(1,"SOURCE.RIL");table=alloc(23680);output=create(filearg(2,"RILL.TMP"));own=1;input=open(filearg(1,"SOURCE.RIL"));if status(){fail(1);}next();lex();outstr("PROC MAIN 0 64\r\n");block();outstr("LIT 0\r\nRETURN\r\n");flush();close(output);output=0;own=0;return 0;}
```

The following old source remains in place:

```rill

fn next() {
```

## Build this stopping point

```dos
CHECK RILLBOOT RC41.RIL RESULT.IR
```

Require `OK RESULT.IR 0000045819` and PASS. Pass RESULT.IR directly to the translator.

```dos
CHECK IWKEEP SOURCE.IR RESULT.ASM
CHECK ASMAKEEP RESULT.ASM RESULT.COM
```

Require IR86 `OK RESULT.ASM 0000096930 text bytes` and PASS **before** the copy. Require assembler `OK RESULT.COM 25638 bytes` and PASS before saving:

```dos
COPY RESULT.COM RC41.COM
```

VIEW.BAS must report RC41.COM length 25638 bytes. Keep this executable and its source together.

## Acceptance check

Create TRC41.RIL with COPY CON or a plain-text editor. Finish COPY CON with Ctrl-Z and Enter:

```rill
{let mut x=65;while x<67{putc(x);x=x+1;}}
```

```dos
CHECK RC41 TRC41.RIL RESULT.IR
```

The checker must report PASS. Inspect the emitted file below.

TYPE RESULT.IR. Its complete IR is:

```ir
PROC MAIN 0 64
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

VIEW.BAS must show length 238 bytes. This is a complete program. Run CHECK IWKEEP RESULT.IR RESULT.ASM, then CHECK ASMAKEEP RESULT.ASM RESULT.COM. Require OK and PASS at both steps. VIEW.BAS must report RESULT.COM length 1445. Copy that file to TRY.COM; CHECK TRY displays `AB` and reports PASS.

## A rejection or boundary check

Create XRC41.RIL:

```rill
{putc();}
```

```dos
CHECK RC41 XRC41.RIL RESULT.IR
```

Require:

```text
ERROR 0000000001 CODE 00004
FAIL
```

An unexpected PASS fails the rejection. The pre-existing RESULT.IR must remain unchanged; preserve a copy before the test.

## If the result differs

Compare statement with the printed addition. Check its arguments and saved state across calls, then inspect the generated text or bytes.
