+++
title = "15 \u00b7 Putting out the fire"
weight = 15
description = "Consume holywater in the study and make the fireplace safe to enter."
download = "V15.RIL"
download_group = "tools/vampire"
reader_names = 1
+++

Some actions change more than an object location. Dropping the water in the Study removes it from play, changes what the room contains and makes another entrance usable.

## What changes

drop handles the water-in-study case before the ordinary drop. It sets fire_out and replaces the fire description with Smoldering Ashes. The bucket stays carried. walk accepts GO FIRE only in the Study; the flag decides between entering the Fireplace room and a fatal burn. Water dropped elsewhere uses the ordinary floor location and can be collected again subject to its bucket rule. A flag expresses a persistent world fact that cannot be inferred from where the water happens to be.

## Enter the source

Copy V14.RIL to V15.RIL. Apply the following edits in order. All locators are existing declarations or unique routine headers; no editor line numbers are needed. Keep the source outside each stated edit.

### Change 1

Find this unique existing declaration or routine header; leave it in place:

```rill
let mut rope_tied=0;
```

Insert the following source immediately before it:

```rill
let mut fire_out=0;
```

### Change 2

Find the unique routine header `fn walk(){`. Within that routine, replace this existing block, including its shown context:

```rill
    }
    let mut obj=nounid();
    if (obj==21)&(location==5){
        if rope_tied{location=6;say("You climb down the rope.\r\n");describe();}
```

With this complete block:

```rill
    }
    let mut obj=nounid();
    if (obj==22)&(location==2){
        if fire_out{location=8;describe();}
        else{lose("The fire burns you to death.\r\n");}
        return 0;
    }
    if (obj==21)&(location==5){
        if rope_tied{location=6;say("You climb down the rope.\r\n");describe();}
```

### Change 3

Find the unique routine header `fn drop(obj){`. Within that routine, replace this existing block, including its shown context:

```rill
    if obj==0{say("I don't know that object.\r\n");return 0;}
    if places[obj]!=0{say("You do not have it.\r\n");return 0;}
    places[obj]=location;say("Dropped: ");say(itemname(obj));say(".\r\n");
    return 0;
```

With this complete block:

```rill
    if obj==0{say("I don't know that object.\r\n");return 0;}
    if places[obj]!=0{say("You do not have it.\r\n");return 0;}
    if (obj==8)&(location==2){
        places[8]=99;fire_out=1;
        store16(things+18*2,"Smoldering Ashes");
        say("The holywater puts out the fire.\r\n");return 0;
    }
    places[obj]=location;say("Dropped: ");say(itemname(obj));say(".\r\n");
    return 0;
```

### Change 4

Find the unique routine header `fn newgame(){`. Within that routine, replace this existing block, including its shown context:

```rill
    elapsed=0;
    finished=0;
    rope_tied=0;
    world();
```

With this complete block:

```rill
    elapsed=0;
    finished=0;
    fire_out=0;
    rope_tied=0;
    world();
```

## Build and try it

```dos
VMAKE V15
```

Require these fresh tool reports, followed by BUILD PASS:

```text
OK RESULT.IR 0000035345
OK RESULT.ASM 0000090366 text bytes
OK RESULT.COM 14686 bytes
BUILD PASS
```

The preserved V15.COM is 14,686 bytes. Its natural display and behavior are the checks below.

Create F042.TXT with these additional commands:

```text
DROP WATER
GO FIRE
```

Join the saved SUPPLY.TXT walk and this tail as T15.TXT:

```dos
COPY /B SUPPLY.TXT+F042.TXT T15.TXT
```

Create X15.TXT as plain text:

```text
W
GO FIRE
```

```dos
CHECK V15 T15.TXT
```

Require these significant game lines, followed by CHECK's PASS:

```text
The holywater puts out the fire.
You are in the Brick Fireplace.
PASS
```

## Check the other case

```dos
CHECK V15 X15.TXT
```

Require these significant lines and PASS:

```text
The fire burns you to death.
PASS
```

A player death or an unsuccessful action is an ordinary game outcome, so CHECK still reports PASS. Judge the stated message and the resulting world as well as the process status.

## If it differs

Do not merely set the water location to the Study: that would leave the object available for another use after it had extinguished the fire.
