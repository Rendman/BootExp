+++
title = "03 \u00b7 Three letters are enough"
weight = 3
description = "Separate the first and last words, fold case, and recognize LOOK, HELP and QUIT."
download = "V03.RIL"
download_group = "tools/vampire"
reader_names = 1
+++

The BASIC adventure makes a useful bargain: the player can write a phrase, but only the first three letters of its first and last words matter. READ THE SIGN can therefore mean the same thing as READ SIGN.

## What changes

parse clears two four-byte buffers, retaining three uppercase letters or spaces and a terminating zero. words counts whole words, even when their spellings are longer. Middle words are deliberately ignored. wordis compares exactly three bytes, so its literal arguments are padded to three characters. main ignores whitespace-only input and recognizes QUIT before dispatching an action. act gives unknown actions a message; they never become a movement by accident. HELP describes the vocabulary currently accepted by the program.

## Enter the source

Copy V02.RIL to V03.RIL. Apply the following edits in order. All locators are existing declarations or unique routine headers; no editor line numbers are needed. Keep the source outside each stated edit.

### Change 1

Find this unique existing declaration or routine header; leave it in place:

```rill
fn main(){
```

Insert the following source immediately before it:

```rill
bytes verb[4];
bytes noun[4];
```

### Change 2

Find this unique existing declaration or routine header; leave it in place:

```rill
let mut playing=1;
```

Insert the following source immediately before it:

```rill
let mut words=0;
```

### Change 3

Find the unique routine header `fn main(){`. Within that routine, replace this existing block, including its shown context:

```rill
        let mut got=readline();
        if got==0{playing=0;}
    }
    close(input);if status(){exit(1);}
```

With this complete block:

```rill
        let mut got=readline();
        if got==0{playing=0;}
        if got==1{
            parse();
            if wordis(verb,"QUI"){say("Goodbye.\r\n");playing=0;}
            else{
                if words{
                    act();
                }
            }
        }
    }
    close(input);if status(){exit(1);}
```

### Change 4

Append these complete routines after the final routine in your source:

```rill
fn help(){
    say("Use the first and last words; only three letters count.\r\n");
    say("LOOK, HELP and QUIT.\r\n");
    return 0;
}
```

### Change 5

Find this unique existing declaration or routine header; leave it in place:

```rill
fn help(){
```

Insert the following source immediately before it:

```rill
fn act(){
    if wordis(verb,"HEL"){help();return 0;}
    if wordis(verb,"LOO"){say("You are in the Entrance Hall.\r\n");return 0;}
    say("I don't know how to do that.\r\n");
    return 0;
}
```

### Change 6

Find this unique existing declaration or routine header; leave it in place:

```rill
fn act(){
```

Insert the following source immediately before it:

```rill
fn wordis(p,s){
    return (load8(p)==load8(s))&
        (load8(p+1)==load8(s+1))&(load8(p+2)==load8(s+2));
}
```

### Change 7

Find this unique existing declaration or routine header; leave it in place:

```rill
fn wordis(p,s){
```

Insert the following source immediately before it:

```rill
fn parse(){
    let mut i=0;
    while i<3{verb[i]=32;noun[i]=32;i=i+1;}
    verb[3]=0;noun[3]=0;words=0;i=0;
    while i<length{
        if command[i]==32{i=i+1;}
        else{
            let mut dest=noun;
            if words==0{dest=verb;}
            let mut n=0;
            while n<3{store8(dest+n,32);n=n+1;}
            n=0;let mut stop=0;
            while (i<length)&(stop==0){
                if command[i]==32{stop=1;}
                else{
                    let mut c=command[i];
                    if (c>=97)&(c<=122){c=c-32;}
                    if n<3{store8(dest+n,c);}
                    n=n+1;i=i+1;
                }
            }
            words=words+1;
        }
    }
    return 0;
}
```

## Build and try it

```dos
VMAKE V03
```

Require these fresh tool reports, followed by BUILD PASS:

```text
OK RESULT.IR 0000008389
OK RESULT.ASM 0000024948 text bytes
OK RESULT.COM 04437 bytes
BUILD PASS
```

The preserved V03.COM is 4,437 bytes. Its natural display and behavior are the checks below.

Create T03.TXT as plain text:

```text
  lOoK   around
help
dance
quit
```

Create X03.TXT as plain text:

```text
	
LOO longer words
quit
```

```dos
CHECK V03 T03.TXT
```

Require these significant game lines, followed by CHECK's PASS:

```text
Use the first and last words
I don't know how to do that.
Goodbye.
PASS
```

## Check the other case

```dos
CHECK V03 X03.TXT
```

Require these significant lines and PASS:

```text
You are in the Entrance Hall.
Goodbye.
PASS
```

## If it differs

If a short direction or keyword fails, check its padding. The three-character token for LOOK is LOO, not the complete spelling.
