+++
title = "The adventure workbench"
weight = 0
description = "Preserve the completed RILL trio and build each game before trying its commands."
download = "VAMPIRE.ZIP"
download_group = "tools/vampire"
reader_names = 1
+++

This optional series begins after the three RILL-written tools and their matching rebuilds. Preserve the compiler as R0.COM, translator as I0.COM and assembler as A0.COM. Use the DOS 3.10 work directory and a plain ASCII editor. Copy the established CHECK.BAT here. No linker, screen service extension or outside development tool is needed.

## A build worth keeping

Create VMAKE.BAT:

```dos
ECHO OFF
IF "%1"=="" GOTO USAGE
R0 %1.RIL RESULT.IR
IF ERRORLEVEL 1 GOTO FAILED
I0 RESULT.IR RESULT.ASM
IF ERRORLEVEL 1 GOTO FAILED
A0 RESULT.ASM RESULT.COM
IF ERRORLEVEL 1 GOTO FAILED
COPY RESULT.COM %1.COM >NUL
IF ERRORLEVEL 1 GOTO FAILED
ECHO BUILD PASS
GOTO END
:USAGE
ECHO Use VMAKE V01
GOTO END
:FAILED
ECHO BUILD FAIL - DO NOT RUN AN OLDER GAME
:END
```

Enter `VMAKE V01` to build V01.RIL through all three tools and preserve V01.COM. Each tool must print a fresh OK report; require BUILD PASS before running the preserved program. A failed build can leave an older .COM with the same name. BUILD FAIL does not authorize running it. Keep all three result names distinct from the checkpoint name. The batch invokes executable tools directly and works without nested batch calls.

## Keyboard and saved commands

Enter `V26` for keyboard play. It opens DOS CON as a readable device and uses ordinary line input; press Return to submit a command. The game writes its replies through putc. The first input-reading checkpoint returns at end of input; Control-Z followed by Return ends console text. From the command-parser checkpoint onward, QUIT also returns to DOS.

```dos
CHECK V26 WIN.TXT
```

The optional filename comes from argc()/arg(1), backed by the saved PSP command tail. It must be an unquoted 8.3 name in the current directory. A command file is read-only and is echoed as it runs. CR/LF, bare CR and LF are accepted. End of file stops play; it does not save a position. A terminal game result can ask for Y/N; include the answer in a script if you want a replay.

## Retain the journeys

Enter each named command file when it first appears and keep it. COPY /B joins a saved prefix and a short tail; it does not run the game. Command files contain ordinary text without a Control-Z terminator. Keep the final newline before appending a tail. The fixtures in the source disk already have the exact DOS line endings.

Every construction article builds its own Vnn.COM, runs a focused accepted walk and checks a relevant alternate. The printed expected lines are the significant parts of the ordinary game transcript, in addition to prompts, room descriptions and echoed commands. CHECK reports PASS for ordinary play, including death and victory; those outcomes are game rules. File, argument or service failures return nonzero and must report FAIL.

## Preserve the finished adventure

```dos
COPY V26.RIL VAMPIRE.RIL
COPY V26.COM VAMPIRE.COM
VAMPIRE
```

The game remains optional. No bootstrap article depends on its executable, source or extra files. Its source disk is self-contained apart from the already constructed RILL trio and DOS/BASIC workbench.
