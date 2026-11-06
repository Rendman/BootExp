+++
title = "RC36 \u00b7 Calls inside expressions"
weight = 36
description = "Evaluate arguments from left to right and save each emitted result."
download = "RC36.RIL"
download_group = "rc"
aliases = ["/bootstrap/rill/124-rc-calls-inside-expressions/"]
+++

Evaluate arguments from left to right and save each emitted result.

## The working parts

Evaluate arguments from left to right and save each emitted result. Check the complete argument count against the intrinsic or procedure record. INVOKE consumes precisely those words and preserves older expression operands.

The entry diagnostic exercises the printed helper. Rejecting placeholders identify forms outside this stopping point. A diagnostic that emits only an IR fragment is inspected as text; it is not a complete compiler or output program.

## Enter the source

Copy RC35.RIL to RC36.RIL. Apply edits **from the bottom of the old file upward**. Physical positions refer to that unchanged old file; use the printed context to identify each place. Keep all other source.

### Edit 1

Unchanged source immediately before the edit:

```rill
    recval = 65535; reclevel = 0; p = newglobal(4); rectype = 4; return p;
}
```

Remove this source at old physical positions 277–277 in RC35.RIL:

```rill
fn callargs(p,bi){fail(2);return 0;}
```

Replace it with:

```rill
fn callargs(p,bi) {
    let mut argc = 0; let mut kind = 0; let mut wanted = 0;
    expect(40);
    while tok != 41 {
        if argc >= 16 { fail(5); } expr(1); outstr("PUSH\r\n"); argc = argc+1;
        if tok != 41 { expect(44); }
    }
    lex();
    if bi {
        if load8(bi-2)-48 != argc { fail(4); }
        outstr(bi); newline(); return 0;
    }
    kind = tword(p+32); if kind != 3 { if kind != 4 { fail(4); } }
    wanted = tword(p+34);
    if wanted == 65535 { set16(table,p+34,argc); }
    else { if wanted != argc { fail(4); } }
    outstr("INVOKE F_"); outname(p); outchar(32); outnum(argc); newline(); return 0;
}
```

The following old source remains in place:

```rill

fn prec() {
```

## Build this stopping point

```dos
COPY RC36.RIL SOURCE.RIL
CHECK RILLBOOT
```

Require `OK RESULT.IR 0000036000` and PASS. Copy RESULT.IR to SOURCE.IR.

```dos
CHECK IWKEEP
COPY RESULT.ASM SOURCE.ASM
CHECK ASMAKEEP
```

Require IR86 `OK RESULT.ASM 0000076405 text bytes` and PASS **before** the copy. Require assembler `OK RESULT.COM 22014 bytes` and PASS before saving:

```dos
COPY RESULT.COM RC36.COM
```

VIEW.BAS must report RC36.COM length 22014 bytes. Keep this executable and its source together.

## Acceptance check

Create TRC36.RIL with COPY CON or a plain-text editor. Finish COPY CON with Ctrl-Z and Enter:

```rill
putc(65)
```

```dos
COPY TRC36.RIL SOURCE.RIL
```

```dos
CHECK RC36
```

Require, apart from command echo and the checker's separator:

```text
OK RILL.TMP
PASS
```

TYPE RILL.TMP. Its complete text is:

```ir
LIT 00065
PUSH
POP
PUTC
```

VIEW.BAS must show length 28 bytes. This is an IR fragment for inspection. Do not translate it as a complete program or execute any file with its name.

After inspection, delete this deliberately created RILL.TMP before another checkpoint. The file is diagnostic text, not an interrupted accepted compiler build.

## A rejection or boundary check

Create XRC36.RIL:

```rill
get8(1)
```

```dos
COPY XRC36.RIL SOURCE.RIL
CHECK RC36
```

Require:

```text
ERROR 0000000001 CODE 00004
FAIL
```

An unexpected PASS fails the rejection. The pre-existing RESULT.IR must remain unchanged; preserve a copy before the test.

## If the result differs

Check the saved pointer or slot, argument order, complete token spelling, and STATUS immediately after each service. A helper's local state must survive calls; an output count is independent of input position. Inspect text and file length before interpreting any bytes as a program.
