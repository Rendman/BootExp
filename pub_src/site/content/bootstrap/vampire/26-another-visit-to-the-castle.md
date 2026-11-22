+++
title = "26 \u00b7 Another visit to the castle"
weight = 26
description = "Offer a replay after victory or death and reset the entire mutable world."
download = "V26.RIL"
download_group = "tools/vampire"
reader_names = 1
+++

I finally have a program worth handing to someone who has never read an assembler listing. Before doing that, I try playing twice. A bookcase that stays open between games is a surprisingly easy mistake to leave behind.

## What changes

main adds an outer replay loop around the existing command loop. newgame restores every flag, counter, room row, object name and object location. replay accepts Y or YES after a terminal result; an ordinary QUIT does not ask again. The command input remains open, allowing a script to include both games. Its input position, end marker and CR/LF state belong to the input stream and must not be reset with the castle. EOF never starts another game. Preserve V26.RIL as VAMPIRE.RIL and its accepted executable as VAMPIRE.COM.

## Enter the source

Copy V25.RIL to V26.RIL. Apply the following edits in order. All locators are existing declarations or unique routine headers; no editor line numbers are needed. Keep the source outside each stated edit.

### Change 1

Find the unique routine header `fn main(){`. Within that routine, replace this existing block, including its shown context:

```rill
    say("Vampire Castle Adventure\r\n");
    startinput();
    newgame();describe();
    while playing{
        say("\r\n> ");
        let mut got=readline();
        if got==0{playing=0;}
        if got==1{
            parse();
            if wordis(verb,"QUI"){say("Goodbye.\r\n");playing=0;}
            else{
                if words{
                    tick();if playing{act();}
                }
            }
        }
    }
    close(input);if status(){exit(1);}
    return 0;
}
```

With this complete block:

```rill
    say("Vampire Castle Adventure\r\n");
    startinput();
    let mut again=1;
    while again{
        newgame();
        describe();
        while playing{
            say("\r\n> ");
            let mut got=readline();
            if got==0{playing=0;}
            if got==1{
                if length{
                    parse();
                    if wordis(verb,"QUI"){
                        say("Goodbye.\r\n");playing=0;
                    }else{
                        if words{
                            tick();
                            if playing{act();}
                        }
                    }
                }
            }
        }
        again=0;
        if finished{again=replay();}
    }
    close(input);
    if status(){exit(1);}
    return 0;
}
```

### Change 2

Find the unique routine header `fn help(){`. Within that routine, replace this existing block, including its shown context:

```rill
fn help(){
    say("Use the first and last words; only three letters count.\r\n");
    say("LOOK, HELP and QUIT\r\n");
    say("GO NORTH or N; also S, E, W, U and D\r\n");
    say("GET and DROP\r\n");
    say("INVENTORY\r\n");
    say("READ\r\n");
    say("PUSH\r\n");
    say("WAIT\r\n");
    say("HIT\r\n");
    say("TIE\r\n");
    say("ROW and SWIM\r\n");
    say("OIL\r\n");
    say("OPEN\r\n");
    say("KILL.\r\n");
    return 0;
}
```

With this complete block:

```rill
fn help(){
    say("Use the first word for an action and the last for its object.\r\n");
    say("Only the first three letters count. READ THE SIGN works.\r\n");
    say("GO NORTH or N; also S, E, W, U and D.\r\n");
    say("LOOK, GET, DROP, INVENTORY, HIT, OPEN, TIE, PUSH, ROW, OIL.\r\n");
    say("KILL, SWIM, WAIT, HELP and QUIT are also understood.\r\n");
    say("Carry at most seven objects. Explore and examine things.\r\n");
    say("Each command except QUIT costs one minute. Blank input is free.\r\n");
    say("Dracula wakes at midnight. Finish before then.\r\n");
    return 0;
}
```

### Change 3

Find the unique routine header `fn newgame(){`. Within that routine, replace this existing block, including its shown context:

```rill
fn newgame(){
    location=1;playing=1;
    elapsed=0;
    finished=0;
    fire_out=0;
    rope_tied=0;
    shore=11;
    stakes=0;
    nails_loose=0;
    door_open=0;
    coffin_open=0;
    world();
    items();
    return 0;
}
```

With this complete block:

```rill
fn newgame(){
    location=1;elapsed=0;playing=1;finished=0;
    fire_out=0;rope_tied=0;stakes=0;nails_loose=0;
    door_open=0;coffin_open=0;shore=11;
    world();items();return 0;
}
```

### Change 4

Append these complete routines after the final routine in your source:

```rill
fn replay(){
    if ended{return 0;}
    say("Play again (Y/N)? ");
    if readline()!=1{return 0;}
    parse();return wordis(verb,"Y  ")|wordis(verb,"YES");
}
```

## Build and try it

```dos
VMAKE V26
```

Require these fresh tool reports, followed by BUILD PASS:

```text
OK RESULT.IR 0000047783
OK RESULT.ASM 0000126562 text bytes
OK RESULT.COM 19834 bytes
BUILD PASS
```

The preserved V26.COM is 19,834 bytes. Its natural display and behavior are the checks below.

Create F064.TXT with these additional commands:

```text
Y
LOOK
QUIT
```

Join the saved WIN.TXT walk and this tail as T26.TXT:

```dos
COPY /B WIN.TXT+F064.TXT T26.TXT
```

Reuse the saved F006.TXT command tail.

Join the saved WIN.TXT walk and this tail as X26.TXT:

```dos
COPY /B WIN.TXT+F006.TXT X26.TXT
```

```dos
CHECK V26 T26.TXT
```

Require these significant game lines, followed by CHECK's PASS:

```text
Play again (Y/N)?
Goodbye.
PASS
```

## Check the other case

```dos
CHECK V26 X26.TXT
```

Require these significant lines and PASS:

```text
Play again (Y/N)?
PASS
```

A player death or an unsuccessful action is an ordinary game outcome, so CHECK still reports PASS. Judge the stated message and the resulting world as well as the process status.

## If it differs

Test a second game after changing a passage or object, not just after quitting at the entrance. A reset must rebuild names and exits as well as numeric flags.
