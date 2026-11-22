+++
title = "06 \u00b7 Remembering an Open Input File"
weight = 6
description = "Distinguish a live input handle from a closed handle for the coming cleanup routine."
download = "A01F.ASM"
download_group = "tools/asm1"
reader_names = 1
command_examples = "literal"
url = "/bootstrap/asma0/01f-remembering-an-open-input/"
+++

A handle word keeps the number DOS returned. That number alone cannot tell a later cleanup routine whether the handle is still open. I give the input file its own small state flag.

**Starting source:** `A01E.ASM`. **Save as:** `A01F.ASM`. **Build with:** `ASMKEEP.COM`.

## What this step adds

INOPEN is one byte, initially zero. OPENFILE first checks that DOS function 3DH succeeded and saves the returned handle. Only then does it store one in INOPEN. A failed open leaves zero.

CLOSEFILE passes the saved handle to DOS function 3EH and checks carry. Only a successful close reaches INPUTCLOSED and stores zero. A failed close takes FILEBAD with the flag still set, rather than falsely recording that the file was closed. The handle word itself may still contain its old number after a close; INOPEN is what describes its lifetime.

This checkpoint records ownership state; it does not yet add cleanup, deletion or recovery behavior. The existing ERROR path still returns to DOS, which releases the process's handles. The flag records whether an explicit close is still needed, independently of the old number retained in HANDLE.

The new byte lives between BAKNAME and OUTPTR. OUTPTR still contains 6000H, and the complete-image output buffer remains in use. No opcode-table record is added here.


## Enter the source

Copy A01E.ASM to A01F.ASM. Apply the changes in the order shown, working upward through the old source. Use Find to locate each label, including its colon, and confirm that it stands alone on a source line. The locator blocks are existing source: leave them in place and type only the stated insertion or replacement. Blank lines and comment-only lines may differ in your copy.

### Change 1 · `OUTPTR:`

Find the unique label `OUTPTR:`. Insert the new source immediately before this existing label:

```asm
OUTPTR:
```

Insert:

```asm
INOPEN:
DB 0
```

### Change 2 · `INPUTCLOSED:`

Find the unique label `INPUTCLOSED:`, then follow this unchanged source through its last displayed instruction:

```asm
INPUTCLOSED:
```

The edit begins immediately after that unchanged block.

Insert:

```asm
MOV AL,0
MOV [INOPEN],AL
```

### Change 3 · `INPUTOPEN:`

Find the unique label `INPUTOPEN:`, then follow this unchanged source through its last displayed instruction:

```asm
INPUTOPEN:
MOV [HANDLE],AX
```

The edit begins immediately after that unchanged block.

Insert:

```asm
MOV AL,1
MOV [INOPEN],AL
```

## Build this stopping point

```dos
COPY A01F.ASM SOURCE.ASM
CHECK ASMKEEP
COPY RESULT.COM A01F.COM
```

Require the preceding ASM0 to report `OK 02931 bytes` and CHECK to report PASS before preserving the result. Keep the source and executable together.

## Check the addition

Create T01F.ASM:

```asm
RET
```

```dos
CHECK A01F T01F.ASM CLOSED.COM
```

Require:

```text
OK CLOSED.COM 00001 bytes
PASS
```

VIEW.BAS must show CLOSED.COM length 1 byte and these complete contents:

```text
C3
```

The file is an encoding check; inspect it rather than executing it.

The open-state flag is internal, so also inspect the bytes retained in A01F.COM. Count file offsets from zero; a COM file offset is its loaded offset minus 0100H. VIEW.BAS prints sixteen bytes on each complete row.

| File offset | Expected bytes | Meaning |
|---|---|---|
| 0088H | `B0 01 88 06 45 0C` | Load AL with one and store it in INOPEN |
| 009CH | `B0 00 88 06 45 0C` | Load AL with zero and store it in INOPEN |

In both stores, the final two bytes are the low and high bytes of INOPEN's loaded address, 0C45H. These are the assembler's own retained instructions, not a temporary printing routine.

Continue with [Adding XOR to the Arithmetic Table](../01-fixed-work-files/index.html).
