+++
title = "10 \u00b7 Seven things in a pocket"
weight = 10
description = "Display the inventory and enforce a seven-object carrying limit."
download = "V10.RIL"
download_group = "tools/vampire"
reader_names = 1
+++

I could keep a separate count and adjust it after every action. Counting the zero locations is simpler, and it cannot drift out of step when a puzzle consumes an object.

## What changes

carried counts entries whose location is zero. inventory displays exactly those entries and prints Nothing when there are none. take checks the carrying limit after rejecting unknown, absent, fixed or already-carried objects. A rejected eighth possession changes no location. Dropping one frees a place immediately. The bound is deliberately a game rule: these tables themselves occupy very little memory. The inventory display is part of the adventure, not a temporary testing routine.

## Enter the source

Copy V09.RIL to V10.RIL. Apply the following edits in order. All locators are existing declarations or unique routine headers; no editor line numbers are needed. Keep the source outside each stated edit.

### Change 1

Find the unique routine header `fn act(){`. Within that routine, replace this existing block, including its shown context:

```rill
fn act(){
    if wordis(verb,"HEL"){help();return 0;}
    if wordis(verb,"GO ")|wordis(verb,"CLI")|((words==1)&(direction()!=0)){walk();return 0;}
    if wordis(verb,"LOO"){describe();return 0;}
```

With this complete block:

```rill
fn act(){
    if wordis(verb,"HEL"){help();return 0;}
    if wordis(verb,"INV"){inventory();return 0;}
    if wordis(verb,"GO ")|wordis(verb,"CLI")|((words==1)&(direction()!=0)){walk();return 0;}
    if wordis(verb,"LOO"){describe();return 0;}
```

### Change 2

Find the unique routine header `fn help(){`. Within that routine, replace this existing block, including its shown context:

```rill
    say("GO NORTH or N; also S, E, W, U and D\r\n");
    say("GET and DROP\r\n");
    say("PUSH.\r\n");
    return 0;
```

With this complete block:

```rill
    say("GO NORTH or N; also S, E, W, U and D\r\n");
    say("GET and DROP\r\n");
    say("INVENTORY\r\n");
    say("PUSH.\r\n");
    return 0;
```

### Change 3

Find the unique routine header `fn take(obj){`. Within that routine, replace this existing block, including its shown context:

```rill
    if places[obj]!=location{say("You cannot see it here.\r\n");return 0;}
    if (obj>=15)&(obj<=23){say("You cannot take that.\r\n");return 0;}
    places[obj]=0;say("Taken: ");say(itemname(obj));say(".\r\n");
    return 0;
```

With this complete block:

```rill
    if places[obj]!=location{say("You cannot see it here.\r\n");return 0;}
    if (obj>=15)&(obj<=23){say("You cannot take that.\r\n");return 0;}
    if carried()==7{say("You cannot carry any more.\r\n");return 0;}
    places[obj]=0;say("Taken: ");say(itemname(obj));say(".\r\n");
    return 0;
```

### Change 4

Find this unique existing declaration or routine header; leave it in place:

```rill
fn take(obj){
```

Insert the following source immediately before it:

```rill
fn inventory(){
    say("You are carrying:\r\n");
    let mut i=1;
    while i<=25{
        if places[i]==0{say("  ");say(itemname(i));say("\r\n");}
        i=i+1;
    }
    if carried()==0{say("  Nothing.\r\n");}
    return 0;
}
```

### Change 5

Find this unique existing declaration or routine header; leave it in place:

```rill
fn inventory(){
```

Insert the following source immediately before it:

```rill
fn carried(){
    let mut i=1;let mut count=0;
    while i<=25{if places[i]==0{count=count+1;}i=i+1;}
    return count;
}
```

## Build and try it

```dos
VMAKE V10
```

Require these fresh tool reports, followed by BUILD PASS:

```text
OK RESULT.IR 0000027999
OK RESULT.ASM 0000070437 text bytes
OK RESULT.COM 11696 bytes
BUILD PASS
```

The preserved V10.COM is 11,696 bytes. Its natural display and behavior are the checks below.

Create T10.TXT as plain text:

```text
GET TIME
W
GET WINE
GET CHEESE
E
E
GET SCROLL
PUSH BOOKCASE
D
GET ROPE
N
GET OIL
N
GET BUCKET
GET CRATE
DROP BUCKET
GET CRATE
INVENTORY
```

Create X10.TXT as plain text:

```text
INVENTORY
```

```dos
CHECK V10 T10.TXT
```

Require these significant game lines, followed by CHECK's PASS:

```text
You cannot carry any more.
Dropped: Bucket.
Taken: Crate.
You are carrying:
PASS
```

## Check the other case

```dos
CHECK V10 X10.TXT
```

Require these significant lines and PASS:

```text
  Nothing.
PASS
```

## If it differs

A failed eighth GET must leave the object in its room. Make the check before writing zero.

![A rat guards an oversized key while a visitor offers a wedge of cheese beside a crowded coat rack.](../../../images/vampire-rat.svg)

*Not every obstacle calls for a larger tool.*

