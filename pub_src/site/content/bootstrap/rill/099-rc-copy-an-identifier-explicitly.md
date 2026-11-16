+++
title = "11 \u00b7 Copying a Name"
weight = 11
description = "Copy an explicit terminated spelling into IDENT."
download = "RC11.RIL"
download_group = "tools/rill"
aliases = ["/bootstrap/rill/099-rc-copy-an-identifier-explicitly/"]
reader_names = 1
url = "/bootstrap/rc/099-rc-copy-an-identifier-explicitly/"
+++

## The working parts

Copy an explicit terminated spelling into IDENT. This is a table-test helper as well as a way to ask for a required entry without depending on the current source token.

## Enter the source

Copy RC10.RIL to RC11.RIL. Apply edits **from the bottom of the old file upward**. Physical positions refer to that unchanged old file; use the printed context to identify each place. Keep all other source.

### Edit 1

Unchanged source immediately before the edit:

```rill
    return 0;
}
```

Insert after old physical line 144.

Insert:

```rill
fn setident(s) { let mut i = 0; while 1 { ident[i] = load8(s+i); if ident[i] == 0 { return 0; } i = i+1; } }
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

Remove this source at old physical positions 35–35 in RC10.RIL:

```rill
fn main(){filearg(1,"SOURCE.RIL");input=open(filearg(1,"SOURCE.RIL"));if status(){fail(1);}next();lex();return (isword("FN"))!=1;}
```

Replace it with:

```rill
fn main(){filearg(1,"SOURCE.RIL");setident("ABC");tok=1;return isword("ABC")!=1;}
```

The following old source remains in place:

```rill

fn next() {
```

## Build this stopping point

```dos
CHECK RILLBOOT RC11.RIL RESULT.IR
```

Require `OK RESULT.IR 0000015925` and PASS. Pass RESULT.IR directly to the translator.

```dos
CHECK IWKEEP SOURCE.IR RESULT.ASM
CHECK ASMAKEEP RESULT.ASM RESULT.COM
```

Require IR86 `OK RESULT.ASM 0000036098 text bytes` and PASS **before** the copy. Require assembler `OK RESULT.COM 15316 bytes` and PASS before saving:

```dos
COPY RESULT.COM RC11.COM
```

VIEW.BAS must report RC11.COM length 15316 bytes. Keep this executable and its source together.

## Acceptance check

```dos
CHECK RC11
```

The checker must report PASS. The driver compares the result with ABC and returns nonzero on a mismatch; it adds no display routine.

## If the result differs

Compare setident with the printed addition. Check its arguments and saved state across calls, then inspect the generated text or bytes.
