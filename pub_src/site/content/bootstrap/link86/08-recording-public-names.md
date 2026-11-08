+++
title = "08 \u00b7 Recording public names"
weight = 8
description = "Record complete public spellings and module-relative offsets in initialized forty-byte records. Check duplicates, extents and pass agreement."
download = "L08.RIL"
download_group = "tools/link86"
reader_names = 1
+++

Record complete public spellings and module-relative offsets in initialized forty-byte records. Check duplicates, extents and pass agreement.

Allocate 10240 bytes for 256 forty-byte records. Bytes 0–31 hold a terminated folded name; words at 32, 34 and 36 hold its relative value, input number and pass-two seen flag. Initialize all forty bytes before inserting an entry. An offset equal to module length may name its end; a larger offset is rejected.

## Enter the source

Copy L07.RIL to L08.RIL. Apply these edits from the bottom of the unchanged old file upward. Physical positions are locators, not source to type. Keep all other source.

### Edit 1

Unchanged source immediately before the edit:

```rill
    if inopen{close(input);inopen=0;}
    if outopen{close(output);outopen=0;}
    if own{if keep==0{delete("LINK.TMP");}}
```

Insert after old physical line 208.

Insert:

```rill
    if table{free(table);table=0;}
```

The following old source remains:

```rill
    print("LINK ERROR ");number(unit);putc(32);number(line);
    print(" CODE ");number(code);print("\r\n");exit(1);return 0;
```

### Edit 2

Unchanged source immediately before the edit:

```rill
    return 0;
}
```

Insert after old physical line 190.

Insert:

```rill
fn validname(){
    if toklen==0{fail(3);}
    let mut i=0;
    while i<toklen{
        let mut c=token[i];
        if (c!=95)&((c<65)|(c>90)){
            if (i==0)|(c<48)|(c>57){fail(3);}
        }
        i=i+1;
    }
    return 0;
}

fn find(){
    let mut n=0;
    while n<symbols{
        let mut i=0;let mut match=1;
        while i<=toklen{
            if get8(table,n*40+i)!=token[i]{match=0;}
            i=i+1;
        }
        if match{return n*40;}n=n+1;
    }
    return 65535;
}

fn definition(){
    scan();validname();let mut p=find();
    if pass==1{
        if p!=65535{fail(3);}if symbols==256{fail(5);}
        p=symbols*40;symbols=symbols+1;
        let mut i=0;while i<40{set8(table,p+i,0);i=i+1;}
        i=0;while i<toklen{set8(table,p+i,token[i]);i=i+1;}
    }else{
        if p==65535{fail(7);}
        if get16(table,p+36){fail(7);}set16(table,p+36,1);
    }
    scan();let mut value=hexvalue(4);finish();
    if pass==1{set16(table,p+32,value);set16(table,p+34,unit);}
    else{if (get16(table,p+32)!=value)|(get16(table,p+34)!=unit){fail(7);}}
    return 0;
}

fn modulecheck(size){
    let mut i=0;
    while i<symbols{
        let mut p=i*40;
        if get16(table,p+34)==unit{if get16(table,p+32)>size{fail(4);}}
        i=i+1;
    }
    return 0;
}
```

The following old source remains:

```rill
fn print(s){
    while load8(s){putc(load8(s));s=s+1;}return 0;
```

### Edit 3

Unchanged source immediately before the edit:

```rill
            }else{
                if same("END"){finish();done=1;}
                else{
```

Remove old physical positions 120–120:

```rill
                    if same("B"){bytesrecord();}else{fail(1);}
```

Replace with:

```rill
                    if same("B"){bytesrecord();}else{if same("P"){definition();}else{fail(1);}}
```

The following old source remains:

```rill
                }
            }
```

### Edit 4

Unchanged source immediately before the edit:

```rill
        if pass==1{unit=0;line=0;createout();}
        pass=pass+1;
    }
```

Remove old physical positions 46–46:

```rill
    unit=0;line=0;finishout();
```

Replace with:

```rill
    unit=0;line=0;let mut i=0;
    while i<symbols{if get16(table,i*40+36)!=1{fail(7);}i=i+1;}
    finishout();free(table);if status(){fail(6);}table=0;
```

The following old source remains:

```rill
    commit();report();return 0;
}
```

### Edit 5

Unchanged source immediately before the edit:

```rill
        while unit<=2{
            base=pc;openunit();records();closein();
            let mut size=pc-base;
```

Insert after old physical line 34.

Insert:

```rill
            modulecheck(size);
```

The following old source remains:

```rill
            if pass==1{
                if unit==1{firstsize=size;}else{secondsize=size;}
```

### Edit 6

Unchanged source immediately before the edit:

```rill
bytes token[32];
fn main(){
    unit=0;preflight();
```

Insert after old physical line 28.

Insert:

```rill
    table=alloc(10240);if status(){fail(6);}
```

The following old source remains:

```rill
    pass=1;
    while pass<=2{
```

### Edit 7

Unchanged source immediately before the edit:

```rill
let mut outopen=0;
let mut own=0;
let mut keep=0;
```

Insert after old physical line 7.

Insert:

```rill
let mut table=0;
let mut symbols=0;
```

The following old source remains:

```rill
let mut unit=1;
let mut pass=1;
```

## Build and preserve the tool

```dos
COPY L08.RIL SOURCE.RIL
CHECK R0
COPY RESULT.IR SOURCE.IR
CHECK I0
COPY RESULT.ASM SOURCE.ASM
CHECK A0
COPY RESULT.COM L08.COM
```

Require compiler `OK RESULT.IR 0000020975`, translator `OK RESULT.ASM 0000044316 text bytes`, assembler `OK RESULT.COM 10101 bytes`, and each PASS before the following copy. VIEW.BAS must show L08.COM length 10101 and these first thirty-two bytes:

```text
FC 81 FC FE FF 74 03 E9 22 27 E8 7A 23 B4 4C CD 21 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
```

## Check the accepted input

Create M08.OBJ as plain ASCII:

```text
OBJ1
B B8 00 4C CD 21
END
```

Create U08.OBJ:

```text
OBJ1
P LETTER 0000
B 41
END
```

```dos
COPY M08.OBJ MAIN.OBJ
COPY U08.OBJ UTIL.OBJ
CHECK L08
```

Require:

```text
OK RESULT.COM 00006 bytes
PASS
```

VIEW.BAS must show RESULT.COM length 6 and these complete bytes:

```text
B8 00 4C CD 21 41
```

Inspect this data/encoding fixture; do not execute it.

## A rejection check

```dos
COPY RESULT.COM HOLD.COM
```

Create X08.OBJ:

```text
OBJ1
P SAME 0000
P SAME 0000
END
```

```dos
COPY X08.OBJ MAIN.OBJ
CHECK L08
```

Require:

```text
LINK ERROR 00001 00003 CODE 00003
FAIL
```

```dos
COMP HOLD.COM RESULT.COM <NO.TXT
```

COMP must report no differences. An unexpected PASS fails the rejection. Require a fresh successful run before preserving any new output.
