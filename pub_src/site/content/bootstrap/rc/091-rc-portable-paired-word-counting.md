+++
title = "RC03 \u00b7 Portable paired-word counting"
weight = 3
description = "Treat the two words as one unsigned count."
download = "RC03.RIL"
download_group = "rc"
aliases = ["/bootstrap/rill/091-rc-portable-paired-word-counting/"]
+++

Treat the two words as one unsigned count.

## The working parts

Treat the two words as one unsigned count. Divide the high word by ten, then carry its remainder through the low word one bit at a time. Store the remainders and display them in reverse order, including leading zeroes.

The entry diagnostic exercises the printed helper. Rejecting placeholders identify forms outside this stopping point. A diagnostic that emits only an IR fragment is inspected as text; it is not a complete compiler or output program.

## Enter the source

Copy RC02.RIL to RC03.RIL. Apply edits **from the bottom of the old file upward**. Physical positions refer to that unchanged old file; use the printed context to identify each place. Keep all other source.

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

fn print32(hi,lo) {
    let mut i = 0; let mut qhi = 0; let mut rem = 0;
    let mut qlo = 0; let mut bit = 0;
    while i < 10 {
        qhi = hi/10; rem = hi%10; qlo = 0; bit = 32768;
        while bit {
            rem = rem*2; if lo & bit { rem = rem+1; }
            qlo = qlo*2;
            if rem >= 10 { rem = rem-10; qlo = qlo+1; }
            bit = bit>>1;
        }
        decimal[i] = rem+48; hi = qhi; lo = qlo; i = i+1;
    }
    while i { i = i-1; putc(decimal[i]); } return 0;
}
```

### Edit 2

Unchanged source immediately before the edit:

```rill
bytes ident[32];
bytes string[512];
```

Remove this source at old physical positions 35–35 in RC02.RIL:

```rill
fn main(){printnum(65535);return 0;}
```

Replace it with:

```rill
fn main(){print32(1,1);return 0;}
```

The following old source remains in place:

```rill

fn print(s) { let mut c = 0; while 1 { c = load8(s); if c == 0 { return 0; } putc(c); s = s+1; } }
```

## Build this stopping point

```dos
COPY RC03.RIL SOURCE.RIL
CHECK RILLBOOT
```

Require `OK RESULT.IR 0000003229` and PASS. Copy RESULT.IR to SOURCE.IR.

```dos
CHECK IWKEEP
COPY RESULT.ASM SOURCE.ASM
CHECK ASMAKEEP
```

Require IR86 `OK RESULT.ASM 0000010455 text bytes` and PASS **before** the copy. Require assembler `OK RESULT.COM 10729 bytes` and PASS before saving:

```dos
COPY RESULT.COM RC03.COM
```

VIEW.BAS must report RC03.COM length 10729 bytes. Keep this executable and its source together.

## Acceptance check

```dos
CHECK RC03
```

Require, apart from command echo and the checker's separator:

```text
0000065537PASS
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
