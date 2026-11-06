+++
title = "28 \u00b7 Proving the larger assembler"
weight = 28
description = "Compare the seed-built program with two native self-assembly generations."
download = "A40.ASM"
+++

The expanded assembler is another working rung, not a source listing dependent on an outside tool.

## The working parts

Save the preceding source as ASM86A.ASM. ASMA0 builds its first executable from that source. ASM86A then assembles the same source twice and both outputs must match the seed-built original. Keep each known working generation under a distinct short disk name.

The tool uses fixed files, streamed I/O, 8192 exact-spelling symbols, an allocated workspace, and the documented native language. The complete ladder exercise carries its output into the IR86 and RILL tools.

## Enter the source

Copy `A39.ASM` to `A40.ASM`. The tested source is retained without edits. This stopping point proves the executable handoff.

## Build the stopping point

```dos
COPY A40.ASM SOURCE.ASM
CHECK ASMA0
```

Require `OK RESULT.COM 06422 bytes` and PASS. Preserve this executable before using its fixed output name:

```dos
COPY RESULT.COM A40.COM
```

VIEW.BAS must report A40.COM length 6422 bytes. Keep that executable and source together.

## Acceptance check

```dos
COPY A40.ASM ASM86A.ASM
COPY A40.COM ASM86A.COM
COPY ASM86A.ASM SOURCE.ASM
```

```dos
CHECK A40
```

Require:

```text
OK RESULT.COM 06422 bytes
PASS
```

In VIEW.BAS, inspect RESULT.COM. Require length **6422 bytes** and these first thirty-two bytes:

```text
FC 81 FC FE FF 74 06 B8 07 00 E9 13 0C E8 D6 0D E8 E4 0C B0 01 88 06 C9 16 B8 00 00 89 06 BF 16
```

Compare the first self-produced executable with the preserved original, then use that new generation to assemble the same source once more:

```dos
ECHO N>NO.TXT
COMP ASM86A.COM RESULT.COM <NO.TXT
COPY RESULT.COM GEN1.COM
CHECK GEN1
COMP ASM86A.COM RESULT.COM <NO.TXT
```

Both COMP comparisons must report no differences. GEN1 must report `OK RESULT.COM 06422 bytes` and PASS. COMP may ask whether to compare more files; NO.TXT answers N. Keep the original ASM86A.COM separately.

```dos
COPY ASM86A.COM ASMAKEEP.COM
```

ASMAKEEP.COM is the preserved fixed-file assembler. ASMKEEP.COM still names the original prompted ASM86.

## A rejection check

Create X40.ASM with this separate source:

```asm
MOV AX,AL
```

```dos
COPY X40.ASM SOURCE.ASM
CHECK A40
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
