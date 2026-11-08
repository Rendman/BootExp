+++
title = "05 \u00b7 Writing literal bytes"
weight = 5
description = "Decode up to sixteen hexadecimal bytes in a B record and stream them to an owned LINK.TMP. Inspect that file before deleting it."
download = "L05.RIL"
download_group = "tools/link86"
reader_names = 1
+++

Decode up to sixteen hexadecimal bytes in a B record and stream them to an owned LINK.TMP. Inspect that file before deleting it.

## Enter the source

Copy L04.RIL to L05.RIL. Apply these edits from the bottom of the unchanged old file upward. Physical positions are locators, not source to type. Keep all other source.

### Edit 1

Unchanged source immediately before the edit:

```rill
    return 0;
}
```

Remove old physical positions 108–108:

```rill
fn fail(code){if inopen{close(input);inopen=0;}print("LINK ERROR ");number(unit);putc(32);number(line);print(" CODE ");number(code);print("\r\n");exit(1);return 0;}
```

Replace with:

```rill
fn fail(code){
    if inopen{close(input);inopen=0;}
    if outopen{close(output);outopen=0;}
    if own{if keep==0{delete("LINK.TMP");}}
    print("LINK ERROR ");number(unit);putc(32);number(line);
    print(" CODE ");number(code);print("\r\n");exit(1);return 0;
}
```

### Edit 2

Unchanged source immediately before the edit:

```rill
    }
    if (header==0)|(done==0){fail(1);}return 0;
}
```

Insert after old physical line 94.

Insert:

```rill

fn hexvalue(digits){
    if toklen!=digits{fail(2);}
    let mut i=0;let mut value=0;
    while i<toklen{
        let mut c=token[i];
        if (c>=48)&(c<=57){c=c-48;}
        else{if (c>=65)&(c<=70){c=c-55;}else{fail(2);}}
        value=value*16+c;i=i+1;
    }
    return value;
}

fn bytesrecord(){
    let mut count=0;
    while scan(){
        if count==16{fail(5);}
        let mut value=hexvalue(2);emit(value);count=count+1;
    }
    if count==0{fail(1);}return 0;
}

fn emit(value){
    if pc==61184{fail(5);}pc=pc+1;
    if pass==2{
        outbuf[outlen]=value;outlen=outlen+1;
        if outlen==1024{flush();}
    }
    return 0;
}

fn flush(){
    if outlen{
        let mut count=write(output,outbuf,outlen);
        if status(){fail(6);}if count!=outlen{fail(6);}outlen=0;
    }
    return 0;
}

fn createout(){
    output=create("LINK.TMP");if status(){fail(6);}
    outopen=1;own=1;return 0;
}

fn finishout(){flush();close(output);if status(){fail(6);}outopen=0;return 0;}

fn preflight(){if exists("LINK.TMP"){fail(8);}if status(){fail(6);}return 0;}
```

The following old source remains:

```rill

fn print(s){
```

### Edit 3

Unchanged source immediately before the edit:

```rill
            }else{
                if same("END"){finish();done=1;}
                else{
```

Remove old physical positions 88–88:

```rill
                    fail(1);
```

Replace with:

```rill
                    if same("B"){bytesrecord();}else{fail(1);}
```

The following old source remains:

```rill
                }
            }
```

### Edit 4

Unchanged source immediately before the edit:

```rill
bytes inbuf[1024];
bytes source[121];
bytes token[32];
```

Remove old physical positions 16–16:

```rill
fn main(){openunit();records();closein();return 0;}
```

Replace with:

```rill
fn main(){preflight();pass=2;openunit();createout();records();closein();finishout();print("OK LINK.TMP ");number(pc);print(" bytes\r\n");return 0;}
```

The following old source remains:

```rill

fn openunit(){
```

### Edit 5

Unchanged source immediately before the edit:

```rill
let mut pos=0;
let mut toklen=0;
bytes inbuf[1024];
```

Insert after old physical line 13.

Insert:

```rill
bytes outbuf[1024];
```

The following old source remains:

```rill
bytes source[121];
bytes token[32];
```

### Edit 6

Unchanged source immediately before the edit:

```rill
let mut length=0;
let mut pos=0;
let mut toklen=0;
```

Insert after old physical line 12.

Insert:

```rill
let mut pc=0;
let mut outlen=0;
```

The following old source remains:

```rill
bytes inbuf[1024];
bytes source[121];
```

### Edit 7

Unchanged source immediately before the edit:

```rill
let mut input=0;
let mut inopen=0;
let mut unit=1;
```

Insert after old physical line 4.

Insert:

```rill
let mut pass=1;
```

The following old source remains:

```rill
let mut line=0;
let mut ended=0;
```

### Edit 8

Unchanged source immediately before the edit:

```rill
// LINK86 construction checkpoint.
let mut input=0;
let mut inopen=0;
```

Insert after old physical line 3.

Insert:

```rill
let mut output=0;
let mut outopen=0;
let mut own=0;
let mut keep=0;
```

The following old source remains:

```rill
let mut unit=1;
let mut line=0;
```

## Build and preserve the tool

```dos
COPY L05.RIL SOURCE.RIL
CHECK R0
COPY RESULT.IR SOURCE.IR
CHECK I0
COPY RESULT.ASM SOURCE.ASM
CHECK A0
COPY RESULT.COM L05.COM
```

Require compiler `OK RESULT.IR 0000012599`, translator `OK RESULT.ASM 0000028504 text bytes`, assembler `OK RESULT.COM 07361 bytes`, and each PASS before the following copy. VIEW.BAS must show L05.COM length 7361 and these first thirty-two bytes:

```text
FC 81 FC FE FF 74 03 E9 6E 1C E8 C6 18 B4 4C CD 21 00 00 00 00 00 00 00 00 00 00 00 00 01 00 01
```

## Check the accepted input

Create M05.OBJ as plain ASCII:

```text
OBJ1
B B8 00 4C CD 21
END
```

```dos
COPY M05.OBJ MAIN.OBJ
CHECK L05
```

Require:

```text
OK LINK.TMP 00005 bytes
PASS
```

VIEW.BAS must show LINK.TMP length 5 and these complete bytes:

```text
B8 00 4C CD 21
```

Inspect this data/encoding fixture; do not execute it.

Delete this deliberately created LINK.TMP after inspection. RESULT.COM still contains the preceding accepted file.

```dos
DEL LINK.TMP
```

## A rejection check

```dos
COPY RESULT.COM HOLD.COM
```

Create X05.OBJ:

```text
OBJ1
B 0G
END
```

```dos
COPY X05.OBJ MAIN.OBJ
CHECK L05
```

Require:

```text
LINK ERROR 00001 00002 CODE 00002
FAIL
```

```dos
COMP HOLD.COM RESULT.COM <NO.TXT
```

COMP must report no differences. An unexpected PASS fails the rejection. Require a fresh successful run before preserving any new output.
