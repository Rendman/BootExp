+++
title = "42 \u00b7 Compiling a Procedure"
weight = 42
description = "Record the procedure name before scanning parameters, verify any earlier call arity, and create parameter bindings."
download = "RC42.RIL"
download_group = "tools/rill"
aliases = ["/bootstrap/rill/130-rc-compile-a-complete-procedure/", "/bootstrap/rc/134-more-local-storage/"]
reader_names = 1
url = "/bootstrap/rc/130-rc-compile-a-complete-procedure/"
+++

## The working parts

Record the procedure name before scanning parameters, verify any earlier call arity, and create parameter bindings. Each procedure accepts at most sixteen parameters. PROC reserves sixty-four local words, matching the declaration routine and IR86 frame bound. Those 128 local bytes are reserved on every call, even when fewer slots are used; parameters, return state and expression temporaries need additional stack space. The native stack guard still applies. Every normal fall-through ends with return value zero.

## Enter the source

Copy RC41.RIL to RC42.RIL. Apply edits **from the bottom of the old file upward**. Physical positions refer to that unchanged old file; use the printed context to identify each place. Keep all other source.

### Edit 1

Unchanged source immediately before the edit:

```rill
    lex(); expect(93); expect(59); return 0;
}
```

Insert after old physical line 272.

Insert:

```rill
fn function() {
    lex(); if tok != 1 { fail(2); }
    let mut p = lookglobal();
    if p == 65535 { recval = 65535; reclevel = 0; p = newglobal(4); }
    else { if rectype != 4 { fail(4); } }
    let mut oldargs = tword(p+34);
    set16(table,p+32,3);
    localcount = 0; nextlocal = 0; level = 0;
    let mut argc = 0;
    lex(); expect(40);
    while tok != 41 {
        if tok != 1 { fail(2); }
        if find(20480,localcount) != 65535 { fail(4); }
        if argc >= 16 { fail(5); }
        recval = argc; reclevel = 0; newlocal(6); argc = argc+1;
        lex(); if tok != 41 { expect(44); }
    }
    if oldargs != 65535 { if oldargs != argc { fail(4); } }
    set16(table,p+34,argc);
    outstr("PROC F_"); outname(p); outchar(32); outnum(argc); outstr(" 64\r\n");
    lex(); block(); outstr("LIT 0\r\nRETURN\r\n"); return 0;
}
```

The following old source remains in place:

```rill
fn block() {
    let mut oldcount = localcount;
```

### Edit 2

Unchanged source immediately before the edit:

```rill
bytes ident[32];
bytes string[512];
```

Remove this source at old physical positions 35–35 in RC41.RIL:

```rill
fn main(){table=alloc(23680);output=create("RILL.TMP");own=1;input=open("SOURCE.RIL");if status(){fail(1);}next();lex();outstr("PROC MAIN 0 64\r\n");block();outstr("LIT 0\r\nRETURN\r\n");flush();close(output);output=0;own=0;return 0;}
```

Replace it with:

```rill
fn main(){table=alloc(23680);output=create("RILL.TMP");own=1;input=open("SOURCE.RIL");if status(){fail(1);}next();lex();function();outstr("PROC MAIN 0 0\r\nINVOKE F_MAIN 0\r\nRETURN\r\n");flush();close(output);output=0;own=0;return 0;}
```

The following old source remains in place:

```rill

fn next() {
```

## Build this stopping point

```dos
COPY RC42.RIL SOURCE.RIL
CHECK RILLBOOT
```

Require `OK RESULT.IR 0000046660` and PASS. Copy RESULT.IR to SOURCE.IR.

```dos
CHECK IWKEEP
COPY RESULT.ASM SOURCE.ASM
CHECK ASMAKEEP
```

Require IR86 `OK RESULT.ASM 0000096277 text bytes` and PASS **before** the copy. Require assembler `OK RESULT.COM 25486 bytes` and PASS before saving:

```dos
COPY RESULT.COM RC42.COM
```

VIEW.BAS must report RC42.COM length 25486 bytes. Keep this executable and its source together.

## Acceptance check

Create TRC42.RIL with COPY CON or a plain-text editor. Finish COPY CON with Ctrl-Z and Enter:

```rill
fn main(){putc(65);return 0;}
```

```dos
COPY TRC42.RIL SOURCE.RIL
```

```dos
CHECK RC42
```

The checker must report PASS. Inspect the emitted file below.

TYPE RILL.TMP. Its complete IR is:

```ir
PROC F_MAIN 00000 64
LIT 00065
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

VIEW.BAS must show length 124 bytes. This is a complete program. Copy it to SOURCE.IR, run CHECK IWKEEP, copy the accepted RESULT.ASM to SOURCE.ASM, and run CHECK ASMAKEEP. Require OK and PASS at both steps. VIEW.BAS must report RESULT.COM length 1061. Copy that file to TRY.COM; CHECK TRY displays `A` and reports PASS.

After inspection, delete this deliberately created RILL.TMP before another checkpoint. The file is diagnostic text, not an interrupted accepted compiler build.

## A rejection or boundary check

Create XRC42.RIL:

```rill
fn main(a,a){}
```

```dos
COPY XRC42.RIL SOURCE.RIL
CHECK RC42
```

Require:

```text
ERROR 0000000001 CODE 00004
FAIL
```

An unexpected PASS fails the rejection. The pre-existing RESULT.IR must remain unchanged; preserve a copy before the test.

## If the result differs

Compare function with the printed addition. Check its arguments and saved state across calls, then inspect the generated text or bytes.
