+++
title = "02 \u00b7 Listening at the gate"
weight = 2
description = "Read bounded command lines from the console or a PSP-selected command file."
download = "V02.RIL"
download_group = "tools/vampire"
reader_names = 1
+++

An adventure needs the player to answer back. The same file operations that read source text can open the DOS console device, CON. A command file gives us a way to repeat a walk through the castle without typing the walk again.

## What changes

startinput selects CON with no arguments, or arg(1) with exactly one. input is an owned readable handle. nextbyte returns a byte or the distinct word 65535 for end of input; it checks status before using the transfer count. readline retains at most eighty characters plus its terminating zero. It drains an overlong or nonprintable line before returning two, so its tail cannot become another command. A complete line returns one; end of input returns zero. CR/LF, bare CR and LF are accepted, as is a final line without a newline. Control-Z ends text input. Scripted commands are echoed; the DOS console supplies keyboard echo.

## Enter the source

Copy V01.RIL to V02.RIL. Apply the following edits in order. All locators are existing declarations or unique routine headers; no editor line numbers are needed. Keep the source outside each stated edit.

### Change 1

Find this unique existing declaration or routine header; leave it in place:

```rill
fn main(){
```

Insert the following source immediately before it:

```rill
let mut input=0;
let mut ended=0;
let mut skip_lf=0;
let mut scripted=0;
let mut length=0;
let mut playing=1;
bytes command[81];
bytes octet[1];
```

### Change 2

Find the unique routine header `fn main(){`. Within that routine, replace this existing block, including its shown context:

```rill
fn main(){
    say("Vampire Castle Adventure\r\n");
    say("You are in the Entrance Hall.\r\n");
    return 0;
}
```

With this complete block:

```rill
fn main(){
    say("Vampire Castle Adventure\r\n");
    startinput();
    say("You are in the Entrance Hall.\r\n");
    while playing{
        say("\r\n> ");
        let mut got=readline();
        if got==0{playing=0;}
    }
    close(input);if status(){exit(1);}
    return 0;
}
```

### Change 3

Append these complete routines after the final routine in your source:

```rill
fn readline(){
    length=0;
    let mut bad=0;
    let mut done=0;
    while done==0{
        let mut c=nextbyte();
        if skip_lf{
            skip_lf=0;
            if c==10{c=nextbyte();}
        }
        if c==65535{done=1;}
        else{
            if (c==13)|(c==10){
                if c==13{skip_lf=1;}
                done=1;
            }else{
                if c==9{c=32;}
                if (c<32)|(c>126){bad=1;}
                if length==80{bad=1;}
                else{command[length]=c;length=length+1;}
            }
        }
    }
    command[length]=0;
    if ended&(length==0)&(bad==0){say("End of commands.\r\n");return 0;}
    if bad{say("Use at most 80 printable characters.\r\n");return 2;}
    if scripted{say(command);say("\r\n");}
    return 1;
}
```

### Change 4

Find this unique existing declaration or routine header; leave it in place:

```rill
fn readline(){
```

Insert the following source immediately before it:

```rill
fn nextbyte(){
    if ended{return 65535;}
    let mut count=read(input,octet,1);
    if status(){say("Cannot read commands.\r\n");close(input);exit(1);}
    if count==0{ended=1;return 65535;}
    if octet[0]==26{ended=1;return 65535;}
    return octet[0];
}
```

### Change 5

Find this unique existing declaration or routine header; leave it in place:

```rill
fn nextbyte(){
```

Insert the following source immediately before it:

```rill
fn startinput(){
    if argc()>1{say("Use VAMPIRE or VAMPIRE COMMANDS.TXT.\r\n");exit(1);}
    let mut name="CON";
    if argc(){name=arg(1);scripted=1;}
    input=open(name);
    if status(){say("Cannot open commands.\r\n");exit(1);}
    return 0;
}
```

## Build and try it

```dos
VMAKE V02
```

Require these fresh tool reports, followed by BUILD PASS:

```text
OK RESULT.IR 0000004674
OK RESULT.ASM 0000016450 text bytes
OK RESULT.COM 03074 bytes
BUILD PASS
```

The preserved V02.COM is 3,074 bytes. Its natural display and behavior are the checks below.

Create T02.TXT as plain text:

```text
hello
second entry
```

Create X02.TXT as plain text:

```text
XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
look
```

```dos
CHECK V02 T02.TXT
```

Require these significant game lines, followed by CHECK's PASS:

```text
hello
second entry
End of commands.
PASS
```

## Check the other case

```dos
CHECK V02 X02.TXT
```

Require these significant lines and PASS:

```text
Use at most 80 printable characters.
look
PASS
```

## If it differs

An accidental zero in the input is rejected, not treated as a string terminator. Check length before storing the next byte.
