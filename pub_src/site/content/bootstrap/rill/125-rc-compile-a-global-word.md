+++
title = "37 \u00b7 Compiling a Global Variable"
weight = 37
description = "A global mutable word has a literal initializer and a stable V_ name."
download = "RC37.RIL"
download_group = "tools/rill"
aliases = ["/bootstrap/rill/125-rc-compile-a-global-word/"]
reader_names = 1
url = "/bootstrap/rc/125-rc-compile-a-global-word/"
+++

## The working parts

A global mutable word has a literal initializer and a stable V_ name. Reject duplicates before emitting its declaration.

## Enter the source

Copy RC36.RIL to RC37.RIL. Apply edits **from the bottom of the old file upward**. Physical positions refer to that unchanged old file; use the printed context to identify each place. Keep all other source.

### Edit 1

Unchanged source immediately before the edit:

```rill
    return 0;
}
```

Insert after old physical line 253.

Insert:

```rill
fn globalword() {
    lex(); if !isword("MUT") { fail(2); } lex(); if tok != 1 { fail(2); }
    if lookglobal() != 65535 { fail(4); }
    recval = 0; reclevel = 0;
    let mut p = newglobal(1);
    lex(); expect(61); if tok != 2 { fail(2); }
    outstr("WORD V_"); outname(p); outchar(32); outnum(value); newline();
    lex(); expect(59); return 0;
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

Remove this source at old physical positions 35–35 in RC36.RIL:

```rill
fn main(){table=alloc(23680);setident("ABC");rectype=1;recval=12345;reclevel=0;record(0);globals=1;output=create("RILL.TMP");own=1;input=open("SOURCE.RIL");if status(){fail(1);}next();lex();expr(1);if tok!=0{fail(2);}flush();close(output);output=0;own=0;return 0;}
```

Replace it with:

```rill
fn main(){table=alloc(23680);output=create("RILL.TMP");own=1;input=open("SOURCE.RIL");if status(){fail(1);}next();lex();globalword();flush();close(output);output=0;own=0;return 0;}
```

The following old source remains in place:

```rill

fn next() {
```

## Build this stopping point

```dos
COPY RC37.RIL SOURCE.RIL
CHECK RILLBOOT
```

Require `OK RESULT.IR 0000036723` and PASS. Copy RESULT.IR to SOURCE.IR.

```dos
CHECK IWKEEP
COPY RESULT.ASM SOURCE.ASM
CHECK ASMAKEEP
```

Require IR86 `OK RESULT.ASM 0000077613 text bytes` and PASS **before** the copy. Require assembler `OK RESULT.COM 22221 bytes` and PASS before saving:

```dos
COPY RESULT.COM RC37.COM
```

VIEW.BAS must report RC37.COM length 22221 bytes. Keep this executable and its source together.

## Acceptance check

Create TRC37.RIL with COPY CON or a plain-text editor. Finish COPY CON with Ctrl-Z and Enter:

```rill
let mut abc=65;
```

```dos
COPY TRC37.RIL SOURCE.RIL
```

```dos
CHECK RC37
```

The checker must report PASS. Inspect the emitted file below.

Use VIEW.BAS to inspect RILL.TMP. Require length 18 bytes. The complete bytes must be:

```text
57 4F 52 44 20 56 5F 41 42 43 20 30 30 30 36 35
0D 0A
```

This is an IR fragment for inspection. Do not translate it as a complete program or execute any file with its name.

After inspection, delete this deliberately created RILL.TMP before another checkpoint. The file is diagnostic text, not an interrupted accepted compiler build.

## A rejection or boundary check

Create XRC37.RIL:

```rill
let abc=65;
```

```dos
COPY XRC37.RIL SOURCE.RIL
CHECK RC37
```

Require:

```text
ERROR 0000000001 CODE 00002
FAIL
```

An unexpected PASS fails the rejection. The pre-existing RESULT.IR must remain unchanged; preserve a copy before the test.

## If the result differs

Compare globalword with the printed addition. Check its arguments and saved state across calls, then inspect the generated text or bytes.
