+++
title = "07 \u00b7 Placing two modules"
weight = 7
description = "Place MAIN.OBJ first and UTIL.OBJ second. Count both modules on pass one, then reopen them and stream the same layout on pass two."
download = "L07.RIL"
download_group = "tools/link86"
reader_names = 1
+++

Place MAIN.OBJ first and UTIL.OBJ second. Count both modules on pass one, then reopen them and stream the same layout on pass two.

## Enter the source

Copy L06.RIL to L07.RIL. Apply these edits from the bottom of the unchanged old file upward. Physical positions are locators, not source to type. Keep all other source.

### Edit 1

Unchanged source immediately before the edit:

```rill
bytes outbuf[1024];
bytes source[121];
bytes token[32];
```

Remove old physical positions 24–24:

```rill
fn main(){preflight();pass=2;openunit();createout();records();closein();unit=0;line=0;finishout();commit();report();return 0;}
```

Replace with:

```rill
fn main(){
    unit=0;preflight();
    pass=1;
    while pass<=2{
        pc=0;unit=1;
        while unit<=2{
            base=pc;openunit();records();closein();
            let mut size=pc-base;
            if pass==1{
                if unit==1{firstsize=size;}else{secondsize=size;}
            }else{
                if unit==1{if size!=firstsize{fail(7);}}
                else{if size!=secondsize{fail(7);}}
            }
            unit=unit+1;
        }
        if pass==1{unit=0;line=0;createout();}
        pass=pass+1;
    }
    unit=0;line=0;finishout();
    commit();report();return 0;
}
```

The following old source remains:

```rill

fn openunit(){
```

### Edit 2

Unchanged source immediately before the edit:

```rill
let mut pos=0;
let mut toklen=0;
let mut pc=0;
```

Insert after old physical line 18.

Insert:

```rill
let mut base=0;
let mut firstsize=0;
let mut secondsize=0;
```

The following old source remains:

```rill
let mut outlen=0;
bytes inbuf[1024];
```

## Build and preserve the tool

```dos
COPY L07.RIL SOURCE.RIL
CHECK R0
COPY RESULT.IR SOURCE.IR
CHECK I0
COPY RESULT.ASM SOURCE.ASM
CHECK A0
COPY RESULT.COM L07.COM
```

Require compiler `OK RESULT.IR 0000015428`, translator `OK RESULT.ASM 0000034281 text bytes`, assembler `OK RESULT.COM 08291 bytes`, and each PASS before the following copy. VIEW.BAS must show L07.COM length 8291 and these first thirty-two bytes:

```text
FC 81 FC FE FF 74 03 E9 10 20 E8 68 1C B4 4C CD 21 00 00 00 00 00 00 00 00 00 00 00 00 01 00 01
```

## Check the accepted input

Create M07.OBJ as plain ASCII:

```text
OBJ1
B B8 00 4C CD 21
END
```

Create U07.OBJ:

```text
OBJ1
B 41 42
END
```

```dos
COPY M07.OBJ MAIN.OBJ
COPY U07.OBJ UTIL.OBJ
CHECK L07
```

Require:

```text
OK RESULT.COM 00007 bytes
PASS
```

VIEW.BAS must show RESULT.COM length 7 and these complete bytes:

```text
B8 00 4C CD 21 41 42
```

Inspect this data/encoding fixture; do not execute it.

## A rejection check

```dos
COPY RESULT.COM HOLD.COM
```

Create X07.OBJ:

```text
OBJ1
B 90
```

```dos
COPY X07.OBJ MAIN.OBJ
CHECK L07
```

Require:

```text
LINK ERROR 00001 00002 CODE 00001
FAIL
```

```dos
COMP HOLD.COM RESULT.COM <NO.TXT
```

COMP must report no differences. An unexpected PASS fails the rejection. Require a fresh successful run before preserving any new output.
