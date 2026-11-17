THE BOOTSTRAP PROJECT - ASM1
A practical course in small-system software

The ladder: BOOTASM -> ASM0 -> ASM1 -> ASM86 -> IR86 -> RILL0
-> RILLBOOT -> RILL.
ASM1 is the streaming seed collection, built directly by ASM0.
Read its workbench, construction articles, reference, and programs.

BOOTASM.BAS and ASM0.ASM: unchanged preceding bootstrap sources.
A01A.ASM through A01F.ASM: six focused opening checkpoints.
A01.ASM adds XOR; A02.ASM through A12.ASM continue the construction.
ASM1.ASM: complete seed, identical to A12.ASM.
Tnn.ASM and Xnn.ASM: exact acceptance/rejection inputs where applicable.
VIEW.BAS inspects bytes; CHECK.BAT forwards filename arguments.
SYMS.BAS: source-text generator for the 2048-definition exercise.
HELLO.ASM, MEMORY.ASM, COUNT.ASM: complete executable examples.

Use your own DOS 3.10 and period GW-BASIC interpreter; note its banner.
Build ASM0 from BOOTASM.BAS. Preserve it as ASMKEEP.COM.
Begin with A01A.ASM copied to SOURCE.ASM for CHECK ASMKEEP.
Preserve RESULT.COM under the checkpoint name. Follow the six
opening articles, then A01 through A12. A01C is a status-only
command-reader probe. A01A/A01B still use fixed work names; A01D
and later accept PSP names. A01E adds the selected result to OK.
Require OK and PASS at every build. Preserve each source/executable.
A03 through A06 copy data; inspect that output, never execute it.
Only fixtures expressly identified as complete programs may be run.

ASM1.COM is 3740 bytes. Compare both self-assembly generations with
its ASM0-built original. The seed accepts PSP source/result names, defaulting to
SOURCE.ASM/RESULT.COM,
1024-byte input/output blocks, 2048 symbols, sixteen-character names,
120-character physical lines, and at most 65535 lines per pass.
It runs in one full 64 KB segment and allocates no extra symbol pages.
Output is streamed, with at most 61184 bytes in the chosen COM profile.
Inspect ASMA.TMP and RESULT.BAK recovery files before another full run.
Source rejection preserves the accepted RESULT.COM. Require fresh OK.

The separate ASM86 collection begins by copying this verified
ASM1.ASM to A13.ASM. Keep the tested ASM1.COM as its builder.
All members are ASCII/CRLF/8.3 source. No executable or interpreter
is supplied in this source collection.

COMMAND-LINE FILENAMES
From ASM1 onward, supply input and output filenames on the command
line: CHECK tool INPUT.EXT OUTPUT.EXT. No arguments select the
default work names. Use unquoted 8.3 filenames in the current directory;
paths and switches are not accepted. Input, output, temporary and backup
names must be distinct. LINK86 takes two object names then the result;
EDIT86 takes one document name and saves that same document.
