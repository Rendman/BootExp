+++
title = "30 \u00b7 Recognizing Built-in Services"
weight = 30
description = "A terminated spelling selects an intrinsic record containing an arity and IR text."
download = "RC30.RIL"
download_group = "tools/rill"
aliases = ["/bootstrap/rill/118-rc-recognize-portable-intrinsics/"]
reader_names = 1
+++

## The working parts

A terminated spelling selects an intrinsic record containing an arity and IR text. Compare the whole name. A failed match advances past both fields before considering another entry.

## Enter the source

Copy RC29.RIL to RC30.RIL. Apply edits **from the bottom of the old file upward**. Physical positions refer to that unchanged old file; use the printed context to identify each place. Keep all other source.

### Edit 1

Unchanged source immediately before the edit:

```rill
    return 0;
}
```

Insert after old physical line 253.

Insert:

```rill
fn builtin() {
    let mut p = "PUTC\01\0POP\nPUTC\0STATUS\00\0STATUS\0OPEN\01\0POP\nOPEN\0CREATE\01\0POP\nCREATE\0CLOSE\01\0POP\nCLOSE\0READ\03\0POP\nREAD\0WRITE\03\0POP\nWRITE\0EXISTS\01\0POP\nEXISTS\0DELETE\01\0POP\nDELETE\0RENAME\02\0POP\nRENAME\0ALLOC\01\0POP\nALLOC\0FREE\01\0POP\nFREEBLOCK\0GET8\02\0POP\nGET8\0GET16\02\0POP\nGET16\0SET8\03\0POP\nSET8\0SET16\03\0POP\nSET16\0LOAD8\01\0POP\nFETCHB\0LOAD16\01\0POP\nFETCH\0STORE8\02\0POP\nPUTB\0STORE16\02\0POP\nPUT\0EXIT\01\0POP\nEXIT\0\0";
    let mut i = 0; let mut same = 0;
    while load8(p) {
        i = 0; same = 1;
        while load8(p+i) { if load8(p+i) != ident[i] { same = 0; } i = i+1; }
        if ident[i] != 0 { same = 0; }
        p = p+i+1; recval = load8(p)-48; p = p+2;
        if same { return p; }
        while load8(p) { p = p+1; } p = p+1;
    }
    return 0;
}
```

The following old source remains in place:

```rill
fn fail(code) {
    if input { close(input); }
```

### Edit 2

Unchanged source immediately before the edit:

```rill
bytes ident[32];
bytes string[512];
```

Remove this source at old physical positions 35–35 in RC29.RIL:

```rill
fn main(){table=alloc(22000);setident("ABC");rectype=1;recval=12345;reclevel=0;record(0);globals=1;output=create("RILL.TMP");own=1;outname(0);flush();close(output);output=0;own=0;return 0;}
```

Replace it with:

```rill
fn main(){setident("PUTC");builtin();return (recval)!=1;}
```

The following old source remains in place:

```rill

fn next() {
```

## Build this stopping point

```dos
COPY RC30.RIL SOURCE.RIL
CHECK RILLBOOT
```

Require `OK RESULT.IR 0000023519` and PASS. Copy RESULT.IR to SOURCE.IR.

```dos
CHECK IWKEEP
COPY RESULT.ASM SOURCE.ASM
CHECK ASMAKEEP
```

Require IR86 `OK RESULT.ASM 0000051337 text bytes` and PASS **before** the copy. Require assembler `OK RESULT.COM 17693 bytes` and PASS before saving:

```dos
COPY RESULT.COM RC30.COM
```

VIEW.BAS must report RC30.COM length 17693 bytes. Keep this executable and its source together.

## Acceptance check

```dos
CHECK RC30
```

The checker must report PASS. The driver compares the result with 1 and returns nonzero on a mismatch; it adds no display routine.

## If the result differs

Compare builtin with the printed addition. Check its arguments and saved state across calls, then inspect the generated text or bytes.
