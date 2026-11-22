+++
title = "05 \u00b7 The upper castle"
weight = 5
description = "Extend the map to the tower, chapel and fireplace rooms."
download = "V05.RIL"
download_group = "tools/vampire"
reader_names = 1
+++

The rooms above ground fit in the same table. No movement routine needs to know how many descriptions I have entered.

## What changes

world adds the remaining upper rooms and opens the Armory eastward to the Tower. The Lower Tower leads south to the Chapel; the Chapel stair returns up to the Armory. The Fireplace leads south into the Study. A stored exit is directional: entering a connection does not create its reverse. Some rooms have no ordinary incoming exit because their entrances are objects or concealed openings. Do not fill those empty cells merely to make the map look symmetrical.

## Enter the source

Copy V04.RIL to V05.RIL. Apply the following edits in order. All locators are existing declarations or unique routine headers; no editor line numbers are needed. Keep the source outside each stated edit.

### Change 1

Find the unique routine header `fn world(){`. Within that routine, replace this existing block, including its shown context:

```rill
    room(2,"Study",0,0,1,0,0,0);
    room(3,"Library",0,0,4,1,0,0);
    room(4,"Armory",0,0,0,3,0,0);
    return 0;
}
```

With this complete block:

```rill
    room(2,"Study",0,0,1,0,0,0);
    room(3,"Library",0,0,4,1,0,0);
    room(4,"Armory",0,0,5,3,0,0);
    room(5,"Tower",0,0,0,4,0,0);
    room(6,"Lower Tower",0,7,0,0,5,0);
    room(7,"Chapel",6,0,0,0,4,0);
    room(8,"Brick Fireplace",0,2,0,0,0,0);
    return 0;
}
```

## Build and try it

```dos
VMAKE V05
```

Require these fresh tool reports, followed by BUILD PASS:

```text
OK RESULT.IR 0000014524
OK RESULT.ASM 0000038180 text bytes
OK RESULT.COM 06721 bytes
BUILD PASS
```

The preserved V05.COM is 6,721 bytes. Its natural display and behavior are the checks below.

Create T05.TXT as plain text:

```text
E
E
E
W
```

Create X05.TXT as plain text:

```text
E
E
E
E
```

```dos
CHECK V05 T05.TXT
```

Require these significant game lines, followed by CHECK's PASS:

```text
You are in the Tower.
You are in the Armory.
PASS
```

## Check the other case

```dos
CHECK V05 X05.TXT
```

Require these significant lines and PASS:

```text
You cannot go that way.
PASS
```

## If it differs

The tower should be east of the Armory, and its west exit should return there. Check the room number as well as the displayed name.
