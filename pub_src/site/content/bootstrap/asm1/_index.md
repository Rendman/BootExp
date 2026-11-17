+++
title = "Building a Streaming Assembler"
weight = 3
description = "A streaming seed built by ASM0 and proved by self-assembly."
cover = true
download = "ASM1.ASM"
download_group = "tools/asm1"
reader_names = 1
tool_id = "ASM1"
collection_key = "asma0"
url = "/bootstrap/asma0/"
+++

ASM0 has made its own working copy. I can build an assembler without returning to BASIC, but I still have to work within the room I gave it. Every output byte waits in memory until assembly is finished, and there is space for only 256 labels. I open the notebook to the memory sketch: making another tool will mean deciding what really needs to stay there.

I'll call this next assembler **ASM1**. I want it to read and write through small blocks, keeping the source and the growing executable on disk. The space freed from the old output buffer can hold more names. ASM0 will build the first copy, and I will ask ASM1 to reproduce that copy before trusting it as a builder.

**BOOTASM → ASM0 → ASM1 → ASM86 → IR86 → RILL0 → RILLBOOT → RILL.** ASM1 is the streaming seed in this bootstrap ladder. It provides the file handling, symbol capacity and segment-access forms needed to construct ASM86.

## What we're adding

- **Command-line filenames:** Take input and output names from the PSP so sources can keep their own names; preserve the old names as no-argument defaults.
- **Streamed input and output:** Work through 1 KiB blocks so source and executable size are independent of the resident file buffers.
- **Larger assembly capacity:** Retain 2,048 symbols and emit as many as 61,184 bytes so the seed can build a substantially larger assembler.
- **XOR:** Add one arithmetic-table record so the successor assembler can hash symbol names; explain its spelling, dispatch class and operation selector in a separate step.
- **Segment access:** Add segment-register MOV and ES overrides on the existing MOV memory forms so the assembler can work with separately allocated storage.
- **Checked publication:** Write a temporary file and use backup/recovery names so rejected source does not replace an accepted RESULT.COM.

**Removing:** The complete-image output buffer; streaming removes the resident output-size bottleneck. SOURCE.ASM/RESULT.COM remain no-argument defaults; COPY is still needed when building with ASM0. ES, CS, SS and DS also become reserved names so labels cannot be confused with the new segment-register operands.

## The construction

This collection constructs a tool that can handle a source and output larger than its own resident image. Branch reach, filename storage, PSP reading, file selection, result reporting, input-handle state and XOR each receive a separate opening step. The construction then adds bounded input and output blocks, two passes, temporary-file ownership and recoverable publication. The completed seed has 2,048 symbols in its original segment and the segment-access forms needed to build ASM86.

Eighteen construction checkpoints finish at ASM1.ASM. A workbench guide, a seed language and memory reference, and three complete programs accompany them. The language remains small enough to be implemented within the preceding ASM0's bounds. The processor remains the 8086/8088 and the output remains DOS `.COM`.

The opening sequence keeps each change visible:

| Article | Saved source | Addition |
|---|---|---|
| 01 | A01A.ASM | Explicit conditional-branch bridges |
| 02 | A01B.ASM | Owned filename buffers and data layout |
| 03 | A01C.ASM | Bounded PSP name reader, checked with a status-only probe |
| 04 | A01D.ASM | Source/result selection and collision checks |
| 05 | A01E.ASM | The selected result name in the success report |
| 06 | A01F.ASM | Input-handle lifetime state |
| 07 | A01.ASM | XOR in the shared arithmetic table |

Begin with [Giving Conditional Branches Room](01a-reaching-error-handlers/index.html). Continue through A01F, then A01, before the block-reader article. A02 through A12 keep their saved filenames; their article numbers continue from 08 through 18.

Read the workbench first and preserve ASMKEEP.COM as the original fixed-file assembler. After the self-assembly comparisons, preserve ASM1.COM and its source. That verified source is the starting file of the separate [ASM86 collection](../asm86a/index.html), which adds allocated symbol pages and a broader language.

The complete source link above is ASM1.ASM. The [ASM1 disk sources](../../downloads/tools/asm1/ASM1.ZIP) include all eighteen checkpoints, acceptance and rejection inputs, the unchanged BASIC foundation and ASM0 source, the viewer and checker, and complete programs. No preassembled executable is included.
