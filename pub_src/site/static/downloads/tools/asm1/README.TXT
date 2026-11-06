THE BOOTSTRAP PROJECT - ASM1
A practical course in small-system software

The ladder: BOOTASM -> ASM0 -> ASM1 -> ASM86 -> IR86 -> RILL.
ASM1 is the streaming seed collection, built directly by ASM0.
Read its workbench, construction articles, reference, and programs.

BOOTASM.BAS and ASM0.ASM: unchanged preceding bootstrap sources.
A01.ASM through A12.ASM: complete seed construction checkpoints.
ASM1.ASM: complete seed, identical to A12.ASM.
Tnn.ASM and Xnn.ASM: exact acceptance/rejection inputs where applicable.
VIEW.BAS and CHECK.BAT: unchanged inspection and DOS status helpers.
SYMS.BAS: source-text generator for the 2048-definition exercise.
HELLO.ASM, MEMORY.ASM, COUNT.ASM: complete executable examples.

Use your own DOS 3.10 and period GW-BASIC interpreter; note its banner.
Build ASM0 from BOOTASM.BAS. Preserve it as ASMKEEP.COM.
CHECK ASMKEEP prompts for A01 through A12 without an extension.
Require OK and PASS at every build. Preserve each source/executable.
A03 through A06 copy data; inspect that output, never execute it.
Only fixtures expressly identified as complete programs may be run.

ASM1.COM is 3342 bytes. Compare both self-assembly generations with
its ASM0-built original. The seed uses fixed SOURCE.ASM/RESULT.COM,
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
