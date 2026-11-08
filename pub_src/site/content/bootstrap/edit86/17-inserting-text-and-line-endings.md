+++
title = "17 \u00b7 Inserting text and line endings"
weight = 17
description = "Insert printable characters, tabs and CR/LF at the gap. Track unsaved changes and ask before discarding them."
download = "E17.RIL"
download_group = "tools/edit86"
reader_names = 1
+++

Insert printable characters, tabs and CR/LF at the gap. Track unsaved changes and ask before discarding them.

An insertion consumes one byte of space, advances gap and length, and leaves gapend unchanged. Enter inserts CR then LF as one action, after checking room for both. A refused insertion changes neither text nor dirty. An ordinary character marks one row for paint; a new line marks the window and layout. `confirm` asks about unsaved changes: S saves and quits only if saving succeeds, Q discards memory changes, and Escape returns to editing. This conservative flag records that an edit occurred; it does not compare the entire document with disk.

## Enter the source

Copy E16.RIL to E17.RIL.

Keep the unchanged source. Apply these edits from the bottom of the old file upward; physical positions locate text and are not source to type.

### Edit 1

Unchanged source immediately before the edit:

```rill
    return 1;
}
```

Insert after old physical line 733.

Insert:

```rill
fn confirm(){
    if dirty==0{
        return 1;
    }
    while 1{
        statusline("Unsaved changes: S save and quit, Q discard, ESC cancel.");
        let mut k=key();
        if (k==83)|(k==115){
            return savefile();
        }
        if (k==81)|(k==113){
            return 1;
        }
        if k==27{
            return 0;
        }
    }
    return 0;
}
```

The following old source remains:

```rill
fn cleanup(){
    let mut bad=0;
```

### Edit 2

Unchanged source immediately before the edit:

```rill
    return 0;
}
```

Insert after old physical line 476.

Insert:

```rill
fn rawinsert(c){
    set8(handle(load16(gap),load16(gap+2)),load16(gap)&32767,c);
    if status(){
        fatal("Text insertion failed.");
    }
    add(gap,1);
    add(length,1);
    sub(space,1);
    return 0;
}
fn typing(c,d,n){
    if load16(space+2)==0{
        if load16(space)<n{
            message="Buffer full; delete text before inserting.";
            return 0;
        }
    }
    rawinsert(c);
    if n==2{
        rawinsert(d);
        allrows=1;
        layout=1;
    }
    else{
        onerow=1;
    }
    dirty=1;
    return 0;
}
```

The following old source remains:

```rill
fn statusline(s){
    let mut i=0;
```

### Edit 3

Unchanged source immediately before the edit:

```rill
        layout=1;
        return 0;
```

Insert after old physical line 109.

Insert:

```rill
    }
    if k==13{
        typing(13,10,2);
        return 0;
    }
    if (k==9)|((k>=32)&(k<=126)){
        typing(k,0,1);
```

The following old source remains:

```rill
    }
    return 0;
```

### Edit 4

Unchanged source immediately before the edit:

```rill
            return cleanup();
        }
```

Remove old physical positions 63–63:

```rill
        command(k);
```

Replace with:

```rill
        else{
            command(k);
        }
```

The following old source remains:

```rill
    }
    return 0;
```

### Edit 5

Unchanged source immediately before the edit:

```rill
        message=0;
        if k==266{
```

Remove old physical positions 61–61:

```rill
            return cleanup();
```

Replace with:

```rill
            if confirm(){
                return cleanup();
            }
```

The following old source remains:

```rill
        }
        command(k);
```

## Build and preserve the program

```dos
COPY E17.RIL SOURCE.RIL
CHECK RILLED
COPY RESULT.IR SOURCE.IR
CHECK IRED
COPY RESULT.ASM SOURCE.ASM
CHECK A0
COPY RESULT.COM E17.COM
```

Require compiler `OK RESULT.IR 0000039445`, translator `OK RESULT.ASM 0000086003 text bytes`, assembler `OK RESULT.COM 18867 bytes`, and each PASS before the following copy. VIEW.BAS must report E17.COM length 18867 bytes, beginning with:

```text
FC 81 FC FE FF 74 03 E9 49 46 E8 A1 42 B4 4C CD 21 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
```

## The document fixture

Create T17.TXT with CR/LF after each displayed line:

```text
one
two
```

```dos
COPY T17.TXT EDIT.TXT
CHECK E17
```

Type ! at the beginning. The status gains an asterisk. Press F10, then Escape: the document must remain open. Press F2, then F10; require CHECK PASS. VIEW.BAS must report eleven bytes, exactly `21 6F 6E 65 0D 0A 74 77 6F 0D 0A`. On a separate run, type a character then F10 and Q: the accepted disk file must stay unchanged.

## If the check disagrees

Check the exact fixture and the freshly preserved executable first. For position errors, compare both words and the gap/space invariant. For file errors, inspect recovery names and keep the accepted input before another run.
