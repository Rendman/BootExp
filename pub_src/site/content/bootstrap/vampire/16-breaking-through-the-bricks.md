+++
title = "16 \u00b7 Breaking through the bricks"
weight = 16
description = "Use the carried hammer to open a passage from inside the fireplace."
download = "V16.RIL"
download_group = "tools/vampire"
reader_names = 1
+++

The entrance is safe now, but its back wall is still solid. HIT FIRE asks which tool is being used and changes the map only when the hammer is available.

## What changes

hit first checks that the target is reachable, with an explicit exception for the fireplace structure viewed from inside it. Its original object entry remains in the Study. ask obtains the tool prefix; HAMMER and SLEDGE name the carried hammer. Success writes room ten into the Fireplace north exit and updates both room and object descriptions. The normal direction code then reaches the Secret Passage. An unsuitable or absent tool produces Nothing happens and changes no exit.

## Enter the source

Copy V15.RIL to V16.RIL. Apply the following edits in order. All locators are existing declarations or unique routine headers; no editor line numbers are needed. Keep the source outside each stated edit.

### Change 1

Find the unique routine header `fn act(){`. Within that routine, replace this existing block, including its shown context:

```rill
    if wordis(verb,"GET")|wordis(verb,"TAK"){take(obj);return 0;}
    if wordis(verb,"DRO"){drop(obj);return 0;}
    if wordis(verb,"TIE"){tie(obj);return 0;}
    if wordis(verb,"PUS"){push(obj);return 0;}
```

With this complete block:

```rill
    if wordis(verb,"GET")|wordis(verb,"TAK"){take(obj);return 0;}
    if wordis(verb,"DRO"){drop(obj);return 0;}
    if wordis(verb,"HIT")|wordis(verb,"BRE"){hit(obj);return 0;}
    if wordis(verb,"TIE"){tie(obj);return 0;}
    if wordis(verb,"PUS"){push(obj);return 0;}
```

### Change 2

Find the unique routine header `fn help(){`. Within that routine, replace this existing block, including its shown context:

```rill
    say("PUSH\r\n");
    say("WAIT\r\n");
    say("TIE.\r\n");
    return 0;
```

With this complete block:

```rill
    say("PUSH\r\n");
    say("WAIT\r\n");
    say("HIT\r\n");
    say("TIE.\r\n");
    return 0;
```

### Change 3

Find this unique existing declaration or routine header; leave it in place:

```rill
fn tie(obj){
```

Insert the following source immediately before it:

```rill
fn hit(obj){
    if obj==0{say("I don't know that object.\r\n");return 0;}
    if (places[obj]!=location)&(places[obj]!=0){
        if (obj!=22)|(location!=8){say("You cannot see it here.\r\n");return 0;}
    }
    if ask("With what? ")==0{return 0;}
    if (obj==22)&(location==8){
        if wordis(verb,"HAM")|wordis(verb,"SLE"){
            if places[1]==0{
                paths[8*6]=10;
                store16(names+8*2,"Broken Fireplace");
                store16(things+22*2,"Broken Fireplace");
                say("The bricks break away. A passage leads north.\r\n");return 0;
            }
        }
    }
    say("Nothing happens.\r\n");return 0;
}
```

## Build and try it

```dos
VMAKE V16
```

Require these fresh tool reports, followed by BUILD PASS:

```text
OK RESULT.IR 0000037321
OK RESULT.ASM 0000095865 text bytes
OK RESULT.COM 15494 bytes
BUILD PASS
```

The preserved V16.COM is 15,494 bytes. Its natural display and behavior are the checks below.

Create F004.TXT with these additional commands:

```text
DROP WATER
DROP BUCKET
GO FIRE
HIT FIRE
HAMMER
N
```

Join the saved SUPPLY.TXT walk and this tail as DARK.TXT:

```dos
COPY /B SUPPLY.TXT+F004.TXT DARK.TXT
```

```dos
COPY DARK.TXT T16.TXT
```

Create F045.TXT with these additional commands:

```text
DROP WATER
GO FIRE
HIT FIRE
AXE
N
```

Join the saved SUPPLY.TXT walk and this tail as X16.TXT:

```dos
COPY /B SUPPLY.TXT+F045.TXT X16.TXT
```

```dos
CHECK V16 T16.TXT
```

Require these significant game lines, followed by CHECK's PASS:

```text
The bricks break away. A passage leads north.
You are in the Secret Passage.
PASS
```

## Check the other case

```dos
CHECK V16 X16.TXT
```

Require these significant lines and PASS:

```text
Nothing happens.
You cannot go that way.
PASS
```

A player death or an unsuccessful action is an ordinary game outcome, so CHECK still reports PASS. Judge the stated message and the resulting world as well as the process status.

## If it differs

If the inner wall is reported absent, check the fireplace exception before the ordinary visibility rejection.
