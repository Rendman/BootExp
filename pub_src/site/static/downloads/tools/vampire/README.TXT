THE BOOTSTRAP PROJECT - VAMPIRE CASTLE ADVENTURE
An optional application after Rebuilding Our Tools in RILL

Begin with the adventure workbench, then read the construction in order.
Preserve the completed RILL-written compiler as R0.COM, translator as
I0.COM and assembler as A0.COM. They are not supplied in this archive.
No LINK86 or EDIT86 extension is needed. This game is not a required
bootstrap stage, and no tool depends on it.

V01.RIL through V26.RIL are complete, continuing source checkpoints.
VAMPIRE.RIL is identical to V26.RIL. VMAKE V01 builds with R0, I0 and
A0 and preserves V01.COM only after successful tool runs. Require
fresh OK reports and BUILD PASS. A failed build can leave an old COM.
Do not run it as though it were a newly accepted executable.

VAMPIRE reads keyboard lines from DOS CON. VAMPIRE COMMANDS.TXT
reads one selected 8.3 command file from the saved PSP arguments.
Use plain ASCII, current-directory filenames, and no extra arguments.
CHECK V26 WIN.TXT exercises the complete winning walk.
Tnn.TXT and Xnn.TXT are focused public-command fixtures; X is an
alternate game case, not necessarily a process failure. Normal play,
death and victory return zero. File/argument/service failures return one.
The CHECK result must be interpreted with the stated game messages.

ROPE, CHAPEL, SUPPLY, DARK, LIGHT, LAKE, GEAR, EQUIP, GATE, KEYBASE,
KEY, TOMB, COFFIN and WIN are reusable TXT journeys. Fnnn.TXT files
are the short tails joined with COPY /B in the articles. They contain
no Control-Z terminator. WAIT.BAS writes the 240-record clock fixture.
The archive already supplies every expanded command file.

The adventure has nineteen rooms and twenty-five objects. First and
last words use three-letter prefixes. Carry at most seven objects;
finish before command 240 brings midnight. Follow-up replies cost no
extra turn. QUIT and blank input spend no time. EOF returns to DOS;
there is no saved-game file. Replay rebuilds all mutable world state.
Use the play guide for hints and its separately marked complete solution.

The BASIC adventure listing supplies the map and puzzle sequence.
This RILL adaptation uses plain DOS text instead of terminal effects
and returns to DOS instead of loading an external menu program.
The workbench tools and their accepted languages are unchanged.
All members are ASCII/CRLF/8.3 source or command text; no executable,
interpreter, compiled IR or generated assembly is distributed here.
