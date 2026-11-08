+++
title = "18 \u00b7 Deleting text at either side"
weight = 18
description = "Delete one character or one complete line ending. Repaint the affected line, or the window when the line layout changes."
download = "E18.RIL"
download_group = "tools/edit86"
reader_names = 1
+++

Delete one character or one complete line ending. Repaint the affected line, or the window when the line layout changes.

Forward deletion removes bytes at gap by advancing gapend and reducing length. Backspace first moves the gap to the character on its left, then uses the same deletion. rightcount and leftcount keep CR/LF pairs together while accepting a lone terminator. Do nothing at either document boundary. Read the removed bytes before extending the gap; they still belong to the document until then. A deleted terminator changes line layout, while a plain deleted byte changes only its row.

## Enter the source

Copy E17.RIL to E18.RIL.

Keep the unchanged source. Apply these edits from the bottom of the old file upward; physical positions locate text and are not source to type.

### Edit 1

Unchanged source immediately before the edit:

```rill
    }
    dirty=1;
```

Insert after old physical line 514.

Insert:

```rill
    return 0;
}
fn erase(back){
    let mut n=rightcount();
    if back{
        n=leftcount();
        if n{
            copypos(target,gap);
            sub(target,n);
            movegap(target);
        }
    }
    if n{
        let mut c=peek(gap);
        let mut d=0;
        if n==2{
            copypos(probe,gap);
            add(probe,1);
            d=peek(probe);
        }
        rawdelete(n);
        dirty=1;
        if (c==13)|(c==10){
            allrows=1;
            layout=1;
        }
        else{
            onerow=1;
        }
    }
```

The following old source remains:

```rill
    return 0;
}
```

### Edit 2

Unchanged source immediately before the edit:

```rill
    return 0;
}
```

Insert after old physical line 497.

Insert:

```rill
fn rawdelete(n){
    add(gapend,n);
    sub(length,n);
    add(space,n);
    return 0;
}
```

The following old source remains:

```rill
fn typing(c,d,n){
    if load16(space+2)==0{
```

### Edit 3

Unchanged source immediately before the edit:

```rill
        movegap(target);
        layout=1;
```

Insert after old physical line 112.

Insert:

```rill
        return 0;
    }
    if k==264{
        erase(0);
        return 0;
    }
    if k==8{
        erase(1);
```

The following old source remains:

```rill
        return 0;
    }
```

## Build and preserve the program

```dos
COPY E18.RIL SOURCE.RIL
CHECK RILLED
COPY RESULT.IR SOURCE.IR
CHECK IRED
COPY RESULT.ASM SOURCE.ASM
CHECK A0
COPY RESULT.COM E18.COM
```

Require compiler `OK RESULT.IR 0000041187`, translator `OK RESULT.ASM 0000088844 text bytes`, assembler `OK RESULT.COM 19387 bytes`, and each PASS before the following copy. VIEW.BAS must report E18.COM length 19387 bytes, beginning with:

```text
FC 81 FC FE FF 74 03 E9 51 48 E8 A9 44 B4 4C CD 21 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
```

## The document fixture

Create T18.TXT with CR/LF after each displayed line:

```text
one
two
```

```dos
COPY T18.TXT EDIT.TXT
CHECK E18
```

Press Delete at the first byte, type !, then F2 and F10. Require PASS and exactly ten file bytes: `21 6E 65 0D 0A 74 77 6F 0D 0A`. Restore T18.TXT. End then Right crosses CR/LF as one action; Backspace there removes the whole pair. At document start Backspace must do nothing.

## If the check disagrees

Check the exact fixture and the freshly preserved executable first. For position errors, compare both words and the gap/space invariant. For file errors, inspect recovery names and keep the accepted input before another run.
