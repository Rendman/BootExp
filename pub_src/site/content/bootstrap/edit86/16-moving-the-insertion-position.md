+++
title = "16 \u00b7 Moving the insertion position"
weight = 16
description = "Connect navigation keys to the gap and window. Preserve the preferred column for vertical movement and keep the cursor visible after a scroll."
download = "E16.RIL"
download_group = "tools/edit86"
reader_names = 1
+++

Connect navigation keys to the gap and window. Preserve the preferred column for vertical movement and keep the cursor visible after a scroll.

The loop refreshes, reads one event and dispatches it through small returning branches. Left and right cross a CR/LF pair as one line ending. Home and End stay on the line; F6 and F7 select document start and end. Up/down preserve a preferred visual column, while Page Up/Down repeat line movement twenty-four times. A nonvertical command ends that preference. Moving across a terminator requests a new layout; ordinary motion within a line needs only cursor placement. Navigation leaves dirty clear and makes no file writes.

## Enter the source

Copy E15.RIL to E16.RIL.

Keep the unchanged source. Apply these edits from the bottom of the old file upward; physical positions locate text and are not source to type.

### Edit 1

Unchanged source immediately before the edit:

```rill
        add(d,1);
    }
```

Insert after old physical line 339.

Insert:

```rill
    return 0;
}
fn leftcount(){
    if (load16(gap)==0)&(load16(gap+2)==0){
        return 0;
    }
    copypos(probe,gap);
    sub(probe,1);
    if peek(probe)==10{
        if (load16(probe)!=0)|(load16(probe+2)!=0){
            sub(probe,1);
            if peek(probe)==13{
                return 2;
            }
        }
    }
    return 1;
}
fn rightcount(){
    if !before(gap,length){
        return 0;
    }
    if peek(gap)==13{
        copypos(probe,gap);
        add(probe,1);
        if before(probe,length){
            if peek(probe)==10{
                return 2;
            }
        }
    }
    return 1;
}
fn left(){
    let mut n=leftcount();
    if n{
        copypos(target,gap);
        sub(target,n);
        let mut c=peek(target);
        if (c==13)|(c==10){
            layout=1;
        }
        movegap(target);
    }
    return 0;
}
fn right(){
    let mut n=rightcount();
    if n{
        let mut c=peek(gap);
        if (c==13)|(c==10){
            layout=1;
        }
        copypos(target,gap);
        add(target,n);
        movegap(target);
    }
    return 0;
}
fn updown(down,count){
    if vertical==0{
        column(prefer,start,gap);
        vertical=1;
    }
    copypos(target,start);
    while count{
        if down{
            nextline(target,target);
        }
        else{
            prevline(target,target);
        }
        count=count-1;
    }
    toward(target,target,prefer);
    movegap(target);
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
    }
    active=1;
```

Remove old physical positions 51–53:

```rill
    refresh();
    let mut k=key();
    return cleanup()|(k!=266);
```

Replace with:

```rill
    while 1{
        refresh();
        let mut k=key();
        if status(){
            fatal("Keyboard service failed.");
        }
        message=0;
        if k==266{
            return cleanup();
        }
        command(k);
    }
    return 0;
}
fn command(k){
    if k==265{
        savefile();
        return 0;
    }
    if (k>=258)&(k<=259){
        updown(k==259,1);
        return 0;
    }
    if (k>=262)&(k<=263){
        updown(k==263,24);
        return 0;
    }
    vertical=0;
    if k==256{
        left();
        return 0;
    }
    if k==257{
        right();
        return 0;
    }
    if k==260{
        copypos(target,start);
        movegap(target);
        return 0;
    }
    if k==261{
        lineend(target,gap);
        movegap(target);
        return 0;
    }
    if k==270{
        zero(target);
        movegap(target);
        layout=1;
        return 0;
    }
    if k==271{
        copypos(target,length);
        movegap(target);
        layout=1;
        return 0;
    }
    return 0;
```

The following old source remains:

```rill
}
fn filename(){
```

### Edit 3

Unchanged source immediately before the edit:

```rill
bytes col[4];
bytes scroll[4];
```

Insert after old physical line 25.

Insert:

```rill
bytes prefer[4];
```

The following old source remains:

```rill
bytes oldtop[4];
bytes oldscroll[4];
```

### Edit 4

Unchanged source immediately before the edit:

```rill
let mut message=0;
let mut crow=0;
```

Insert after old physical line 11.

Insert:

```rill
let mut vertical=0;
```

The following old source remains:

```rill
let mut layout=1;
let mut allrows=1;
```

## Build and preserve the program

```dos
COPY E16.RIL SOURCE.RIL
CHECK RILLED
COPY RESULT.IR SOURCE.IR
CHECK IRED
COPY RESULT.ASM SOURCE.ASM
CHECK A0
COPY RESULT.COM E16.COM
```

Require compiler `OK RESULT.IR 0000036851`, translator `OK RESULT.ASM 0000080213 text bytes`, assembler `OK RESULT.COM 17933 bytes`, and each PASS before the following copy. VIEW.BAS must report E16.COM length 17933 bytes, beginning with:

```text
FC 81 FC FE FF 74 03 E9 A3 42 E8 FB 3E B4 4C CD 21 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
```

## The document fixture

Create T16.TXT with CR/LF after each displayed line:

```text
one
two
```

```dos
COPY T16.TXT EDIT.TXT
CHECK E16
```

Try arrows, Home, End, Page Up, Page Down, F6 and F7. The insertion cursor must remain in the document window. F2 saves an unchanged file. F10 returns CHECK PASS; COMP against T16.TXT must show no difference. At the first byte, Left does nothing; at EOF, Right does nothing.

## If the check disagrees

Check the exact fixture and the freshly preserved executable first. For position errors, compare both words and the gap/space invariant. For file errors, inspect recovery names and keep the accepted input before another run.
