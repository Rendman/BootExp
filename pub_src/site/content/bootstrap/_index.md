+++
title = "The Bootstrap Experiment"
weight = 1
description = "Building a software workbench from the tools already on the desk."
cover = true
+++

A program is usually made with another program. An assembler translates instructions into bytes; a compiler translates a language into instructions. Where does the first tool come from?

We shall begin with GW-BASIC on an 8088 personal computer. The first collection builds **BOOTASM**, a small assembler whose complete source can be entered at the keyboard. The next collection, **ASM86**, will use that assembler to build an assembler written in assembly language. After that come an intermediate language called IR86 and a compiler for RILL, a language with Rust-like syntax. We then intend to rebuild the tools in RILL. A linker, libraries, and a small operating system belong farther along the road.

That is the direction of the experiment, not a promise to hurry. Each addition must be short enough to type, clear enough to explain, and useful enough to test before another is added.

## A workbench we can understand

Our reference machine is a Leading Edge Model D: an IBM PC/XT-compatible computer with a 4.77 MHz 8088, 640 KB of conventional memory, a 360 KB floppy drive, a small hard disk, and an 80-column monochrome display. The software workbench is MS-DOS 3.10 and its period-appropriate GW-BASIC interpreter. WordPerfect 4.1 may serve other writing work; assembly sources must be plain ASCII, without word-processor formatting.

All executable output is in DOS `.COM` format. The instruction baseline is the 8086/8088. We begin with DOS and BASIC and construct the translation tools ourselves; an outside assembler or compiler is not a prerequisite.

## Reading and typing

Read the explanation before entering a listing. Save a working copy at every stopping point. A source listing is not proved by its appearance on paper: use the supplied input, inspect the result, and try the rejection case as well.

The BASIC construction proceeds through small additions and replacements. Existing lines retain their numbers; the instructions identify every replacement. The complete listings and saved stopping points provide a second way to compare your work.

## The collections

BOOTASM and ASM86 occupy the same level in this course. Open a collection to find its individual installments. BOOTASM builds the BASIC foundation; ASM86 builds an assembler in assembly language and finishes by assembling its own source twice.

This is an original practical course with a 1986 technical setting. It is not a reproduction of, or affiliated with, a historical magazine.
