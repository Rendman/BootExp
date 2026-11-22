+++
title = "22 \u00b7 The rat and the key"
weight = 22
description = "Discover the hidden key and distract its guardian with cheese."
download = "V22.RIL"
download_group = "tools/vampire"
reader_names = 1
+++

A LOOK can change what is known. The key starts absent; examining the rat brings it into the room, where GET can find it.

## What changes

inspect reveals the key only when the rat itself is reachable. take refuses it while the rat is present unless the cheese is on that room floor. With cheese supplied, the rat and cheese leave play and the key becomes carried. The ordinary visibility and capacity checks still happen first. Already-carried objects retain their usual response. The longer KEY.TXT walk collects cheese before entering the passage, then reuses the established gallery actions to reach the Antechamber with the key.

## Enter the source

Copy V21.RIL to V22.RIL. Apply the following edits in order. All locators are existing declarations or unique routine headers; no editor line numbers are needed. Keep the source outside each stated edit.

### Change 1

Find the unique routine header `fn take(obj){`. Within that routine, replace this existing block, including its shown context:

```rill
        paths[16*6]=17;say("A hole opens behind the tapestry.\r\n");
    }
    places[obj]=0;say("Taken: ");say(itemname(obj));say(".\r\n");
    return 0;
```

With this complete block:

```rill
        paths[16*6]=17;say("A hole opens behind the tapestry.\r\n");
    }
    if obj==7{
        if places[23]==location{
            if places[25]!=location{say("The rat guards the key.\r\n");return 0;}
            places[23]=99;say("The rat runs off with the cheese.\r\n");places[25]=99;
        }
    }
    places[obj]=0;say("Taken: ");say(itemname(obj));say(".\r\n");
    return 0;
```

### Change 2

Find the unique routine header `fn inspect(obj){`. Within that routine, replace this existing block, including its shown context:

```rill
        return 0;
    }
    say("You see nothing special.\r\n");return 0;
}
```

With this complete block:

```rill
        return 0;
    }
    if obj==23{places[7]=location;say("There is a key in the rat's mouth.\r\n");return 0;}
    say("You see nothing special.\r\n");return 0;
}
```

## Build and try it

```dos
VMAKE V22
```

Require these fresh tool reports, followed by BUILD PASS:

```text
OK RESULT.IR 0000042996
OK RESULT.ASM 0000111302 text bytes
OK RESULT.COM 17751 bytes
BUILD PASS
```

The preserved V22.COM is 17,751 bytes. Its natural display and behavior are the checks below.

Create F010.TXT with these additional commands:

```text
DROP WATER
DROP BUCKET
GET CHEESE
GO FIRE
GET TORCH
HIT FIRE
HAMMER
N
W
LOOK RAT
DROP OAR
GET KEY
GET OAR
DROP CHEESE
GET KEY
E
N
GO BOAT
ROW
```

Join the saved GEAR.TXT walk and this tail as KEYBASE.TXT:

```dos
COPY /B GEAR.TXT+F010.TXT KEYBASE.TXT
```

Reuse the saved F009.TXT command tail.

Join the saved KEYBASE.TXT walk and this tail as KEY.TXT:

```dos
COPY /B KEYBASE.TXT+F009.TXT KEY.TXT
```

```dos
COPY KEY.TXT T22.TXT
```

Create X22.TXT as plain text:

```text
LOOK RAT
```

```dos
CHECK V22 T22.TXT
```

Require these significant game lines, followed by CHECK's PASS:

```text
There is a key in the rat's mouth.
The rat guards the key.
The rat runs off with the cheese.
Taken: Key.
PASS
```

## Check the other case

```dos
CHECK V22 X22.TXT
```

Require these significant lines and PASS:

```text
You cannot see it here.
PASS
```

A player death or an unsuccessful action is an ordinary game outcome, so CHECK still reports PASS. Judge the stated message and the resulting world as well as the process status.

## If it differs

The cheese must be dropped, not merely carried. Inspecting a rat elsewhere must not reveal the key in the player's current room.
