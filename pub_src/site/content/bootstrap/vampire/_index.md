+++
title = "Vampire Castle Adventure"
weight = 100
description = "An optional text adventure built with our completed RILL workbench."
download = "VAMPIRE.RIL"
download_group = "tools/vampire"
reader_names = 1
cover = true
optional = true
tool_id = "VAMPIRE"
collection_key = "vampire"
+++

The compiler finally builds programs of its own, and I want to use it for an evening in a different sort of workshop. A BASIC adventure listing offers a castle, a sleeping vampire and a collection of objects that are never quite where I need them. Vampire Castle Adventure is an optional RILL application after [Rebuilding Our Tools in RILL](../toolchain/index.html); it is outside the required bootstrap ladder.

## What we're adding

- **An optional RILL application:** Use the completed compiler, translator and assembler to build a text adventure without adding a required rung to the toolchain.
- **A castle represented by tables:** Keep nineteen rooms, six directions and twenty-five objects in ordinary byte storage so exploration changes data rather than the movement code.
- **Commands and connected puzzles:** Recognize short phrases, manage seven carried objects and reach Dracula before a command-driven midnight deadline.
- **Console or saved commands:** Read keyboard input through DOS CON, or select an 8.3 command filename through the portable startup arguments so a walk can be repeated.
- **Small playable stopping points:** Preserve each growing game, with focused checks and reusable journey transcripts.

**Removing:** None of the workbench tools or language features. The adaptation uses plain DOS text in place of the BASIC listing's terminal escape effects and returns to DOS instead of loading an external menu program.

## The construction

Twenty-six working stopping points grow the title into the complete adventure. Each uses the established compiler, translator and assembler. The world, command reader and puzzles are built in small pieces; saved journeys avoid entering the same long route for each check. LINK86 and EDIT86 are not prerequisites.

The BASIC listing supplies the map, objects and puzzle sequence. The RILL program uses plain DOS text, bounded input, visible object checks and an independent reset for each game. It contains no BASIC interpreter and loads no external game data.

Begin with [the adventure workbench](00-workbench/index.html). The [source disk](../../downloads/tools/vampire/VAMPIRE.ZIP) contains every RILL stopping point, command fixture and the complete game, without prebuilt executables. [Playing the adventure](27-playing/index.html) keeps the solution separate from the construction; [the program reference](28-reference/index.html) records the rules and limits.

![A young programmer holding a disk asks a castle gatekeeper to admit a small compiler.](../../images/vampire-gate.svg)

*The tools have brought us to a different sort of gate.*
