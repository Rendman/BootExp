+++
title = "21 \u00b7 Writing a Buffered Block"
weight = 21
description = "Write only a nonempty output block."
download = "RC21.RIL"
download_group = "tools/rill"
aliases = ["/bootstrap/rill/109-rc-flush-a-bounded-text-block/"]
reader_names = 1
url = "/bootstrap/rc/109-rc-flush-a-bounded-text-block/"
+++

## The working parts

Write only a nonempty output block. Check STATUS and the exact returned count before clearing OUTLEN. A zero-count DOS write is never used to flush or truncate the file.

## Enter the source

Copy RC20.RIL to RC21.RIL. Apply edits **from the bottom of the old file upward**. Physical positions refer to that unchanged old file; use the printed context to identify each place. Keep all other source.

### Edit 1

Unchanged source immediately before the edit:

```rill
    return found;
}
```

Insert after old physical line 203.

Insert:

```rill
fn flush() {
    if outlen {
        let mut n = write(output,outbuf,outlen);
        if status() { fail(1); }
        if n != outlen { fail(1); }
        outlen = 0;
    }
    return 0;
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

Remove this source at old physical positions 35–35 in RC20.RIL:

```rill
fn main(){filearg(1,"SOURCE.RIL");table=alloc(23680);setident("ABC");rectype=1;recval=12345;reclevel=0;record(0);globals=1;resolve();return (recval)!=12345;}
```

Replace it with:

```rill
fn main(){filearg(1,"SOURCE.RIL");output=create(filearg(2,"RILL.TMP"));own=1;outbuf[0]=65;outlen=1;flush();close(output);output=0;own=0;return 0;}
```

The following old source remains in place:

```rill

fn next() {
```

## Build this stopping point

```dos
CHECK RILLBOOT RC21.RIL RESULT.IR
```

Require `OK RESULT.IR 0000020447` and PASS. Pass RESULT.IR directly to the translator.

```dos
CHECK IWKEEP SOURCE.IR RESULT.ASM
CHECK ASMAKEEP RESULT.ASM RESULT.COM
```

Require IR86 `OK RESULT.ASM 0000044425 text bytes` and PASS **before** the copy. Require assembler `OK RESULT.COM 16800 bytes` and PASS before saving:

```dos
COPY RESULT.COM RC21.COM
```

VIEW.BAS must report RC21.COM length 16800 bytes. Keep this executable and its source together.

## Acceptance check

```dos
CHECK RC21 RC21.RIL RESULT.IR
```

The checker must report PASS. Inspect the emitted file below.

Use VIEW.BAS to inspect RESULT.IR. Require length 1 bytes. The complete bytes must be:

```text
41
```

This is an IR fragment for inspection. Do not translate it as a complete program or execute any file with its name.

## If the result differs

Compare flush with the printed addition. Check its arguments and saved state across calls, then inspect the generated text or bytes.
