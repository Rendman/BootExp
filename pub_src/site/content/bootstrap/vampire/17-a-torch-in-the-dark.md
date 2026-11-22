+++
title = "17 \u00b7 A torch in the dark"
weight = 17
description = "Hide room contents in unlit underground areas and make the carried torch reveal them."
download = "V17.RIL"
download_group = "tools/vampire"
reader_names = 1
+++

Knowing a room number is not the same as being able to see its contents. The torch gives the description routine a reason to leave some information out.

## What changes

dark is true in rooms ten through twelve and eighteen unless the torch is carried. describe still identifies the room but withholds objects and exits. inspect and object-changing actions also respect darkness. Movement, inventory and HELP remain available, allowing the player to retrace a known route. The torch found in the fireplace is already burning; this game has no separate lighting or fuel system. Dropping it removes the carried-light condition immediately.

## Enter the source

Copy V16.RIL to V17.RIL. Apply the following edits in order. All locators are existing declarations or unique routine headers; no editor line numbers are needed. Keep the source outside each stated edit.

### Change 1

Find the unique routine header `fn act(){`. Within that routine, replace this existing block, including its shown context:

```rill
    if wordis(verb,"GO ")|wordis(verb,"CLI")|((words==1)&(direction()!=0)){walk();return 0;}
    if wordis(verb,"LOO")|wordis(verb,"REA"){inspect(nounid());return 0;}
    let mut obj=nounid();
    if wordis(verb,"GET")|wordis(verb,"TAK"){take(obj);return 0;}
```

With this complete block:

```rill
    if wordis(verb,"GO ")|wordis(verb,"CLI")|((words==1)&(direction()!=0)){walk();return 0;}
    if wordis(verb,"LOO")|wordis(verb,"REA"){inspect(nounid());return 0;}
    if dark(){say("It is too dark to do that.\r\n");return 0;}
    let mut obj=nounid();
    if wordis(verb,"GET")|wordis(verb,"TAK"){take(obj);return 0;}
```

### Change 2

Find the unique routine header `fn describe(){`. Within that routine, replace this existing block, including its shown context:

```rill
fn describe(){
    say("\r\nYou are in the ");say(roomname(location));say(".\r\n");
    lookitems();
    say("Exits:");
```

With this complete block:

```rill
fn describe(){
    say("\r\nYou are in the ");say(roomname(location));say(".\r\n");
    if dark(){say("It is dark. You cannot see.\r\n");return 0;}
    lookitems();
    say("Exits:");
```

### Change 3

Find the unique routine header `fn inspect(obj){`. Within that routine, replace this existing block, including its shown context:

```rill
fn inspect(obj){
    if wordis(noun,"   "){describe();return 0;}
    if obj==0{say("I don't know that object.\r\n");return 0;}
    if (places[obj]!=location)&(places[obj]!=0){say("You cannot see it here.\r\n");return 0;}
```

With this complete block:

```rill
fn inspect(obj){
    if wordis(noun,"   "){describe();return 0;}
    if dark(){say("It is too dark to do that.\r\n");return 0;}
    if obj==0{say("I don't know that object.\r\n");return 0;}
    if (places[obj]!=location)&(places[obj]!=0){say("You cannot see it here.\r\n");return 0;}
```

### Change 4

Find this unique existing declaration or routine header; leave it in place:

```rill
fn ask(text){
```

Insert the following source immediately before it:

```rill
fn dark(){
    if places[12]==0{return 0;}
    return ((location>=10)&(location<=12))|(location==18);
}
```

## Build and try it

```dos
VMAKE V17
```

Require these fresh tool reports, followed by BUILD PASS:

```text
OK RESULT.IR 0000038122
OK RESULT.ASM 0000098158 text bytes
OK RESULT.COM 15836 bytes
BUILD PASS
```

The preserved V17.COM is 15,836 bytes. Its natural display and behavior are the checks below.

Create F005.TXT with these additional commands:

```text
S
GET TORCH
N
```

Join the saved DARK.TXT walk and this tail as LIGHT.TXT:

```dos
COPY /B DARK.TXT+F005.TXT LIGHT.TXT
```

```dos
COPY LIGHT.TXT T17.TXT
```

Create F047.TXT with these additional commands:

```text
DROP TORCH
LOOK
GET TORCH
```

Join the saved LIGHT.TXT walk and this tail as X17.TXT:

```dos
COPY /B LIGHT.TXT+F047.TXT X17.TXT
```

```dos
CHECK V17 T17.TXT
```

Require these significant game lines, followed by CHECK's PASS:

```text
It is dark. You cannot see.
Taken: Torch.
You are in the Secret Passage.
PASS
```

## Check the other case

```dos
CHECK V17 X17.TXT
```

Require these significant lines and PASS:

```text
It is too dark to do that.
PASS
```

A player death or an unsuccessful action is an ordinary game outcome, so CHECK still reports PASS. Judge the stated message and the resulting world as well as the process status.

## If it differs

Test both sides of the condition in the same room. Merely seeing a torch on the floor does not mean places[12] is zero.
