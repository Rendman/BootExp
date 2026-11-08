+++
title = "43 \u00b7 Compiling a Complete Program"
weight = 43
description = "Open the fixed source, stream accepted IR through an owned temporary file, and verify all pending procedures."
download = "RC43.RIL"
download_group = "tools/rill"
aliases = ["/bootstrap/rill/131-rc-the-compiler-compiles-its-own-language/"]
reader_names = 1
url = "/bootstrap/rc/131-rc-the-compiler-compiles-its-own-language/"
+++

## The working parts

Open the fixed source, stream accepted IR through an owned temporary file, and verify all pending procedures. Require an argument-free main. Publish only after parsing, source close, flush, and output close succeed.

## Enter the source

Copy RC42.RIL to RC43.RIL. Apply edits **from the bottom of the old file upward**. Physical positions refer to that unchanged old file; use the printed context to identify each place. Keep all other source.

### Edit 1

Unchanged source immediately before the edit:

```rill
}

// Divide a pair of words by ten without requiring a wider machine value.
```

Remove this source at old physical positions 483–483 in RC42.RIL:

```rill

```

There is no replacement source.

The following old source remains in place:

```rill
fn print32(hi,lo) {
    let mut i = 0; let mut qhi = 0; let mut rem = 0;
```

### Edit 2

Unchanged source immediately before the edit:

```rill
    if tok == 91 { outstr("PUSH\r\n"); lex(); expr(1); expect(93); outstr("ADD\r\nFETCHB\r\n"); }
    return 0;
}
```

Remove this source at old physical positions 470–470 in RC42.RIL:

```rill

```

There is no replacement source.

The following old source remains in place:

```rill
fn fail(code) {
    if input { close(input); }
```

### Edit 3

Unchanged source immediately before the edit:

```rill
    if op == 60 { return outstr("CULT\r\n"); }
    return outstr("CUGT\r\n");
}
```

Remove this source at old physical positions 440–440 in RC42.RIL:

```rill

```

There is no replacement source.

The following old source remains in place:

```rill
fn primary() {
    let mut p = 0; let mut kind = 0; let mut slot = 0; let mut bi = 0;
```

### Edit 4

Unchanged source immediately before the edit:

```rill
    }
    exprdepth = exprdepth-1; return 0;
}
```

Remove this source at old physical positions 421–421 in RC42.RIL:

```rill

```

There is no replacement source.

The following old source remains in place:

```rill
fn binary(op) {
    if op == 43 { return outstr("ADD\r\n"); }
```

### Edit 5

Unchanged source immediately before the edit:

```rill
    if tok == 42 { return 7; } if tok == 47 { return 7; } if tok == 37 { return 7; }
    return 0;
}
```

Remove this source at old physical positions 410–410 in RC42.RIL:

```rill

```

There is no replacement source.

The following old source remains in place:

```rill
fn expr(min) {
    let mut p = 0; let mut op = 0;
```

### Edit 6

Unchanged source immediately before the edit:

```rill
    else { if wanted != argc { fail(4); } }
    outstr("INVOKE F_"); outname(p); outchar(32); outnum(argc); newline(); return 0;
}
```

Remove this source at old physical positions 399–399 in RC42.RIL:

```rill

```

There is no replacement source.

The following old source remains in place:

```rill
fn prec() {
    if tok == 124 { return 1; } if tok == 94 { return 2; } if tok == 38 { return 3; }
```

### Edit 7

Unchanged source immediately before the edit:

```rill
    p = lookglobal(); if p != 65535 { return p; }
    recval = 65535; reclevel = 0; p = newglobal(4); rectype = 4; return p;
}
```

Remove this source at old physical positions 380–380 in RC42.RIL:

```rill

```

There is no replacement source.

The following old source remains in place:

```rill
fn callargs(p,bi) {
    let mut argc = 0; let mut kind = 0; let mut wanted = 0;
```

### Edit 8

Unchanged source immediately before the edit:

```rill
    }
    return 0;
}
```

Remove this source at old physical positions 371–371 in RC42.RIL:

```rill

```

There is no replacement source.

The following old source remains in place:

```rill
fn resolveoptional() {
    callbuiltin = builtin();
```

### Edit 9

Unchanged source immediately before the edit:

```rill
    if kind == 2 { outstr("PUTB\r\n"); } else { outstr("PUT\r\n"); }
    expect(59); return 0;
}
```

Remove this source at old physical positions 357–357 in RC42.RIL:

```rill

```

There is no replacement source.

The following old source remains in place:

```rill
fn builtin() {
    let mut p = "PUTC\01\0POP\nPUTC\0STATUS\00\0STATUS\0OPEN\01\0POP\nOPEN\0CREATE\01\0POP\nCREATE\0CLOSE\01\0POP\nCLOSE\0READ\03\0POP\nREAD\0WRITE\03\0POP\nWRITE\0EXISTS\01\0POP\nEXISTS\0DELETE\01\0POP\nDELETE\0RENAME\02\0POP\nRENAME\0ALLOC\01\0POP\nALLOC\0FREE\01\0POP\nFREEBLOCK\0GET8\02\0POP\nGET8\0GET16\02\0POP\nGET16\0SET8\03\0POP\nSET8\0SET16\03\0POP\nSET16\0LOAD8\01\0POP\nFETCHB\0LOAD16\01\0POP\nFETCH\0STORE8\02\0POP\nPUTB\0STORE16\02\0POP\nPUT\0EXIT\01\0POP\nEXIT\0\0";
```

### Edit 10

Unchanged source immediately before the edit:

```rill
    lex(); expect(61); expr(1); set16(table,p+32,5);
    outstr("SETLOCAL "); outnum(slot); newline(); expect(59); return 0;
}
```

Remove this source at old physical positions 315–315 in RC42.RIL:

```rill

```

There is no replacement source.

The following old source remains in place:

```rill
fn statement() {
    let mut p = 0; let mut kind = 0; let mut slot = 0;
```

### Edit 11

Unchanged source immediately before the edit:

```rill
    while tok != 125 { if tok == 0 { fail(2); } statement(); }
    lex(); localcount = oldcount; nextlocal = oldnext; level = level-1; return 0;
}
```

Remove this source at old physical positions 304–304 in RC42.RIL:

```rill

```

There is no replacement source.

The following old source remains in place:

```rill
fn declare() {
    lex(); if !isword("MUT") { fail(2); } lex(); if tok != 1 { fail(2); }
```

### Edit 12

Unchanged source immediately before the edit:

```rill
    outstr("PROC F_"); outname(p); outchar(32); outnum(argc); outstr(" 64\r\n");
    lex(); block(); outstr("LIT 0\r\nRETURN\r\n"); return 0;
}
```

Remove this source at old physical positions 295–295 in RC42.RIL:

```rill

```

There is no replacement source.

The following old source remains in place:

```rill
fn block() {
    let mut oldcount = localcount;
```

### Edit 13

Unchanged source immediately before the edit:

```rill
    outstr("BUFFER V_"); outname(p); outchar(32); outnum(value); newline();
    lex(); expect(93); expect(59); return 0;
}
```

Remove this source at old physical positions 272–272 in RC42.RIL:

```rill

```

There is no replacement source.

The following old source remains in place:

```rill
fn function() {
    lex(); if tok != 1 { fail(2); }
```

### Edit 14

Unchanged source immediately before the edit:

```rill
    outstr("WORD V_"); outname(p); outchar(32); outnum(value); newline();
    lex(); expect(59); return 0;
}
```

Remove this source at old physical positions 263–263 in RC42.RIL:

```rill

```

There is no replacement source.

The following old source remains in place:

```rill
fn globalbuffer() {
    lex(); if tok != 1 { fail(2); } if lookglobal() != 65535 { fail(4); }
```

### Edit 15

Unchanged source immediately before the edit:

```rill
    while place { c = 48; while n >= place { n = n-place; c = c+1; } putc(c); place = place/10; }
    return 0;
}
```

Remove this source at old physical positions 253–253 in RC42.RIL:

```rill

```

There is no replacement source.

The following old source remains in place:

```rill
fn globalword() {
    lex(); if !isword("MUT") { fail(2); } lex(); if tok != 1 { fail(2); }
```

### Edit 16

Unchanged source immediately before the edit:

```rill
fn labeljump(n) { outstr(" B_"); outnum(n); newline(); return 0; }

fn print(s) { let mut c = 0; while 1 { c = load8(s); if c == 0 { return 0; } putc(c); s = s+1; } }
```

Remove this source at old physical positions 247–247 in RC42.RIL:

```rill

```

There is no replacement source.

The following old source remains in place:

```rill
fn printnum(n) {
    let mut place = 10000; let mut c = 0;
```

### Edit 17

Unchanged source immediately before the edit:

```rill
fn labeldef(n) { outstr("LABEL B_"); outnum(n); newline(); return 0; }

fn labeljump(n) { outstr(" B_"); outnum(n); newline(); return 0; }
```

Remove this source at old physical positions 245–245 in RC42.RIL:

```rill

```

There is no replacement source.

The following old source remains in place:

```rill
fn print(s) { let mut c = 0; while 1 { c = load8(s); if c == 0 { return 0; } putc(c); s = s+1; } }
```

### Edit 18

Unchanged source immediately before the edit:

```rill
fn newlabel() { labelno = labelno+1; if labelno == 0 { fail(5); } return labelno; }

fn labeldef(n) { outstr("LABEL B_"); outnum(n); newline(); return 0; }
```

Remove this source at old physical positions 243–243 in RC42.RIL:

```rill

```

There is no replacement source.

The following old source remains in place:

```rill
fn labeljump(n) { outstr(" B_"); outnum(n); newline(); return 0; }
```

### Edit 19

Unchanged source immediately before the edit:

```rill
fn newline() { return outstr("\r\n"); }

fn newlabel() { labelno = labelno+1; if labelno == 0 { fail(5); } return labelno; }
```

Remove this source at old physical positions 241–241 in RC42.RIL:

```rill

```

There is no replacement source.

The following old source remains in place:

```rill
fn labeldef(n) { outstr("LABEL B_"); outnum(n); newline(); return 0; }
```

### Edit 20

Unchanged source immediately before the edit:

```rill
}

fn newline() { return outstr("\r\n"); }
```

Remove this source at old physical positions 239–239 in RC42.RIL:

```rill

```

There is no replacement source.

The following old source remains in place:

```rill
fn newlabel() { labelno = labelno+1; if labelno == 0 { fail(5); } return labelno; }
```

### Edit 21

Unchanged source immediately before the edit:

```rill
    while place { c = 48; while n >= place { n = n-place; c = c+1; } outchar(c); place = place/10; }
    return 0;
}
```

Remove this source at old physical positions 237–237 in RC42.RIL:

```rill

```

There is no replacement source.

The following old source remains in place:

```rill
fn newline() { return outstr("\r\n"); }
```

### Edit 22

Unchanged source immediately before the edit:

```rill
        outchar(c); previous=c; s=s+1;
    }
}
```

Remove this source at old physical positions 231–231 in RC42.RIL:

```rill

```

There is no replacement source.

The following old source remains in place:

```rill
fn outnum(n) {
    let mut place = 10000; let mut c = 0;
```

### Edit 23

Unchanged source immediately before the edit:

```rill
    }
    return 0;
}
```

Remove this source at old physical positions 222–222 in RC42.RIL:

```rill

```

There is no replacement source.

The following old source remains in place:

```rill
fn outstr(s) {
    let mut c=0; let mut previous=0;
```

### Edit 24

Unchanged source immediately before the edit:

```rill
    if outlen == 4096 { flush(); }
    return 0;
}
```

Remove this source at old physical positions 212–212 in RC42.RIL:

```rill

```

There is no replacement source.

The following old source remains in place:

```rill
fn flush() {
    if outlen {
```

### Edit 25

Unchanged source immediately before the edit:

```rill
}

fn outname(p) { let mut i = 0; let mut c = 0; while 1 { c = tbyte(p+i); if c == 0 { return 0; } outchar(c); i = i+1; } }
```

Remove this source at old physical positions 205–205 in RC42.RIL:

```rill

```

There is no replacement source.

The following old source remains in place:

```rill
fn outchar(c) {
    outbuf[outlen] = c; outlen = outlen+1; total = total+1;
```

### Edit 26

Unchanged source immediately before the edit:

```rill
    if found == 65535 { found = lookglobal(); if found == 65535 { fail(4); } }
    return found;
}
```

Remove this source at old physical positions 203–203 in RC42.RIL:

```rill

```

There is no replacement source.

The following old source remains in place:

```rill
fn outname(p) { let mut i = 0; let mut c = 0; while 1 { c = tbyte(p+i); if c == 0 { return 0; } outchar(c); i = i+1; } }
```

### Edit 27

Unchanged source immediately before the edit:

```rill
}

fn lookglobal() { return find(0,globals); }
```

Remove this source at old physical positions 197–197 in RC42.RIL:

```rill

```

There is no replacement source.

The following old source remains in place:

```rill
fn resolve() {
    found = find(20480,localcount);
```

### Edit 28

Unchanged source immediately before the edit:

```rill
    let mut p = 20480+localcount*40; localcount = localcount+1;
    return record(p);
}
```

Remove this source at old physical positions 195–195 in RC42.RIL:

```rill

```

There is no replacement source.

The following old source remains in place:

```rill
fn lookglobal() { return find(0,globals); }
```

### Edit 29

Unchanged source immediately before the edit:

```rill
    let mut p = globals*40; globals = globals+1;
    return record(p);
}
```

Remove this source at old physical positions 188–188 in RC42.RIL:

```rill

```

There is no replacement source.

The following old source remains in place:

```rill
fn newlocal(kind) {
    if localcount >= 80 { fail(5); }
```

### Edit 30

Unchanged source immediately before the edit:

```rill
}

fn recordfields(p) { set16(table,p+32,rectype); set16(table,p+34,recval); set16(table,p+36,reclevel); return p; }
```

Remove this source at old physical positions 181–181 in RC42.RIL:

```rill

```

There is no replacement source.

The following old source remains in place:

```rill
fn newglobal(kind) {
    if globals >= 512 { fail(5); }
```

### Edit 31

Unchanged source immediately before the edit:

```rill
    i = 0;
    while 1 { set8(table,p+i,ident[i]); if ident[i] == 0 { return recordfields(p); } i = i+1; }
}
```

Remove this source at old physical positions 179–179 in RC42.RIL:

```rill

```

There is no replacement source.

The following old source remains in place:

```rill
fn recordfields(p) { set16(table,p+32,rectype); set16(table,p+34,recval); set16(table,p+36,reclevel); return p; }
```

### Edit 32

Unchanged source immediately before the edit:

```rill
    }
    return 65535;
}
```

Remove this source at old physical positions 172–172 in RC42.RIL:

```rill

```

There is no replacement source.

The following old source remains in place:

```rill
fn record(p) {
    let mut i = 0;
```

### Edit 33

Unchanged source immediately before the edit:

```rill
fn tword(p) { return get16(table,p); }

fn tbyte(p) { return get8(table,p); }
```

Remove this source at old physical positions 150–150 in RC42.RIL:

```rill

```

There is no replacement source.

The following old source remains in place:

```rill
fn find(base,count) {
    let mut p = 0;
```

### Edit 34

Unchanged source immediately before the edit:

```rill
fn setident(s) { let mut i = 0; while 1 { ident[i] = load8(s+i); if ident[i] == 0 { return 0; } i = i+1; } }

fn tword(p) { return get16(table,p); }
```

Remove this source at old physical positions 148–148 in RC42.RIL:

```rill

```

There is no replacement source.

The following old source remains in place:

```rill
fn tbyte(p) { return get8(table,p); }
```

### Edit 35

Unchanged source immediately before the edit:

```rill
}

fn setident(s) { let mut i = 0; while 1 { ident[i] = load8(s+i); if ident[i] == 0 { return 0; } i = i+1; } }
```

Remove this source at old physical positions 146–146 in RC42.RIL:

```rill

```

There is no replacement source.

The following old source remains in place:

```rill
fn tword(p) { return get16(table,p); }
```

### Edit 36

Unchanged source immediately before the edit:

```rill
    while ident[i] == load8(s+i) { if ident[i] == 0 { return 1; } i = i+1; }
    return 0;
}
```

Remove this source at old physical positions 144–144 in RC42.RIL:

```rill

```

There is no replacement source.

The following old source remains in place:

```rill
fn setident(s) { let mut i = 0; while 1 { ident[i] = load8(s+i); if ident[i] == 0 { return 0; } i = i+1; } }
```

### Edit 37

Unchanged source immediately before the edit:

```rill
}

fn expect(t) { if tok != t { fail(2); } lex(); return 0; }
```

Remove this source at old physical positions 137–137 in RC42.RIL:

```rill

```

There is no replacement source.

The following old source remains in place:

```rill
fn isword(s) {
    let mut i = 0;
```

### Edit 38

Unchanged source immediately before the edit:

```rill
    }
    return 0;
}
```

Remove this source at old physical positions 135–135 in RC42.RIL:

```rill

```

There is no replacement source.

The following old source remains in place:

```rill
fn expect(t) { if tok != t { fail(2); } lex(); return 0; }
```

### Edit 39

Unchanged source immediately before the edit:

```rill
        else { return lexkind(); }
    }
}
```

Remove this source at old physical positions 80–80 in RC42.RIL:

```rill

```

There is no replacement source.

The following old source remains in place:

```rill
fn lexkind() {
    let mut n = 0;
```

### Edit 40

Unchanged source immediately before the edit:

```rill
}

fn digit(c) { if c < 48 { return 0; } if c > 57 { return 0; } return 1; }
```

Remove this source at old physical positions 67–67 in RC42.RIL:

```rill

```

There is no replacement source.

The following old source remains in place:

```rill
fn lex() {
    while 1 {
```

### Edit 41

Unchanged source immediately before the edit:

```rill
    if c >= 97 { if c <= 122 { return 1; } }
    return 0;
}
```

Remove this source at old physical positions 65–65 in RC42.RIL:

```rill

```

There is no replacement source.

The following old source remains in place:

```rill
fn digit(c) { if c < 48 { return 0; } if c > 57 { return 0; } return 1; }
```

### Edit 42

Unchanged source immediately before the edit:

```rill
    }
    return 0;
}
```

Remove this source at old physical positions 58–58 in RC42.RIL:

```rill

```

There is no replacement source.

The following old source remains in place:

```rill
fn letter(c) {
    if c == 95 { return 1; }
```

### Edit 43

Unchanged source immediately before the edit:

```rill
bytes outbuf[4096];
bytes ident[32];
bytes string[512];
```

Remove this source at old physical positions 34–36 in RC42.RIL:

```rill

fn main(){table=alloc(23680);output=create("RILL.TMP");own=1;input=open("SOURCE.RIL");if status(){fail(1);}next();lex();function();outstr("PROC MAIN 0 0\r\nINVOKE F_MAIN 0\r\nRETURN\r\n");flush();close(output);output=0;own=0;return 0;}
```

Replace it with:

```rill
fn main() {
    if exists("RILL.TMP") != 0 { fail(5); }
    if exists("RILL.BAK") != 0 { fail(5); }
    input = open("SOURCE.RIL");
    if status() != 0 { fail(1); }
    output = create("RILL.TMP");
    if status() != 0 { fail(1); }
    own = 1;
    table = alloc(23680);
    if status() != 0 { fail(5); }
    next(); lex();
    while tok != 0 {
        if isword("FN") { function(); }
        else {
            if isword("LET") { globalword(); }
            else {
                if isword("BYTES") { globalbuffer(); }
                else { fail(2); }
            }
        }
    }
    setident("MAIN");
    let mut p = find(0,globals);
    if p == 65535 { fail(4); }
    if rectype != 3 { fail(4); }
    if recval != 0 { fail(4); }
    p = 0;
    while p < globals {
        if tword(p*40+32) == 4 { fail(4); }
        p = p+1;
    }
    outstr("PROC MAIN 0 0\r\nINVOKE F_MAIN 0\r\nRETURN\r\n");
    close(input);
    if status() != 0 { fail(1); }
    flush(); close(output);
    if status() != 0 { fail(1); }
    let mut present=exists("RESULT.IR");
    if status() { fail(1); }
    if present {
        rename("RESULT.IR","RILL.BAK");
        if status() != 0 { fail(1); }
        backup = 1;
    }
    rename("RILL.TMP","RESULT.IR");
    if status() != 0 { fail(1); }
    own = 0;
    if backup {
        delete("RILL.BAK");
        if status() != 0 { fail(1); }
    }
    free(table);
    if status() != 0 { fail(1); }
    print("OK RESULT.IR ");
    print32(totalhi,total);
    print("\r\n");
    return 0;
}
```

The following old source remains in place:

```rill
fn next() {
    if ch == 10 {
```

## Build this stopping point

```dos
COPY RC43.RIL SOURCE.RIL
CHECK RILLBOOT
```

Require `OK RESULT.IR 0000049992` and PASS. Copy RESULT.IR to SOURCE.IR.

```dos
CHECK IWKEEP
COPY RESULT.ASM SOURCE.ASM
CHECK ASMAKEEP
```

Require IR86 `OK RESULT.ASM 0000103091 text bytes` and PASS **before** the copy. Require assembler `OK RESULT.COM 26617 bytes` and PASS before saving:

```dos
COPY RESULT.COM RC43.COM
```

VIEW.BAS must report RC43.COM length 26617 bytes. Keep this executable and its source together.

## Acceptance check

Create TRC43.RIL with COPY CON or a plain-text editor. Finish COPY CON with Ctrl-Z and Enter:

```rill
fn main(){putc(72);putc(73);return 0;}
```

```dos
COPY TRC43.RIL SOURCE.RIL
```

```dos
CHECK RC43
```

Require:

```text
OK RESULT.IR 0000000152
PASS
```

TYPE RESULT.IR. Its complete IR is:

```ir
PROC F_MAIN 00000 64
LIT 00072
PUSH
POP
PUTC
LIT 00073
PUSH
POP
PUTC
LIT 00000
RETURN
LIT 0
RETURN
PROC MAIN 0 0
INVOKE F_MAIN 0
RETURN
```

VIEW.BAS must show length 152 bytes. This is a complete program. Copy it to SOURCE.IR, run CHECK IWKEEP, copy the accepted RESULT.ASM to SOURCE.ASM, and run CHECK ASMAKEEP. Require OK and PASS at both steps. VIEW.BAS must report RESULT.COM length 1069. Copy that file to TRY.COM; CHECK TRY displays `HI` and reports PASS.

## A rejection or boundary check

Create XRC43.RIL:

```rill
fn main(){return 65536;}
```

```dos
COPY XRC43.RIL SOURCE.RIL
CHECK RC43
```

Require:

```text
ERROR 0000000001 CODE 00003
FAIL
```

An unexpected PASS fails the rejection. The pre-existing RESULT.IR must remain unchanged; preserve a copy before the test.

## If the result differs

Compare main with the printed addition. Check its arguments and saved state across calls, then inspect the generated text or bytes.

## Local and parameter capacity

The completed compiler now combines the record, scope, and frame routines. Create TLOCAL.RIL:

```rill
fn check(a0,a1,a2,a3,a4,a5,a6,a7,a8,a9,a10,a11,a12,a13,a14,a15){
let mut v0=0;let mut v1=1;let mut v2=2;let mut v3=3;let mut v4=4;let mut v5=5;let mut v6=6;let mut v7=7;
let mut v8=8;let mut v9=9;let mut v10=10;let mut v11=11;let mut v12=12;let mut v13=13;let mut v14=14;let mut v15=15;
let mut v16=16;let mut v17=17;let mut v18=18;let mut v19=19;let mut v20=20;let mut v21=21;let mut v22=22;let mut v23=23;
let mut v24=24;let mut v25=25;let mut v26=26;let mut v27=27;let mut v28=28;let mut v29=29;let mut v30=30;let mut v31=31;
let mut v32=32;let mut v33=33;let mut v34=34;let mut v35=35;let mut v36=36;let mut v37=37;let mut v38=38;let mut v39=39;
let mut v40=40;let mut v41=41;let mut v42=42;let mut v43=43;let mut v44=44;let mut v45=45;let mut v46=46;let mut v47=47;
let mut v48=48;let mut v49=49;let mut v50=50;let mut v51=51;let mut v52=52;let mut v53=53;let mut v54=54;let mut v55=55;
let mut v56=56;let mut v57=57;let mut v58=58;let mut v59=59;let mut v60=60;let mut v61=61;let mut v62=62;let mut v63=63;
if (v0!=0) | (v1!=1) | (v2!=2) | (v3!=3) | (v4!=4) | (v5!=5) | (v6!=6) | (v7!=7) {return 1;}
if (v8!=8) | (v9!=9) | (v10!=10) | (v11!=11) | (v12!=12) | (v13!=13) | (v14!=14) | (v15!=15) {return 1;}
if (v16!=16) | (v17!=17) | (v18!=18) | (v19!=19) | (v20!=20) | (v21!=21) | (v22!=22) | (v23!=23) {return 1;}
if (v24!=24) | (v25!=25) | (v26!=26) | (v27!=27) | (v28!=28) | (v29!=29) | (v30!=30) | (v31!=31) {return 1;}
if (v32!=32) | (v33!=33) | (v34!=34) | (v35!=35) | (v36!=36) | (v37!=37) | (v38!=38) | (v39!=39) {return 1;}
if (v40!=40) | (v41!=41) | (v42!=42) | (v43!=43) | (v44!=44) | (v45!=45) | (v46!=46) | (v47!=47) {return 1;}
if (v48!=48) | (v49!=49) | (v50!=50) | (v51!=51) | (v52!=52) | (v53!=53) | (v54!=54) | (v55!=55) {return 1;}
if (v56!=56) | (v57!=57) | (v58!=58) | (v59!=59) | (v60!=60) | (v61!=61) | (v62!=62) | (v63!=63) {return 1;}
return (a0!=0)|(a15!=15);
}
fn main(){return check(0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15);}
```

```dos
COPY TLOCAL.RIL SOURCE.RIL
CHECK RC43
COPY RESULT.IR SOURCE.IR
CHECK IWKEEP
COPY RESULT.ASM SOURCE.ASM
CHECK ASMAKEEP
COPY RESULT.COM TRY.COM
CHECK TRY
```

Require compiler `OK RESULT.IR 0000005625`, translator `OK RESULT.ASM 0000015732 text bytes`, and assembler `OK RESULT.COM 03098 bytes`, with PASS before each following copy. TRY must return zero and report PASS; it needs no display routine. VIEW.BAS must show 3098 bytes and these first thirty-two bytes:

```text
FC 81 FC FE FF 74 03 E9 C7 0B E8 1F 08 B4 4C CD 21 55 8B EC 81 EC 80 00 81 FC 00 F0 73 03 E9 B0
```

## Reject one more live local

Copy TLOCAL.RIL to XLOCAL.RIL. Just before `return (a0!=0)|(a15!=15);`, insert:

```rill
let mut extra=0;
```

```dos
COPY XLOCAL.RIL SOURCE.RIL
CHECK RC43
```

Require `ERROR 0000000018 CODE 00005` and FAIL. The accepted RESULT.IR must remain unchanged; keep a copy for comparison before this check.

## Reusing local slots

Create TSCOPE.RIL using the following skeleton. At each comment, copy the eight declaration lines for v0 through v63 from TLOCAL.RIL; the comments are placement markers. There are two sibling scopes, each filling all sixty-four slots.

```rill
let mut result=0;
 fn reuse(){
 {
 // Copy the eight declaration lines here.
 v63=17;result=result+v63;
 }
 {
 // Copy the same eight declaration lines here.
 v63=29;result=result+v63;
 }
 return 0;
 }
 fn main(){
 let mut v63=7;
 {let mut v63=9;if v63!=9{return 1;}}
 reuse();
 return (result!=46)|(v63!=7);
 }
```

The complete disk source has the declarations in place. It checks both slot reuse between sibling scopes and restoration of an outer binding after a shadowing block.

```dos
COPY TSCOPE.RIL SOURCE.RIL
CHECK RC43
COPY RESULT.IR SOURCE.IR
CHECK IWKEEP
COPY RESULT.ASM SOURCE.ASM
CHECK ASMAKEEP
COPY RESULT.COM TRY.COM
CHECK TRY
```

Require compiler `OK RESULT.IR 0000004080`, translator `OK RESULT.ASM 0000010171 text bytes`, and assembler `OK RESULT.COM 02133 bytes`, with PASS before each following copy. TRY must return zero and report PASS; it needs no display routine. VIEW.BAS must show 2133 bytes and these first thirty-two bytes:

```text
FC 81 FC FE FF 74 03 E9 02 08 E8 5A 04 B4 4C CD 21 00 00 55 8B EC 81 EC 80 00 81 FC 00 F0 73 03
```


Preserve RC43.COM as RBOOT.COM and RC43.RIL as RILL.RIL. The self-build exercise uses that source to establish R0 with the RILL frame convention, then compares R0, R1 and R2.
