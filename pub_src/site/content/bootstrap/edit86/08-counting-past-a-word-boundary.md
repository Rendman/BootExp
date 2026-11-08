+++
title = "08 \u00b7 Counting past a word boundary"
weight = 8
description = "Represent document positions as low and high words. A 256 KiB document needs carry, borrow and complete-position comparisons."
download = "E08.RIL"
download_group = "tools/edit86"
reader_names = 1
+++

Represent document positions as low and high words. A 256 KiB document needs carry, borrow and complete-position comparisons.

Each position occupies four near bytes: the low word at its address and the high word two bytes after it. `add` and `sub` accept a word-sized distance and propagate one carry or borrow. `difference` subtracts complete positions; `before` compares high words first. No physical address is represented by these pairs. The stopping test crosses 65535 in both directions, checks a difference of two and returns a status. No console output is part of this arithmetic.

## Enter the source

Create E08.RIL as plain ASCII:

```rill
// EDIT86 construction checkpoint.
bytes cap[4];
bytes target[4];
bytes work[4];
bytes other[4];
fn main(){
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
}
fn copypos(d,s){
    store16(d,load16(s));
    store16(d+2,load16(s+2));
    return 0;
}
fn before(a,b){
    return (load16(a+2)<load16(b+2))|((load16(a+2)==load16(b+2))&(load16(a)<load16(b)));
}
fn equal(a,b){
    return (load16(a)==load16(b))&(load16(a+2)==load16(b+2));
}
fn add(p,n){
    let mut old=load16(p);
    let mut next=old+n;
    store16(p,next);
    if next<old{
        store16(p+2,load16(p+2)+1);
    }
    return 0;
}
fn sub(p,n){
    let mut old=load16(p);
    store16(p,old-n);
    if old<n{
        store16(p+2,load16(p+2)-1);
    }
    return 0;
}
fn difference(d,a,b){
    let mut lo=load16(a);
    let mut other=load16(b);
    store16(d,lo-other);
    store16(d+2,load16(a+2)-load16(b+2)-(lo<other));
    return 0;
}
```

## Build and preserve the program

Use the completed S07.ASM binding throughout the editor construction:

```dos
COPY S07.ASM EDITRT.ASM
```

```dos
COPY E08.RIL SOURCE.RIL
CHECK RILLED
COPY RESULT.IR SOURCE.IR
CHECK IRED
COPY RESULT.ASM SOURCE.ASM
CHECK A0
COPY RESULT.COM E08.COM
```

Require compiler `OK RESULT.IR 0000003388`, translator `OK RESULT.ASM 0000015515 text bytes`, assembler `OK RESULT.COM 02993 bytes`, and each PASS before the following copy. VIEW.BAS must report E08.COM length 2993 bytes, beginning with:

```text
FC 81 FC FE FF 74 03 E9 47 08 E8 9F 04 B4 4C CD 21 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
```

## Check the stopping point

```dos
CHECK E08
```

CHECK must report PASS. The arithmetic crosses the low-word boundary, borrows back and checks complete ordering and subtraction. A mistake in carry or borrow must return FAIL rather than merely wrap the low word.

## If the check disagrees

Check the exact fixture and the freshly preserved executable first. For position errors, compare both words and the gap/space invariant. For file errors, inspect recovery names and keep the accepted input before another run.
