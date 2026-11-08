+++
title = "19 \u00b7 Remembering edits for undo"
weight = 19
description = "Keep a bounded ring of edit records in one extra block. Reverse insertion or deletion without copying the complete document."
download = "E19.RIL"
download_group = "tools/edit86"
reader_names = 1
+++

Keep a bounded ring of edit records in one extra block. Reverse insertion or deletion without copying the complete document.

Allocate a separate 16384-byte undo block only now. Each eight-byte record holds kind, count, a paired logical position and up to two deleted bytes. uhead selects the next slot; ucount retains at most 2048 edits. On overflow the oldest record is replaced. Remember an insertion before consuming space and a deletion before discarding its bytes. Undo moves the gap to the saved position, removes an inserted span or restores deleted bytes, and conservatively marks the document dirty. There is no redo and no saved copy of the whole document.

## Enter the source

Copy E18.RIL to E19.RIL.

Keep the unchanged source. Apply these edits from the bottom of the old file upward; physical positions locate text and are not source to type.

### Edit 1

Unchanged source immediately before the edit:

```rill
        }
    }
```

Insert after old physical line 558.

Insert:

```rill
    return 0;
}
fn undone(){
    if ucount==0{
        message="No earlier edit remains in undo storage.";
        return 0;
    }
    uhead=(uhead+2047)&2047;
    ucount=ucount-1;
    let mut p=uhead*8;
    let mut kind=get8(undo,p);
    let mut n=get8(undo,p+1);
    store16(target,get16(undo,p+2));
    store16(target+2,get16(undo,p+4));
    let mut c=get8(undo,p+6);
    let mut d=get8(undo,p+7);
    movegap(target);
    if kind==1{
        rawdelete(n);
    }
    else{
        rawinsert(c);
        if n==2{
            rawinsert(d);
        }
    }
    dirty=1;
    allrows=1;
    layout=1;
```

The following old source remains:

```rill
    return 0;
}
```

### Edit 2

Unchanged source immediately before the edit:

```rill
            d=peek(probe);
        }
```

Insert after old physical line 548.

Insert:

```rill
        remember(2,n,c,d);
```

The following old source remains:

```rill
        rawdelete(n);
        dirty=1;
```

### Edit 3

Unchanged source immediately before the edit:

```rill
        }
    }
```

Insert after old physical line 518.

Insert:

```rill
    remember(1,n,0,0);
```

The following old source remains:

```rill
    rawinsert(c);
    if n==2{
```

### Edit 4

Unchanged source immediately before the edit:

```rill
    return 0;
}
```

Insert after old physical line 511.

Insert:

```rill
fn remember(kind,n,c,d){
    let mut p=uhead*8;
    set8(undo,p,kind);
    set8(undo,p+1,n);
    set16(undo,p+2,load16(gap));
    set16(undo,p+4,load16(gap+2));
    set8(undo,p+6,c);
    set8(undo,p+7,d);
    if status(){
        fatal("Undo storage failed.");
    }
    uhead=(uhead+1)&2047;
    if ucount<2048{
        ucount=ucount+1;
    }
    return 0;
}
```

The following old source remains:

```rill
fn typing(c,d,n){
    if load16(space+2)==0{
```

### Edit 5

Unchanged source immediately before the edit:

```rill
        }
        i=i+1;
```

Insert after old physical line 216.

Insert:

```rill
    }
    if undo{
        free(undo);
        if status(){
            bad=1;
        }
        undo=0;
```

The following old source remains:

```rill
    }
    return bad;
```

### Edit 6

Unchanged source immediately before the edit:

```rill
        i=i+1;
    }
```

Insert after old physical line 201.

Insert:

```rill
    undo=alloc(16384);
    if status(){
        fatal("Not enough DOS memory for undo storage.");
    }
```

The following old source remains:

```rill
    return 0;
}
```

### Edit 7

Unchanged source immediately before the edit:

```rill
    if k==265{
        savefile();
```

Insert after old physical line 73.

Insert:

```rill
        return 0;
    }
    if k==267{
        undone();
        vertical=0;
```

The following old source remains:

```rill
        return 0;
    }
```

### Edit 8

Unchanged source immediately before the edit:

```rill
// EDIT86 construction checkpoint.
```

Insert after old physical line 1.

Insert:

```rill
let mut undo=0;
let mut uhead=0;
let mut ucount=0;
```

The following old source remains:

```rill
let mut input=0;
let mut inopen=0;
```

## Build and preserve the program

```dos
COPY E19.RIL SOURCE.RIL
CHECK RILLED
COPY RESULT.IR SOURCE.IR
CHECK IRED
COPY RESULT.ASM SOURCE.ASM
CHECK A0
COPY RESULT.COM E19.COM
```

Require compiler `OK RESULT.IR 0000044523`, translator `OK RESULT.ASM 0000095700 text bytes`, assembler `OK RESULT.COM 20506 bytes`, and each PASS before the following copy. VIEW.BAS must report E19.COM length 20506 bytes, beginning with:

```text
FC 81 FC FE FF 74 03 E9 B0 4C E8 08 49 B4 4C CD 21 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
```

## The document fixture

Create T19.TXT with CR/LF after each displayed line:

```text
one
two
```

```dos
COPY T19.TXT EDIT.TXT
CHECK E19
```

Press Delete, type !, then F4 twice. Save with F2 and leave with F10. Require CHECK PASS and COMP equality with T19.TXT. Another F4 reports that no earlier edit remains. Undoing a line ending restores both CR and LF; navigation alone never creates an undo record.

## If the check disagrees

Check the exact fixture and the freshly preserved executable first. For position errors, compare both words and the gap/space invariant. For file errors, inspect recovery names and keep the accepted input before another run.
