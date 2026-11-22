+++
title = "18 \u00b7 Across the underground lake"
weight = 18
description = "Enter the boat, row with the oar and keep track of its current shore."
download = "V18.RIL"
download_group = "tools/vampire"
reader_names = 1
+++

The Boat is a room while I am aboard and an object while I stand beside it. Its shore must agree with both representations.

## What changes

GO BOAT requires the boat object at the current location. rowboat requires room twelve and the carried oar. shore alternates between eleven and sixteen because their sum is twenty-seven. The action moves both player and boat to that shore, and updates the Boat south exit to the same destination. Thus leaving the boat without rowing returns to the correct bank. SWIM in the lake chamber is fatal; swimming elsewhere does not end the game. All travel still uses ordinary word values and table bytes.

## Enter the source

Copy V17.RIL to V18.RIL. Apply the following edits in order. All locators are existing declarations or unique routine headers; no editor line numbers are needed. Keep the source outside each stated edit.

### Change 1

Find this unique existing declaration or routine header; leave it in place:

```rill
bytes command[81];
```

Insert the following source immediately before it:

```rill
let mut shore=11;
```

### Change 2

Find the unique routine header `fn act(){`. Within that routine, replace this existing block, including its shown context:

```rill
    if wordis(verb,"INV"){inventory();return 0;}
    if wordis(verb,"WAI"){say("Time passes.\r\n");return 0;}
    if wordis(verb,"GO ")|wordis(verb,"CLI")|((words==1)&(direction()!=0)){walk();return 0;}
    if wordis(verb,"LOO")|wordis(verb,"REA"){inspect(nounid());return 0;}
    if dark(){say("It is too dark to do that.\r\n");return 0;}
    let mut obj=nounid();
    if wordis(verb,"GET")|wordis(verb,"TAK"){take(obj);return 0;}
    if wordis(verb,"DRO"){drop(obj);return 0;}
    if wordis(verb,"HIT")|wordis(verb,"BRE"){hit(obj);return 0;}
    if wordis(verb,"TIE"){tie(obj);return 0;}
    if wordis(verb,"PUS"){push(obj);return 0;}
    say("I don't know how to do that.\r\n");
    return 0;
```

With this complete block:

```rill
    if wordis(verb,"INV"){inventory();return 0;}
    if wordis(verb,"WAI"){say("Time passes.\r\n");return 0;}
    if wordis(verb,"SWI"){
        if location==11{lose("The ice-cold lake pulls you under.\r\n");}
        else{say("There is nowhere to swim here.\r\n");}
        return 0;
    }
    if wordis(verb,"GO ")|wordis(verb,"CLI")|((words==1)&(direction()!=0)){walk();return 0;}
    if wordis(verb,"LOO")|wordis(verb,"REA"){inspect(nounid());return 0;}
    if dark(){say("It is too dark to do that.\r\n");return 0;}
    let mut obj=nounid();
    if wordis(verb,"GET")|wordis(verb,"TAK"){take(obj);return 0;}
    if wordis(verb,"DRO"){drop(obj);return 0;}
    if wordis(verb,"HIT")|wordis(verb,"BRE"){hit(obj);return 0;}
    if wordis(verb,"TIE"){tie(obj);return 0;}
    if wordis(verb,"PUS"){push(obj);return 0;}
    if wordis(verb,"ROW"){rowboat();return 0;}
    say("I don't know how to do that.\r\n");
    return 0;
```

### Change 3

Find the unique routine header `fn help(){`. Within that routine, replace this existing block, including its shown context:

```rill
    say("WAIT\r\n");
    say("HIT\r\n");
    say("TIE.\r\n");
    return 0;
}
```

With this complete block:

```rill
    say("WAIT\r\n");
    say("HIT\r\n");
    say("TIE\r\n");
    say("ROW and SWIM.\r\n");
    return 0;
}
```

### Change 4

Find the unique routine header `fn walk(){`. Within that routine, replace this existing block, including its shown context:

```rill
        return 0;
    }
    say("You cannot go there.\r\n");
    return 0;
```

With this complete block:

```rill
        return 0;
    }
    if (obj==15)&(places[15]==location){location=12;describe();return 0;}
    say("You cannot go there.\r\n");
    return 0;
```

### Change 5

Find the unique routine header `fn newgame(){`. Within that routine, replace this existing block, including its shown context:

```rill
    fire_out=0;
    rope_tied=0;
    world();
    items();
```

With this complete block:

```rill
    fire_out=0;
    rope_tied=0;
    shore=11;
    world();
    items();
```

### Change 6

Find this unique existing declaration or routine header; leave it in place:

```rill
fn newgame(){
```

Insert the following source immediately before it:

```rill
fn rowboat(){
    if (location!=12)|(places[6]!=0){say("You need the boat and the oar.\r\n");return 0;}
    shore=27-shore;places[15]=shore;paths[12*6+1]=shore;location=shore;
    say("You row across the lake.\r\n");describe();return 0;
}
```

## Build and try it

```dos
VMAKE V18
```

Require these fresh tool reports, followed by BUILD PASS:

```text
OK RESULT.IR 0000039679
OK RESULT.ASM 0000102401 text bytes
OK RESULT.COM 16455 bytes
BUILD PASS
```

The preserved V18.COM is 16,455 bytes. Its natural display and behavior are the checks below.

Create F006.TXT with these additional commands:

```text
N
```

Join the saved LIGHT.TXT walk and this tail as LAKE.TXT:

```dos
COPY /B LIGHT.TXT+F006.TXT LAKE.TXT
```

Create F048.TXT with these additional commands:

```text
GO BOAT
ROW
GO BOAT
S
GO BOAT
ROW
```

Join the saved LAKE.TXT walk and this tail as T18.TXT:

```dos
COPY /B LAKE.TXT+F048.TXT T18.TXT
```

Create F049.TXT with these additional commands:

```text
SWIM
```

Join the saved LAKE.TXT walk and this tail as X18.TXT:

```dos
COPY /B LAKE.TXT+F049.TXT X18.TXT
```

```dos
CHECK V18 T18.TXT
```

Require these significant game lines, followed by CHECK's PASS:

```text
You are in the Gallery.
You row across the lake.
You are in the Underground Lake Chamber.
PASS
```

## Check the other case

```dos
CHECK V18 X18.TXT
```

Require these significant lines and PASS:

```text
The ice-cold lake pulls you under.
PASS
```

A player death or an unsuccessful action is an ordinary game outcome, so CHECK still reports PASS. Judge the stated message and the resulting world as well as the process status.

## If it differs

After crossing, test GO BOAT followed by SOUTH. A stale exit would return the player to the wrong bank.
