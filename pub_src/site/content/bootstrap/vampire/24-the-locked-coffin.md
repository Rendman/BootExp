+++
title = "24 \u00b7 The locked coffin"
weight = 24
description = "Use the carried key to open the coffin and reveal Dracula."
download = "V24.RIL"
download_group = "tools/vampire"
reader_names = 1
+++

An open door is not an open coffin. The final room has its own condition, and opening it should not work from the other end of the castle.

## What changes

openobject first requires the target in the current room. A rusty door reports its open or rusted condition. The coffin requires the carried key before setting coffin_open and replacing its description with Dracula in the Coffin. A key merely dropped beside the coffin is insufficient. COFFIN and DRACULA refer to the same fixed object number; its changing description never alters that identity. The existing darkness gate requires the torch here too.

## Enter the source

Copy V23.RIL to V24.RIL. Apply the following edits in order. All locators are existing declarations or unique routine headers; no editor line numbers are needed. Keep the source outside each stated edit.

### Change 1

Find this unique existing declaration or routine header; leave it in place:

```rill
let mut shore=11;
```

Insert the following source immediately before it:

```rill
let mut coffin_open=0;
```

### Change 2

Find the unique routine header `fn act(){`. Within that routine, replace this existing block, including its shown context:

```rill
    if wordis(verb,"ROW"){rowboat();return 0;}
    if wordis(verb,"OIL"){oil(obj);return 0;}
    say("I don't know how to do that.\r\n");
    return 0;
```

With this complete block:

```rill
    if wordis(verb,"ROW"){rowboat();return 0;}
    if wordis(verb,"OIL"){oil(obj);return 0;}
    if wordis(verb,"OPE"){openobject(obj);return 0;}
    say("I don't know how to do that.\r\n");
    return 0;
```

### Change 3

Find the unique routine header `fn help(){`. Within that routine, replace this existing block, including its shown context:

```rill
    say("TIE\r\n");
    say("ROW and SWIM\r\n");
    say("OIL.\r\n");
    return 0;
}
```

With this complete block:

```rill
    say("TIE\r\n");
    say("ROW and SWIM\r\n");
    say("OIL\r\n");
    say("OPEN.\r\n");
    return 0;
}
```

### Change 4

Find the unique routine header `fn newgame(){`. Within that routine, replace this existing block, including its shown context:

```rill
    nails_loose=0;
    door_open=0;
    world();
    items();
```

With this complete block:

```rill
    nails_loose=0;
    door_open=0;
    coffin_open=0;
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
fn openobject(obj){
    if obj==0{say("I don't know that object.\r\n");return 0;}
    if places[obj]!=location{say("You cannot see it here.\r\n");return 0;}
    if obj==16{
        if door_open{say("The door is already open.\r\n");}
        else{say("There is too much rust.\r\n");}
        return 0;
    }
    if obj==17{
        if places[7]!=0{say("The coffin is locked.\r\n");return 0;}
        coffin_open=1;store16(things+17*2,"Dracula in the Coffin");
        say("The lid opens. Dracula lies inside.\r\n");return 0;
    }
    say("Nothing happens.\r\n");return 0;
}
```

## Build and try it

```dos
VMAKE V24
```

Require these fresh tool reports, followed by BUILD PASS:

```text
OK RESULT.IR 0000045547
OK RESULT.ASM 0000118707 text bytes
OK RESULT.COM 18802 bytes
BUILD PASS
```

The preserved V24.COM is 18,802 bytes. Its natural display and behavior are the checks below.

Create F013.TXT with these additional commands:

```text
OPEN COFFIN
```

Join the saved TOMB.TXT walk and this tail as COFFIN.TXT:

```dos
COPY /B TOMB.TXT+F013.TXT COFFIN.TXT
```

```dos
COPY COFFIN.TXT T24.TXT
```

Create F061.TXT with these additional commands:

```text
DROP KEY
OPEN COFFIN
```

Join the saved TOMB.TXT walk and this tail as X24.TXT:

```dos
COPY /B TOMB.TXT+F061.TXT X24.TXT
```

```dos
CHECK V24 T24.TXT
```

Require these significant game lines, followed by CHECK's PASS:

```text
The lid opens. Dracula lies inside.
PASS
```

## Check the other case

```dos
CHECK V24 X24.TXT
```

Require these significant lines and PASS:

```text
The coffin is locked.
PASS
```

A player death or an unsuccessful action is an ordinary game outcome, so CHECK still reports PASS. Judge the stated message and the resulting world as well as the process status.

## If it differs

Check that key location is zero, not eighteen. Keep the reachability check ahead of the object-specific cases.
