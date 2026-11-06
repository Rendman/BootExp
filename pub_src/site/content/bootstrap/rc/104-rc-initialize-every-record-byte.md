+++
title = "RC16 \u00b7 Initialize every record byte"
weight = 16
description = "Initialize the entire forty-byte record, copy the complete spelling, then write the explicit fields."
download = "RC16.RIL"
download_group = "rc"
aliases = ["/bootstrap/rill/104-rc-initialize-every-record-byte/"]
+++

Initialize the entire forty-byte record, copy the complete spelling, then write the explicit fields.

## The working parts

Initialize the entire forty-byte record, copy the complete spelling, then write the explicit fields. The global region begins at zero in TABLE; the local region begins at byte offset 20480.

The entry diagnostic exercises the printed helper. Rejecting placeholders identify forms outside this stopping point. A diagnostic that emits only an IR fragment is inspected as text; it is not a complete compiler or output program.

## Enter the source

Copy RC15.RIL to RC16.RIL. Apply edits **from the bottom of the old file upward**. Physical positions refer to that unchanged old file; use the printed context to identify each place. Keep all other source.

### Edit 1

Unchanged source immediately before the edit:

```rill
    return 65535;
}
```

Insert after old physical line 172.

Insert:

```rill
fn record(p) {
    let mut i = 0;
    while i < 40 { set8(table,p+i,0); i = i+1; }
    i = 0;
    while 1 { set8(table,p+i,ident[i]); if ident[i] == 0 { return recordfields(p); } i = i+1; }
}
```

The following old source remains in place:

```rill
fn recordfields(p) { set16(table,p+32,rectype); set16(table,p+34,recval); set16(table,p+36,reclevel); return p; }
```

### Edit 2

Unchanged source immediately before the edit:

```rill
bytes ident[32];
bytes string[512];
```

Remove this source at old physical positions 35–35 in RC15.RIL:

```rill
fn main(){table=alloc(22000);rectype=1;recval=12345;reclevel=0;recordfields(0);printnum(tword(34));return 0;}
```

Replace it with:

```rill
fn main(){table=alloc(22000);setident("ABC");rectype=1;recval=12345;reclevel=0;record(0);globals=1;printnum(tword(34));return 0;}
```

The following old source remains in place:

```rill

fn next() {
```

## Build this stopping point

```dos
COPY RC16.RIL SOURCE.RIL
CHECK RILLBOOT
```

Require `OK RESULT.IR 0000017197` and PASS. Copy RESULT.IR to SOURCE.IR.

```dos
CHECK IWKEEP
COPY RESULT.ASM SOURCE.ASM
CHECK ASMAKEEP
```

Require IR86 `OK RESULT.ASM 0000036663 text bytes` and PASS **before** the copy. Require assembler `OK RESULT.COM 15377 bytes` and PASS before saving:

```dos
COPY RESULT.COM RC16.COM
```

VIEW.BAS must report RC16.COM length 15377 bytes. Keep this executable and its source together.

## Acceptance check

```dos
CHECK RC16
```

Require, apart from command echo and the checker's separator:

```text
12345PASS
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
