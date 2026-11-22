+++
title = "11 \u00b7 Reading the warnings"
weight = 11
description = "Examine reachable objects, including the sign and parchment scroll."
download = "V11.RIL"
download_group = "tools/vampire"
reader_names = 1
+++

The entrance sign is a warning; the scroll is a hint. LOOK and READ can share the same inspection rules while ordinary LOOK still describes the room.

## What changes

inspect receives nounid and treats an empty noun as a room description. It rejects an unknown or unreachable object before examining its particular number. The sign can be read where it hangs. The scroll must be carried, so finding it and reading it are separate actions. All other accessible objects receive the ordinary nothing-special response. This ordering prevents a special description from disclosing an object from anywhere in the castle.

## Enter the source

Copy V10.RIL to V11.RIL. Apply the following edits in order. All locators are existing declarations or unique routine headers; no editor line numbers are needed. Keep the source outside each stated edit.

### Change 1

Find the unique routine header `fn act(){`. Within that routine, replace this existing block, including its shown context:

```rill
    if wordis(verb,"INV"){inventory();return 0;}
    if wordis(verb,"GO ")|wordis(verb,"CLI")|((words==1)&(direction()!=0)){walk();return 0;}
    if wordis(verb,"LOO"){describe();return 0;}
    let mut obj=nounid();
    if wordis(verb,"GET")|wordis(verb,"TAK"){take(obj);return 0;}
```

With this complete block:

```rill
    if wordis(verb,"INV"){inventory();return 0;}
    if wordis(verb,"GO ")|wordis(verb,"CLI")|((words==1)&(direction()!=0)){walk();return 0;}
    if wordis(verb,"LOO")|wordis(verb,"REA"){inspect(nounid());return 0;}
    let mut obj=nounid();
    if wordis(verb,"GET")|wordis(verb,"TAK"){take(obj);return 0;}
```

### Change 2

Find the unique routine header `fn help(){`. Within that routine, replace this existing block, including its shown context:

```rill
    say("GET and DROP\r\n");
    say("INVENTORY\r\n");
    say("PUSH.\r\n");
    return 0;
```

With this complete block:

```rill
    say("GET and DROP\r\n");
    say("INVENTORY\r\n");
    say("READ\r\n");
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
fn inspect(obj){
    if wordis(noun,"   "){describe();return 0;}
    if obj==0{say("I don't know that object.\r\n");return 0;}
    if (places[obj]!=location)&(places[obj]!=0){say("You cannot see it here.\r\n");return 0;}
    if obj==20{say("The sign reads: Dracula wakes at midnight.\r\n");return 0;}
    if obj==4{
        if places[4]==0{say("The scroll reads: Not all exits are obvious.\r\n");}
        else{say("Pick up the scroll to read it.\r\n");}
        return 0;
    }
    say("You see nothing special.\r\n");return 0;
}
```

## Build and try it

```dos
VMAKE V11
```

Require these fresh tool reports, followed by BUILD PASS:

```text
OK RESULT.IR 0000029456
OK RESULT.ASM 0000075131 text bytes
OK RESULT.COM 12352 bytes
BUILD PASS
```

The preserved V11.COM is 12,352 bytes. Its natural display and behavior are the checks below.

Create T11.TXT as plain text:

```text
READ THE SIGN
E
READ SCROLL
GET SCROLL
READ THE SCROLL
```

Create X11.TXT as plain text:

```text
READ AXE
```

```dos
CHECK V11 T11.TXT
```

Require these significant game lines, followed by CHECK's PASS:

```text
Dracula wakes at midnight.
Pick up the scroll to read it.
Not all exits are obvious.
PASS
```

## Check the other case

```dos
CHECK V11 X11.TXT
```

Require these significant lines and PASS:

```text
You cannot see it here.
PASS
```

## If it differs

READ THE SCROLL uses the last word. If the command is recognized but asks you to pick it up, inspect places[4], not the parser.
