THE BOOTSTRAP PROJECT - ASM86A
A practical course in small-system software

The bootstrap ladder: BOOTASM -> ASM86 -> ASMA0 -> ASM86A -> IR86 -> RILL.
Begin with the separate completed ASMA0 collection and its self-builds.
Read the workbench, then the construction articles in order.

BOOTASM.BAS  Completed BASIC foundation, unchanged.
ASM86.ASM    Preceding native assembler, unchanged.
ASMA0.ASM    Seed, identical to A12.ASM; built directly with ASM86.
ASM86A.ASM   Complete assembler, identical to A40.ASM; built by ASMA0.
A13.ASM through A40.ASM: twenty-eight construction checkpoints.
A12.ASM: identical to the verified ASMA0 prerequisite.
Tnn.ASM and Xnn.ASM: acceptance and rejection inputs where applicable.
VIEW.BAS and CHECK.BAT: unchanged viewer and immediate DOS checker.
HELLO.ASM, FRAME.ASM, BRIDGE.ASM, COPYTEXT.ASM: complete programs.
LONGSRC.BAS and SYMS.BAS: BASIC generators of source text only.

Use your own DOS 3.10 and period GW-BASIC interpreter. Note its banner.
Build ASM86 with BOOTASM.BAS; preserve it as ASMKEEP.COM.
The ASMA0 collection uses ASMKEEP to build A01 through A12.
The completed seed is 3342 bytes, with two matching self-builds.
Keep the tested ASMA0.COM to build A13 through A40.

For a fixed-file build: COPY A13.ASM SOURCE.ASM; CHECK ASMA0.
Require OK and PASS, then COPY RESULT.COM A13.COM before testing.
The complete ASM86A is 6422 bytes; preserve it as ASMAKEEP.COM.
It has no filename prompt. ASMKEEP remains the original ASM86.
SOURCE.ASM is reopened for two passes and must remain unchanged.
RESULT.COM is the published output; ASMA.TMP and RESULT.BAK are
reserved recovery names. Inspect existing recovery files before use.
Require a fresh OK and PASS before using any result.

Many output fixtures are encoding data. Inspect them rather than
executing them. Run only expressly identified complete programs.
A40 acceptance input is the canonical ASM86A self-build source.

The seed streams 1024-byte blocks with 2048 symbols in one segment.
The complete tool streams 4096-byte blocks and allocates 8192 records
in eight symbol pages plus a hash block: 392 KiB including its main
segment, before DOS/environment/allocation overhead. Names may have
31 characters. Physical lines have at most 1023 characters. Output
has at most 61184 bytes in the chosen single-segment COM profile.
Its source language is a selected 8086 subset, not all Intel syntax.
Consult the reference for exact forms, limits, and recovery behavior.

All packaged files are source, ASCII, DOS line endings, and 8.3 names.
No preassembled program, DOS copy, or BASIC interpreter is included.
