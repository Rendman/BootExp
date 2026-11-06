+++
title = "19 \u00b7 Finding a Global Name"
weight = 19
description = "Restrict FIND to the active global entries."
download = "RC19.RIL"
download_group = "tools/rill"
aliases = ["/bootstrap/rill/107-rc-select-the-global-namespace/"]
reader_names = 1
+++

## The working parts

Restrict FIND to the active global entries. A local shadow must not change how a procedure definition is found.

## Enter the source

Copy RC18.RIL to RC19.RIL. Apply edits **from the bottom of the old file upward**. Physical positions refer to that unchanged old file; use the printed context to identify each place. Keep all other source.

### Edit 1

Unchanged source immediately before the edit:

```rill
    return record(p);
}
```

Insert after old physical line 195.

Insert:

```rill
fn lookglobal() { return find(0,globals); }
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

Remove this source at old physical positions 35–35 in RC18.RIL:

```rill
fn main(){table=alloc(22000);setident("ABC");recval=7;newlocal(5);return (tword(20514))!=7;}
```

Replace it with:

```rill
fn main(){table=alloc(22000);setident("ABC");rectype=1;recval=12345;reclevel=0;record(0);globals=1;lookglobal();return (recval)!=12345;}
```

The following old source remains in place:

```rill

fn next() {
```

## Build this stopping point

```dos
COPY RC19.RIL SOURCE.RIL
CHECK RILLBOOT
```

Require `OK RESULT.IR 0000018074` and PASS. Copy RESULT.IR to SOURCE.IR.

```dos
CHECK IWKEEP
COPY RESULT.ASM SOURCE.ASM
CHECK ASMAKEEP
```

Require IR86 `OK RESULT.ASM 0000038333 text bytes` and PASS **before** the copy. Require assembler `OK RESULT.COM 15675 bytes` and PASS before saving:

```dos
COPY RESULT.COM RC19.COM
```

VIEW.BAS must report RC19.COM length 15675 bytes. Keep this executable and its source together.

## Acceptance check

```dos
CHECK RC19
```

The checker must report PASS. The driver compares the result with 12345 and returns nonzero on a mismatch; it adds no display routine.

## If the result differs

Compare lookglobal with the printed addition. Check its arguments and saved state across calls, then inspect the generated text or bytes.
