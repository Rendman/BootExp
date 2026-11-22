+++
title = "The adventure reference"
weight = 28
description = "Input, world storage, puzzle rules, memory bounds and return status."
download = "VAMPIRE.RIL"
download_group = "tools/vampire"
reader_names = 1
+++

VAMPIRE is a native DOS .COM program written in RILL. Its map, text and logic are compiled into the executable. The compiler, translator and assembler are build tools; they are not loaded to play the game. The program uses only the completed language and its ordinary portable services.

## Input and results

| Item | Contract |
|---|---|
| No arguments | Read lines from DOS CON |
| One argument | Read an unquoted current-directory 8.3 command file supplied through the portable PSP-backed argument services |
| Command | At most 80 printable ASCII characters; tabs become spaces |
| Parser | Uppercase three-character prefixes of first and last words; middle words ignored |
| Line endings | CR/LF, CR, LF, final unterminated line; Control-Z ends text |
| Overlong or invalid record | Drain to its end, print the input diagnostic, spend no turn |
| EOF or QUIT | Return normally; no position is written |
| Exit zero | Ordinary play, including victory and death |
| Exit one | Argument, file or checked service failure |

The input handle is closed on normal return and on a detected read failure. Output errors terminate with failure. No output file or recovery file is created. Keyboard echo comes from DOS; command files are echoed by the game. Follow-up answers use the same input stream and have no separate clock tick.

## World representation

There are nineteen rooms numbered 1–19 and twenty-five objects numbered 1–25. Six exit bytes per room represent North, South, East, West, Up and Down. Zero means no exit. Object locations are zero for carried, 1–19 for a room, and 99 for absent or consumed. Names are ordinary pointers stored with load16/store16; these tables are private program data, not a new language feature. Room zero and object zero are reserved.

Mutable flags record extinguished fire, tied rope, stakes, loose nails, open door and open coffin. The boat shore is eleven or sixteen. A replay calls both world and items, restoring all names and map rows as well as flags and locations. Input stream state is preserved across replay.

## Memory and omissions

The accepted complete image is **19,834 bytes**, including generated code, literals, tables and shared runtime. The declared byte arrays total 328 bytes, and the game allocates no auxiliary blocks. It retains only the current command, not a whole command file. All code and ordinary data fit the existing 61,184-byte image profile; the upper 4 KiB remains the native stack reservation. RILL still reserves its standard sixty-four local words per procedure call.

There is no screen buffer, graphics renderer, sound, random movement, disk paging, saved-game format or external resource file. The torch is already lit, carrying capacity counts objects rather than weight, and oil quantities are not tracked. These choices keep the application small enough to type and understand. The BASIC terminal escape effects and external menu handoff are replaced by plain DOS text and return to DOS. Ordinary visibility checks apply consistently, and leaving the boat returns to its current shore.

The engine keeps processor registers, DOS function numbers and PSP offsets out of its RILL source. DOS-specific CON naming is confined to selecting its default input device. The same world and action routines do not depend on that name.
