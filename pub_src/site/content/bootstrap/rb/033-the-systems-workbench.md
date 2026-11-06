+++
title = "The RILLBOOT compiler-seed workbench"
weight = 0
description = "Construct the systems-language compiler in IR86 and preserve it as RILLBOOT."
download = "RILLBOOT.ZIP"
download_group = "tools/rillboot"
aliases = ["/bootstrap/rill/033-the-systems-workbench/"]
reader_names = 1
+++

RILL is a rung of a working bootstrap ladder. The first compiler construction establishes scanning, emitted IR, variables, and structured control. This workbench adds the procedures, local state, storage, and portable services needed to write the assembler, IR translator, and compiler in RILL itself.

Begin with the completed streaming IR workbench: IWKEEP.COM is the fixed-file native translator, and ASMAKEEP.COM is the tested native ASM86. Their sources remain available. No outside compiler, assembler, linker, or supplied executable participates in these builds.

## The compiler seed in IR

RB01 begins with an executable formatting diagnostic. The RILLBOOT stopping points add character reading, complete spellings, symbol records, streamed output, expression parsing, lexical scopes, arguments, statements, and procedure definitions. The complete source is RILLBOOT.IR, identical to RB47.IR.

Build each seed checkpoint through the preceding project tools:

```dos
COPY RB01.IR SOURCE.IR
CHECK IWKEEP
COPY RESULT.ASM SOURCE.ASM
CHECK ASMAKEEP
COPY RESULT.COM RB01.COM
```

Require each stated OK and PASS **before** the next copy. Keep source and executable together. Early helpers may emit an IR fragment into RILL.TMP. TYPE and VIEW inspect that text; it is not a complete output program. Delete a deliberately created diagnostic temporary file after inspection. Use a fresh work directory for the diagnostic exercises and inspect any pre-existing recovery names first.

After RB47 passes, preserve RB47.COM as RILLBOOT.COM. This is an IR-written compiler, built with the native translator and assembler. It accepts the complete language used to implement the three tools.

## Handoff to RILL

Work through the complete programs after the seed reference. They introduce the language used to write the tools: word expressions, arguments, recursion, scopes, byte storage, strings, and opaque block/file services. Save the tested RILLBOOT.COM and RILLBOOT.IR separately.

The [RILL collection](../../rc/index.html) starts a compiler written in this language. RILLBOOT is its builder; its source is retained rather than replaced by an unexplained executable.

## Storage and service conventions

Words wrap at sixteen bits. Names are compared in folded ASCII case. Local variables and parameters live in an individual procedure call; global byte buffers have stable addresses. A pointer to a local must not outlive its frame. Ordinary pointer arithmetic and byte indexing are unchecked. This is a bounded systems language, without ownership checking or a memory-safety claim.

Allocated blocks use opaque handles and checked byte offsets. File handles are also opaque and carry their access mode. Neither value is a processor register, segment, or DOS descriptor. STATUS is persistent and must be checked immediately after a service when failure matters.

## Publication

The compiler reads SOURCE.RIL and streams RILL.TMP. Full acceptance, source close, final flush, and output close precede publication as RESULT.IR, with RILL.BAK retaining the previous result during the rename sequence. Existing recovery names prevent a full compiler run. Source rejection preserves the previous result; failed publication can require manual recovery.

Preserve every known working builder under its own short name. Use the same DOS 3.10 and period BASIC workbench, the unchanged CHECK.BAT, and VIEW.BAS.
