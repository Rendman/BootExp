+++
title = "08 \u00b7 Picking up and putting down"
weight = 8
description = "Move objects between a room and the player without copying their descriptions."
download = "V08.RIL"
download_group = "tools/vampire"
reader_names = 1
+++

GET and DROP are small changes to places. The name table does not move. That separation makes taking the scroll no more complicated than taking the timepiece.

## What changes

take checks that a noun was recognized, that the object is not already carried, and that it is actually in this room. Only then does it write zero into places. drop requires zero and writes the current room number. Both messages name the object through itemname. GET and TAKE use the same routine. Calls receive an object number before doing any work, keeping parsing separate from game rules. The bookcase command now obtains its number through nounid as well.

## Enter the source

Copy V07.RIL to V08.RIL. Apply the following edits in order. All locators are existing declarations or unique routine headers; no editor line numbers are needed. Keep the source outside each stated edit.

### Change 1

Find the unique routine header `fn act(){`. Within that routine, replace this existing block, including its shown context:

```rill
    if wordis(verb,"GO ")|wordis(verb,"CLI")|((words==1)&(direction()!=0)){walk();return 0;}
    if wordis(verb,"LOO"){describe();return 0;}
    if wordis(verb,"PUS"){
        let mut obj=0;if wordis(noun,"BOO"){obj=19;}
        push(obj);return 0;
    }
    say("I don't know how to do that.\r\n");
    return 0;
```

With this complete block:

```rill
    if wordis(verb,"GO ")|wordis(verb,"CLI")|((words==1)&(direction()!=0)){walk();return 0;}
    if wordis(verb,"LOO"){describe();return 0;}
    let mut obj=nounid();
    if wordis(verb,"GET")|wordis(verb,"TAK"){take(obj);return 0;}
    if wordis(verb,"DRO"){drop(obj);return 0;}
    if wordis(verb,"PUS"){push(obj);return 0;}
    say("I don't know how to do that.\r\n");
    return 0;
```

### Change 2

Find the unique routine header `fn help(){`. Within that routine, replace this existing block, including its shown context:

```rill
    say("LOOK, HELP and QUIT\r\n");
    say("GO NORTH or N; also S, E, W, U and D\r\n");
    say("PUSH.\r\n");
    return 0;
```

With this complete block:

```rill
    say("LOOK, HELP and QUIT\r\n");
    say("GO NORTH or N; also S, E, W, U and D\r\n");
    say("GET and DROP\r\n");
    say("PUSH.\r\n");
    return 0;
```

### Change 3

Find this unique existing declaration or routine header; leave it in place:

```rill
fn push(obj){
```

Insert the following source immediately before it:

```rill
fn drop(obj){
    if obj==0{say("I don't know that object.\r\n");return 0;}
    if places[obj]!=0{say("You do not have it.\r\n");return 0;}
    places[obj]=location;say("Dropped: ");say(itemname(obj));say(".\r\n");
    return 0;
}
```

### Change 4

Find this unique existing declaration or routine header; leave it in place:

```rill
fn drop(obj){
```

Insert the following source immediately before it:

```rill
fn take(obj){
    if obj==0{say("I don't know that object.\r\n");return 0;}
    if places[obj]==0{say("You already have it.\r\n");return 0;}
    if places[obj]!=location{say("You cannot see it here.\r\n");return 0;}
    places[obj]=0;say("Taken: ");say(itemname(obj));say(".\r\n");
    return 0;
}
```

## Build and try it

```dos
VMAKE V08
```

Require these fresh tool reports, followed by BUILD PASS:

```text
OK RESULT.IR 0000022415
OK RESULT.ASM 0000057112 text bytes
OK RESULT.COM 09684 bytes
BUILD PASS
```

The preserved V08.COM is 9,684 bytes. Its natural display and behavior are the checks below.

Create T08.TXT as plain text:

```text
GET TIME
GET TIME
DROP TIME
GET SCROLL
```

Create X08.TXT as plain text:

```text
GET DRAGON
DROP AXE
```

```dos
CHECK V08 T08.TXT
```

Require these significant game lines, followed by CHECK's PASS:

```text
Taken: Timepiece.
You already have it.
Dropped: Timepiece.
You cannot see it here.
PASS
```

## Check the other case

```dos
CHECK V08 X08.TXT
```

Require these significant lines and PASS:

```text
I don't know that object.
You do not have it.
PASS
```

## If it differs

If GET seems to work from another room, check the location comparison before the assignment. Never index places with an unrecognized zero noun.
