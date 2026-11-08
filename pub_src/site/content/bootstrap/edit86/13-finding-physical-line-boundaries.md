+++
title = "13 \u00b7 Finding physical line boundaries"
weight = 13
description = "Locate beginnings and endings without building a full line index. Treat CR/LF as a pair while also accepting bare CR and LF."
download = "E13.RIL"
download_group = "tools/edit86"
reader_names = 1
+++

Locate beginnings and endings without building a full line index. Treat CR/LF as a pair while also accepting bare CR and LF.

A line ends before CR or LF; nextline consumes CR/LF together and accepts either byte alone. linebegin scans backward to the byte after a terminator. prevline steps over the preceding terminator before finding that line's beginning. Empty lines and a final unterminated line need no special stored records. The routines use logical positions and `peek`, so page boundaries and the gap do not change their meaning. Their position arguments may alias as shown; probe is private scratch for the backward scans.

## Enter the source

Copy E12.RIL to E13.RIL.

Keep the unchanged source. Apply these edits from the bottom of the old file upward; physical positions locate text and are not source to type.

### Edit 1

Unchanged source immediately before the edit:

```rill
    return 0;
}
```

Insert after old physical line 236.

Insert:

```rill
fn linebegin(d,p){
    copypos(d,p);
    while (load16(d)!=0)|(load16(d+2)!=0){
        copypos(probe,d);
        sub(probe,1);
        let mut c=peek(probe);
        if (c==13)|(c==10){
            return 0;
        }
        sub(d,1);
    }
    return 0;
}
fn lineend(d,p){
    copypos(d,p);
    while before(d,length){
        let mut c=peek(d);
        if (c==13)|(c==10){
            return 0;
        }
        add(d,1);
    }
    return 0;
}
fn nextline(d,p){
    lineend(d,p);
    if before(d,length){
        let mut c=peek(d);
        add(d,1);
        if (c==13)&before(d,length){
            if peek(d)==10{
                add(d,1);
            }
        }
    }
    return 0;
}
fn prevline(d,p){
    linebegin(d,p);
    if (load16(d)!=0)|(load16(d+2)!=0){
        sub(d,1);
        if peek(d)==10{
            if (load16(d)!=0)|(load16(d+2)!=0){
                copypos(probe,d);
                sub(probe,1);
                if peek(probe)==13{
                    sub(d,1);
                }
            }
        }
        linebegin(d,d);
    }
    return 0;
}
```

The following old source remains:

```rill
fn reserved(){
    let mut found=exists("EDIT.TMP");
```

### Edit 2

Unchanged source immediately before the edit:

```rill
    copypos(gap,length);
    store16(target,5);
```

Remove old physical positions 32–37:

```rill
    if before(length,target){
        fatal("Fixture is shorter than the gap position.");
    }
    movegap(target);
    let mut saved=savefile();
    return cleanup()|!saved;
```

Replace with:

```rill
    linebegin(start,target);
    lineend(at,start);
    nextline(other,start);
    prevline(work,other);
    let mut bad=(load16(start)!=5)|(load16(at)!=8)|(load16(other)!=10)|(load16(work)!=5);
    return cleanup()|bad;
```

The following old source remains:

```rill
}
fn filename(){
```

### Edit 3

Unchanged source immediately before the edit:

```rill
    copypos(gapend,cap);
    copypos(space,cap);
```

Remove old physical positions 25–27:

```rill
    if reserved(){
        fatal("Recovery files EDIT.TMP or EDIT.BAK already exist.");
    }
```

There is no replacement source.

The following old source remains:

```rill
    allocate();
    loadfile();
```

### Edit 4

Unchanged source immediately before the edit:

```rill
bytes target[4];
bytes at[4];
```

Insert after old physical line 17.

Insert:

```rill
bytes probe[4];
```

The following old source remains:

```rill
bytes work[4];
bytes other[4];
```

### Edit 5

Unchanged source immediately before the edit:

```rill
bytes cap[4];
bytes target[4];
```

Insert after old physical line 16.

Insert:

```rill
bytes start[4];
```

The following old source remains:

```rill
bytes at[4];
bytes work[4];
```

## Build and preserve the program

```dos
COPY E13.RIL SOURCE.RIL
CHECK RILLED
COPY RESULT.IR SOURCE.IR
CHECK IRED
COPY RESULT.ASM SOURCE.ASM
CHECK A0
COPY RESULT.COM E13.COM
```

Require compiler `OK RESULT.IR 0000022097`, translator `OK RESULT.ASM 0000053540 text bytes`, assembler `OK RESULT.COM 13322 bytes`, and each PASS before the following copy. VIEW.BAS must report E13.COM length 13322 bytes, beginning with:

```text
FC 81 FC FE FF 74 03 E9 A0 30 E8 F8 2C B4 4C CD 21 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
```

## The document fixture

Create T13.TXT with CR/LF after each displayed line:

```text
one
two
```

```dos
COPY T13.TXT EDIT.TXT
CHECK E13
```

Require PASS. The beginning, end and following-line positions must be five, eight and ten, and stepping back must recover five. Repeat with an empty document: require FAIL, since these diagnostic positions deliberately describe the supplied two-line fixture. The line routines themselves accept empty documents.

## If the check disagrees

Check the exact fixture and the freshly preserved executable first. For position errors, compare both words and the gap/space invariant. For file errors, inspect recovery names and keep the accepted input before another run.
