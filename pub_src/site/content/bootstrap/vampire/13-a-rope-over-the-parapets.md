+++
title = "13 \u00b7 A rope over the parapets"
weight = 13
description = "Ask for a second object and tie the carried rope to the tower parapets."
download = "V13.RIL"
download_group = "tools/vampire"
reader_names = 1
+++

TIE ROPE is not quite a complete instruction. The question To what? lets the player finish it without turning the command parser into a grammar for every possible sentence.

## What changes

ask uses the same bounded reader and parser, returning whether a usable answer exists. The object number passed to tie is already in its private parameter, so parsing the answer cannot lose the original object. Tying requires the rope in inventory and the Tower as the current room. It removes the loose rope, sets rope_tied, and changes the parapets description. ROPE then names that fixed anchor for movement. Going over the parapets without the rope is fatal. The answer to the question costs no additional minute.

## Enter the source

Copy V12.RIL to V13.RIL. Apply the following edits in order. All locators are existing declarations or unique routine headers; no editor line numbers are needed. Keep the source outside each stated edit.

### Change 1

Find this unique existing declaration or routine header; leave it in place:

```rill
bytes command[81];
```

Insert the following source immediately before it:

```rill
let mut rope_tied=0;
```

### Change 2

Find the unique routine header `fn act(){`. Within that routine, replace this existing block, including its shown context:

```rill
    if wordis(verb,"GET")|wordis(verb,"TAK"){take(obj);return 0;}
    if wordis(verb,"DRO"){drop(obj);return 0;}
    if wordis(verb,"PUS"){push(obj);return 0;}
    say("I don't know how to do that.\r\n");
```

With this complete block:

```rill
    if wordis(verb,"GET")|wordis(verb,"TAK"){take(obj);return 0;}
    if wordis(verb,"DRO"){drop(obj);return 0;}
    if wordis(verb,"TIE"){tie(obj);return 0;}
    if wordis(verb,"PUS"){push(obj);return 0;}
    say("I don't know how to do that.\r\n");
```

### Change 3

Find the unique routine header `fn help(){`. Within that routine, replace this existing block, including its shown context:

```rill
    say("READ\r\n");
    say("PUSH\r\n");
    say("WAIT.\r\n");
    return 0;
}
```

With this complete block:

```rill
    say("READ\r\n");
    say("PUSH\r\n");
    say("WAIT\r\n");
    say("TIE.\r\n");
    return 0;
}
```

### Change 4

Find the unique routine header `fn walk(){`. Within that routine, replace this existing block, including its shown context:

```rill
        return 0;
    }
    say("You cannot go there.\r\n");
    return 0;
```

With this complete block:

```rill
        return 0;
    }
    let mut obj=nounid();
    if (obj==21)&(location==5){
        if rope_tied{location=6;say("You climb down the rope.\r\n");describe();}
        else{lose("You fall from the parapets.\r\n");}
        return 0;
    }
    say("You cannot go there.\r\n");
    return 0;
```

### Change 5

Find the unique routine header `fn nounid(){`. Within that routine, replace this existing block, including its shown context:

```rill
    if wordis(noun,"TIM"){return 2;}
    if wordis(noun,"ROP"){
        return 3;
    }
    if (location==5)&wordis(noun,"PAR"){return 21;}
```

With this complete block:

```rill
    if wordis(noun,"TIM"){return 2;}
    if wordis(noun,"ROP"){
        if rope_tied{return 21;}return 3;
    }
    if (location==5)&wordis(noun,"PAR"){return 21;}
```

### Change 6

Find the unique routine header `fn newgame(){`. Within that routine, replace this existing block, including its shown context:

```rill
    elapsed=0;
    finished=0;
    world();
    items();
```

With this complete block:

```rill
    elapsed=0;
    finished=0;
    rope_tied=0;
    world();
    items();
```

### Change 7

Find this unique existing declaration or routine header; leave it in place:

```rill
fn push(obj){
```

Insert the following source immediately before it:

```rill
fn tie(obj){
    if (obj!=3)|(places[3]!=0)|(location!=5){say("You cannot tie that here.\r\n");return 0;}
    if ask("To what? "){
        if wordis(verb,"PAR"){
            places[3]=99;rope_tied=1;
            store16(things+21*2,"Rope tied to the Parapets");
            say("The rope is tied to the parapets.\r\n");return 0;
        }
    }
    say("The rope needs a secure anchor.\r\n");return 0;
}
```

### Change 8

Find this unique existing declaration or routine header; leave it in place:

```rill
fn tie(obj){
```

Insert the following source immediately before it:

```rill
fn ask(text){
    say(text);
    let mut got=readline();
    if got==0{playing=0;return 0;}
    if got!=1{return 0;}
    parse();return words!=0;
}
```

## Build and try it

```dos
VMAKE V13
```

Require these fresh tool reports, followed by BUILD PASS:

```text
OK RESULT.IR 0000033847
OK RESULT.ASM 0000086447 text bytes
OK RESULT.COM 14106 bytes
BUILD PASS
```

The preserved V13.COM is 14,106 bytes. Its natural display and behavior are the checks below.

Create ROPE.TXT as plain text:

```text
E
PUSH BOOKCASE
D
GET ROPE
U
E
E
```

Create F002.TXT with these additional commands:

```text
TIE ROPE
PARAPETS
GO ROPE
S
```

Join the saved ROPE.TXT walk and this tail as CHAPEL.TXT:

```dos
COPY /B ROPE.TXT+F002.TXT CHAPEL.TXT
```

```dos
COPY CHAPEL.TXT T13.TXT
```

Create X13.TXT as plain text:

```text
E
E
E
GO PARAPETS
```

```dos
CHECK V13 T13.TXT
```

Require these significant game lines, followed by CHECK's PASS:

```text
The rope is tied to the parapets.
You climb down the rope.
You are in the Chapel.
PASS
```

## Check the other case

```dos
CHECK V13 X13.TXT
```

Require these significant lines and PASS:

```text
You fall from the parapets.
PASS
```

A player death or an unsuccessful action is an ordinary game outcome, so CHECK still reports PASS. Judge the stated message and the resulting world as well as the process status.

## If it differs

Keep the tower-specific PARAPETS alias ahead of PARCHMENT. Both begin with PAR; the room supplies the distinction.
