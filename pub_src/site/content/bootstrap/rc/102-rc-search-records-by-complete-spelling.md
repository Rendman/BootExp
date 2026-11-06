+++
title = "14 \u00b7 Finding a Name in the Table"
weight = 14
description = "Search entries from the end toward the beginning and compare complete spellings."
download = "RC14.RIL"
download_group = "tools/rill"
aliases = ["/bootstrap/rill/102-rc-search-records-by-complete-spelling/"]
reader_names = 1
+++

## The working parts

Search entries from the end toward the beginning and compare complete spellings. This selects the innermost active binding. Return 65535 for absence; offset zero is a valid found record.

## Enter the source

Copy RC13.RIL to RC14.RIL. Apply edits **from the bottom of the old file upward**. Physical positions refer to that unchanged old file; use the printed context to identify each place. Keep all other source.

### Edit 1

Unchanged source immediately before the edit:

```rill

fn tbyte(p) { return get8(table,p); }
```

Insert after old physical line 150.

Insert:

```rill
fn find(base,count) {
    let mut p = 0;
    let mut i = 0;
    let mut c = 0;
    let mut same = 0;
    while count {
        count = count-1; p = base+count*40; i = 0; same = 1;
        while same {
            c = tbyte(p+i);
            if c != ident[i] { same = 0; }
            else {
                if c == 0 {
                    rectype = tword(p+32); recval = tword(p+34); reclevel = tword(p+36);
                    return p;
                }
                i = i+1;
            }
        }
    }
    return 65535;
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

Remove this source at old physical positions 35–35 in RC13.RIL:

```rill
fn main(){table=alloc(22000);set16(table,100,4660);return (tbyte(100))!=52;}
```

Replace it with:

```rill
fn main(){table=alloc(22000);setident("ABC");return (find(0,0))!=65535;}
```

The following old source remains in place:

```rill

fn next() {
```

## Build this stopping point

```dos
COPY RC14.RIL SOURCE.RIL
CHECK RILLBOOT
```

Require `OK RESULT.IR 0000015894` and PASS. Copy RESULT.IR to SOURCE.IR.

```dos
CHECK IWKEEP
COPY RESULT.ASM SOURCE.ASM
CHECK ASMAKEEP
```

Require IR86 `OK RESULT.ASM 0000034228 text bytes` and PASS **before** the copy. Require assembler `OK RESULT.COM 14951 bytes` and PASS before saving:

```dos
COPY RESULT.COM RC14.COM
```

VIEW.BAS must report RC14.COM length 14951 bytes. Keep this executable and its source together.

## Acceptance check

```dos
CHECK RC14
```

The checker must report PASS. The driver compares the result with 65535 and returns nonzero on a mismatch; it adds no display routine.

## If the result differs

Compare find with the printed addition. Check its arguments and saved state across calls, then inspect the generated text or bytes.
