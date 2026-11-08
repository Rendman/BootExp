+++
title = "02 \u00b7 Refilling a bounded input block"
weight = 2
description = "Read through a 1024-byte block and consume every positive read before refilling. Zero count is EOF; Control-Z ends object text."
download = "L02.RIL"
download_group = "tools/link86"
reader_names = 1
+++

Read through a 1024-byte block and consume every positive read before refilling. Zero count is EOF; Control-Z ends object text.

This reader test counts the eleven disk bytes in the supplied OBJ1/END fixture, including CR/LF. A mismatch returns nonzero; no display helper is added.

## Enter the source

Copy L01.RIL to L02.RIL. Apply these edits from the bottom of the unchanged old file upward. Physical positions are locators, not source to type. Keep all other source.

### Edit 1

Unchanged source immediately before the edit:

```rill

fn closein(){close(input);if status(){fail(6);}inopen=0;return 0;}
```

Insert after old physical line 9.

Insert:

```rill
fn nextbyte(){
    if ended{return 65535;}
    if inpos==inlen{
        inlen=read(input,inbuf,1024);if status(){fail(6);}inpos=0;
        if inlen==0{ended=1;return 65535;}
    }
    let mut c=inbuf[inpos];inpos=inpos+1;
    if c==26{ended=1;return 65535;}return c;
}
```

The following old source remains:

```rill
fn fail(code){if inopen{close(input);}exit(1);return 0;}
```

### Edit 2

Unchanged source immediately before the edit:

```rill
let mut inopen=0;
fn main(){openunit();closein();return 0;}
```

Remove old physical positions 6–6:

```rill
fn openunit(){input=open("MAIN.OBJ");if status(){fail(6);}inopen=1;return 0;}
```

Replace with:

```rill
fn openunit(){
    line=0;ended=0;skip=0;inpos=0;inlen=0;
    if unit==1{input=open("MAIN.OBJ");}
    else{input=open("UTIL.OBJ");}
    if status(){fail(6);}inopen=1;return 0;
}
```

The following old source remains:

```rill

fn closein(){close(input);if status(){fail(6);}inopen=0;return 0;}
```

### Edit 3

Unchanged source immediately before the edit:

```rill
// LINK86 construction checkpoint.
let mut input=0;
let mut inopen=0;
```

Remove old physical positions 4–4:

```rill
fn main(){openunit();closein();return 0;}
```

Replace with:

```rill
let mut unit=1;
let mut line=0;
let mut ended=0;
let mut skip=0;
let mut inpos=0;
let mut inlen=0;
bytes inbuf[1024];
fn main(){openunit();let mut count=0;while nextbyte()!=65535{count=count+1;}closein();return count!=11;}
```

The following old source remains:

```rill

fn openunit(){input=open("MAIN.OBJ");if status(){fail(6);}inopen=1;return 0;}
```

## Build and preserve the tool

```dos
COPY L02.RIL SOURCE.RIL
CHECK R0
COPY RESULT.IR SOURCE.IR
CHECK I0
COPY RESULT.ASM SOURCE.ASM
CHECK A0
COPY RESULT.COM L02.COM
```

Require compiler `OK RESULT.IR 0000002403`, translator `OK RESULT.ASM 0000009198 text bytes`, assembler `OK RESULT.COM 02797 bytes`, and each PASS before the following copy. VIEW.BAS must show L02.COM length 2797 and these first thirty-two bytes:

```text
FC 81 FC FE FF 74 03 E9 9A 0A E8 F2 06 B4 4C CD 21 00 00 00 00 01 00 00 00 00 00 00 00 00 00 00
```

## Check the accepted input

Create M02.OBJ as plain ASCII:

```text
OBJ1
END
```

```dos
COPY M02.OBJ MAIN.OBJ
CHECK L02
```

CHECK must report PASS. This checkpoint creates no linked output. Its input handling is checked by its return status; its retained executable was inspected above.

## A rejection check

```dos
COPY RESULT.COM HOLD.COM
```

```dos
REN MAIN.OBJ HOLD.OBJ
CHECK L02
```

Use an unused HOLD.OBJ name and restore it to MAIN.OBJ after the check.

Require:

```text
FAIL
```

```dos
COMP HOLD.COM RESULT.COM <NO.TXT
```

COMP must report no differences. An unexpected PASS fails the rejection. Require a fresh successful run before preserving any new output.
