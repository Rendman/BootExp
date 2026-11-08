+++
title = "06 \u00b7 Publishing the accepted image"
weight = 6
description = "Publish a closed temporary file as RESULT.COM, retaining the accepted image on source rejection and recovery files after a failed restoration."
download = "L06.RIL"
download_group = "tools/link86"
reader_names = 1
+++

Publish a closed temporary file as RESULT.COM, retaining the accepted image on source rejection and recovery files after a failed restoration.

## Enter the source

Copy L05.RIL to L06.RIL. Apply these edits from the bottom of the unchanged old file upward. Physical positions are locators, not source to type. Keep all other source.

### Edit 1

Unchanged source immediately before the edit:

```rill
    return 0;
}
```

Insert after old physical line 162.

Insert:

```rill
fn report(){print("OK RESULT.COM ");number(pc);print(" bytes\r\n");return 0;}
```

The following old source remains:

```rill
fn fail(code){
    if inopen{close(input);inopen=0;}
```

### Edit 2

Unchanged source immediately before the edit:

```rill

fn finishout(){flush();close(output);if status(){fail(6);}outopen=0;return 0;}
```

Remove old physical positions 149–149:

```rill
fn preflight(){if exists("LINK.TMP"){fail(8);}if status(){fail(6);}return 0;}
```

Replace with:

```rill
fn preflight(){
    if exists("LINK.TMP"){fail(8);}if status(){fail(6);}
    if exists("LINK.BAK"){fail(8);}if status(){fail(6);}return 0;
}

fn commit(){
    let mut backup=exists("RESULT.COM");if status(){fail(6);}
    if backup{rename("RESULT.COM","LINK.BAK");if status(){fail(6);}}
    rename("LINK.TMP","RESULT.COM");
    if status(){
        if backup{rename("LINK.BAK","RESULT.COM");if status(){keep=1;}}
        fail(6);
    }
    own=0;
    if backup{delete("LINK.BAK");if status(){keep=1;fail(6);}}
    return 0;
}
```

The following old source remains:

```rill

fn print(s){
```

### Edit 3

Unchanged source immediately before the edit:

```rill
bytes outbuf[1024];
bytes source[121];
bytes token[32];
```

Remove old physical positions 24–24:

```rill
fn main(){preflight();pass=2;openunit();createout();records();closein();finishout();print("OK LINK.TMP ");number(pc);print(" bytes\r\n");return 0;}
```

Replace with:

```rill
fn main(){preflight();pass=2;openunit();createout();records();closein();unit=0;line=0;finishout();commit();report();return 0;}
```

The following old source remains:

```rill

fn openunit(){
```

## Build and preserve the tool

```dos
COPY L06.RIL SOURCE.RIL
CHECK R0
COPY RESULT.IR SOURCE.IR
CHECK I0
COPY RESULT.ASM SOURCE.ASM
CHECK A0
COPY RESULT.COM L06.COM
```

Require compiler `OK RESULT.IR 0000014111`, translator `OK RESULT.ASM 0000031978 text bytes`, assembler `OK RESULT.COM 07892 bytes`, and each PASS before the following copy. VIEW.BAS must show L06.COM length 7892 and these first thirty-two bytes:

```text
FC 81 FC FE FF 74 03 E9 81 1E E8 D9 1A B4 4C CD 21 00 00 00 00 00 00 00 00 00 00 00 00 01 00 01
```

## Check the accepted input

Create M06.OBJ as plain ASCII:

```text
OBJ1
B B8 00 4C CD 21
END
```

```dos
COPY M06.OBJ MAIN.OBJ
CHECK L06
```

Require:

```text
OK RESULT.COM 00005 bytes
PASS
```

VIEW.BAS must show RESULT.COM length 5 and these complete bytes:

```text
B8 00 4C CD 21
```

Inspect this data/encoding fixture; do not execute it.

## A rejection check

```dos
COPY RESULT.COM HOLD.COM
```

Create X06.OBJ:

```text
OBJ1
B 90
END
B 90
```

```dos
COPY X06.OBJ MAIN.OBJ
CHECK L06
```

Require:

```text
LINK ERROR 00001 00004 CODE 00001
FAIL
```

```dos
COMP HOLD.COM RESULT.COM <NO.TXT
```

COMP must report no differences. An unexpected PASS fails the rejection. Require a fresh successful run before preserving any new output.
