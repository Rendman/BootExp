+++
title = "04 \u00b7 Recognizing the object envelope"
weight = 4
description = "Recognize OBJ1 and END, including blank lines and semicolon comments. Reject unknown records instead of silently copying malformed text."
download = "L04.RIL"
download_group = "tools/link86"
reader_names = 1
+++

Recognize OBJ1 and END, including blank lines and semicolon comments. Reject unknown records instead of silently copying malformed text.

## Enter the source

Copy L03.RIL to L04.RIL. Apply these edits from the bottom of the unchanged old file upward. Physical positions are locators, not source to type. Keep all other source.

### Edit 1

Unchanged source immediately before the edit:

```rill
    source[length]=0;pos=0;return 0;
}
```

Insert after old physical line 54.

Insert:

```rill
fn scan(){
    toklen=0;
    while (pos<length)&((source[pos]==32)|(source[pos]==9)){pos=pos+1;}
    while pos<length{
        let mut c=source[pos];
        if (c==32)|(c==9)|(c==59){token[toklen]=0;return toklen;}
        if toklen==31{fail(5);}
        if (c>=97)&(c<=122){c=c-32;}
        token[toklen]=c;toklen=toklen+1;pos=pos+1;
    }
    token[toklen]=0;return toklen;
}

fn same(s){
    let mut i=0;
    while token[i]==load8(s+i){if token[i]==0{return 1;}i=i+1;}
    return 0;
}

fn finish(){if scan(){fail(1);}return 0;}

fn records(){
    let mut header=0;let mut done=0;
    while readline(){
        if scan(){
            if done{fail(1);}
            if header==0{
                if !same("OBJ1"){fail(1);}finish();header=1;
            }else{
                if same("END"){finish();done=1;}
                else{
                    fail(1);
                }
            }
        }
    }
    if (header==0)|(done==0){fail(1);}return 0;
}
```

The following old source remains:

```rill
fn print(s){
    while load8(s){putc(load8(s));s=s+1;}return 0;
```

### Edit 2

Unchanged source immediately before the edit:

```rill
let mut pos=0;
bytes inbuf[1024];
bytes source[121];
```

Remove old physical positions 14–14:

```rill
fn main(){openunit();let mut count=0;while readline(){count=count+1;}closein();return count!=2;}
```

Replace with:

```rill
bytes token[32];
fn main(){openunit();records();closein();return 0;}
```

The following old source remains:

```rill

fn openunit(){
```

### Edit 3

Unchanged source immediately before the edit:

```rill
let mut inlen=0;
let mut length=0;
let mut pos=0;
```

Insert after old physical line 11.

Insert:

```rill
let mut toklen=0;
```

The following old source remains:

```rill
bytes inbuf[1024];
bytes source[121];
```

## Build and preserve the tool

```dos
COPY L04.RIL SOURCE.RIL
CHECK R0
COPY RESULT.IR SOURCE.IR
CHECK I0
COPY RESULT.ASM SOURCE.ASM
CHECK A0
COPY RESULT.COM L04.COM
```

Require compiler `OK RESULT.IR 0000008313`, translator `OK RESULT.ASM 0000020492 text bytes`, assembler `OK RESULT.COM 04952 bytes`, and each PASS before the following copy. VIEW.BAS must show L04.COM length 4952 and these first thirty-two bytes:

```text
FC 81 FC FE FF 74 03 E9 05 13 E8 5D 0F B4 4C CD 21 00 00 00 00 01 00 00 00 00 00 00 00 00 00 00
```

## Check the accepted input

Create M04.OBJ as plain ASCII:

```text
OBJ1
END
```

```dos
COPY M04.OBJ MAIN.OBJ
CHECK L04
```

CHECK must report PASS. This checkpoint creates no linked output. Its input handling is checked by its return status; its retained executable was inspected above.

## A rejection check

```dos
COPY RESULT.COM HOLD.COM
```

Create X04.OBJ:

```text
OBJ2
END
```

```dos
COPY X04.OBJ MAIN.OBJ
CHECK L04
```

Require:

```text
LINK ERROR 00001 00001 CODE 00001
FAIL
```

```dos
COMP HOLD.COM RESULT.COM <NO.TXT
```

COMP must report no differences. An unexpected PASS fails the rejection. Require a fresh successful run before preserving any new output.
