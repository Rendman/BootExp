+++
title = "12 \u00b7 Keeping free space at the cursor"
weight = 12
description = "Move the gap to a requested logical position without changing the document. Clip each transfer at both page boundaries and copy in the safe direction."
download = "E12.RIL"
download_group = "tools/edit86"
reader_names = 1
+++

Move the gap to a requested logical position without changing the document. Clip each transfer at both page boundaries and copy in the safe direction.

The logical insertion position is gap. The corresponding free interval in physical storage is [gap,gapend), whose size is space. Moving right copies bytes after the gap into its beginning. Moving left copies bytes before it into its end. Choose a chunk no larger than the remaining distance or either page remainder. Left moves work from the end; right moves from the start. The block primitive handles overlap within an individual chunk. A zero-sized gap needs only new position words. Moving the gap changes no document length and creates no disk writes.

## Enter the source

Copy E11.RIL to E12.RIL.

Keep the unchanged source. Apply these edits from the bottom of the old file upward; physical positions locate text and are not source to type.

### Edit 1

Unchanged source immediately before the edit:

```rill
        }
        add(length,n);
```

Insert after old physical line 163.

Insert:

```rill
    }
    return 0;
}
fn movegap(p){
    if (load16(space)==0)&(load16(space+2)==0){
        copypos(gap,p);
        copypos(gapend,p);
        return 0;
    }
    while before(gap,p){
        difference(work,p,gap);
        let mut n=32768;
        if load16(work+2)==0{
            if load16(work)<n{
                n=load16(work);
            }
        }
        let mut so=load16(gapend)&32767;
        let mut dest=load16(gap)&32767;
        if n>32768-so{
            n=32768-so;
        }
        if n>32768-dest{
            n=32768-dest;
        }
        blockmove(handle(load16(gapend),load16(gapend+2)),so,handle(load16(gap),load16(gap+2)),dest,n);
        if status(){
            fatal("Gap move failed.");
        }
        add(gap,n);
        add(gapend,n);
    }
    while before(p,gap){
        difference(work,gap,p);
        let mut n=32768;
        if load16(work+2)==0{
            if load16(work)<n{
                n=load16(work);
            }
        }
        copypos(at,gap);
        sub(at,1);
        copypos(other,gapend);
        sub(other,1);
        let mut so=(load16(at)&32767)+1;
        let mut dest=(load16(other)&32767)+1;
        if n>so{
            n=so;
        }
        if n>dest{
            n=dest;
        }
        copypos(at,gap);
        sub(at,n);
        copypos(other,gapend);
        sub(other,n);
        blockmove(handle(load16(at),load16(at+2)),load16(at)&32767,handle(load16(other),load16(other+2)),load16(other)&32767,n);
        if status(){
            fatal("Gap move failed.");
        }
        sub(gap,n);
        sub(gapend,n);
```

The following old source remains:

```rill
    }
    return 0;
```

### Edit 2

Unchanged source immediately before the edit:

```rill
    loadfile();
    copypos(gap,length);
```

Insert after old physical line 27.

Insert:

```rill
    store16(target,5);
    if before(length,target){
        fatal("Fixture is shorter than the gap position.");
    }
    movegap(target);
```

The following old source remains:

```rill
    let mut saved=savefile();
    return cleanup()|!saved;
```

### Edit 3

Unchanged source immediately before the edit:

```rill
bytes space[4];
bytes cap[4];
```

Insert after old physical line 15.

Insert:

```rill
bytes target[4];
bytes at[4];
bytes work[4];
```

The following old source remains:

```rill
bytes other[4];
bytes io[4096];
```

## Build and preserve the program

```dos
COPY E12.RIL SOURCE.RIL
CHECK RILLED
COPY RESULT.IR SOURCE.IR
CHECK IRED
COPY RESULT.ASM SOURCE.ASM
CHECK A0
COPY RESULT.COM E12.COM
```

Require compiler `OK RESULT.IR 0000019069`, translator `OK RESULT.ASM 0000048955 text bytes`, assembler `OK RESULT.COM 12406 bytes`, and each PASS before the following copy. VIEW.BAS must report E12.COM length 12406 bytes, beginning with:

```text
FC 81 FC FE FF 74 03 E9 0C 2D E8 64 29 B4 4C CD 21 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
```

## The document fixture

Create T12.TXT with CR/LF after each displayed line:

```text
one
two
```

```dos
COPY T12.TXT EDIT.TXT
CHECK E12
```

Require PASS and an unchanged document by COMP against T12.TXT. The gap has moved to logical position five, but saving must still reproduce all ten bytes. Try a three-byte document: require FAIL with the shorter-than-gap diagnostic and preserve those input bytes. Restore the fixture.

## If the check disagrees

Check the exact fixture and the freshly preserved executable first. For position errors, compare both words and the gap/space invariant. For file errors, inspect recovery names and keep the accepted input before another run.
