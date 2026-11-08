+++
title = "09 \u00b7 Allocating the document pages"
weight = 9
description = "Obtain eight separately allocated 32 KiB pages. Release every successful allocation even if a later request fails."
download = "E09.RIL"
download_group = "tools/edit86"
reader_names = 1
+++

Obtain eight separately allocated 32 KiB pages. Release every successful allocation even if a later request fails.

`pages` holds eight opaque allocation handles. The main block is reduced to 64 KiB by the established allocator before its first DOS request. Each request asks for 32768 bytes, keeping offsets within a word. Store a successful handle immediately so cleanup can find it if the next allocation fails. `release` frees only recorded handles, clears them and remembers a failed release. The fatal path uses that same cleanup. Text bytes need no initial clearing because no byte is read before it becomes occupied document storage.

## Enter the source

Copy E08.RIL to E09.RIL.

Keep the unchanged source. Apply these edits from the bottom of the old file upward; physical positions locate text and are not source to type.

### Edit 1

Unchanged source immediately before the edit:

```rill
    return 0;
}
```

Insert after old physical line 55.

Insert:

```rill
fn allocate(){
    let mut i=0;
    while i<8{
        let mut h=alloc(32768);
        if status(){
            fatal("Not enough DOS memory for 256 KiB text storage.");
        }
        store16(pages+i*2,h);
        i=i+1;
    }
    return 0;
}
fn release(){
    let mut bad=0;
    let mut i=0;
    while i<8{
        let mut h=load16(pages+i*2);
        if h{
            free(h);
            if status(){
                bad=1;
            }
            store16(pages+i*2,0);
        }
        i=i+1;
    }
    return bad;
}
fn cleanup(){
    return release();
}
fn print(s){
    while load8(s){
        putc(load8(s));
        s=s+1;
    }
    return 0;
}
fn fatal(s){
    cleanup();
    print(s);
    print("\r\n");
    exit(1);
    return 0;
}
```

### Edit 2

Unchanged source immediately before the edit:

```rill
bytes other[4];
fn main(){
```

Remove old physical positions 7–19:

```rill
    store16(cap,65535);
    add(cap,2);
    if (load16(cap)!=1)|(load16(cap+2)!=1){
        return 1;
    }
    sub(cap,3);
    if (load16(cap)!=65534)|(load16(cap+2)!=0){
        return 1;
    }
    copypos(target,cap);
    add(target,2);
    difference(work,target,cap);
    return !before(cap,target)|equal(cap,target)|(load16(work)!=2)|(load16(work+2)!=0);
```

Replace with:

```rill
    store16(cap+2,4);
    copypos(gapend,cap);
    copypos(space,cap);
    allocate();
    return cleanup();
```

The following old source remains:

```rill
}
fn copypos(d,s){
```

### Edit 3

Unchanged source immediately before the edit:

```rill
// EDIT86 construction checkpoint.
bytes cap[4];
```

Remove old physical positions 3–4:

```rill
bytes target[4];
bytes work[4];
```

There is no replacement source.

The following old source remains:

```rill
bytes other[4];
fn main(){
```

### Edit 4

Unchanged source immediately before the edit:

```rill
// EDIT86 construction checkpoint.
```

Insert after old physical line 1.

Insert:

```rill
bytes pages[16];
bytes gapend[4];
bytes space[4];
```

The following old source remains:

```rill
bytes cap[4];
bytes target[4];
```

## Build and preserve the program

```dos
COPY E09.RIL SOURCE.RIL
CHECK RILLED
COPY RESULT.IR SOURCE.IR
CHECK IRED
COPY RESULT.ASM SOURCE.ASM
CHECK A0
COPY RESULT.COM E09.COM
```

Require compiler `OK RESULT.IR 0000004264`, translator `OK RESULT.ASM 0000017505 text bytes`, assembler `OK RESULT.COM 03329 bytes`, and each PASS before the following copy. VIEW.BAS must report E09.COM length 3329 bytes, beginning with:

```text
FC 81 FC FE FF 74 03 E9 97 09 E8 EF 05 B4 4C CD 21 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
```

## Check the stopping point

```dos
CHECK E09
```

CHECK must report PASS after obtaining and freeing all eight text pages. In an environment with too little free DOS memory, require FAIL and the allocation diagnostic; previously obtained pages are released. Do not reduce the document capacity silently to hide an allocation failure.

## If the check disagrees

Check the exact fixture and the freshly preserved executable first. For position errors, compare both words and the gap/space invariant. For file errors, inspect recovery names and keep the accepted input before another run.
