+++
title = "The Bootstrap Experiment"
weight = 1
description = "An 8088, a BASIC interpreter, and a young programmer determined to make his own tools."
cover = true
+++

It is 1986. I am still in school, and there is usually a programming magazine open beside the computer. Sometimes I type in a listing. Sometimes I change a few things to see what happens. An evening can disappear into finding a missing quotation mark, but getting the program to run makes me want to try something larger.

I have started reading about assembly language and compilers. The articles describe programs that seem much closer to the machine than the BASIC programs I know. I want to write those programs, and I want to understand how the tools that build them work.

The difficulty is getting the tools. The assemblers and compilers advertised in the back of the magazines cost more than I can spend. I have no development package to borrow and nobody nearby with a disk I can use. I keep coming back to articles whose first instruction is to run a program I do not have.

What I do have is DOS, its BASIC interpreter, some manuals, and time at the keyboard.

One question keeps bothering me: somebody had to write the first assembler. What did they use? BASIC can read a text file. It can work with numbers and write bytes to disk. Perhaps I can use it to make a small assembler of my own. It would only have to understand enough instructions to build a useful program.

I begin with a smaller job: write one byte to a file and look at it. Once that works, I can try a sequence of bytes. Then instruction names. Then labels, so I can move a piece of code without calculating all its addresses again. Each working piece gives me something I can use to build the next.

That is how this experiment begins. I want an assembler, a compiler, an editor, and a workbench I can keep extending. I am going to try to make them with the tools already on my desk.

This series is the notebook for that attempt. It contains the source to enter, the reasons for each addition, and the checks that tell us whether it works. If you have DOS and BASIC, you can pull up a chair and build along with me.

## One working tool at a time

The first assembler is **BOOTASM**, written in GW-BASIC. It builds **ASM0**, an assembler written in assembly language. ASM0 builds the streaming **ASM1**, and that seed builds the larger **ASM86**. Each accepted tool becomes the means of constructing another.

From there we build **IR86**, an intermediate language, and the **RILL** compiler through its small, seed, and self-hosted stages. Eventually the compiler, translator, and assembler can rebuild themselves. A linker and screen editor make the workbench more useful; libraries and a small operating system belong farther along the road.

There is no need to finish all of that in one sitting. Every addition should be small enough to type and understand, with a working stopping point worth saving before we continue.

## A workbench we can understand

Our reference machine is a Leading Edge Model D: an IBM PC/XT-compatible computer with a 4.77 MHz 8088, 640 KB of conventional memory, a 360 KB floppy drive, a small hard disk, and an 80-column monochrome display. The software workbench is MS-DOS 3.10 and its period-appropriate GW-BASIC interpreter. WordPerfect 4.1 may serve other writing work; assembly sources must be plain ASCII, without word-processor formatting.

All executable output is in DOS `.COM` format. The instruction baseline is the 8086/8088. We begin with DOS and BASIC and construct the translation tools ourselves; an outside assembler or compiler is not a prerequisite.

## Reading and typing

Read the explanation before entering a listing. Save a working copy at every stopping point. A source listing is not proved by its appearance on paper: use the supplied input, inspect the result, and try the rejection case as well.

The BASIC construction proceeds through small additions and replacements. Existing lines retain their numbers; the instructions identify every replacement. The complete listings and saved stopping points provide a second way to compare your work.

## The collections

Each tool has its own collection, with the individual construction articles beneath it. Follow **BOOTASM → ASM0 → ASM1 → ASM86 → IR86 → RILL0 → RILLBOOT → RILL**. RILL0 grows into RILLBOOT; that seed builds the compiler written in RILL. [Rebuilding Our Tools in RILL](toolchain/index.html) brings the compiler, translator, and assembler together and compares their rebuilds.

This is an original practical course with a 1986 technical setting. It is not a reproduction of, or affiliated with, a historical magazine.

[Linking Our First Modules](link86/index.html) follows the completed RILL-written toolchain. It builds LINK86 in RILL and links two hand-entered text objects, with public names and relative or absolute word references.

[Building Our Screen Editor](edit86/index.html) supplies EDIT86 after LINK86. Its twenty construction steps add screen and key services, a 256 KiB document buffer, a window, editing, undo and search. The text remains in memory while navigating; Save publishes the fixed EDIT.TXT through temporary and backup files.
