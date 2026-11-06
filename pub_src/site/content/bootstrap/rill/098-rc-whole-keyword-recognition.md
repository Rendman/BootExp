+++
title = "RC10 \u00b7 Whole-keyword recognition"
weight = 98
description = "Check the token class and every character through the zero terminator."
download = "RC10.RIL"
download_group = "toolchain"
+++

Check the token class and every character through the zero terminator.

## The working parts

Check the token class and every character through the zero terminator. A keyword prefix is insufficient: FN and FNN are different spellings.

The entry diagnostic exercises the printed helper. Rejecting placeholders identify forms outside this stopping point. A diagnostic that emits only an IR fragment is inspected as text; it is not a complete compiler or output program.

## Enter the source

Copy RC09.RIL to RC10.RIL. Apply edits **from the bottom of the old file upward**. Physical positions refer to that unchanged old file; use the printed context to identify each place. Keep all other source.

### Edit 1

Unchanged source immediately before the edit:

```rill

fn expect(t) { if tok != t { fail(2); } lex(); return 0; }
```

Insert after old physical line 137.

Insert:

```rill
fn isword(s) {
    let mut i = 0;
    if tok != 1 { return 0; }
    while ident[i] == load8(s+i) { if ident[i] == 0 { return 1; } i = i+1; }
    return 0;
}
```

The following old source remains in place:

```rill
fn print(s) { let mut c = 0; while 1 { c = load8(s); if c == 0 { return 0; } putc(c); s = s+1; } }
```

### Edit 2

Unchanged source immediately before the edit:

```rill
bytes ident[32];
bytes string[512];
```

Remove this source at old physical positions 35–35 in RC09.RIL:

```rill
fn main(){input=open("SOURCE.RIL");if status(){fail(1);}next();lex();expect(43);print("OK");return 0;}
```

Replace it with:

```rill
fn main(){input=open("SOURCE.RIL");if status(){fail(1);}next();lex();printnum(isword("FN"));return 0;}
```

The following old source remains in place:

```rill

fn next() {
```

## Build this stopping point

```dos
COPY RC10.RIL SOURCE.RIL
CHECK RILLBOOT
```

Require `OK RESULT.IR 0000014174` and PASS. Copy RESULT.IR to SOURCE.IR.

```dos
CHECK IWKEEP
COPY RESULT.ASM SOURCE.ASM
CHECK ASMAKEEP
```

Require IR86 `OK RESULT.ASM 0000031042 text bytes` and PASS **before** the copy. Require assembler `OK RESULT.COM 14374 bytes` and PASS before saving:

```dos
COPY RESULT.COM RC10.COM
```

VIEW.BAS must report RC10.COM length 14374 bytes. Keep this executable and its source together.

## Acceptance check

Create TRC10.RIL with COPY CON or a plain-text editor. Finish COPY CON with Ctrl-Z and Enter:

```rill
fn
```

```dos
COPY TRC10.RIL SOURCE.RIL
```

```dos
CHECK RC10
```

Require, apart from command echo and the checker's separator:

```text
00001PASS
```

## A rejection or boundary check

Rename SOURCE.RIL to an unused HOLD.RIL and run CHECK RC10. Restore the source afterward.

Require:

```text
ERROR 0000000001 CODE 00001
FAIL
```

An unexpected PASS fails the rejection. The pre-existing RESULT.IR must remain unchanged; preserve a copy before the test.

## If the result differs

Check the saved pointer or slot, argument order, complete token spelling, and STATUS immediately after each service. A helper's local state must survive calls; an output count is independent of input position. Inspect text and file length before interpreting any bytes as a program.
