+++
title = "23 \u00b7 Writing Text Through the Buffer"
weight = 23
description = "Walk a terminated template while preserving its pointer."
download = "RC23.RIL"
download_group = "tools/rill"
aliases = ["/bootstrap/rill/111-rc-append-a-template-string/"]
reader_names = 1
url = "/bootstrap/rc/111-rc-append-a-template-string/"
+++

## The working parts

Walk a terminated template while preserving its pointer. Normalize a bare LF in an IR template to CR/LF while retaining existing CR/LF. Quoted source escapes are still printable backslash spellings at this point.

## Enter the source

Copy RC22.RIL to RC23.RIL. Apply edits **from the bottom of the old file upward**. Physical positions refer to that unchanged old file; use the printed context to identify each place. Keep all other source.

### Edit 1

Unchanged source immediately before the edit:

```rill
    return 0;
}
```

Insert after old physical line 220.

Insert:

```rill
fn outstr(s) {
    let mut c=0; let mut previous=0;
    while 1 {
        c=load8(s); if c==0 { return 0; }
        if c==10 { if previous!=13 { outchar(13); } }
        outchar(c); previous=c; s=s+1;
    }
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

Remove this source at old physical positions 35–35 in RC22.RIL:

```rill
fn main(){filearg(1,"SOURCE.RIL");output=create(filearg(2,"RILL.TMP"));own=1;outchar(65);flush();close(output);output=0;own=0;return 0;}
```

Replace it with:

```rill
fn main(){filearg(1,"SOURCE.RIL");output=create(filearg(2,"RILL.TMP"));own=1;outstr("HI");flush();close(output);output=0;own=0;return 0;}
```

The following old source remains in place:

```rill

fn next() {
```

## Build this stopping point

```dos
CHECK RILLBOOT RC23.RIL RESULT.IR
```

Require `OK RESULT.IR 0000021710` and PASS. Pass RESULT.IR directly to the translator.

```dos
CHECK IWKEEP SOURCE.IR RESULT.ASM
CHECK ASMAKEEP RESULT.ASM RESULT.COM
```

Require IR86 `OK RESULT.ASM 0000046762 text bytes` and PASS **before** the copy. Require assembler `OK RESULT.COM 17218 bytes` and PASS before saving:

```dos
COPY RESULT.COM RC23.COM
```

VIEW.BAS must report RC23.COM length 17218 bytes. Keep this executable and its source together.

## Acceptance check

```dos
CHECK RC23 RC23.RIL RESULT.IR
```

The checker must report PASS. Inspect the emitted file below.

Use VIEW.BAS to inspect RESULT.IR. Require length 2 bytes. The complete bytes must be:

```text
48 49
```

This is an IR fragment for inspection. Do not translate it as a complete program or execute any file with its name.

## If the result differs

Compare outstr with the printed addition. Check its arguments and saved state across calls, then inspect the generated text or bytes.
