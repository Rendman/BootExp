+++
title = "09 \u00b7 Consuming the Required Token"
weight = 9
description = "Compare the current token before advancing."
download = "RC09.RIL"
download_group = "tools/rill"
aliases = ["/bootstrap/rill/097-rc-consume-a-required-token/"]
reader_names = 1
+++

## The working parts

Compare the current token before advancing. On success, leave the following token ready; a caller must not advance once more accidentally.

## Enter the source

Copy RC08.RIL to RC09.RIL. Apply edits **from the bottom of the old file upward**. Physical positions refer to that unchanged old file; use the printed context to identify each place. Keep all other source.

### Edit 1

Unchanged source immediately before the edit:

```rill
    return 0;
}
```

Insert after old physical line 135.

Insert:

```rill
fn expect(t) { if tok != t { fail(2); } lex(); return 0; }
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

Remove this source at old physical positions 35–35 in RC08.RIL:

```rill
fn main(){input=open("SOURCE.RIL");if status(){fail(1);}next();lex();return (value)!=65535;}
```

Replace it with:

```rill
fn main(){input=open("SOURCE.RIL");if status(){fail(1);}next();lex();expect(43);print("OK");return 0;}
```

The following old source remains in place:

```rill

fn next() {
```

## Build this stopping point

```dos
COPY RC09.RIL SOURCE.RIL
CHECK RILLBOOT
```

Require `OK RESULT.IR 0000013622` and PASS. Copy RESULT.IR to SOURCE.IR.

```dos
CHECK IWKEEP
COPY RESULT.ASM SOURCE.ASM
CHECK ASMAKEEP
```

Require IR86 `OK RESULT.ASM 0000029931 text bytes` and PASS **before** the copy. Require assembler `OK RESULT.COM 14177 bytes` and PASS before saving:

```dos
COPY RESULT.COM RC09.COM
```

VIEW.BAS must report RC09.COM length 14177 bytes. Keep this executable and its source together.

## Acceptance check

Create TRC09.RIL with COPY CON or a plain-text editor. Finish COPY CON with Ctrl-Z and Enter:

```rill
+
```

```dos
COPY TRC09.RIL SOURCE.RIL
```

```dos
CHECK RC09
```

Require:

```text
OK
PASS
```

## A rejection or boundary check

Create XRC09.RIL:

```rill
-
```

```dos
COPY XRC09.RIL SOURCE.RIL
CHECK RC09
```

Require:

```text
ERROR 0000000001 CODE 00002
FAIL
```

An unexpected PASS fails the rejection. The pre-existing RESULT.IR must remain unchanged; preserve a copy before the test.

## If the result differs

Compare expect with the printed addition. Check its arguments and saved state across calls, then inspect the generated text or bytes.
