+++
title = "14 \u00b7 A bucket of holywater"
weight = 14
description = "Require a carried bucket when collecting holywater in the chapel."
download = "V14.RIL"
download_group = "tools/vampire"
reader_names = 1
+++

A location table tells us where the water is, but not whether we can carry it. The bucket is the extra condition for this particular GET.

## What changes

take calls water only after the ordinary visibility and capacity checks. water asks In what? and accepts the BUCKET prefix only when the bucket is carried. A failed answer leaves the holywater in the Chapel. The bucket and water retain separate object entries; taking the water occupies another carrying place. This simple representation avoids inventing a general container system for a single puzzle. The supply transcript gathers a bucket before visiting the Tower and carries an oar and hammer for its walk.

## Enter the source

Copy V13.RIL to V14.RIL. Apply the following edits in order. All locators are existing declarations or unique routine headers; no editor line numbers are needed. Keep the source outside each stated edit.

### Change 1

Find the unique routine header `fn take(obj){`. Within that routine, replace this existing block, including its shown context:

```rill
    if (obj>=15)&(obj<=23){say("You cannot take that.\r\n");return 0;}
    if carried()==7{say("You cannot carry any more.\r\n");return 0;}
    places[obj]=0;say("Taken: ");say(itemname(obj));say(".\r\n");
    return 0;
```

With this complete block:

```rill
    if (obj>=15)&(obj<=23){say("You cannot take that.\r\n");return 0;}
    if carried()==7{say("You cannot carry any more.\r\n");return 0;}
    if obj==8{if water()==0{return 0;}}
    places[obj]=0;say("Taken: ");say(itemname(obj));say(".\r\n");
    return 0;
```

### Change 2

Find this unique existing declaration or routine header; leave it in place:

```rill
fn tie(obj){
```

Insert the following source immediately before it:

```rill
fn water(){
    if ask("In what? "){
        if wordis(verb,"BUC")&(places[11]==0){return 1;}
    }
    say("You need to carry the bucket.\r\n");return 0;
}
```

## Build and try it

```dos
VMAKE V14
```

Require these fresh tool reports, followed by BUILD PASS:

```text
OK RESULT.IR 0000034491
OK RESULT.ASM 0000088087 text bytes
OK RESULT.COM 14360 bytes
BUILD PASS
```

The preserved V14.COM is 14,360 bytes. Its natural display and behavior are the checks below.

Create SUPPLY.TXT as plain text:

```text
E
PUSH BOOKCASE
D
GET ROPE
N
N
GET BUCKET
U
E
E
E
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

Create F040.TXT with these additional commands:

```text
INVENTORY
```

Join the saved SUPPLY.TXT walk and this tail as T14.TXT:

```dos
COPY /B SUPPLY.TXT+F040.TXT T14.TXT
```

Create F041.TXT with these additional commands:

```text
GET WATER
BUCKET
```

Join the saved CHAPEL.TXT walk and this tail as X14.TXT:

```dos
COPY /B CHAPEL.TXT+F041.TXT X14.TXT
```

```dos
CHECK V14 T14.TXT
```

Require these significant game lines, followed by CHECK's PASS:

```text
Taken: Holywater.
  Holywater
PASS
```

## Check the other case

```dos
CHECK V14 X14.TXT
```

Require these significant lines and PASS:

```text
You need to carry the bucket.
PASS
```

A player death or an unsuccessful action is an ordinary game outcome, so CHECK still reports PASS. Judge the stated message and the resulting world as well as the process status.

## If it differs

The container answer is parsed into verb, since it is the first word of a new reply. Checking noun would inspect an empty last-word field.
