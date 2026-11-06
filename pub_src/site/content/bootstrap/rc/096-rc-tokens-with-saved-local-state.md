+++
title = "RC08 \u00b7 Tokens with saved local state"
weight = 8
description = "Keep source position, token kind, numeric value, and complete spelling distinct."
download = "RC08.RIL"
download_group = "rc"
aliases = ["/bootstrap/rill/096-rc-tokens-with-saved-local-state/"]
+++

Keep source position, token kind, numeric value, and complete spelling distinct.

## The working parts

Keep source position, token kind, numeric value, and complete spelling distinct. Save temporary values in local slots across NEXT calls. Paired punctuation is recognized before returning a single character; comments consume source without manufacturing a token.

The entry diagnostic exercises the printed helper. Rejecting placeholders identify forms outside this stopping point. A diagnostic that emits only an IR fragment is inspected as text; it is not a complete compiler or output program.

## Enter the source

Copy RC07.RIL to RC08.RIL. Apply edits **from the bottom of the old file upward**. Physical positions refer to that unchanged old file; use the printed context to identify each place. Keep all other source.

### Edit 1

Unchanged source immediately before the edit:

```rill
}

fn digit(c) { if c < 48 { return 0; } if c > 57 { return 0; } return 1; }
```

Insert after old physical line 66.

Insert:

```rill

fn lex() {
    while 1 {
        while (ch!=0) & (ch<=32) { next(); }
        if ch==0 { tok=0; return 0; }
        if ch==47 {
            next();
            if ch==47 { while (ch!=0) & (ch!=10) { next(); } }
            else { tok=47; return 0; }
        }
        else { return lexkind(); }
    }
}

fn lexkind() {
    let mut n = 0;
    let mut c = 0;
    let mut escaped = 0;
    if letter(ch) {
        while letter(ch) | digit(ch) {
            if n >= 24 { fail(4); }
            c = ch;
            if c >= 97 { if c <= 122 { c = c-32; } }
            ident[n] = c; n = n+1; next();
        }
        ident[n] = 0; tok = 1; return 0;
    }
    if digit(ch) {
        value = 0;
        while digit(ch) {
            if value > 6553 { fail(3); }
            if value == 6553 { if ch > 53 { fail(3); } }
            value = value*10+ch-48; next();
        }
        tok = 2; return 0;
    }
    if ch == 34 {
        while 1 {
            if n >= 510 { fail(5); }
            if ch==10 | ch==13 { fail(2); }
            if ch == 0 { fail(2); }
            string[n] = ch; n = n+1; c = ch; next();
            if n != 1 {
                if escaped {
                    if c!=110 { if c!=114 { if c!=116 { if c!=48 { if c!=92 { if c!=34 { fail(2); } } } } } }
                    escaped = 0;
                }
                else {
                    if c == 34 { string[n] = 0; tok = 3; return 0; }
                    if c == 92 { escaped = 1; }
                }
            }
        }
    }
    tok = ch; next();
    if tok == 61 { if ch == 61 { tok = 256; next(); } return 0; }
    if tok == 33 { if ch == 61 { tok = 257; next(); } return 0; }
    if tok == 60 {
        if ch == 61 { tok = 258; next(); }
        else { if ch == 60 { tok = 260; next(); } }
        return 0;
    }
    if tok == 62 {
        if ch == 61 { tok = 259; next(); }
        else { if ch == 62 { tok = 261; next(); } }
    }
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

Remove this source at old physical positions 35–35 in RC07.RIL:

```rill
fn main(){input=open("SOURCE.RIL");if status(){fail(1);}next();printnum(ch);return 0;}
```

Replace it with:

```rill
fn main(){input=open("SOURCE.RIL");if status(){fail(1);}next();lex();printnum(value);return 0;}
```

The following old source remains in place:

```rill

fn next() {
```

## Build this stopping point

```dos
COPY RC08.RIL SOURCE.RIL
CHECK RILLBOOT
```

Require `OK RESULT.IR 0000013381` and PASS. Copy RESULT.IR to SOURCE.IR.

```dos
CHECK IWKEEP
COPY RESULT.ASM SOURCE.ASM
CHECK ASMAKEEP
```

Require IR86 `OK RESULT.ASM 0000029422 text bytes` and PASS **before** the copy. Require assembler `OK RESULT.COM 14083 bytes` and PASS before saving:

```dos
COPY RESULT.COM RC08.COM
```

VIEW.BAS must report RC08.COM length 14083 bytes. Keep this executable and its source together.

## Acceptance check

Create TRC08.RIL with COPY CON or a plain-text editor. Finish COPY CON with Ctrl-Z and Enter:

```rill
65535
```

```dos
COPY TRC08.RIL SOURCE.RIL
```

```dos
CHECK RC08
```

Require, apart from command echo and the checker's separator:

```text
65535PASS
```

## A rejection or boundary check

Create XRC08.RIL:

```rill
65536
```

```dos
COPY XRC08.RIL SOURCE.RIL
CHECK RC08
```

Require:

```text
ERROR 0000000001 CODE 00003
FAIL
```

An unexpected PASS fails the rejection. The pre-existing RESULT.IR must remain unchanged; preserve a copy before the test.

## If the result differs

Check the saved pointer or slot, argument order, complete token spelling, and STATUS immediately after each service. A helper's local state must survive calls; an output count is independent of input position. Inspect text and file length before interpreting any bytes as a program.
