+++
title = "07 \u00b7 Putting things in rooms"
weight = 7
description = "List named objects separately from the room map."
download = "V07.RIL"
download_group = "tools/vampire"
reader_names = 1
+++

The first objects are ordinary possessions: a timepiece, scroll, rope, axe, hammer and oar. Their names stay fixed while their locations will change. I keep these facts in separate tables.

## What changes

things stores word pointers to object names; places stores one byte per object. A positive room number places an object there. Zero means carried, and 99 means absent from play. item writes the name and location together. Unintroduced object slots are explicitly set to 99, so they cannot appear in an inventory by accident. lookitems walks the object numbers in a stable order and prints those in the current room. nounid gives command prefixes the corresponding object number; zero means unrecognized.

## Enter the source

Copy V06.RIL to V07.RIL. Apply the following edits in order. All locators are existing declarations or unique routine headers; no editor line numbers are needed. Keep the source outside each stated edit.

### Change 1

Find this unique existing declaration or routine header; leave it in place:

```rill
fn main(){
```

Insert the following source immediately before it:

```rill
bytes things[52];
bytes places[26];
```

### Change 2

Find the unique routine header `fn describe(){`. Within that routine, replace this existing block, including its shown context:

```rill
fn describe(){
    say("\r\nYou are in the ");say(roomname(location));say(".\r\n");
    say("Exits:");
    let mut i=0;
```

With this complete block:

```rill
fn describe(){
    say("\r\nYou are in the ");say(roomname(location));say(".\r\n");
    lookitems();
    say("Exits:");
    let mut i=0;
```

### Change 3

Find the unique routine header `fn newgame(){`. Within that routine, replace this existing block, including its shown context:

```rill
    location=1;playing=1;
    world();
    return 0;
}
```

With this complete block:

```rill
    location=1;playing=1;
    world();
    items();
    return 0;
}
```

### Change 4

Find this unique existing declaration or routine header; leave it in place:

```rill
fn push(obj){
```

Insert the following source immediately before it:

```rill
fn lookitems(){
    say("You see:\r\n");
    let mut i=1;let mut count=0;
    while i<=25{
        if places[i]==location{say("  ");say(itemname(i));say("\r\n");count=count+1;}
        i=i+1;
    }
    if count==0{say("  Nothing interesting.\r\n");}
    return 0;
}
```

### Change 5

Find this unique existing declaration or routine header; leave it in place:

```rill
fn lookitems(){
```

Insert the following source immediately before it:

```rill
fn nounid(){
    if wordis(noun,"HAM")|wordis(noun,"SLE"){return 1;}
    if wordis(noun,"TIM"){return 2;}
    if wordis(noun,"ROP"){
        return 3;
    }
    if (location==5)&wordis(noun,"PAR"){return 21;}
    if wordis(noun,"SCR")|wordis(noun,"PAR"){return 4;}
    if wordis(noun,"AXE")|wordis(noun,"AX "){return 5;}
    if wordis(noun,"OAR"){return 6;}
    if wordis(noun,"BOO"){return 19;}
    return 0;
}
```

### Change 6

Find this unique existing declaration or routine header; leave it in place:

```rill
fn nounid(){
```

Insert the following source immediately before it:

```rill
fn items(){
    let mut i=1;
    while i<=25{places[i]=99;i=i+1;}
    item(1,"Sledge Hammer",5);item(2,"Timepiece",1);
    item(3,"Coil of Rope",9);item(4,"Parchment Scroll",3);
    item(5,"Axe",4);item(6,"Oar",6);
    return 0;
}
```

### Change 7

Find this unique existing declaration or routine header; leave it in place:

```rill
fn items(){
```

Insert the following source immediately before it:

```rill
fn itemname(n){return load16(things+n*2);}
```

### Change 8

Find this unique existing declaration or routine header; leave it in place:

```rill
fn itemname(n){return load16(things+n*2);}
```

Insert the following source immediately before it:

```rill
fn item(n,text,where){store16(things+n*2,text);places[n]=where;return 0;}
```

## Build and try it

```dos
VMAKE V07
```

Require these fresh tool reports, followed by BUILD PASS:

```text
OK RESULT.IR 0000020580
OK RESULT.ASM 0000052082 text bytes
OK RESULT.COM 08928 bytes
BUILD PASS
```

The preserved V07.COM is 8,928 bytes. Its natural display and behavior are the checks below.

Create T07.TXT as plain text:

```text
LOOK
E
LOOK
```

Create X07.TXT as plain text:

```text
W
LOOK
```

```dos
CHECK V07 T07.TXT
```

Require these significant game lines, followed by CHECK's PASS:

```text
  Timepiece
  Parchment Scroll
PASS
```

## Check the other case

```dos
CHECK V07 X07.TXT
```

Require these significant lines and PASS:

```text
You are in the Study.
  Nothing interesting.
PASS
```

## If it differs

Do not confuse object numbers with room numbers. Both begin at one, but they index different tables.
