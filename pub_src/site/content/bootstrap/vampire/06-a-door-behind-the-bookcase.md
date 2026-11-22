+++
title = "06 \u00b7 A door behind the bookcase"
weight = 6
description = "Add the underground map and reveal a hidden exit by pushing the library bookcase."
download = "V06.RIL"
download_group = "tools/vampire"
reader_names = 1
+++

A map need not show every way out at first. The Library has a bookcase, and moving it changes a connection rather than changing the rules for movement.

## What changes

world supplies the remaining eleven room rows. push recognizes the bookcase only in the Library and writes room nine into its Down exit. At this stopping point act obtains the bookcase number directly from the noun prefix; push already receives an object number. describe then shows Down, and walk uses the altered row without a special case. Repeating PUSH BOOKCASE writes the same destination and is harmless. The hidden corridor, laboratory and storeroom can now be explored, including the storeroom stair back to the Study.

## Enter the source

Copy V05.RIL to V06.RIL. Apply the following edits in order. All locators are existing declarations or unique routine headers; no editor line numbers are needed. Keep the source outside each stated edit.

### Change 1

Find the unique routine header `fn act(){`. Within that routine, replace this existing block, including its shown context:

```rill
    if wordis(verb,"GO ")|wordis(verb,"CLI")|((words==1)&(direction()!=0)){walk();return 0;}
    if wordis(verb,"LOO"){describe();return 0;}
    say("I don't know how to do that.\r\n");
    return 0;
```

With this complete block:

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

### Change 2

Find the unique routine header `fn help(){`. Within that routine, replace this existing block, including its shown context:

```rill
    say("Use the first and last words; only three letters count.\r\n");
    say("LOOK, HELP and QUIT\r\n");
    say("GO NORTH or N; also S, E, W, U and D.\r\n");
    return 0;
}
```

With this complete block:

```rill
    say("Use the first and last words; only three letters count.\r\n");
    say("LOOK, HELP and QUIT\r\n");
    say("GO NORTH or N; also S, E, W, U and D\r\n");
    say("PUSH.\r\n");
    return 0;
}
```

### Change 3

Find the unique routine header `fn world(){`. Within that routine, replace this existing block, including its shown context:

```rill
    room(7,"Chapel",6,0,0,0,4,0);
    room(8,"Brick Fireplace",0,2,0,0,0,0);
    return 0;
}
```

With this complete block:

```rill
    room(7,"Chapel",6,0,0,0,4,0);
    room(8,"Brick Fireplace",0,2,0,0,0,0);
    room(9,"Hidden Corridor",13,0,0,0,3,0);
    room(10,"Secret Passage",11,8,0,19,0,0);
    room(11,"Underground Lake Chamber",0,10,0,0,0,0);
    room(12,"Boat",0,11,0,0,0,0);
    room(13,"Alchemist's Lab",14,9,0,0,0,0);
    room(14,"Storeroom",0,13,0,0,2,0);
    room(15,"Overhang",0,0,0,0,0,16);
    room(16,"Gallery",0,0,0,0,0,0);
    room(17,"Antechamber",0,16,0,0,0,0);
    room(18,"Dracula's Tomb",0,17,0,0,0,0);
    room(19,"Torture Chamber",0,0,10,13,0,0);
    return 0;
}
```

### Change 4

Find this unique existing declaration or routine header; leave it in place:

```rill
fn newgame(){
```

Insert the following source immediately before it:

```rill
fn push(obj){
    if (obj==19)&(location==3){
        paths[3*6+5]=9;say("A doorway opens behind the bookcase.\r\n");
    }else{say("Nothing happens.\r\n");}
    return 0;
}
```

## Build and try it

```dos
VMAKE V06
```

Require these fresh tool reports, followed by BUILD PASS:

```text
OK RESULT.IR 0000017186
OK RESULT.ASM 0000044492 text bytes
OK RESULT.COM 07653 bytes
BUILD PASS
```

The preserved V06.COM is 7,653 bytes. Its natural display and behavior are the checks below.

Create T06.TXT as plain text:

```text
E
PUSH BOOKCASE
D
N
N
U
```

Create X06.TXT as plain text:

```text
PUSH BOOKCASE
D
```

```dos
CHECK V06 T06.TXT
```

Require these significant game lines, followed by CHECK's PASS:

```text
A doorway opens behind the bookcase.
You are in the Hidden Corridor.
You are in the Storeroom.
You are in the Study.
PASS
```

## Check the other case

```dos
CHECK V06 X06.TXT
```

Require these significant lines and PASS:

```text
Nothing happens.
You cannot go that way.
PASS
```

## If it differs

If Down appears in the wrong room, check the row calculation: the Library starts at 3*6, and Down adds five.
