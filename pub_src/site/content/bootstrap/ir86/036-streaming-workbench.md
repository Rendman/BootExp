+++
title = "The streaming IR workbench"
weight = 36
description = "Use ASM86 to construct a fixed-file translator with room for larger tools."
download = "TOOLCHN.ZIP"
download_group = "tools/toolchain"
reader_names = 1
+++

The bootstrap ladder is BOOTASM → ASM0 → ASM1 → ASM86 → IR86 → RILL. The streaming assembler supplies the source and symbol capacity needed for the native IR workbench. This construction keeps the virtual machine independent of the processor: frame slots, word operations, strings, and opaque services belong to the language; instruction spellings and DOS calls belong to its backend.

Begin with the completed ASM86 workbench and preserve its tested 6422-byte assembler as ASMAKEEP.COM. Keep the original prompted ASMKEEP.COM and IRKEEP.COM separately. The fixed-file tools have different interfaces; do not overwrite a working predecessor merely because another program has the same general purpose.

## Fixed files and saved checkpoints

IW01 starts from the published ASM86.ASM. Its first task is a bounded source reader. Each following IW source starts with a copy of the preceding one. Apply the printed edits from the bottom upward. Reading, tokens, output blocks, operation records, declarations, expressions, services, frames, strings, and allocated blocks have separate stopping points.

To build a checkpoint:

```dos
COPY IW01.ASM SOURCE.ASM
CHECK ASMAKEEP
COPY RESULT.COM IW01.COM
```

Require the assembler's stated OK count and PASS **before** copying its result. The first diagnostics inspect source or copy bytes; their text output is not an executable. Each article identifies its complete output programs explicitly.

A complete translator reads SOURCE.IR and publishes RESULT.ASM through IRTX.TMP and IRRES.BAK. Its blocks are 4096 bytes; it retains one physical line and one token. Input and output extent are independent. It does not hold a whole assembly result or inherit an 8192-byte target ceiling. ASM86 separately checks its genuine single-segment image and symbol limits.

## The native handoff

IW23.ASM is identical to IRWIDE.ASM. Preserve its executable as IRWIDE.COM and IWKEEP.COM. It builds the IR-written compiler seed used in the RILL collection. IWKEEP has no filename prompt:

```dos
COPY PROGRAM.IR SOURCE.IR
CHECK IWKEEP
```

Require OK and PASS before copying RESULT.ASM to SOURCE.ASM and invoking ASMAKEEP. The completed RILL-written IR86 uses this same fixed-file interface. Keep the native bridge as a separately named, reproducible builder.

## Disk and recovery

Use a hard-disk work directory with room for sources, generated IR and assembly, preserved executables, and recovery files. The saved course need not fit one floppy. Use plain ASCII and DOS line endings; a word processor must not add formatting.

A pre-existing temporary or backup name prevents a completed translator from starting. Inspect or rename it before proceeding. Source rejection leaves the accepted result unchanged. Publication is a checked rename sequence, with recovery files retained if restoration fails; it is not atomic replacement. Require a fresh OK and immediate PASS before using output.

Use the unchanged VIEW.BAS for both length and hexadecimal bytes, and CHECK.BAT for immediate executable status. DOS echo and the checker's separating blank line are not part of the tool's own report. A valid empty file is an inspection result, never a runnable program.
