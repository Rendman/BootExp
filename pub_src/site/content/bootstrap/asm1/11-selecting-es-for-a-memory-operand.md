+++
title = "17 \u00b7 Selecting ES for a memory operand"
weight = 17
description = "Emit a segment prefix on the existing memory forms."
download = "A11.ASM"
aliases = ["/bootstrap/asm86a/11-selecting-es-for-a-memory-operand/"]
download_group = "tools/asm1"
reader_names = 1
url = "/bootstrap/asma0/11-selecting-es-for-a-memory-operand/"
+++

Selecting a segment register is only part of addressing storage elsewhere. A memory instruction must also use that segment. I'll add the explicit `ES:` spelling and follow the extra prefix byte into the output, keeping the ordinary offset and width rules in place.

## The working parts

SEGOPERAND distinguishes a standalone segment register from ES: followed by a memory operand. It saves and restores the source cursor when a colon is absent. PREFIX belongs to the current operand; P1 saves it for the first operand.

LOADMEM and STOREMEM emit prefix 26H before the ordinary MOV encoding. An ES override changes the selected memory segment, not the offset or operand width. At this seed stopping point only ES is accepted as a memory override.

## Enter the source

Copy `A10.ASM` to `A11.ASM`. Apply the changes in the order shown, working upward through the old source. Use Find to locate each label, including its colon, and confirm that it stands alone on a source line. The locator blocks are existing source: leave them in place and type only the stated insertion or replacement. Blank lines and comment-only lines may differ in your copy.

### Change 1 · `SEGREGISTER:`

Find the unique label `SEGREGISTER:`. Insert the new source immediately before this existing label:

```asm
SEGREGISTER:
```

Insert:

```asm
SEGES:
CALL SCAN
MOV AL,[4080H]
CMP AL,91
JE SEGMEMORY
JMP TWOBAD
SEGMEMORY:
CALL MEMORY
MOV AL,38
MOV [PREFIX],AL
RET
```

### Change 2 · `SEGOPERAND:`

Find the unique label `SEGOPERAND:`, then follow this unchanged source through its last displayed instruction:

```asm
SEGOPERAND:
MOV [SEGCODE],AX
PUSH SI
CALL SCAN
MOV AL,[4080H]
CMP AL,58
JNE SEGREGISTER
POP AX
```

The edit begins immediately after that unchanged block.

Insert:

```asm
MOV AX,[SEGCODE]
CMP AX,16
JE SEGES
```

## Build the stopping point

Copy `A11.ASM` to `SOURCE.ASM`, run `CHECK ASMKEEP`, and require `OK 03740 bytes` and PASS. This uses the preceding published ASM0, not the new checkpoint. Preserve the accepted executable with `COPY RESULT.COM A11.COM`.

VIEW.BAS must report A11.COM length 3740 bytes. Keep that executable and source together.

## Acceptance check

Create T11.ASM as plain ASCII with COPY CON or an editor. Finish COPY CON with Ctrl-Z and Enter:

```asm
MOV AX,ES:[BX]
MOV AX,[BX]
MOV ES:[1234H],DX
MOV [1234H],DX
MOV AL,ES:[1234H]
MOV ES:[BX],AL
```

```dos
CHECK A11 T11.ASM RESULT.COM
```

Require:

```text
OK RESULT.COM 00022 bytes
PASS
```

In VIEW.BAS, inspect RESULT.COM. Require length **22 bytes** and these complete contents:

```text
26 8B 07 8B 07 26 89 16 34 12 89 16 34 12 26 8A 06 34 12 26 88 07
```

Read the result in the groups below. The ES accesses begin with 26H. The ordinary load immediately after the first ES load must begin with 8BH, and the ordinary store after the ES store must begin with 89H. Neither may inherit 26H. The last two instructions also check byte width and the opposite direct/BX address choices.

| Source instruction | Emitted bytes |
|---|---|
| `MOV AX,ES:[BX]` | `26 8B 07` |
| `MOV AX,[BX]` | `8B 07` |
| `MOV ES:[1234H],DX` | `26 89 16 34 12` |
| `MOV [1234H],DX` | `89 16 34 12` |
| `MOV AL,ES:[1234H]` | `26 8A 06 34 12` |
| `MOV ES:[BX],AL` | `26 88 07` |

This fixture is an encoding fragment, not a complete DOS program. Inspect its bytes; do not run RESULT.COM.

## A rejection check

Create X11.ASM with this separate source:

```asm
MOV AX,DS:[BX]
```

```dos
CHECK A11 X11.ASM RESULT.COM
```

Require:

```text
ERROR 00001 CODE 1
FAIL
```

The accepted RESULT.COM must remain unchanged. Keep a copy and compare it with C:\DOS\FC.EXE /B if in doubt. Require a fresh OK before using any output.

DS is a valid segment-register operand, but DS: is not an accepted memory override in this seed. Then replace X11.ASM with each unsupported override below, one at a time, and rerun the same command. Each must report ERROR 00001 CODE 1 and FAIL, preserving the accepted result.

```asm
MOV AX,CS:[BX]
```

```asm
MOV AX,SS:[BX]
```

An unexpected PASS fails this rejection test.

## If the result differs

Check SEGOPERAND's saved cursor and ES-only selector, PREFIX for the current operand, and P1 for the first operand. OPERAND must clear PREFIX on each new operand; a store must use saved P1. A spare 26H on an ordinary access reveals a prefix that was not cleared.
