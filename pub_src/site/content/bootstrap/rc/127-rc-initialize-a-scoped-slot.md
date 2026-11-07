+++
title = "39 \u00b7 Initializing a Local Variable"
weight = 39
description = "Allocate a local slot and record its lexical level."
download = "RC39.RIL"
download_group = "tools/rill"
aliases = ["/bootstrap/rill/127-rc-initialize-a-scoped-slot/"]
reader_names = 1
+++

## The working parts

Allocate a local slot and record its lexical level. Mark it unavailable during its own initializer, then publish the binding after acceptance. Save its slot across recursive expression parsing. Slot numbers run from zero through sixty-three; the sixty-fifth live local is a capacity error.

## Enter the source

Copy RC38.RIL to RC39.RIL. Apply edits **from the bottom of the old file upward**. Physical positions refer to that unchanged old file; use the printed context to identify each place. Keep all other source.

### Edit 1

Unchanged source immediately before the edit:

```rill
    lex(); expect(93); expect(59); return 0;
}
```

Insert after old physical line 272.

Insert:

```rill
fn declare() {
    lex(); if !isword("MUT") { fail(2); } lex(); if tok != 1 { fail(2); }
    let mut old = find(20480,localcount);
    if old != 65535 { if reclevel == level { fail(4); } }
    if nextlocal >= 64 { fail(5); }
    let mut slot = nextlocal;
    recval = slot; reclevel = level; let mut p = newlocal(8); nextlocal = nextlocal+1;
    lex(); expect(61); expr(1); set16(table,p+32,5);
    outstr("SETLOCAL "); outnum(slot); newline(); expect(59); return 0;
}
```

The following old source remains in place:

```rill
fn builtin() {
    let mut p = "PUTC\01\0POP\nPUTC\0STATUS\00\0STATUS\0OPEN\01\0POP\nOPEN\0CREATE\01\0POP\nCREATE\0CLOSE\01\0POP\nCLOSE\0READ\03\0POP\nREAD\0WRITE\03\0POP\nWRITE\0EXISTS\01\0POP\nEXISTS\0DELETE\01\0POP\nDELETE\0RENAME\02\0POP\nRENAME\0ALLOC\01\0POP\nALLOC\0FREE\01\0POP\nFREEBLOCK\0GET8\02\0POP\nGET8\0GET16\02\0POP\nGET16\0SET8\03\0POP\nSET8\0SET16\03\0POP\nSET16\0LOAD8\01\0POP\nFETCHB\0LOAD16\01\0POP\nFETCH\0STORE8\02\0POP\nPUTB\0STORE16\02\0POP\nPUT\0EXIT\01\0POP\nEXIT\0\0";
```

### Edit 2

Unchanged source immediately before the edit:

```rill
bytes ident[32];
bytes string[512];
```

Remove this source at old physical positions 35–35 in RC38.RIL:

```rill
fn main(){table=alloc(23680);output=create("RILL.TMP");own=1;input=open("SOURCE.RIL");if status(){fail(1);}next();lex();globalbuffer();flush();close(output);output=0;own=0;return 0;}
```

Replace it with:

```rill
fn main(){table=alloc(23680);output=create("RILL.TMP");own=1;input=open("SOURCE.RIL");if status(){fail(1);}next();lex();level=1;declare();flush();close(output);output=0;own=0;return 0;}
```

The following old source remains in place:

```rill

fn next() {
```

## Build this stopping point

```dos
COPY RC39.RIL SOURCE.RIL
CHECK RILLBOOT
```

Require `OK RESULT.IR 0000039231` and PASS. Copy RESULT.IR to SOURCE.IR.

```dos
CHECK IWKEEP
COPY RESULT.ASM SOURCE.ASM
CHECK ASMAKEEP
```

Require IR86 `OK RESULT.ASM 0000082004 text bytes` and PASS **before** the copy. Require assembler `OK RESULT.COM 23023 bytes` and PASS before saving:

```dos
COPY RESULT.COM RC39.COM
```

VIEW.BAS must report RC39.COM length 23023 bytes. Keep this executable and its source together.

## Acceptance check

Create TRC39.RIL with COPY CON or a plain-text editor. Finish COPY CON with Ctrl-Z and Enter:

```rill
let mut x=7;
```

```dos
COPY TRC39.RIL SOURCE.RIL
```

```dos
CHECK RC39
```

The checker must report PASS. Inspect the emitted file below.

Use VIEW.BAS to inspect RILL.TMP. Require length 27 bytes. The complete bytes must be:

```text
4C 49 54 20 30 30 30 30 37 0D 0A 53 45 54 4C 4F
43 41 4C 20 30 30 30 30 30 0D 0A
```

This is an IR fragment for inspection. Do not translate it as a complete program or execute any file with its name.

After inspection, delete this deliberately created RILL.TMP before another checkpoint. The file is diagnostic text, not an interrupted accepted compiler build.

## A rejection or boundary check

Create XRC39.RIL:

```rill
let mut x=x;
```

```dos
COPY XRC39.RIL SOURCE.RIL
CHECK RC39
```

Require:

```text
ERROR 0000000001 CODE 00004
FAIL
```

An unexpected PASS fails the rejection. The pre-existing RESULT.IR must remain unchanged; preserve a copy before the test.

## If the result differs

Compare declare with the printed addition. Check its arguments and saved state across calls, then inspect the generated text or bytes.
