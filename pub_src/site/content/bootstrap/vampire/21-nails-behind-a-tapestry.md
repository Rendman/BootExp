+++
title = "21 \u00b7 Nails behind a tapestry"
weight = 21
description = "Loosen the nails with the hammer and uncover an exit by taking the tapestry."
download = "V21.RIL"
download_group = "tools/vampire"
reader_names = 1
+++

The tapestry conceals a doorway, but pulling at it from the floor is not enough. Getting above it and removing the nails makes the two sides of the room agree.

## What changes

take gives Nails and Tapestry separate conditions. loosen requires the carried hammer, sets nails_loose and then allows the nails to enter inventory. Taking the tapestry requires that flag and writes the Gallery north exit to room seventeen. Capacity is checked before either change, so a full inventory cannot silently loosen nails or reveal a doorway. Dropping the nails does not attach them again. The shared gallery transcript leaves spare inventory space rather than treating the carrying limit as an exception.

## Enter the source

Copy V20.RIL to V21.RIL. Apply the following edits in order. All locators are existing declarations or unique routine headers; no editor line numbers are needed. Keep the source outside each stated edit.

### Change 1

Find this unique existing declaration or routine header; leave it in place:

```rill
let mut shore=11;
```

Insert the following source immediately before it:

```rill
let mut nails_loose=0;
```

### Change 2

Find the unique routine header `fn take(obj){`. Within that routine, replace this existing block, including its shown context:

```rill
    if carried()==7{say("You cannot carry any more.\r\n");return 0;}
    if obj==8{if water()==0{return 0;}}
    places[obj]=0;say("Taken: ");say(itemname(obj));say(".\r\n");
    return 0;
```

With this complete block:

```rill
    if carried()==7{say("You cannot carry any more.\r\n");return 0;}
    if obj==8{if water()==0{return 0;}}
    if obj==13{if loosen()==0{return 0;}}
    if obj==14{
        if nails_loose==0{say("It is nailed to the overhang.\r\n");return 0;}
        paths[16*6]=17;say("A hole opens behind the tapestry.\r\n");
    }
    places[obj]=0;say("Taken: ");say(itemname(obj));say(".\r\n");
    return 0;
```

### Change 3

Find the unique routine header `fn newgame(){`. Within that routine, replace this existing block, including its shown context:

```rill
    shore=11;
    stakes=0;
    world();
    items();
```

With this complete block:

```rill
    shore=11;
    stakes=0;
    nails_loose=0;
    world();
    items();
```

### Change 4

Find this unique existing declaration or routine header; leave it in place:

```rill
fn newgame(){
```

Insert the following source immediately before it:

```rill
fn loosen(){
    if places[1]!=0{say("You need the hammer.\r\n");return 0;}
    nails_loose=1;say("The tapestry comes loose.\r\n");return 1;
}
```

## Build and try it

```dos
VMAKE V21
```

Require these fresh tool reports, followed by BUILD PASS:

```text
OK RESULT.IR 0000042135
OK RESULT.ASM 0000108853 text bytes
OK RESULT.COM 17402 bytes
BUILD PASS
```

The preserved V21.COM is 17,402 bytes. Its natural display and behavior are the checks below.

Create F009.TXT with these additional commands:

```text
DROP CRATE
GO OVERHANG
GET NAILS
DROP NAILS
D
GET TAPESTRY
DROP TAPESTRY
GET CRATE
HIT CRATE
AXE
DROP AXE
N
```

Join the saved EQUIP.TXT walk and this tail as GATE.TXT:

```dos
COPY /B EQUIP.TXT+F009.TXT GATE.TXT
```

```dos
COPY GATE.TXT T21.TXT
```

Create F055.TXT with these additional commands:

```text
DROP CRATE
DROP HAMMER
GO OVERHANG
GET NAILS
D
GET TAPESTRY
```

Join the saved EQUIP.TXT walk and this tail as X21.TXT:

```dos
COPY /B EQUIP.TXT+F055.TXT X21.TXT
```

```dos
CHECK V21 T21.TXT
```

Require these significant game lines, followed by CHECK's PASS:

```text
The tapestry comes loose.
A hole opens behind the tapestry.
You are in the Antechamber.
PASS
```

## Check the other case

```dos
CHECK V21 X21.TXT
```

Require these significant lines and PASS:

```text
You need the hammer.
It is nailed to the overhang.
PASS
```

A player death or an unsuccessful action is an ordinary game outcome, so CHECK still reports PASS. Judge the stated message and the resulting world as well as the process status.

## If it differs

If the tapestry moves while still nailed, check that its conditional return precedes the ordinary places[obj]=0 assignment.
