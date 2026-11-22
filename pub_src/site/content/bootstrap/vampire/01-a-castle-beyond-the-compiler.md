+++
title = "01 \u00b7 A castle beyond the compiler"
weight = 1
description = "Print the adventure title and our first room using the completed RILL toolchain."
download = "V01.RIL"
download_group = "tools/vampire"
reader_names = 1
+++

I have spent so many evenings making programs that make other programs that I want to try something different. A castle, a locked coffin and a few troublesome objects will do. This is an optional excursion from the completed RILL workbench: an adventure adapted from the BASIC listing, with its nineteen rooms and midnight deadline.

## What changes

say walks a zero-terminated string one byte at a time. Its parameter is a byte address, not a BASIC string variable. putc writes each character; failed output terminates with status one. CR followed by LF starts a DOS display line. main supplies only the title and the Entrance Hall. Both strings remain part of the game.

## Enter the source

Create V01.RIL as plain ASCII:

```rill
// Vampire Castle Adventure.


fn main(){
    say("Vampire Castle Adventure\r\n");
    say("You are in the Entrance Hall.\r\n");
    return 0;
}

fn say(text){
    while load8(text){
        putc(load8(text));
        if status(){exit(1);}
        text=text+1;
    }
    return 0;
}
```

## Build and try it

```dos
VMAKE V01
```

Require these fresh tool reports, followed by BUILD PASS:

```text
OK RESULT.IR 0000000568
OK RESULT.ASM 0000007824 text bytes
OK RESULT.COM 01617 bytes
BUILD PASS
```

The preserved V01.COM is 1,617 bytes. Its natural display and behavior are the checks below.

```dos
CHECK V01
```

Require these significant game lines, followed by CHECK's PASS:

```text
Vampire Castle Adventure
You are in the Entrance Hall.
PASS
```

## If it differs

A missing backslash changes the displayed line ending. Keep the quotes and both escape sequences.
