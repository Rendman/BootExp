+++
title = "25 · Preserving the assembler ladder"
weight = 25
description = "Keep the BASIC-built assembler, streaming seed, and larger assembler as tested builders."
download = "ASM86.ASM"
download_group = "tools/asm86"
reader_names = 1
+++

The assembler ladder is BOOTASM → ASM0 → ASM1 → ASM86. Keep each source and accepted executable under its own name. Each native assembler must reproduce the executable made by its preceding builder.

## The original native assembler

Run GWBASIC BOOTASM.BAS and enter ASM0. Require its OK report; use SYSTEM to return to DOS. VIEW.BAS must show ASM0.COM length 2574. Keep the tested copy as ASMKEEP.COM. The ASM0 self-assembly exercise compares two native copies against this original.

## Preserve the streaming seed

Run CHECK ASMKEEP and enter ASM1. Require `OK 03302 bytes` and PASS before preserving ASM1.COM. Its source stays within ASM0's instruction and workspace limits. Keep the two matching self-assembly copies from the ASM1 workbench.

## Build the larger assembler

```dos
COPY ASM86.ASM SOURCE.ASM
CHECK ASM1
COPY RESULT.COM A0.COM
```

Require `OK RESULT.COM 05995 bytes` and PASS before the copy. VIEW.BAS must show A0.COM length 5995. Now use that executable for the same source:

```dos
CHECK A0
COPY RESULT.COM A1.COM
ECHO N>NO.TXT
COMP A0.COM A1.COM <NO.TXT
```

Require the same OK and PASS before the copy, and no COMP differences. SOURCE.ASM remains the complete ASM86 source. Build one more copy:

```dos
CHECK A1
COPY RESULT.COM A2.COM
COMP A0.COM A2.COM <NO.TXT
```

Again require fresh OK and PASS and no differences. All three files have length 5995. Preserve A0.COM as ASMAKEEP.COM, together with ASM86.ASM and the preceding builder sources.

The [complete assembly programs](../43-programs/index.html) exercise counted output, a procedure frame, a distant conditional, and explicit byte movement. Inspect the byte counts before executing each program.
