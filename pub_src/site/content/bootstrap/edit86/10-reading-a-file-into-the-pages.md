+++
title = "10 \u00b7 Reading a file into the pages"
weight = 10
description = "Read EDIT.TXT through a 4096-byte buffer into the pages. Count every positive read, distinguish an absent file from an I/O failure, and reject excess input."
download = "E10.RIL"
download_group = "tools/edit86"
reader_names = 1
+++

Read EDIT.TXT through a 4096-byte buffer into the pages. Count every positive read, distinguish an absent file from an I/O failure, and reject excess input.

Loading fills the prefix of the pages. The gap is initially at the file end: gap equals length, gapend equals capacity, and space equals capacity minus length. `handle` divides a position into a page number and a 0–32767 offset. `peek` adds space for logical bytes at or after the gap. It is called only for positions strictly below length. The reader clips a refill at its current page boundary as well as 4096 bytes, so short positive DOS reads cannot make the next transfer cross a page. At full capacity it probes for one more input byte: EOF is accepted, another byte is rejected.

## Enter the source

Copy E09.RIL to E10.RIL.

Keep the unchanged source. Apply these edits from the bottom of the old file upward; physical positions locate text and are not source to type.

### Edit 1

Unchanged source immediately before the edit:

```rill
}
fn cleanup(){
```

Remove old physical positions 78–78:

```rill
    return release();
```

Replace with:

```rill
    let mut bad=0;
    if inopen{
        close(input);
        if status(){
            bad=1;
        }
        inopen=0;
    }
    return release()|bad;
```

The following old source remains:

```rill
}
fn print(s){
```

### Edit 2

Unchanged source immediately before the edit:

```rill
    return bad;
}
```

Insert after old physical line 76.

Insert:

```rill
fn loadfile(){
    let mut present=exists(filename());
    if status(){
        fatal("Cannot inspect EDIT.TXT.");
    }
    if present==0{
        return 0;
    }
    input=open(filename());
    if status(){
        fatal("Cannot open EDIT.TXT.");
    }
    inopen=1;
    while 1{
        let mut request=4096;
        if load16(length+2)==4{
            request=1;
        }
        else{
            let mut left=32768-(load16(length)&32767);
            if request>left{
                request=left;
            }
        }
        let mut n=read(input,io,request);
        if status(){
            fatal("Cannot read EDIT.TXT.");
        }
        if n==0{
            close(input);
            if status(){
                fatal("Cannot close EDIT.TXT.");
            }
            inopen=0;
            difference(space,cap,length);
            return 0;
        }
        if load16(length+2)==4{
            fatal("EDIT.TXT exceeds the 256 KiB text capacity.");
        }
        blockload(handle(load16(length),load16(length+2)),load16(length)&32767,io,n);
        if status(){
            fatal("Text load exceeds its allocated page.");
        }
        add(length,n);
    }
    return 0;
}
```

The following old source remains:

```rill
fn cleanup(){
    return release();
```

### Edit 3

Unchanged source immediately before the edit:

```rill
    return 0;
}
```

Insert after old physical line 48.

Insert:

```rill
fn handle(lo,hi){
    return load16(pages+(hi*2+(lo>>15))*2);
}
fn peek(p){
    let mut lo=load16(p);
    let mut hi=load16(p+2);
    if (hi>load16(gap+2))|((hi==load16(gap+2))&(lo>=load16(gap))){
        let mut next=lo+load16(space);
        hi=hi+load16(space+2)+(next<lo);
        lo=next;
    }
    let mut value=get8(handle(lo,hi),lo&32767);
    if status(){
        fatal("Text storage failed.");
    }
    return value;
}
```

The following old source remains:

```rill
fn allocate(){
    let mut i=0;
```

### Edit 4

Unchanged source immediately before the edit:

```rill
    copypos(space,cap);
    allocate();
```

Remove old physical positions 12–12:

```rill
    return cleanup();
```

Replace with:

```rill
    loadfile();
    copypos(gap,length);
    let mut bad=(load16(length)!=10)|(load16(length+2)!=0);
    zero(target);
    if before(target,length){
        bad=bad|(peek(target)!=111);
    }
    else{
        bad=1;
    }
    return cleanup()|bad;
}
fn filename(){
    return "EDIT.TXT";
}
fn zero(p){
    store16(p,0);
    store16(p+2,0);
    return 0;
```

The following old source remains:

```rill
}
fn copypos(d,s){
```

### Edit 5

Unchanged source immediately before the edit:

```rill
bytes cap[4];
bytes other[4];
```

Insert after old physical line 6.

Insert:

```rill
bytes io[4096];
```

The following old source remains:

```rill
fn main(){
    store16(cap+2,4);
```

### Edit 6

Unchanged source immediately before the edit:

```rill
bytes space[4];
bytes cap[4];
```

Insert after old physical line 5.

Insert:

```rill
bytes target[4];
```

The following old source remains:

```rill
bytes other[4];
fn main(){
```

### Edit 7

Unchanged source immediately before the edit:

```rill
bytes pages[16];
bytes gapend[4];
```

Insert after old physical line 3.

Insert:

```rill
bytes length[4];
```

The following old source remains:

```rill
bytes space[4];
bytes cap[4];
```

### Edit 8

Unchanged source immediately before the edit:

```rill
// EDIT86 construction checkpoint.
bytes pages[16];
```

Insert after old physical line 2.

Insert:

```rill
bytes gap[4];
```

The following old source remains:

```rill
bytes gapend[4];
bytes space[4];
```

### Edit 9

Unchanged source immediately before the edit:

```rill
// EDIT86 construction checkpoint.
```

Insert after old physical line 1.

Insert:

```rill
let mut input=0;
let mut inopen=0;
```

The following old source remains:

```rill
bytes pages[16];
bytes gapend[4];
```

## Build and preserve the program

```dos
COPY E10.RIL SOURCE.RIL
CHECK RILLED
COPY RESULT.IR SOURCE.IR
CHECK IRED
COPY RESULT.ASM SOURCE.ASM
CHECK A0
COPY RESULT.COM E10.COM
```

Require compiler `OK RESULT.IR 0000008946`, translator `OK RESULT.ASM 0000027742 text bytes`, assembler `OK RESULT.COM 09046 bytes`, and each PASS before the following copy. VIEW.BAS must report E10.COM length 9046 bytes, beginning with:

```text
FC 81 FC FE FF 74 03 E9 EC 1F E8 44 1C B4 4C CD 21 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
```

## The document fixture

Create T10.TXT with CR/LF after each displayed line:

```text
one
two
```

```dos
COPY T10.TXT EDIT.TXT
CHECK E10
```

Require PASS. The diagnostic expects ten file bytes and the first byte 6F. It makes no output file. Copy `123` without a line ending over EDIT.TXT and repeat: require FAIL. Restore the fixture before continuing. A missing file is an empty new document in the retained reader, but this diagnostic intentionally rejects a length other than ten.

## If the check disagrees

Check the exact fixture and the freshly preserved executable first. For position errors, compare both words and the gap/space invariant. For file errors, inspect recovery names and keep the accepted input before another run.
