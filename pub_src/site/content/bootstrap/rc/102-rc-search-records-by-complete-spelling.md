+++
title = "RC14 \u00b7 Search records by complete spelling"
weight = 14
description = "Search entries from the end toward the beginning and compare complete spellings."
download = "RC14.RIL"
download_group = "rc"
aliases = ["/bootstrap/rill/102-rc-search-records-by-complete-spelling/"]
+++

Search entries from the end toward the beginning and compare complete spellings.

## The working parts

Search entries from the end toward the beginning and compare complete spellings. This selects the innermost active binding. Return 65535 for absence; offset zero is a valid found record.

The entry diagnostic exercises the printed helper. Rejecting placeholders identify forms outside this stopping point. A diagnostic that emits only an IR fragment is inspected as text; it is not a complete compiler or output program.

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
fn main(){table=alloc(22000);set16(table,100,4660);printnum(tbyte(100));return 0;}
```

Replace it with:

```rill
fn main(){table=alloc(22000);setident("ABC");printnum(find(0,0));return 0;}
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

Require `OK RESULT.IR 0000015914` and PASS. Copy RESULT.IR to SOURCE.IR.

```dos
CHECK IWKEEP
COPY RESULT.ASM SOURCE.ASM
CHECK ASMAKEEP
```

Require IR86 `OK RESULT.ASM 0000034216 text bytes` and PASS **before** the copy. Require assembler `OK RESULT.COM 14949 bytes` and PASS before saving:

```dos
COPY RESULT.COM RC14.COM
```

VIEW.BAS must report RC14.COM length 14949 bytes. Keep this executable and its source together.

## Acceptance check

```dos
CHECK RC14
```

Require, apart from command echo and the checker's separator:

```text
65535PASS
```

## A rejection or boundary check

Check the same word boundary in the compiler seed. Create BAD.RIL:

```rill
fn main(){return 65536;}
```

```dos
COPY BAD.RIL SOURCE.RIL
CHECK RILLBOOT
```

Require `ERROR 0000000001 CODE 00003` and FAIL, preserving the accepted RESULT.IR. An unexpected PASS fails this check.

## If the result differs

Check the saved pointer or slot, argument order, complete token spelling, and STATUS immediately after each service. A helper's local state must survive calls; an output count is independent of input position. Inspect text and file length before interpreting any bytes as a program.
