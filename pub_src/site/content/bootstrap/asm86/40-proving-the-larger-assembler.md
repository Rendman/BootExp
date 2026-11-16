+++
title = "24 \u00b7 Proving the larger assembler"
weight = 24
description = "Compare the seed-built program with two native self-assembly generations."
download = "A40.ASM"
download_group = "tools/asm86"
reader_names = 1
url = "/bootstrap/asm86a/40-proving-the-larger-assembler/"
+++

I put the completed source beside the copy built by ASM1. The memory sketch now includes allocated pages, and the instruction notes cover far more operand forms than when I began. The builder is still the preserved seed. I'll ask the larger assembler to reproduce that executable, then let its copy repeat the job.

## The working parts

Save the preceding source as ASM86.ASM. ASM1 builds its first executable from that source. ASM86 then assembles the same source twice and both outputs must match the seed-built original. Keep each known working generation under a distinct short disk name.

The tool uses command-line filenames, streamed I/O, 8192 exact-spelling symbols, an allocated workspace, and the documented native language. The complete ladder exercise carries its output into the IR86 and RILL tools.

## Enter the source

Copy `A37.ASM` to `A40.ASM`. The tested source is retained without edits. This stopping point proves the executable handoff.

## Build the stopping point

```dos
CHECK ASM1 A40.ASM RESULT.COM
```

Require `OK RESULT.COM 06433 bytes` and PASS. Preserve this executable before using its fixed output name:

```dos
COPY RESULT.COM A40.COM
```

VIEW.BAS must report A40.COM length 6433 bytes. Keep that executable and source together.

## Acceptance check

```dos
COPY A40.ASM ASM86.ASM
COPY A40.COM ASM86.COM
```

```dos
CHECK A40 ASM86.ASM RESULT.COM
```

Require:

```text
OK RESULT.COM 06433 bytes
PASS
```

In VIEW.BAS, inspect RESULT.COM. Require length **6433 bytes** and these first thirty-two bytes:

```text
FC 81 FC FE FF 74 06 B8 07 00 E9 10 0C E8 CB 15 E8 D0 0D E8 DE 0C B0 01 88 06 A6 17 B8 00 00 89
```

Compare the first self-produced executable with the preserved original, then use that new generation to assemble the same source once more:

```dos
ECHO N>NO.TXT
COMP ASM86.COM RESULT.COM <NO.TXT
COPY RESULT.COM GEN1.COM
CHECK GEN1 ASM86.ASM RESULT.COM
COMP ASM86.COM RESULT.COM <NO.TXT
```

Both COMP comparisons must report no differences. GEN1 must report `OK RESULT.COM 06433 bytes` and PASS. COMP may ask whether to compare more files; NO.TXT answers N. Keep the original ASM86.COM separately.

I keep the seed-built copy beside the two matching generations. Its file is still a single COM program; the extra symbol pages are workspace it obtains when it runs. I can follow how ASM1 made the first copy and how that copy made the next.

```dos
COPY ASM86.COM ASMAKEEP.COM
```

ASMAKEEP.COM is the preserved command-line assembler. ASMKEEP.COM still names the original ASM0.

## A rejection check

Create X40.ASM with this separate source:

```asm
MOV AX,AL
```

```dos
CHECK A40 X40.ASM RESULT.COM
```

Require:

```text
ERROR 0000000001 CODE 1
FAIL
```

The accepted RESULT.COM must remain unchanged. Keep a copy and compare it with COMP if in doubt. Require a fresh OK before using any output.

An unexpected PASS fails this rejection test.

## If the result differs

Check descriptor width, segment selection, ModR/M bits, displacement order, and registers changed by EMIT. Use the printed bytes to distinguish a parser mistake from an encoding mistake. Keep the branch size the same in both passes.
