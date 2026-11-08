+++
title = "15 \u00b7 Painting a window on the document"
weight = 15
description = "Draw twenty-four document rows and one status row. Keep a horizontal window for long lines and show control bytes without changing the stored file."
download = "E15.RIL"
download_group = "tools/edit86"
reader_names = 1
+++

Draw twenty-four document rows and one status row. Keep a horizontal window for long lines and show control bytes without changing the stored file.

`paintrow` initializes an eighty-byte row, expands tabs into spaces, and substitutes a dot for other controls and high bytes. The underlying text is unchanged. `top` names the first displayed line; `scroll` is the first visible visual column. `refresh` keeps the insertion position within twenty-four rows and eighty columns, then puts the status on row twenty-four. It remembers the previous top and horizontal origin, repainting the whole window when either changes. `layout`, `allrows` and `onerow` distinguish line-layout work from a changed row. The returned hardware cursor is always in a document row.

## Enter the source

Copy E14.RIL to E15.RIL.

Keep the unchanged source. Apply these edits from the bottom of the old file upward; physical positions locate text and are not source to type.

### Edit 1

Unchanged source immediately before the edit:

```rill
fn cleanup(){
    let mut bad=0;
```

Insert after old physical line 446.

Insert:

```rill
    if active{
        vend();
        if status(){
            bad=1;
        }
        active=0;
    }
```

The following old source remains:

```rill
    if inopen{
        close(input);
```

### Edit 2

Unchanged source immediately before the edit:

```rill
    return 0;
}
```

Insert after old physical line 327.

Insert:

```rill
fn statusline(s){
    let mut i=0;
    while i<80{
        rowbuf[i]=32;
        i=i+1;
    }
    i=0;
    while load8(s+i){
        if i==80{
            vpos(1920);
            vwrite(rowbuf,80);
            return 0;
        }
        rowbuf[i]=load8(s+i);
        i=i+1;
    }
    vpos(1920);
    vwrite(rowbuf,80);
    return 0;
}
fn paintrow(row,p){
    let mut i=0;
    while i<80{
        rowbuf[i]=32;
        i=i+1;
    }
    zero(col);
    while before(p,length){
        let mut c=peek(p);
        if (c==13)|(c==10){
            nextline(p,p);
            vpos(row*80);
            vwrite(rowbuf,80);
            return 0;
        }
        let mut width=1;
        if c==9{
            width=8-(load16(col)&7);
            c=32;
        }
        else{
            if (c<32)|(c>126){
                c=46;
            }
        }
        while width{
            if !before(col,scroll){
                difference(work,col,scroll);
                if (load16(work+2)==0)&(load16(work)<80){
                    rowbuf[load16(work)]=c;
                }
            }
            add(col,1);
            width=width-1;
        }
        add(p,1);
    }
    vpos(row*80);
    vwrite(rowbuf,80);
    return 0;
}
fn refresh(){
    if layout{
        linebegin(start,gap);
        if before(start,top){
            copypos(top,start);
        }
        copypos(target,top);
        crow=0;
        while before(target,start)&(crow<24){
            nextline(target,target);
            crow=crow+1;
        }
        if crow==24{
            copypos(top,start);
            let mut i=0;
            while i<23{
                prevline(top,top);
                i=i+1;
            }
            copypos(target,top);
            crow=0;
            while before(target,start){
                nextline(target,target);
                crow=crow+1;
            }
        }
        layout=0;
    }
    column(col,start,gap);
    if before(col,scroll){
        copypos(scroll,col);
    }
    else{
        difference(work,col,scroll);
        if (load16(work+2)!=0)|(load16(work)>=80){
            copypos(scroll,col);
            sub(scroll,79);
        }
    }
    difference(work,col,scroll);
    let mut x=load16(work);
    if !equal(top,oldtop)|!equal(scroll,oldscroll){
        allrows=1;
    }
    if allrows{
        copypos(at,top);
        let mut row=0;
        while row<24{
            paintrow(row,at);
            row=row+1;
        }
    }
    else{
        if onerow{
            copypos(at,start);
            paintrow(crow,at);
        }
    }
    copypos(oldtop,top);
    copypos(oldscroll,scroll);
    allrows=0;
    onerow=0;
    if message{
        statusline(message);
    }
    else{
        if dirty{
            statusline("EDIT86 EDIT.TXT *  F2 Save F3 Find F4 Undo F5 Next F10 Quit");
        }
        else{
            statusline("EDIT86 EDIT.TXT    F2 Save F3 Find F4 Undo F5 Next F10 Quit");
        }
    }
    vpos(crow*80+x);
    if status(){
        fatal("Screen service failed.");
    }
    return 0;
}
```

The following old source remains:

```rill
fn reserved(){
    let mut found=exists("EDIT.TMP");
```

### Edit 3

Unchanged source immediately before the edit:

```rill
    loadfile();
    copypos(gap,length);
```

Remove old physical positions 32–39:

```rill
    zero(start);
    store16(target,3);
    column(col,start,target);
    let mut bad=(load16(col)!=9)|(load16(col+2)!=0);
    store16(prefer,8);
    toward(target,start,prefer);
    bad=bad|(load16(target)!=2);
    return cleanup()|bad;
```

Replace with:

```rill
    copypos(target,top);
    movegap(target);
    vbegin();
    if status(){
        fatal("EDIT86 requires an 80-column text screen.");
    }
    active=1;
    refresh();
    let mut k=key();
    return cleanup()|(k!=266);
```

The following old source remains:

```rill
}
fn filename(){
```

### Edit 4

Unchanged source immediately before the edit:

```rill
    copypos(gapend,cap);
    copypos(space,cap);
```

Insert after old physical line 28.

Insert:

```rill
    if reserved(){
        fatal("Recovery files EDIT.TMP or EDIT.BAK already exist.");
    }
```

The following old source remains:

```rill
    allocate();
    loadfile();
```

### Edit 5

Unchanged source immediately before the edit:

```rill
bytes other[4];
bytes io[4096];
```

Insert after old physical line 24.

Insert:

```rill
bytes rowbuf[80];
```

The following old source remains:

```rill
fn main(){
    store16(cap+2,4);
```

### Edit 6

Unchanged source immediately before the edit:

```rill
bytes start[4];
bytes col[4];
```

Remove old physical positions 19–19:

```rill
bytes prefer[4];
```

Replace with:

```rill
bytes scroll[4];
bytes oldtop[4];
bytes oldscroll[4];
```

The following old source remains:

```rill
bytes at[4];
bytes probe[4];
```

### Edit 7

Unchanged source immediately before the edit:

```rill
bytes cap[4];
bytes target[4];
```

Insert after old physical line 16.

Insert:

```rill
bytes top[4];
```

The following old source remains:

```rill
bytes start[4];
bytes col[4];
```

### Edit 8

Unchanged source immediately before the edit:

```rill
let mut dirty=0;
let mut message=0;
```

Insert after old physical line 9.

Insert:

```rill
let mut crow=0;
let mut layout=1;
let mut allrows=1;
let mut onerow=0;
```

The following old source remains:

```rill
bytes pages[16];
bytes gap[4];
```

### Edit 9

Unchanged source immediately before the edit:

```rill
let mut own=0;
let mut keep=0;
```

Insert after old physical line 7.

Insert:

```rill
let mut active=0;
```

The following old source remains:

```rill
let mut dirty=0;
let mut message=0;
```

## Build and preserve the program

```dos
COPY E15.RIL SOURCE.RIL
CHECK RILLED
COPY RESULT.IR SOURCE.IR
CHECK IRED
COPY RESULT.ASM SOURCE.ASM
CHECK A0
COPY RESULT.COM E15.COM
```

Require compiler `OK RESULT.IR 0000031010`, translator `OK RESULT.ASM 0000070076 text bytes`, assembler `OK RESULT.COM 16133 bytes`, and each PASS before the following copy. VIEW.BAS must report E15.COM length 16133 bytes, beginning with:

```text
FC 81 FC FE FF 74 03 E9 9B 3B E8 F3 37 B4 4C CD 21 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
```

## The document fixture

Create T15.TXT with CR/LF after each displayed line:

```text
one
two
```

```dos
COPY T15.TXT EDIT.TXT
CHECK E15
```

The screen must show one on the first row, two on the next and the help line on the last row. Press F10; CHECK must report PASS. COMP must still find EDIT.TXT identical to T15.TXT. An empty document displays blank document rows and leaves with PASS. A different exit key deliberately returns FAIL in this screen-only stopping test.

## If the check disagrees

Check the exact fixture and the freshly preserved executable first. For position errors, compare both words and the gap/space invariant. For file errors, inspect recovery names and keep the accepted input before another run.
