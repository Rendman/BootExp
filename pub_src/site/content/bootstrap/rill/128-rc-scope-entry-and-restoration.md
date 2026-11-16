+++
title = "40 \u00b7 Remembering Which Names Are Visible"
weight = 40
description = "Save the active local-name count and next local slot at entry."
download = "RC40.RIL"
download_group = "tools/rill"
cartoon = "rill-drawers.png"
aliases = ["/bootstrap/rill/128-rc-scope-entry-and-restoration/"]
reader_names = 1
url = "/bootstrap/rc/128-rc-scope-entry-and-restoration/"
+++

## The working parts

Save the active local-name count and next local slot at entry. Restore both at the closing brace. This permits a nested binding to shadow an outer one without permanently consuming its name or slot.

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
fn main(){filearg(1,"SOURCE.RIL");table=alloc(23680);output=create(filearg(2,"RILL.TMP"));own=1;input=open(filearg(1,"SOURCE.RIL"));if status(){fail(1);}next();lex();level=1;declare();flush();close(output);output=0;own=0;return 0;}
```

Replace it with:

```rill
fn main(){filearg(1,"SOURCE.RIL");table=alloc(23680);output=create(filearg(2,"RILL.TMP"));own=1;input=open(filearg(1,"SOURCE.RIL"));if status(){fail(1);}next();lex();block();flush();close(output);output=0;own=0;return 0;}
```

The following old source remains in place:

```rill

fn next() {
```

## Build this stopping point

```dos
CHECK RILLBOOT RC40.RIL RESULT.IR
```

Require `OK RESULT.IR 0000041625` and PASS. Pass RESULT.IR directly to the translator.

```dos
CHECK IWKEEP SOURCE.IR RESULT.ASM
CHECK ASMAKEEP RESULT.ASM RESULT.COM
```

Require IR86 `OK RESULT.ASM 0000088530 text bytes` and PASS **before** the copy. Require assembler `OK RESULT.COM 24225 bytes` and PASS before saving:

```dos
COPY RESULT.COM RC40.COM
```

VIEW.BAS must report RC40.COM length 24225 bytes. Keep this executable and its source together.

## Acceptance check

Create TRC40.RIL with COPY CON or a plain-text editor. Finish COPY CON with Ctrl-Z and Enter:

```rill
{}
```

```dos
CHECK RC40 TRC40.RIL RESULT.IR
```

The checker must report PASS. Inspect the emitted file below.

Use VIEW.BAS to inspect RESULT.IR. Require length 0 bytes. An empty file is the expected result.

This is an IR fragment for inspection. Do not translate it as a complete program or execute any file with its name.

## A rejection or boundary check

Create XRC40.RIL:

```rill
{putc(65);}
```

```dos
CHECK RC40 XRC40.RIL RESULT.IR
```

Require:

```text
ERROR 0000000001 CODE 00002
FAIL
```

An unexpected PASS fails the rejection. The pre-existing RESULT.IR must remain unchanged; preserve a copy before the test.

## If the result differs

Check the saved name count and next local slot at block entry and restoration at its closing brace.
