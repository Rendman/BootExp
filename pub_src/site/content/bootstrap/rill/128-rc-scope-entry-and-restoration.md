+++
title = "RC40 \u00b7 Scope entry and restoration"
weight = 128
description = "Save the active local-name count and next local slot at entry."
download = "RC40.RIL"
download_group = "toolchain"
cartoon = "rill-drawers.png"
+++

Save the active local-name count and next local slot at entry.

## The working parts

Save the active local-name count and next local slot at entry. Restore both at the closing brace. This permits a nested binding to shadow an outer one without permanently consuming its name or slot.

The entry diagnostic exercises the printed helper. Rejecting placeholders identify forms outside this stopping point. A diagnostic that emits only an IR fragment is inspected as text; it is not a complete compiler or output program.

## Enter the source

Copy RC39.RIL to RC40.RIL. Apply edits **from the bottom of the old file upward**. Physical positions refer to that unchanged old file; use the printed context to identify each place. Keep all other source.

### Edit 1

Unchanged source immediately before the edit:

```rill
    lex(); expect(61); expr(1); set16(table,p+32,5);
    outstr("SETLOCAL "); outnum(slot); newline(); expect(59); return 0;
}
```

Insert after old physical line 282.

Insert:

```rill

fn statement(){fail(2);return 0;}
```

The following old source remains in place:

```rill

fn builtin() {
```

### Edit 2

Unchanged source immediately before the edit:

```rill
    lex(); expect(93); expect(59); return 0;
}
```

Insert after old physical line 272.

Insert:

```rill
fn block() {
    let mut oldcount = localcount;
    let mut oldnext = nextlocal;
    level = level+1; if level > 16 { fail(5); }
    expect(123);
    while tok != 125 { if tok == 0 { fail(2); } statement(); }
    lex(); localcount = oldcount; nextlocal = oldnext; level = level-1; return 0;
}
```

The following old source remains in place:

```rill
fn declare() {
    lex(); if !isword("MUT") { fail(2); } lex(); if tok != 1 { fail(2); }
```

### Edit 3

Unchanged source immediately before the edit:

```rill
bytes ident[32];
bytes string[512];
```

Remove this source at old physical positions 35–35 in RC39.RIL:

```rill
fn main(){table=alloc(22000);output=create("RILL.TMP");own=1;input=open("SOURCE.RIL");if status(){fail(1);}next();lex();level=1;declare();flush();close(output);output=0;own=0;print("OK RILL.TMP\r\n");return 0;}
```

Replace it with:

```rill
fn main(){table=alloc(22000);output=create("RILL.TMP");own=1;input=open("SOURCE.RIL");if status(){fail(1);}next();lex();block();flush();close(output);output=0;own=0;print("OK RILL.TMP\r\n");return 0;}
```

The following old source remains in place:

```rill

fn next() {
```

## Build this stopping point

```dos
COPY RC40.RIL SOURCE.RIL
CHECK RILLBOOT
```

Require `OK RESULT.IR 0000040044` and PASS. Copy RESULT.IR to SOURCE.IR.

```dos
CHECK IWKEEP
COPY RESULT.ASM SOURCE.ASM
CHECK ASMAKEEP
```

Require IR86 `OK RESULT.ASM 0000083529 text bytes` and PASS **before** the copy. Require assembler `OK RESULT.COM 23330 bytes` and PASS before saving:

```dos
COPY RESULT.COM RC40.COM
```

VIEW.BAS must report RC40.COM length 23330 bytes. Keep this executable and its source together.

## Acceptance check

Create TRC40.RIL with COPY CON or a plain-text editor. Finish COPY CON with Ctrl-Z and Enter:

```rill
{}
```

```dos
COPY TRC40.RIL SOURCE.RIL
```

```dos
CHECK RC40
```

Require, apart from command echo and the checker's separator:

```text
OK RILL.TMP
PASS
```

TYPE RILL.TMP. Its complete text is:

```ir

```

VIEW.BAS must show length 0 bytes. For an empty fragment, length zero is the expected visible result. This is an IR fragment for inspection. Do not translate it as a complete program or execute any file with its name.

After inspection, delete this deliberately created RILL.TMP before another checkpoint. The file is diagnostic text, not an interrupted accepted compiler build.

## A rejection or boundary check

Create XRC40.RIL:

```rill
{putc(65);}
```

```dos
COPY XRC40.RIL SOURCE.RIL
CHECK RC40
```

Require:

```text
ERROR 0000000001 CODE 00002
FAIL
```

An unexpected PASS fails the rejection. The pre-existing RESULT.IR must remain unchanged; preserve a copy before the test.

## If the result differs

Check the saved pointer or slot, argument order, complete token spelling, and STATUS immediately after each service. A helper's local state must survive calls; an output count is independent of input position. Inspect text and file length before interpreting any bytes as a program.
