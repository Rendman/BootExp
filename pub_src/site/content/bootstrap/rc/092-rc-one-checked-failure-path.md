+++
title = "04 \u00b7 Reporting an Error"
weight = 4
description = "An error category is an explicit parameter."
download = "RC04.RIL"
download_group = "tools/rill"
aliases = ["/bootstrap/rill/092-rc-one-checked-failure-path/"]
reader_names = 1
+++

## The working parts

An error category is an explicit parameter. Close owned handles, retain recovery files when restoration fails, and exit nonzero. No ordinary parse routine returns a successful result after this path.

## Enter the source

Copy RC03.RIL to RC04.RIL. Apply edits **from the bottom of the old file upward**. Physical positions refer to that unchanged old file; use the printed context to identify each place. Keep all other source.

### Edit 1

Unchanged source immediately before the edit:

```rill
    while place { c = 48; while n >= place { n = n-place; c = c+1; } putc(c); place = place/10; }
    return 0;
}
```

Insert after old physical line 43.

Insert:

```rill

fn fail(code) {
    if input { close(input); }
    if output { close(output); }
    let mut recovery = 0;
    if backup { rename("RILL.BAK","RESULT.IR"); if status() { recovery = 1; } }
    if recovery == 0 { if own { delete("RILL.TMP"); if status() { recovery=1; } } }
    if table { free(table); table = 0; }
    print("ERROR "); print32(linehi,line); print(" CODE "); printnum(code); print("\r\n");
    if recovery { print("Recovery: inspect RILL.TMP and RILL.BAK\r\n"); } exit(1); return 0;
}

// Divide a pair of words by ten without requiring a wider machine value.
```

The following old source remains in place:

```rill

fn print32(hi,lo) {
```

### Edit 2

Unchanged source immediately before the edit:

```rill
bytes ident[32];
bytes string[512];
```

Remove this source at old physical positions 35–35 in RC03.RIL:

```rill
fn main(){print32(1,1);return 0;}
```

Replace it with:

```rill
fn main(){fail(2);return 0;}
```

The following old source remains in place:

```rill

fn print(s) { let mut c = 0; while 1 { c = load8(s); if c == 0 { return 0; } putc(c); s = s+1; } }
```

## Build this stopping point

```dos
COPY RC04.RIL SOURCE.RIL
CHECK RILLBOOT
```

Require `OK RESULT.IR 0000004547` and PASS. Copy RESULT.IR to SOURCE.IR.

```dos
CHECK IWKEEP
COPY RESULT.ASM SOURCE.ASM
CHECK ASMAKEEP
```

Require IR86 `OK RESULT.ASM 0000013492 text bytes` and PASS **before** the copy. Require assembler `OK RESULT.COM 11189 bytes` and PASS before saving:

```dos
COPY RESULT.COM RC04.COM
```

VIEW.BAS must report RC04.COM length 11189 bytes. Keep this executable and its source together.

## Acceptance check

```dos
CHECK RC04
```

Require:

```text
ERROR 0000000001 CODE 00002
FAIL
```

FAIL is the intended status here: the routine being tested reports an error and terminates with status one.

## If the result differs

Check owned handles and recovery files before the final error report.
