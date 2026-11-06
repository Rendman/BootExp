+++
title = "29 \u00b7 The bootstrap ladder"
weight = 29
description = "Carry the BASIC-built foundation through two assembler handoffs to working compiler output."
download = "ASM86.ASM"
download_group = "tools/asm86"
reader_names = 1
+++

A rung is useful when the tool below can build it and the tool above can use its result. This exercise follows the published chain:

```text
GW-BASIC → BOOTASM → ASM0 → ASM1 → ASM86 → IR86 → RILL0 → RILLBOOT → RILL
```

ASM1 is the completed streaming-seed collection between ASM0 and ASM86. Retain the canonical sources and the two matching self-assembly generations from each assembler handoff.

## From BASIC to the larger assembler

The BOOTASM collection constructs BOOTASM.BAS. Run GWBASIC BOOTASM.BAS, enter ASM0, require its OK report, then use SYSTEM to return to DOS. VIEW.BAS must report ASM0.COM length 2622. Preserve ASMKEEP.COM as that original native assembler. The ASM0 collection's self-assembly exercise compares its native generations.

Now make the seed with that preceding builder:

```dos
CHECK ASMKEEP
```

Enter ASM1. Require `OK 03342 bytes` and PASS. Preserve ASM1.COM. The seed handoff article compares two self-produced copies with this original. Then build the larger source:

```dos
COPY ASM86.ASM SOURCE.ASM
CHECK ASM1
```

Require `OK RESULT.COM 06422 bytes` and PASS. Copy RESULT.COM to ASM86.COM and ASMAKEEP.COM. The final handoff article compares two self-builds against this seed-produced executable. The accepted source itself uses only the seed's instruction language.

Check compatibility with the preceding assembler:

```dos
COPY ASM0.ASM SOURCE.ASM
CHECK ASMAKEEP
ECHO N>NO.TXT
COMP ASMKEEP.COM RESULT.COM <NO.TXT
```

Require `OK RESULT.COM 02622 bytes`, PASS, and no COMP differences. The larger tool reproduces the original builder, including its filename prompt. Do not replace ASMAKEEP with this output.

## Build the published IR86 and RILL

Use IR86.ASM from the [IR86 collection](../../ir86/index.html), and RILL0.IR from the [RILL collection](../../rill/index.html). Those collections supply their full construction and language explanations. This is a build of their published sources; extra assembler capacity does not remove the translators' own bounds.

```dos
COPY IR86.ASM SOURCE.ASM
CHECK ASMAKEEP
COPY RESULT.COM IR86.COM
COPY IR86.COM IRKEEP.COM
CHECK IRKEEP
```

Require `OK RESULT.COM 06407 bytes` and PASS before the copies. At IR source name, enter RILL. Require `OK RILL0.ASM 24676 text bytes` and PASS. Assemble the generated compiler:

```dos
COPY RILL0.ASM SOURCE.ASM
CHECK ASMAKEEP
COPY RESULT.COM RILL0.COM
COPY RILL0.COM RLKEEP.COM
```

Require `OK RESULT.COM 05173 bytes` and PASS before saving RILL0.COM. The compiler source is IR86; ASM86 assembles the translator's output. No hidden native compiler is involved.

## Run the complete translation

Create HI.RIL:

```rill
fn main() {
    putc(72);
    putc(73);
}
```

```dos
COPY HI.RIL SOURCE.RIL
CHECK RLKEEP
COPY RESULT.IR HI.IR
CHECK IRKEEP
```

Require `OK RESULT.IR 00052` and PASS before copying it. At IR source name enter HI; require `OK HI.ASM 02600 text bytes` and PASS. Then:

```dos
COPY HI.ASM SOURCE.ASM
CHECK ASMAKEEP
COPY RESULT.COM HI.COM
CHECK HI
```

Require `OK RESULT.COM 00480 bytes` and PASS before copying. HI displays HI and reports PASS. Its source mentions neither processor registers nor DOS interrupts; those belong to the selected backend and runtime.

## Observe a failed rung

Preserve HI.ASM. Make BAD.ASM containing:

```asm
MOV CS,AX
```

Copy BAD.ASM to SOURCE.ASM and run CHECK ASMAKEEP. Require `ERROR 0000000001 CODE 1` and FAIL. RESULT.COM must still compare equal to HI.COM. An unexpected PASS fails the rejection check. Restore the accepted source before another build.

If any build differs, stop at the first missing OK, count mismatch, or failed comparison. Inspect that tool's source and its immediate output. A later executable cannot prove a failed earlier translation, and an old RESULT.COM must never stand in for a newly successful assembly.
