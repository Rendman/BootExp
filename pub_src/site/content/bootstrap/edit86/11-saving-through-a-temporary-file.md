+++
title = "11 \u00b7 Saving through a temporary file"
weight = 11
description = "Write the occupied document ranges into EDIT.TMP and publish a closed file. Preserve the accepted EDIT.TXT and retain recovery files when restoration fails."
download = "E11.RIL"
download_group = "tools/edit86"
reader_names = 1
+++

Write the occupied document ranges into EDIT.TMP and publish a closed file. Preserve the accepted EDIT.TXT and retain recovery files when restoration fails.

`writepart` streams an occupied physical range through io, clipping both at 4096 bytes and at a page boundary. Saving writes [0,gap) and [gapend,capacity), never the free bytes between them. `savefile` refuses pre-existing recovery names, creates its own temporary file, writes and closes it, then backs up the old document before renaming the temporary file. If that rename fails, it attempts restoration. `own` identifies our temporary file; `keep` protects recovery material after an unsuccessful restoration or backup deletion. Abort and cleanup remove only owned, unprotected temporary output. A successful save clears dirty; a failed save leaves the editor open.

## Enter the source

Copy E10.RIL to E11.RIL.

Keep the unchanged source. Apply these edits from the bottom of the old file upward; physical positions locate text and are not source to type.

### Edit 1

Unchanged source immediately before the edit:

```rill
        inopen=0;
    }
```

Remove old physical positions 176–176:

```rill
    return release()|bad;
```

Replace with:

```rill
    if outopen{
        close(output);
        if status(){
            bad=1;
        }
        else{
            outopen=0;
        }
    }
    if own&(keep==0)&(outopen==0){
        delete("EDIT.TMP");
        if status(){
            bad=1;
        }
        else{
            own=0;
        }
    }
    if release(){
        bad=1;
    }
    if keep{
        print("Recovery files retained: inspect EDIT.TMP / EDIT.BAK.\r\n");
        bad=1;
    }
    return bad;
```

The following old source remains:

```rill
}
fn print(s){
```

### Edit 2

Unchanged source immediately before the edit:

```rill
            bad=1;
        }
```

Remove old physical positions 174–174:

```rill
        inopen=0;
```

Replace with:

```rill
        else{
            inopen=0;
        }
```

The following old source remains:

```rill
    }
    return release()|bad;
```

### Edit 3

Unchanged source immediately before the edit:

```rill
    return 0;
}
```

Insert after old physical line 166.

Insert:

```rill
fn reserved(){
    let mut found=exists("EDIT.TMP");
    if status(){
        return 1;
    }
    if found{
        return 1;
    }
    found=exists("EDIT.BAK");
    if status(){
        return 1;
    }
    return found;
}
fn writepart(lo,hi,endlo,endhi){
    while (hi<endhi)|((hi==endhi)&(lo<endlo)){
        let mut n=4096;
        let mut remaining=endlo-lo;
        let mut high=endhi-hi-(endlo<lo);
        if high==0{
            if remaining<n{
                n=remaining;
            }
        }
        let mut offset=lo&32767;
        if n>32768-offset{
            n=32768-offset;
        }
        blockread(handle(lo,hi),offset,io,n);
        if status(){
            return 0;
        }
        let mut done=write(output,io,n);
        if status(){
            return 0;
        }
        if done!=n{
            return 0;
        }
        let mut next=lo+n;
        hi=hi+(next<lo);
        lo=next;
    }
    return 1;
}
fn abortsave(){
    if outopen{
        close(output);
        if status()==0{
            outopen=0;
        }
    }
    if own&(outopen==0)&(keep==0){
        delete("EDIT.TMP");
        if status()==0{
            own=0;
        }
    }
    message="Save failed. Inspect EDIT.TMP / EDIT.BAK before retrying.";
    return 0;
}
fn savefile(){
    if reserved(){
        message="Recovery files block saving: EDIT.TMP / EDIT.BAK.";
        return 0;
    }
    keep=0;
    output=create("EDIT.TMP");
    if status(){
        message="Cannot create EDIT.TMP.";
        return 0;
    }
    outopen=1;
    own=1;
    if !writepart(0,0,load16(gap),load16(gap+2)){
        return abortsave();
    }
    if !writepart(load16(gapend),load16(gapend+2),0,4){
        return abortsave();
    }
    close(output);
    if status(){
        return abortsave();
    }
    outopen=0;
    let mut backup=exists(filename());
    if status(){
        return abortsave();
    }
    if backup{
        rename(filename(),"EDIT.BAK");
        if status(){
            return abortsave();
        }
    }
    rename("EDIT.TMP",filename());
    if status(){
        if backup{
            rename("EDIT.BAK",filename());
            if status(){
                keep=1;
            }
        }
        return abortsave();
    }
    own=0;
    if backup{
        delete("EDIT.BAK");
        if status(){
            keep=1;
            return abortsave();
        }
    }
    dirty=0;
    message="Saved.";
    return 1;
}
```

The following old source remains:

```rill
fn cleanup(){
    let mut bad=0;
```

### Edit 4

Unchanged source immediately before the edit:

```rill
    loadfile();
    copypos(gap,length);
```

Remove old physical positions 21–29:

```rill
    let mut bad=(load16(length)!=10)|(load16(length+2)!=0);
    zero(target);
    if before(target,length){
        bad=bad|(peek(target)!=111);
    }
    else{
        bad=1;
    }
    return cleanup()|bad;
```

Replace with:

```rill
    let mut saved=savefile();
    return cleanup()|!saved;
```

The following old source remains:

```rill
}
fn filename(){
```

### Edit 5

Unchanged source immediately before the edit:

```rill
    copypos(gapend,cap);
    copypos(space,cap);
```

Insert after old physical line 17.

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

### Edit 6

Unchanged source immediately before the edit:

```rill
bytes space[4];
bytes cap[4];
```

Remove old physical positions 10–10:

```rill
bytes target[4];
```

There is no replacement source.

The following old source remains:

```rill
bytes other[4];
bytes io[4096];
```

### Edit 7

Unchanged source immediately before the edit:

```rill
let mut input=0;
let mut inopen=0;
```

Insert after old physical line 3.

Insert:

```rill
let mut output=0;
let mut outopen=0;
let mut own=0;
let mut keep=0;
let mut dirty=0;
let mut message=0;
```

The following old source remains:

```rill
bytes pages[16];
bytes gap[4];
```

## Build and preserve the program

```dos
CHECK RILLED E11.RIL RESULT.IR
CHECK IRED RESULT.IR RESULT.ASM EDITRT.ASM
CHECK A0 RESULT.ASM RESULT.COM
COPY RESULT.COM E11.COM
```

Require compiler `OK RESULT.IR 0000015811`, translator `OK RESULT.ASM 0000044629 text bytes`, assembler `OK RESULT.COM 11817 bytes`, and each PASS before the following copy. VIEW.BAS must report E11.COM length 11817 bytes, beginning with:

```text
FC 81 FC FE FF 74 03 E9 61 29 E8 A7 29 81 F8 FF FF 75 03 E9 55 29 E8 AD 25 B4 4C CD 21 00 00 00
```

## The document fixture

Create T11.TXT with CR/LF after each displayed line:

```text
one
two
```

```dos
COPY T11.TXT HOLD.TXT
CHECK E11 T11.TXT
```

Require PASS and an unchanged document. Compare T11.TXT with HOLD.TXT using C:\DOS\FC.EXE /B. For rejection, create EDIT.TMP containing HOLD, run CHECK E11 T11.TXT and require FAIL with the recovery-file diagnostic. TYPE EDIT.TMP must still show HOLD and FC must still find the document unchanged. Inspect and remove only that exercise recovery file before continuing.

```dos
C:\DOS\FC.EXE /B T11.TXT HOLD.TXT
```

## If the check disagrees

Check the exact fixture and the freshly preserved executable first. For position errors, compare both words and the gap/space invariant. For file errors, inspect recovery names and keep the accepted input before another run.
