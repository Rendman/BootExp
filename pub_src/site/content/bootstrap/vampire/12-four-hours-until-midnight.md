+++
title = "12 \u00b7 Four hours until midnight"
weight = 12
description = "Advance one minute per command, read the timepiece and end the game at midnight."
download = "V12.RIL"
download_group = "tools/vampire"
reader_names = 1
+++

A countdown makes a familiar room feel different. The clock advances when I decide what to do, not while I sit thinking at the keyboard.

## What changes

elapsed starts at zero, meaning 8:00 p.m. tick runs before each nonempty action except QUIT. At 240 it calls lose before the requested action can run. Blank lines and rejected input records cost nothing; an unknown but well-formed command costs a minute. clock prints two decimal digits each for hours and minutes. Reading the carried timepiece includes the minute spent on READ itself. finished records a terminal result while playing controls the command loop. No hardware timer or processor-specific operation is needed.

## Enter the source

Copy V11.RIL to V12.RIL. Apply the following edits in order. All locators are existing declarations or unique routine headers; no editor line numbers are needed. Keep the source outside each stated edit.

### Change 1

Find this unique existing declaration or routine header; leave it in place:

```rill
bytes command[81];
```

Insert the following source immediately before it:

```rill
let mut elapsed=0;
```

### Change 2

Find this unique existing declaration or routine header; leave it in place:

```rill
let mut location=1;
```

Insert the following source immediately before it:

```rill
let mut finished=0;
```

### Change 3

Find the unique routine header `fn main(){`. Within that routine, replace this existing block, including its shown context:

```rill
            else{
                if words{
                    act();
                }
            }
```

With this complete block:

```rill
            else{
                if words{
                    tick();if playing{act();}
                }
            }
```

### Change 4

Find the unique routine header `fn act(){`. Within that routine, replace this existing block, including its shown context:

```rill
    if wordis(verb,"HEL"){help();return 0;}
    if wordis(verb,"INV"){inventory();return 0;}
    if wordis(verb,"GO ")|wordis(verb,"CLI")|((words==1)&(direction()!=0)){walk();return 0;}
    if wordis(verb,"LOO")|wordis(verb,"REA"){inspect(nounid());return 0;}
```

With this complete block:

```rill
    if wordis(verb,"HEL"){help();return 0;}
    if wordis(verb,"INV"){inventory();return 0;}
    if wordis(verb,"WAI"){say("Time passes.\r\n");return 0;}
    if wordis(verb,"GO ")|wordis(verb,"CLI")|((words==1)&(direction()!=0)){walk();return 0;}
    if wordis(verb,"LOO")|wordis(verb,"REA"){inspect(nounid());return 0;}
```

### Change 5

Find the unique routine header `fn help(){`. Within that routine, replace this existing block, including its shown context:

```rill
    say("INVENTORY\r\n");
    say("READ\r\n");
    say("PUSH.\r\n");
    return 0;
}
```

With this complete block:

```rill
    say("INVENTORY\r\n");
    say("READ\r\n");
    say("PUSH\r\n");
    say("WAIT.\r\n");
    return 0;
}
```

### Change 6

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
    if obj==2{
        if places[2]==0{clock();}else{say("Pick up the timepiece to read it.\r\n");}
        return 0;
    }
    say("You see nothing special.\r\n");return 0;
}
```

### Change 7

Find the unique routine header `fn newgame(){`. Within that routine, replace this existing block, including its shown context:

```rill
fn newgame(){
    location=1;playing=1;
    world();
    items();
```

With this complete block:

```rill
fn newgame(){
    location=1;playing=1;
    elapsed=0;
    finished=0;
    world();
    items();
```

### Change 8

Find this unique existing declaration or routine header; leave it in place:

```rill
fn push(obj){
```

Insert the following source immediately before it:

```rill
fn lose(text){say(text);finished=1;playing=0;return 0;}
```

### Change 9

Find this unique existing declaration or routine header; leave it in place:

```rill
fn lose(text){say(text);finished=1;playing=0;return 0;}
```

Insert the following source immediately before it:

```rill
fn tick(){
    elapsed=elapsed+1;
    if elapsed==240{lose("It is midnight. Dracula wakes and finds you.\r\n");}
    return 0;
}
```

### Change 10

Find this unique existing declaration or routine header; leave it in place:

```rill
fn tick(){
```

Insert the following source immediately before it:

```rill
fn clock(){
    say("Time: ");
    putc(48+(8+elapsed/60)/10);if status(){exit(1);}
    putc(48+(8+elapsed/60)%10);if status(){exit(1);}
    say(":");
    putc(48+(elapsed%60)/10);if status(){exit(1);}
    putc(48+elapsed%10);if status(){exit(1);}
    say(" p.m.\r\n");return 0;
}
```

## Build and try it

```dos
VMAKE V12
```

Require these fresh tool reports, followed by BUILD PASS:

```text
OK RESULT.IR 0000031639
OK RESULT.ASM 0000080604 text bytes
OK RESULT.COM 13237 bytes
BUILD PASS
```

The preserved V12.COM is 13,237 bytes. Its natural display and behavior are the checks below.

Create T12.TXT as plain text:

```text
GET TIME
READ TIME
WAIT
READ TIME
```

Create WAIT.BAS to make the long deadline input without repeatedly typing WAIT:

```basic
10 OPEN "O", #1, "X12.TXT"
20 FOR I=1 TO 240
30 PRINT #1, "WAIT"
40 NEXT I
50 CLOSE: END
```

```dos
GWBASIC WAIT.BAS
```

This writes 240 WAIT records to X12.TXT.

```dos
CHECK V12 T12.TXT
```

Require these significant game lines, followed by CHECK's PASS:

```text
Time: 08:02 p.m.
Time: 08:04 p.m.
PASS
```

## Check the other case

```dos
CHECK V12 X12.TXT
```

Require these significant lines and PASS:

```text
It is midnight. Dracula wakes and finds you.
PASS
```

A player death or an unsuccessful action is an ordinary game outcome, so CHECK still reports PASS. Judge the stated message and the resulting world as well as the process status.

## If it differs

If the display is a minute behind, check whether tick runs before act. Both input prompts belonging to one action must not receive separate ticks.
