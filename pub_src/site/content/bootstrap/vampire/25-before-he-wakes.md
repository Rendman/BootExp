+++
title = "25 \u00b7 Before he wakes"
weight = 25
description = "Finish the adventure with carried wooden stakes, or suffer the result of a wrong weapon."
download = "V25.RIL"
download_group = "tools/vampire"
reader_names = 1
+++

The last action uses the same small pieces as the first: a recognized noun, a private parameter, an answer to a question and a few persistent facts about the world.

## What changes

kill requires the Tomb and an open coffin before asking With what? A stake prefix succeeds only when the crate has actually become stakes and object ten is carried. Victory prints its natural message and time, sets finished to two, and stops command processing. An unsuitable answer wakes Dracula and calls lose. EOF while answering stops input without pretending a weapon was supplied. The winning transcript exercises the complete map and puzzle chain with the same public commands as keyboard play.

## Enter the source

Copy V24.RIL to V25.RIL. Apply the following edits in order. All locators are existing declarations or unique routine headers; no editor line numbers are needed. Keep the source outside each stated edit.

### Change 1

Find the unique routine header `fn act(){`. Within that routine, replace this existing block, including its shown context:

```rill
    if wordis(verb,"OIL"){oil(obj);return 0;}
    if wordis(verb,"OPE"){openobject(obj);return 0;}
    say("I don't know how to do that.\r\n");
    return 0;
```

With this complete block:

```rill
    if wordis(verb,"OIL"){oil(obj);return 0;}
    if wordis(verb,"OPE"){openobject(obj);return 0;}
    if wordis(verb,"KIL")|wordis(verb,"THR"){kill(obj);return 0;}
    say("I don't know how to do that.\r\n");
    return 0;
```

### Change 2

Find the unique routine header `fn help(){`. Within that routine, replace this existing block, including its shown context:

```rill
    say("ROW and SWIM\r\n");
    say("OIL\r\n");
    say("OPEN.\r\n");
    return 0;
}
```

With this complete block:

```rill
    say("ROW and SWIM\r\n");
    say("OIL\r\n");
    say("OPEN\r\n");
    say("KILL.\r\n");
    return 0;
}
```

### Change 3

Find this unique existing declaration or routine header; leave it in place:

```rill
fn newgame(){
```

Insert the following source immediately before it:

```rill
fn kill(obj){
    if (obj!=17)|(location!=18)|(coffin_open==0){say("You cannot do that here.\r\n");return 0;}
    if ask("With what? ")==0{return 0;}
    if wordis(verb,"WOO")|wordis(verb,"STA"){
        if stakes&(places[10]==0){
            say("You drive a wooden stake into Dracula's heart.\r\n");
            say("Congratulations! You have killed Dracula.\r\n");clock();
            finished=2;playing=0;return 0;
        }
    }
    lose("Dracula wakes. You have failed.\r\n");return 0;
}
```

## Build and try it

```dos
VMAKE V25
```

Require these fresh tool reports, followed by BUILD PASS:

```text
OK RESULT.IR 0000046986
OK RESULT.ASM 0000123087 text bytes
OK RESULT.COM 19421 bytes
BUILD PASS
```

The preserved V25.COM is 19,421 bytes. Its natural display and behavior are the checks below.

Create F014.TXT with these additional commands:

```text
KILL DRACULA
STAKES
```

Join the saved COFFIN.TXT walk and this tail as WIN.TXT:

```dos
COPY /B COFFIN.TXT+F014.TXT WIN.TXT
```

```dos
COPY WIN.TXT T25.TXT
```

Create F063.TXT with these additional commands:

```text
KILL DRACULA
AXE
```

Join the saved COFFIN.TXT walk and this tail as X25.TXT:

```dos
COPY /B COFFIN.TXT+F063.TXT X25.TXT
```

```dos
CHECK V25 T25.TXT
```

Require these significant game lines, followed by CHECK's PASS:

```text
Congratulations! You have killed Dracula.
PASS
```

## Check the other case

```dos
CHECK V25 X25.TXT
```

Require these significant lines and PASS:

```text
Dracula wakes. You have failed.
PASS
```

A player death or an unsuccessful action is an ordinary game outcome, so CHECK still reports PASS. Judge the stated message and the resulting world as well as the process status.

## If it differs

Seeing Wooden Stakes in an earlier inventory is not enough if they were dropped. Check their current location at the point of the attack.

![A vampire in a nightcap watches a clock while a programmer carries a little wooden stake.](../../../images/vampire-clock.svg)

*One command before midnight.*

