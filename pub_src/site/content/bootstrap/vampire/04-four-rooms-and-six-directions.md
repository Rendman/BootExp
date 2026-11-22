+++
title = "04 \u00b7 Four rooms and six directions"
weight = 4
description = "Represent room names and exits as tables, then walk through the first four rooms."
download = "V04.RIL"
download_group = "tools/vampire"
reader_names = 1
+++

A room number is easier to move around than a whole description. I sketch four boxes on paper before entering their connections. The sketch catches a wrong east or west more quickly than staring at a long string of numbers.

## What changes

names holds word-sized pointers: room n uses bytes n*2 and n*2+1. paths holds six bytes per room, ordered North, South, East, West, Up, Down. Zero means no exit; actual rooms begin at one. room writes one complete row, and roomname reads its pointer. describe prints the current room and its nonzero exits. direction accepts full direction prefixes and one-letter commands. walk changes location only when the selected exit is nonzero. All table indices remain within the declared twenty room records.

## Enter the source

Copy V03.RIL to V04.RIL. Apply the following edits in order. All locators are existing declarations or unique routine headers; no editor line numbers are needed. Keep the source outside each stated edit.

### Change 1

Find this unique existing declaration or routine header; leave it in place:

```rill
fn main(){
```

Insert the following source immediately before it:

```rill
bytes names[40];
bytes paths[120];
```

### Change 2

Find this unique existing declaration or routine header; leave it in place:

```rill
bytes command[81];
```

Insert the following source immediately before it:

```rill
let mut location=1;
```

### Change 3

Find the unique routine header `fn main(){`. Within that routine, replace this existing block, including its shown context:

```rill
    say("Vampire Castle Adventure\r\n");
    startinput();
    say("You are in the Entrance Hall.\r\n");
    while playing{
        say("\r\n> ");
```

With this complete block:

```rill
    say("Vampire Castle Adventure\r\n");
    startinput();
    newgame();describe();
    while playing{
        say("\r\n> ");
```

### Change 4

Find the unique routine header `fn act(){`. Within that routine, replace this existing block, including its shown context:

```rill
fn act(){
    if wordis(verb,"HEL"){help();return 0;}
    if wordis(verb,"LOO"){say("You are in the Entrance Hall.\r\n");return 0;}
    say("I don't know how to do that.\r\n");
    return 0;
```

With this complete block:

```rill
fn act(){
    if wordis(verb,"HEL"){help();return 0;}
    if wordis(verb,"GO ")|wordis(verb,"CLI")|((words==1)&(direction()!=0)){walk();return 0;}
    if wordis(verb,"LOO"){describe();return 0;}
    say("I don't know how to do that.\r\n");
    return 0;
```

### Change 5

Find the unique routine header `fn help(){`. Within that routine, replace this existing block, including its shown context:

```rill
fn help(){
    say("Use the first and last words; only three letters count.\r\n");
    say("LOOK, HELP and QUIT.\r\n");
    return 0;
}
```

With this complete block:

```rill
fn help(){
    say("Use the first and last words; only three letters count.\r\n");
    say("LOOK, HELP and QUIT\r\n");
    say("GO NORTH or N; also S, E, W, U and D.\r\n");
    return 0;
}
```

### Change 6

Append these complete routines after the final routine in your source:

```rill
fn newgame(){
    location=1;playing=1;
    world();
    return 0;
}
```

### Change 7

Find this unique existing declaration or routine header; leave it in place:

```rill
fn newgame(){
```

Insert the following source immediately before it:

```rill
fn walk(){
    let mut d=direction();
    if d{
        let mut next=paths[location*6+d-1];
        if next{location=next;describe();}
        else{say("You cannot go that way.\r\n");}
        return 0;
    }
    say("You cannot go there.\r\n");
    return 0;
}
```

### Change 8

Find this unique existing declaration or routine header; leave it in place:

```rill
fn walk(){
```

Insert the following source immediately before it:

```rill
fn direction(){
    let mut p=noun;
    if words==1{p=verb;}
    if wordis(p,"NOR")|wordis(p,"N  "){return 1;}
    if wordis(p,"SOU")|wordis(p,"S  "){return 2;}
    if wordis(p,"EAS")|wordis(p,"E  "){return 3;}
    if wordis(p,"WES")|wordis(p,"W  "){return 4;}
    if wordis(p,"UP ")|wordis(p,"U  "){return 5;}
    if wordis(p,"DOW")|wordis(p,"D  "){return 6;}
    return 0;
}
```

### Change 9

Find this unique existing declaration or routine header; leave it in place:

```rill
fn direction(){
```

Insert the following source immediately before it:

```rill
fn dirname(n){
    if n==1{return "North";}if n==2{return "South";}
    if n==3{return "East";}if n==4{return "West";}
    if n==5{return "Up";}return "Down";
}
```

### Change 10

Find this unique existing declaration or routine header; leave it in place:

```rill
fn dirname(n){
```

Insert the following source immediately before it:

```rill
fn describe(){
    say("\r\nYou are in the ");say(roomname(location));say(".\r\n");
    say("Exits:");
    let mut i=0;
    while i<6{
        if paths[location*6+i]{say(" ");say(dirname(i+1));}
        i=i+1;
    }
    say("\r\n");
    return 0;
}
```

### Change 11

Find this unique existing declaration or routine header; leave it in place:

```rill
fn describe(){
```

Insert the following source immediately before it:

```rill
fn roomname(n){return load16(names+n*2);}
```

### Change 12

Find this unique existing declaration or routine header; leave it in place:

```rill
fn roomname(n){return load16(names+n*2);}
```

Insert the following source immediately before it:

```rill
fn world(){
    room(1,"Entrance Hall",0,0,3,2,0,0);
    room(2,"Study",0,0,1,0,0,0);
    room(3,"Library",0,0,4,1,0,0);
    room(4,"Armory",0,0,0,3,0,0);
    return 0;
}
```

### Change 13

Find this unique existing declaration or routine header; leave it in place:

```rill
fn world(){
```

Insert the following source immediately before it:

```rill
fn room(n,text,north,south,east,west,up,down){
    store16(names+n*2,text);
    let mut p=n*6;
    paths[p]=north;paths[p+1]=south;
    paths[p+2]=east;paths[p+3]=west;
    paths[p+4]=up;paths[p+5]=down;
    return 0;
}
```

## Build and try it

```dos
VMAKE V04
```

Require these fresh tool reports, followed by BUILD PASS:

```text
OK RESULT.IR 0000013867
OK RESULT.ASM 0000036794 text bytes
OK RESULT.COM 06512 bytes
BUILD PASS
```

The preserved V04.COM is 6,512 bytes. Its natural display and behavior are the checks below.

Create T04.TXT as plain text:

```text
E
W
N
GET NORTH
```

Create X04.TXT as plain text:

```text
GO UP
```

```dos
CHECK V04 T04.TXT
```

Require these significant game lines, followed by CHECK's PASS:

```text
You are in the Library.
You cannot go that way.
I don't know how to do that.
PASS
```

## Check the other case

```dos
CHECK V04 X04.TXT
```

Require these significant lines and PASS:

```text
You cannot go that way.
PASS
```

## If it differs

Check the six argument positions against the heading on your paper map. A room pointer is a word, so use store16 and load16.
