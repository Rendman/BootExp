+++
title = "14 \u00b7 Measuring columns and tab stops"
weight = 14
description = "Count visual columns separately from byte positions. Expand tabs to stops eight columns apart and retain the desired column across unequal line lengths."
download = "E14.RIL"
download_group = "tools/edit86"
reader_names = 1
+++

Count visual columns separately from byte positions. Expand tabs to stops eight columns apart and retain the desired column across unequal line lengths.

A column is a visual distance, not a file offset. Ordinary bytes occupy one cell; a tab occupies 8 minus the current column modulo 8. Keep columns as paired words too, because an unusually long line may exceed 65535 cells. `toward` walks a line until another character would pass the wanted column or until a terminator. It stops before a tab that would overshoot. The fixture contains a literal tab between T and X: X begins in column eight, and the position after X has column nine.

## Enter the source

Copy E13.RIL to E14.RIL.

Keep the unchanged source. Apply these edits from the bottom of the old file upward; physical positions locate text and are not source to type.

### Edit 1

Unchanged source immediately before the edit:

```rill
    return 0;
}
```

Insert after old physical line 289.

Insert:

```rill
fn column(d,from,to){
    zero(d);
    copypos(probe,from);
    while before(probe,to){
        let mut c=peek(probe);
        if c==9{
            add(d,8-(load16(d)&7));
        }
        else{
            add(d,1);
        }
        add(probe,1);
    }
    return 0;
}
fn toward(d,from,wanted){
    copypos(d,from);
    zero(col);
    while before(d,length){
        let mut c=peek(d);
        if (c==13)|(c==10){
            return 0;
        }
        let mut width=1;
        if c==9{
            width=8-(load16(col)&7);
        }
        add(col,width);
        if before(wanted,col){
            return 0;
        }
        add(d,1);
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
    loadfile();
    copypos(gap,length);
```

Remove old physical positions 30–35:

```rill
    store16(target,5);
    linebegin(start,target);
    lineend(at,start);
    nextline(other,start);
    prevline(work,other);
    let mut bad=(load16(start)!=5)|(load16(at)!=8)|(load16(other)!=10)|(load16(work)!=5);
```

Replace with:

```rill
    zero(start);
    store16(target,3);
    column(col,start,target);
    let mut bad=(load16(col)!=9)|(load16(col+2)!=0);
    store16(prefer,8);
    toward(target,start,prefer);
    bad=bad|(load16(target)!=2);
```

The following old source remains:

```rill
    return cleanup()|bad;
}
```

### Edit 3

Unchanged source immediately before the edit:

```rill
bytes target[4];
bytes start[4];
```

Insert after old physical line 17.

Insert:

```rill
bytes col[4];
bytes prefer[4];
```

The following old source remains:

```rill
bytes at[4];
bytes probe[4];
```

## Build and preserve the program

```dos
COPY E14.RIL SOURCE.RIL
CHECK RILLED
COPY RESULT.IR SOURCE.IR
CHECK IRED
COPY RESULT.ASM SOURCE.ASM
CHECK A0
COPY RESULT.COM E14.COM
```

Require compiler `OK RESULT.IR 0000023742`, translator `OK RESULT.ASM 0000056236 text bytes`, assembler `OK RESULT.COM 13819 bytes`, and each PASS before the following copy. VIEW.BAS must report E14.COM length 13819 bytes, beginning with:

```text
FC 81 FC FE FF 74 03 E9 91 32 E8 E9 2E B4 4C CD 21 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
```

## The document fixture

Create T14.TXT with CR/LF after each displayed line and a literal tab between T and X:

```text
T	X
abc
```

```dos
COPY T14.TXT EDIT.TXT
CHECK E14
```

Require PASS: the position after T, tab and X is visual column nine, and reaching column eight stops before X at byte position two. Repeat with T13.TXT in EDIT.TXT: require FAIL because that file does not contain the tab fixture. No file is saved by either run.

## If the check disagrees

Check the exact fixture and the freshly preserved executable first. For position errors, compare both words and the gap/space invariant. For file errors, inspect recovery names and keep the accepted input before another run.
