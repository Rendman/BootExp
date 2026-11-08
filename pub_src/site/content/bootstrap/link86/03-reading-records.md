+++
title = "03 \u00b7 Reading one physical record"
weight = 3
description = "Bound a physical record to 120 characters, count its line, and accept ordinary DOS text endings without retaining the complete object."
download = "L03.RIL"
download_group = "tools/link86"
reader_names = 1
+++

Bound a physical record to 120 characters, count its line, and accept ordinary DOS text endings without retaining the complete object.

This stopping test requires exactly two physical records in its fixture. Error reports now use the owned input number, current physical record and reason code. The source buffer stores only the current record.

## Enter the source

Copy L02.RIL to L03.RIL. Apply these edits from the bottom of the unchanged old file upward. Physical positions are locators, not source to type. Keep all other source.

### Edit 1

Unchanged source immediately before the edit:

```rill
    if c==26{ended=1;return 65535;}return c;
}
```

Remove old physical positions 32–32:

```rill
fn fail(code){if inopen{close(input);}exit(1);return 0;}
```

Replace with:

```rill
fn readline(){
    length=0;let mut started=0;
    while 1{
        let mut c=nextbyte();
        if skip{skip=0;if c==10{c=nextbyte();}}
        if c==65535{if length==0{return 0;}else{breakline();return 1;}}
        if started==0{if line==65535{fail(5);}line=line+1;started=1;}
        if c==13{skip=1;breakline();return 1;}
        if c==10{breakline();return 1;}
        if (c<32)&(c!=9){fail(1);}if c>126{fail(1);}
        if length==120{fail(5);}
        source[length]=c;length=length+1;
    }
    return 0;
}

fn breakline(){
    source[length]=0;pos=0;return 0;
}

fn print(s){
    while load8(s){putc(load8(s));s=s+1;}return 0;
}

fn number(value){
    let mut place=10000;
    while place{
        putc(value/place+48);value=value%place;place=place/10;
    }
    return 0;
}

fn fail(code){if inopen{close(input);inopen=0;}print("LINK ERROR ");number(unit);putc(32);number(line);print(" CODE ");number(code);print("\r\n");exit(1);return 0;}
```

### Edit 2

Unchanged source immediately before the edit:

```rill
let mut inpos=0;
let mut inlen=0;
bytes inbuf[1024];
```

Remove old physical positions 11–11:

```rill
fn main(){openunit();let mut count=0;while nextbyte()!=65535{count=count+1;}closein();return count!=11;}
```

Replace with:

```rill
bytes source[121];
fn main(){openunit();let mut count=0;while readline(){count=count+1;}closein();return count!=2;}
```

The following old source remains:

```rill

fn openunit(){
```

### Edit 3

Unchanged source immediately before the edit:

```rill
let mut skip=0;
let mut inpos=0;
let mut inlen=0;
```

Insert after old physical line 9.

Insert:

```rill
let mut length=0;
let mut pos=0;
```

The following old source remains:

```rill
bytes inbuf[1024];
fn main(){openunit();let mut count=0;while nextbyte()!=65535{count=count+1;}closein();return count!=11;}
```

## Build and preserve the tool

```dos
COPY L03.RIL SOURCE.RIL
CHECK R0
COPY RESULT.IR SOURCE.IR
CHECK I0
COPY RESULT.ASM SOURCE.ASM
CHECK A0
COPY RESULT.COM L03.COM
```

Require compiler `OK RESULT.IR 0000005405`, translator `OK RESULT.ASM 0000014890 text bytes`, assembler `OK RESULT.COM 03926 bytes`, and each PASS before the following copy. VIEW.BAS must show L03.COM length 3926 and these first thirty-two bytes:

```text
FC 81 FC FE FF 74 03 E9 03 0F E8 5B 0B B4 4C CD 21 00 00 00 00 01 00 00 00 00 00 00 00 00 00 00
```

## Check the accepted input

Create M03.OBJ as plain ASCII:

```text
OBJ1
END
```

```dos
COPY M03.OBJ MAIN.OBJ
CHECK L03
```

CHECK must report PASS. This checkpoint creates no linked output. Its input handling is checked by its return status; its retained executable was inspected above.

## A rejection check

```dos
COPY RESULT.COM HOLD.COM
```

Create X03.OBJ:

```text
XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
```

```dos
COPY X03.OBJ MAIN.OBJ
CHECK L03
```

Require:

```text
LINK ERROR 00001 00001 CODE 00005
FAIL
```

```dos
COMP HOLD.COM RESULT.COM <NO.TXT
```

COMP must report no differences. An unexpected PASS fails the rejection. Require a fresh successful run before preserving any new output.
