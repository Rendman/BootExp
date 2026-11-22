+++
title = "19 \u00b7 Making wooden stakes"
weight = 19
description = "Chop the crate with the axe and preserve its identity while changing its use."
download = "V19.RIL"
download_group = "tools/vampire"
reader_names = 1
+++

The crate can become a weapon, but breaking it is a decision. Its object number stays ten, so the inventory and location rules need no new entry.

## What changes

hit adds the crate-and-axe case after the fireplace case. The axe must be carried and the crate reachable. stakes records the change, and the name pointer becomes Wooden Stakes. nounid now recognizes WOO and STA only after that change. The ordinary crate prefix still identifies the same object. Chopping twice cannot produce another set. GEAR.TXT is a copy of the established supply walk with a crate, axe and oil added; its object count remains within seven.

## Enter the source

Copy V18.RIL to V19.RIL. Apply the following edits in order. All locators are existing declarations or unique routine headers; no editor line numbers are needed. Keep the source outside each stated edit.

### Change 1

Find this unique existing declaration or routine header; leave it in place:

```rill
let mut shore=11;
```

Insert the following source immediately before it:

```rill
let mut stakes=0;
```

### Change 2

Find the unique routine header `fn nounid(){`. Within that routine, replace this existing block, including its shown context:

```rill
    if wordis(noun,"FLA")|wordis(noun,"OIL"){return 9;}
    if wordis(noun,"CRA"){return 10;}
    if wordis(noun,"BUC"){return 11;}if wordis(noun,"TOR"){return 12;}
    if wordis(noun,"NAI"){return 13;}if wordis(noun,"TAP"){return 14;}
```

With this complete block:

```rill
    if wordis(noun,"FLA")|wordis(noun,"OIL"){return 9;}
    if wordis(noun,"CRA"){return 10;}
    if wordis(noun,"WOO")|wordis(noun,"STA"){
        if stakes{return 10;}return 0;
    }
    if wordis(noun,"BUC"){return 11;}if wordis(noun,"TOR"){return 12;}
    if wordis(noun,"NAI"){return 13;}if wordis(noun,"TAP"){return 14;}
```

### Change 3

Find the unique routine header `fn hit(obj){`. Within that routine, replace this existing block, including its shown context:

```rill
        }
    }
    say("Nothing happens.\r\n");return 0;
}
```

With this complete block:

```rill
        }
    }
    if (obj==10)&(stakes==0)&wordis(verb,"AXE"){
        if places[5]==0{
            stakes=1;store16(things+10*2,"Wooden Stakes");
            say("The crate splits into wooden stakes.\r\n");return 0;
        }
    }
    say("Nothing happens.\r\n");return 0;
}
```

### Change 4

Find the unique routine header `fn newgame(){`. Within that routine, replace this existing block, including its shown context:

```rill
    rope_tied=0;
    shore=11;
    world();
    items();
```

With this complete block:

```rill
    rope_tied=0;
    shore=11;
    stakes=0;
    world();
    items();
```

## Build and try it

```dos
VMAKE V19
```

Require these fresh tool reports, followed by BUILD PASS:

```text
OK RESULT.IR 0000040591
OK RESULT.ASM 0000104659 text bytes
OK RESULT.COM 16787 bytes
BUILD PASS
```

The preserved V19.COM is 16,787 bytes. Its natural display and behavior are the checks below.

Create GEAR.TXT as plain text:

```text
E
PUSH BOOKCASE
D
GET ROPE
N
GET OIL
N
GET BUCKET
GET CRATE
U
E
E
E
GET AXE
E
GET HAMMER
TIE ROPE
PARAPETS
GO ROPE
GET OAR
S
GET WATER
BUCKET
U
W
W
W
```

Create F050.TXT with these additional commands:

```text
HIT CRATE
AXE
INVENTORY
```

Join the saved GEAR.TXT walk and this tail as T19.TXT:

```dos
COPY /B GEAR.TXT+F050.TXT T19.TXT
```

Create F051.TXT with these additional commands:

```text
HIT CRATE
HAMMER
```

Join the saved GEAR.TXT walk and this tail as X19.TXT:

```dos
COPY /B GEAR.TXT+F051.TXT X19.TXT
```

```dos
CHECK V19 T19.TXT
```

Require these significant game lines, followed by CHECK's PASS:

```text
The crate splits into wooden stakes.
  Wooden Stakes
PASS
```

## Check the other case

```dos
CHECK V19 X19.TXT
```

Require these significant lines and PASS:

```text
Nothing happens.
PASS
```

A player death or an unsuccessful action is an ordinary game outcome, so CHECK still reports PASS. Judge the stated message and the resulting world as well as the process status.

## If it differs

Check both the flag and the name pointer. Renaming the crate alone must not make its other uses depend on the spelling of a message.
