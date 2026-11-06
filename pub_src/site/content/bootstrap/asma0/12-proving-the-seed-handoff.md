+++
title = "12 \u00b7 Proving the seed handoff"
weight = 12
description = "Build ASMA0 with ASM86 and compare two self-assembly generations."
download = "A12.ASM"
aliases = ["/bootstrap/asm86a/12-proving-the-seed-handoff/"]
+++

A successor becomes a rung of the ladder only when its preceding builder can make it.

## The working parts

The source is the preceding tested checkpoint, saved here under a permanent seed name. ASM86 builds it directly. ASMA0 then reads that same source through SOURCE.ASM, writes RESULT.COM, and must reproduce its own executable. A second generation must match too.

Keep the initial ASM86-built executable while making both comparisons. The seed has streaming I/O, 2048 symbols, a larger output profile, and explicit segment access. No outside assembler supplies an executable.

## Enter the source

Copy `A11.ASM` to `A12.ASM`. The tested source is retained without edits. This stopping point proves the executable handoff.

## Build the stopping point

Run `CHECK ASMKEEP`, enter `A12` at `Source name:`, and require `OK 03342 bytes` and PASS. This uses the preceding published ASM86, not the new checkpoint. It creates A12.COM.

VIEW.BAS must report A12.COM length 3342 bytes. Keep that executable and source together.

## Acceptance check

```dos
COPY A12.ASM ASMA0.ASM
COPY A12.COM ASMA0.COM
COPY ASMA0.ASM SOURCE.ASM
```

```dos
CHECK A12
```

Require:

```text
OK RESULT.COM 03342 bytes
PASS
```

In VIEW.BAS, inspect RESULT.COM. Require length **3342 bytes** and these first thirty-two bytes:

```text
FC 81 FC FE FF 74 06 B8 07 00 E9 8A 08 E8 5A 09 B0 01 88 06 4F 0C B8 00 00 89 06 43 0C B8 00 50
```

Compare the first self-produced executable with the preserved original, then use that new generation to assemble the same source once more:

```dos
ECHO N>NO.TXT
COMP ASMA0.COM RESULT.COM <NO.TXT
COPY RESULT.COM GEN1.COM
CHECK GEN1
COMP ASMA0.COM RESULT.COM <NO.TXT
```

Both COMP comparisons must report no differences. GEN1 must report `OK RESULT.COM 03342 bytes` and PASS. COMP may ask whether to compare more files; NO.TXT answers N. Keep the original ASMA0.COM separately.

Continue with the separate [ASM86A collection](../../asm86a/index.html). For its construction builds, ASMA0.COM is the preceding builder. ASMKEEP.COM remains the original ASM86. Their filename interfaces differ; do not overwrite one with the other.

## A rejection check

Create X12.ASM with this separate source:

```asm
MOV AX,AL
```

```dos
COPY X12.ASM SOURCE.ASM
CHECK A12
```

Require:

```text
ERROR 00001 CODE 1
FAIL
```

The accepted RESULT.COM must remain unchanged. Keep a copy and compare it with COMP if in doubt. Require a fresh OK before using any output.

An unexpected PASS fails this rejection test.

## If the result differs

Check the fixed name bytes, handle ownership flags, reader cursors at each pass, and the current output count. Inspect file length as well as the leading bytes. A copied data file is not an executable proof.
