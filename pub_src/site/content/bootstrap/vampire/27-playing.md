+++
title = "Playing the adventure"
weight = 27
description = "Keyboard commands, hints and a separately marked winning walk."
download = "VAMPIRE.RIL"
download_group = "tools/vampire"
reader_names = 1
+++

Compile the complete VAMPIRE.RIL with the same three tools, or preserve the accepted V26.COM under that name. Enter VAMPIRE for keyboard play, or VAMPIRE followed by a saved command filename. This is a text adventure: no color display, cursor-addressing driver or sound hardware is required.

## Commands

Use the first word for an action and the last for its object; only the first three letters of each count. LOOK describes the room; READ THE SIGN examines the sign. N, S, E, W, U and D move through ordinary exits. GET/TAKE, DROP and INVENTORY manage possessions. HIT, OPEN, TIE, PUSH, ROW and OIL act on the surroundings. CLIMB shares GO; BREAK shares HIT; THRUST shares KILL. HELP lists the commands, WAIT spends a minute and QUIT returns to DOS. When asked With what?, In what? or To what?, answer with the object, such as HAMMER or BUCKET.

The adventure begins at 8:00 p.m. Every nonempty, well-formed command except QUIT spends one minute, including LOOK, HELP and an unknown action. A follow-up answer belongs to its original action. Midnight ends play before the 240th action can run. There is room for seven carried objects. A visible fixed object cannot be taken; an object in another room cannot be inspected by guessing its name.

## Hints

Read the entrance sign and the parchment. Try moving furniture. An opening may require a tool even after it is safe to enter. A rope needs an anchor; water needs a vessel. Keep the crate intact until it has served as a step. A small guardian may prefer food to a fight. The timepiece is useful but need not occupy a carrying place throughout the walk.

## Solution — stop here to explore unaided

WIN.TXT is a complete winning walk assembled from the saved journeys in the construction. It leaves the oar briefly on the Torture Chamber floor to demonstrate that the rat still guards a reachable key, then retrieves it before crossing the lake. The crate supports the climb before becoming stakes. Nails, tapestry and axe are dropped when their jobs are complete.

```dos
CHECK VAMPIRE WIN.TXT
```

Require the following ending; EOF after the replay question returns to DOS:

```text
Congratulations! You have killed Dracula.
Time: 08:58 p.m.
Play again (Y/N)?
PASS
```

The actual commands in the complete walk are:

```text
E
PUSH BOOKCASE
D
GET ROPE
N
GET OIL
N
GET BUCKET
GET CRATE
U
E
E
E
GET AXE
E
GET HAMMER
TIE ROPE
PARAPETS
GO ROPE
GET OAR
S
GET WATER
BUCKET
U
W
W
W
DROP WATER
DROP BUCKET
GET CHEESE
GO FIRE
GET TORCH
HIT FIRE
HAMMER
N
W
LOOK RAT
DROP OAR
GET KEY
GET OAR
DROP CHEESE
GET KEY
E
N
GO BOAT
ROW
DROP CRATE
GO OVERHANG
GET NAILS
DROP NAILS
D
GET TAPESTRY
DROP TAPESTRY
GET CRATE
HIT CRATE
AXE
DROP AXE
N
OIL DOOR
N
OPEN COFFIN
KILL DRACULA
STAKES
```

The game does not write a saved position. To replay a journey, run its command file again. A new game resets every object, exit and puzzle flag.
