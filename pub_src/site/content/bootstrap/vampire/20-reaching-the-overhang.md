+++
title = "20 \u00b7 Reaching the overhang"
weight = 20
description = "Stand on an intact crate placed in the gallery to reach the overhang."
download = "V20.RIL"
download_group = "tools/vampire"
reader_names = 1
+++

A useful object need not be carried. The crate works as a step only when it is on the Gallery floor, and wooden stakes no longer make a suitable platform.

## What changes

walk recognizes OVERHANG in the Gallery after checking ordinary directions and the boat. It requires places[10] to be sixteen and stakes to be zero before moving to room fifteen. The Overhang down exit returns to the Gallery through the regular map. Neither entering nor leaving moves the crate. An unsuccessful climb changes no location. This is why the crate conversion is represented separately from its object number.

## Enter the source

Copy V19.RIL to V20.RIL. Apply the following edits in order. All locators are existing declarations or unique routine headers; no editor line numbers are needed. Keep the source outside each stated edit.

### Change 1

Find the unique routine header `fn walk(){`. Within that routine, replace this existing block, including its shown context:

```rill
    }
    if (obj==15)&(places[15]==location){location=12;describe();return 0;}
    say("You cannot go there.\r\n");
    return 0;
```

With this complete block:

```rill
    }
    if (obj==15)&(places[15]==location){location=12;describe();return 0;}
    if (location==16)&wordis(noun,"OVE"){
        if (places[10]==16)&(stakes==0){location=15;describe();}
        else{say("The overhang is too high.\r\n");}
        return 0;
    }
    say("You cannot go there.\r\n");
    return 0;
```

## Build and try it

```dos
VMAKE V20
```

Require these fresh tool reports, followed by BUILD PASS:

```text
OK RESULT.IR 0000041069
OK RESULT.ASM 0000105856 text bytes
OK RESULT.COM 16970 bytes
BUILD PASS
```

The preserved V20.COM is 16,970 bytes. Its natural display and behavior are the checks below.

Create F008.TXT with these additional commands:

```text
DROP WATER
DROP BUCKET
GO FIRE
GET TORCH
HIT FIRE
HAMMER
N
N
GO BOAT
ROW
```

Join the saved GEAR.TXT walk and this tail as EQUIP.TXT:

```dos
COPY /B GEAR.TXT+F008.TXT EQUIP.TXT
```

Create F052.TXT with these additional commands:

```text
GO OVERHANG
DROP CRATE
GO OVERHANG
D
```

Join the saved EQUIP.TXT walk and this tail as T20.TXT:

```dos
COPY /B EQUIP.TXT+F052.TXT T20.TXT
```

Create F053.TXT with these additional commands:

```text
DROP CRATE
HIT CRATE
AXE
GO OVERHANG
```

Join the saved EQUIP.TXT walk and this tail as X20.TXT:

```dos
COPY /B EQUIP.TXT+F053.TXT X20.TXT
```

```dos
CHECK V20 T20.TXT
```

Require these significant game lines, followed by CHECK's PASS:

```text
The overhang is too high.
You are in the Overhang.
You are in the Gallery.
PASS
```

## Check the other case

```dos
CHECK V20 X20.TXT
```

Require these significant lines and PASS:

```text
The overhang is too high.
PASS
```

A player death or an unsuccessful action is an ordinary game outcome, so CHECK still reports PASS. Judge the stated message and the resulting world as well as the process status.

## If it differs

A crate in inventory does not satisfy the floor-location test. Drop it before climbing, and compare against room sixteen rather than zero.
