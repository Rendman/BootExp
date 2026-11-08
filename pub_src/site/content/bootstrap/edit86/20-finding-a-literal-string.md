+++
title = "20 \u00b7 Finding a literal string"
weight = 20
description = "Find literal text from the current position and repeat the search from the next byte. Search the document through logical positions, including page boundaries."
download = "E20.RIL"
download_group = "tools/edit86"
reader_names = 1
+++

Find literal text from the current position and repeat the search from the next byte. Search the document through logical positions, including page boundaries.

The query accepts up to sixty-four printable characters and Escape cancels it. Enter installs a nonempty literal needle. findnext compares bytes through logical positions, checking length before each read; it can match across a page boundary. F3 begins at the insertion position, while F5 begins one byte later. A found match moves the gap to its first byte and requests layout. Matching is case-sensitive and does not wrap from EOF. Searching changes neither text nor undo records.

## Enter the source

Copy E19.RIL to E20.RIL.

Keep the unchanged source. Apply these edits from the bottom of the old file upward; physical positions locate text and are not source to type.

### Edit 1

Unchanged source immediately before the edit:

```rill
    return 0;
}
```

Insert after old physical line 767.

Insert:

```rill
fn askfind(){
    let mut n=0;
    while 1{
        let mut i=0;
        while i<80{
            rowbuf[i]=32;
            i=i+1;
        }
        rowbuf[0]=70;
        rowbuf[1]=105;
        rowbuf[2]=110;
        rowbuf[3]=100;
        rowbuf[4]=58;
        i=0;
        while i<n{
            rowbuf[i+6]=query[i];
            i=i+1;
        }
        vpos(1920);
        vwrite(rowbuf,80);
        vpos(1926+n);
        let mut k=key();
        if k==27{
            return 0;
        }
        if k==13{
            if n{
                nlen=n;
                i=0;
                while i<n{
                    needle[i]=query[i];
                    i=i+1;
                }
                findnext(0);
            }
            return 0;
        }
        if k==8{
            if n{
                n=n-1;
            }
        }
        else{
            if (k>=32)&(k<=126)&(n<64){
                query[n]=k;
                n=n+1;
            }
        }
    }
    return 0;
}
fn findnext(skip){
    if nlen==0{
        message="Use F3 to enter a literal search string.";
        return 0;
    }
    copypos(probe,gap);
    if skip{
        if before(probe,length){
            add(probe,1);
        }
    }
    while before(probe,length){
        copypos(matchpos,probe);
        let mut i=0;
        let mut found=1;
        while (i<nlen)&found{
            if !before(matchpos,length){
                found=0;
            }
            else{
                if peek(matchpos)!=needle[i]{
                    found=0;
                }
            }
            if found{
                add(matchpos,1);
                i=i+1;
            }
        }
        if found{
            copypos(target,probe);
            movegap(target);
            layout=1;
            message="Found.";
            return 0;
        }
        add(probe,1);
    }
    message="Text not found before end of file.";
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
    if k==265{
        savefile();
```

Insert after old physical line 76.

Insert:

```rill
        return 0;
    }
    if k==268{
        askfind();
        vertical=0;
        return 0;
    }
    if k==269{
        findnext(1);
        vertical=0;
```

The following old source remains:

```rill
        return 0;
    }
```

### Edit 3

Unchanged source immediately before the edit:

```rill
bytes io[4096];
bytes rowbuf[80];
```

Insert after old physical line 38.

Insert:

```rill
bytes needle[65];
bytes query[65];
```

The following old source remains:

```rill
fn main(){
    store16(cap+2,4);
```

### Edit 4

Unchanged source immediately before the edit:

```rill
bytes at[4];
bytes probe[4];
```

Insert after old physical line 34.

Insert:

```rill
bytes matchpos[4];
```

The following old source remains:

```rill
bytes work[4];
bytes other[4];
```

### Edit 5

Unchanged source immediately before the edit:

```rill
let mut allrows=1;
let mut onerow=0;
```

Insert after old physical line 18.

Insert:

```rill
let mut nlen=0;
```

The following old source remains:

```rill
bytes pages[16];
bytes gap[4];
```

## Build and preserve the program

```dos
COPY E20.RIL SOURCE.RIL
CHECK RILLED
COPY RESULT.IR SOURCE.IR
CHECK IRED
COPY RESULT.ASM SOURCE.ASM
CHECK A0
COPY RESULT.COM E20.COM
```

Require compiler `OK RESULT.IR 0000049157`, translator `OK RESULT.ASM 0000104350 text bytes`, assembler `OK RESULT.COM 22073 bytes`, and each PASS before the following copy. VIEW.BAS must report E20.COM length 22073 bytes, beginning with:

```text
FC 81 FC FE FF 74 03 E9 CF 52 E8 27 4F B4 4C CD 21 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
```

## The document fixture

Create T20.TXT with CR/LF after each displayed line:

```text
one
two
```

```dos
COPY T20.TXT EDIT.TXT
CHECK E20
```

Press F3, type two and press Enter. The cursor must move to the second line. Type !, then F2 and F10. Require CHECK PASS and eleven bytes: `6F 6E 65 0D 0A 21 74 77 6F 0D 0A`. Restore T20.TXT; search for absent text and require the not-found message with no document change. Escape cancels a partly entered query. F5 repeats from the byte after the current position.

Preserve E20.COM as EDIT86.COM. EDIT86.RIL is the same source as E20.RIL. Keep RILLED.RIL, IRED.RIL and EDITRT.ASM with it so the editor can be rebuilt from the established trio.

## If the check disagrees

Check the exact fixture and the freshly preserved executable first. For position errors, compare both words and the gap/space invariant. For file errors, inspect recovery names and keep the accepted input before another run.
