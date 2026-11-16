+++
title = "38 \u00b7 Compiling a Byte Buffer"
weight = 38
description = "Declare a nonempty global byte extent."
download = "RC38.RIL"
download_group = "tools/rill"
aliases = ["/bootstrap/rill/126-rc-compile-a-byte-extent/"]
reader_names = 1
url = "/bootstrap/rc/126-rc-compile-a-byte-extent/"
+++

## The working parts

Declare a nonempty global byte extent. The buffer is materialized in the COM image. Extra allocated blocks are a different service and are not pointers into this declaration.

## Enter the source

Copy RC37.RIL to RC38.RIL. Apply edits **from the bottom of the old file upward**. Physical positions refer to that unchanged old file; use the printed context to identify each place. Keep all other source.

### Edit 1

Unchanged source immediately before the edit:

```rill
    lex(); expect(59); return 0;
}
```

Insert after old physical line 263.

Insert:

```rill
fn globalbuffer() {
    lex(); if tok != 1 { fail(2); } if lookglobal() != 65535 { fail(4); }
    recval = 0; reclevel = 0;
    let mut p = newglobal(2);
    lex(); expect(91); if tok != 2 { fail(2); } if value == 0 { fail(5); }
    outstr("BUFFER V_"); outname(p); outchar(32); outnum(value); newline();
    lex(); expect(93); expect(59); return 0;
}
```

The following old source remains in place:

```rill
fn builtin() {
    let mut p = "PUTC\01\0POP\nPUTC\0STATUS\00\0STATUS\0OPEN\01\0POP\nOPEN\0CREATE\01\0POP\nCREATE\0CLOSE\01\0POP\nCLOSE\0READ\03\0POP\nREAD\0WRITE\03\0POP\nWRITE\0EXISTS\01\0POP\nEXISTS\0DELETE\01\0POP\nDELETE\0RENAME\02\0POP\nRENAME\0ALLOC\01\0POP\nALLOC\0FREE\01\0POP\nFREEBLOCK\0GET8\02\0POP\nGET8\0GET16\02\0POP\nGET16\0SET8\03\0POP\nSET8\0SET16\03\0POP\nSET16\0LOAD8\01\0POP\nFETCHB\0LOAD16\01\0POP\nFETCH\0STORE8\02\0POP\nPUTB\0STORE16\02\0POP\nPUT\0EXIT\01\0POP\nEXIT\0ARGC\00\0ARGC\0ARG\01\0POP\nARG\0\0";
```

### Edit 2

Unchanged source immediately before the edit:

```rill
bytes ident[32];
bytes string[512];
```

Remove this source at old physical positions 35–35 in RC37.RIL:

```rill
fn main(){filearg(1,"SOURCE.RIL");table=alloc(23680);output=create(filearg(2,"RILL.TMP"));own=1;input=open(filearg(1,"SOURCE.RIL"));if status(){fail(1);}next();lex();globalword();flush();close(output);output=0;own=0;return 0;}
```

Replace it with:

```rill
fn main(){filearg(1,"SOURCE.RIL");table=alloc(23680);output=create(filearg(2,"RILL.TMP"));own=1;input=open(filearg(1,"SOURCE.RIL"));if status(){fail(1);}next();lex();globalbuffer();flush();close(output);output=0;own=0;return 0;}
```

The following old source remains in place:

```rill

fn next() {
```

## Build this stopping point

```dos
CHECK RILLBOOT RC38.RIL RESULT.IR
```

Require `OK RESULT.IR 0000039401` and PASS. Pass RESULT.IR directly to the translator.

```dos
CHECK IWKEEP SOURCE.IR RESULT.ASM
CHECK ASMAKEEP RESULT.ASM RESULT.COM
```

Require IR86 `OK RESULT.ASM 0000084542 text bytes` and PASS **before** the copy. Require assembler `OK RESULT.COM 23500 bytes` and PASS before saving:

```dos
COPY RESULT.COM RC38.COM
```

VIEW.BAS must report RC38.COM length 23500 bytes. Keep this executable and its source together.

## Acceptance check

Create TRC38.RIL with COPY CON or a plain-text editor. Finish COPY CON with Ctrl-Z and Enter:

```rill
bytes abc[8];
```

```dos
CHECK RC38 TRC38.RIL RESULT.IR
```

The checker must report PASS. Inspect the emitted file below.

Use VIEW.BAS to inspect RESULT.IR. Require length 20 bytes. The complete bytes must be:

```text
42 55 46 46 45 52 20 56 5F 41 42 43 20 30 30 30
30 38 0D 0A
```

This is an IR fragment for inspection. Do not translate it as a complete program or execute any file with its name.

## A rejection or boundary check

Create XRC38.RIL:

```rill
bytes abc[0];
```

```dos
CHECK RC38 XRC38.RIL RESULT.IR
```

Require:

```text
ERROR 0000000001 CODE 00005
FAIL
```

An unexpected PASS fails the rejection. The pre-existing RESULT.IR must remain unchanged; preserve a copy before the test.

## If the result differs

Compare globalbuffer with the printed addition. Check its arguments and saved state across calls, then inspect the generated text or bytes.
