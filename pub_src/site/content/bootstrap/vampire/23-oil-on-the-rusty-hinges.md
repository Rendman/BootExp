+++
title = "23 \u00b7 Oil on the rusty hinges"
weight = 23
description = "Open the antechamber door with the carried flask of oil."
download = "V23.RIL"
download_group = "tools/vampire"
reader_names = 1
+++

The door has a place and a name like other scenery, but its passage is another table entry. The oil changes all three facts consistently.

## What changes

oil requires the door noun, the Antechamber and the carried flask. It sets door_open, changes the visible name and installs the north exit to the Tomb. It does not consume the flask; this game does not measure remaining quantities of oil. Repeating the action is harmless. Wrong locations and missing oil leave the map untouched. The KEY.TXT route provides the carried oil without requiring a special command-line setup or a hidden test mode.

## Enter the source

Copy V22.RIL to V23.RIL. Apply the following edits in order. All locators are existing declarations or unique routine headers; no editor line numbers are needed. Keep the source outside each stated edit.

### Change 1

Find this unique existing declaration or routine header; leave it in place:

```rill
let mut shore=11;
```

Insert the following source immediately before it:

```rill
let mut door_open=0;
```

### Change 2

Find the unique routine header `fn act(){`. Within that routine, replace this existing block, including its shown context:

```rill
    if wordis(verb,"PUS"){push(obj);return 0;}
    if wordis(verb,"ROW"){rowboat();return 0;}
    say("I don't know how to do that.\r\n");
    return 0;
```

With this complete block:

```rill
    if wordis(verb,"PUS"){push(obj);return 0;}
    if wordis(verb,"ROW"){rowboat();return 0;}
    if wordis(verb,"OIL"){oil(obj);return 0;}
    say("I don't know how to do that.\r\n");
    return 0;
```

### Change 3

Find the unique routine header `fn help(){`. Within that routine, replace this existing block, including its shown context:

```rill
    say("HIT\r\n");
    say("TIE\r\n");
    say("ROW and SWIM.\r\n");
    return 0;
}
```

With this complete block:

```rill
    say("HIT\r\n");
    say("TIE\r\n");
    say("ROW and SWIM\r\n");
    say("OIL.\r\n");
    return 0;
}
```

### Change 4

Find the unique routine header `fn newgame(){`. Within that routine, replace this existing block, including its shown context:

```rill
    stakes=0;
    nails_loose=0;
    world();
    items();
```

With this complete block:

```rill
    stakes=0;
    nails_loose=0;
    door_open=0;
    world();
    items();
```

### Change 5

Find this unique existing declaration or routine header; leave it in place:

```rill
fn newgame(){
```

Insert the following source immediately before it:

```rill
fn oil(obj){
    if (obj!=16)|(location!=17)|(places[9]!=0){say("You cannot oil that here.\r\n");return 0;}
    door_open=1;store16(things+16*2,"Open Door");paths[17*6]=18;
    say("The rusty door squeaks open.\r\n");return 0;
}
```

## Build and try it

```dos
VMAKE V23
```

Require these fresh tool reports, followed by BUILD PASS:

```text
OK RESULT.IR 0000043914
OK RESULT.ASM 0000113771 text bytes
OK RESULT.COM 18116 bytes
BUILD PASS
```

The preserved V23.COM is 18,116 bytes. Its natural display and behavior are the checks below.

Create F012.TXT with these additional commands:

```text
OIL DOOR
N
```

Join the saved KEY.TXT walk and this tail as TOMB.TXT:

```dos
COPY /B KEY.TXT+F012.TXT TOMB.TXT
```

```dos
COPY TOMB.TXT T23.TXT
```

Create F059.TXT with these additional commands:

```text
DROP OIL
OIL DOOR
N
```

Join the saved GATE.TXT walk and this tail as X23.TXT:

```dos
COPY /B GATE.TXT+F059.TXT X23.TXT
```

```dos
CHECK V23 T23.TXT
```

Require these significant game lines, followed by CHECK's PASS:

```text
The rusty door squeaks open.
You are in the Dracula's Tomb.
PASS
```

## Check the other case

```dos
CHECK V23 X23.TXT
```

Require these significant lines and PASS:

```text
You cannot oil that here.
You cannot go that way.
PASS
```

A player death or an unsuccessful action is an ordinary game outcome, so CHECK still reports PASS. Judge the stated message and the resulting world as well as the process status.

## If it differs

Use paths[17*6] for North. Changing the door description without changing that byte would leave an apparently open but impassable door.
