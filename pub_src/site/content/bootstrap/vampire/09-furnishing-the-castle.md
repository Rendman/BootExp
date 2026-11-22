+++
title = "09 \u00b7 Furnishing the castle"
weight = 9
description = "Enter all twenty-five objects and distinguish possessions from scenery."
download = "V09.RIL"
download_group = "tools/vampire"
reader_names = 1
+++

A boat, sign and fireplace are visible objects, but they do not belong in a pocket. Filling the tables makes the castle feel like a place rather than a corridor between compiler tests.

## What changes

items initializes every object name and location, including the absent key. nounid adds aliases such as HAM for Sledge Hammer and DOO for Rusty Door. Objects fifteen through twenty-three are fixed scenery; take refuses them. This contiguous range is a property of our table, not a rule built into RILL. Other objects remain movable unless a particular puzzle adds a condition. The unused zero slot is never visited. Names use pointers to terminated literal strings, with no private string allocator.

## Enter the source

Copy V08.RIL to V09.RIL. Apply the following edits in order. All locators are existing declarations or unique routine headers; no editor line numbers are needed. Keep the source outside each stated edit.

### Change 1

Find the unique routine header `fn items(){`. Within that routine, replace this existing block, including its shown context:

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

With this complete block:

```rill
fn items(){
    item(1,"Sledge Hammer",5);item(2,"Timepiece",1);
    item(3,"Coil of Rope",9);item(4,"Parchment Scroll",3);
    item(5,"Axe",4);item(6,"Oar",6);item(7,"Key",99);
    item(8,"Holywater",7);item(9,"Flask of Oil",13);
    item(10,"Crate",14);item(11,"Bucket",14);item(12,"Torch",8);
    item(13,"Nails",15);item(14,"Tapestry",16);item(15,"Boat",11);
    item(16,"Rusty Door",17);item(17,"Closed Coffin",18);
    item(18,"Fire in the Fireplace",2);item(19,"Bookcase",3);
    item(20,"Sign",1);item(21,"Parapets",5);item(22,"Brick Fireplace",2);
    item(23,"Rat",19);item(24,"Wine",2);item(25,"Cheddar Cheese",2);
    return 0;
}
```

### Change 2

Find the unique routine header `fn nounid(){`. Within that routine, replace this existing block, including its shown context:

```rill
    if wordis(noun,"SCR")|wordis(noun,"PAR"){return 4;}
    if wordis(noun,"AXE")|wordis(noun,"AX "){return 5;}
    if wordis(noun,"OAR"){return 6;}
    if wordis(noun,"BOO"){return 19;}
    return 0;
}
```

With this complete block:

```rill
    if wordis(noun,"SCR")|wordis(noun,"PAR"){return 4;}
    if wordis(noun,"AXE")|wordis(noun,"AX "){return 5;}
    if wordis(noun,"OAR"){return 6;}if wordis(noun,"KEY"){return 7;}
    if wordis(noun,"HOL")|wordis(noun,"WAT"){return 8;}
    if wordis(noun,"FLA")|wordis(noun,"OIL"){return 9;}
    if wordis(noun,"CRA"){return 10;}
    if wordis(noun,"BUC"){return 11;}if wordis(noun,"TOR"){return 12;}
    if wordis(noun,"NAI"){return 13;}if wordis(noun,"TAP"){return 14;}
    if wordis(noun,"BOA"){return 15;}
    if wordis(noun,"RUS")|wordis(noun,"DOO"){return 16;}
    if wordis(noun,"CLO")|wordis(noun,"COF")|wordis(noun,"DRA"){return 17;}
    if wordis(noun,"BOO"){return 19;}if wordis(noun,"SIG"){return 20;}
    if wordis(noun,"FIR")|wordis(noun,"BRI"){return 22;}
    if wordis(noun,"RAT"){return 23;}if wordis(noun,"WIN"){return 24;}
    if wordis(noun,"CHE"){return 25;}
    return 0;
}
```

### Change 3

Find the unique routine header `fn take(obj){`. Within that routine, replace this existing block, including its shown context:

```rill
    if places[obj]==0{say("You already have it.\r\n");return 0;}
    if places[obj]!=location{say("You cannot see it here.\r\n");return 0;}
    places[obj]=0;say("Taken: ");say(itemname(obj));say(".\r\n");
    return 0;
```

With this complete block:

```rill
    if places[obj]==0{say("You already have it.\r\n");return 0;}
    if places[obj]!=location{say("You cannot see it here.\r\n");return 0;}
    if (obj>=15)&(obj<=23){say("You cannot take that.\r\n");return 0;}
    places[obj]=0;say("Taken: ");say(itemname(obj));say(".\r\n");
    return 0;
```

## Build and try it

```dos
VMAKE V09
```

Require these fresh tool reports, followed by BUILD PASS:

```text
OK RESULT.IR 0000026444
OK RESULT.ASM 0000066805 text bytes
OK RESULT.COM 11112 bytes
BUILD PASS
```

The preserved V09.COM is 11,112 bytes. Its natural display and behavior are the checks below.

Create T09.TXT as plain text:

```text
LOOK
W
LOOK
```

Create X09.TXT as plain text:

```text
GET SIGN
E
GET BOOKCASE
```

```dos
CHECK V09 T09.TXT
```

Require these significant game lines, followed by CHECK's PASS:

```text
  Sign
  Fire in the Fireplace
  Cheddar Cheese
PASS
```

## Check the other case

```dos
CHECK V09 X09.TXT
```

Require these significant lines and PASS:

```text
You cannot take that.
PASS
```

## If it differs

The fire and brick fireplace have separate entries. FIRE and BRICK commands refer to the brick structure; the fire entry supplies its visible description.
