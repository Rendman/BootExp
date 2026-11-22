+++
title = "05 \u00b7 Naming the Result in the Report"
weight = 5
description = "Print the selected result through a small zero-terminated string routine."
download = "A01E.ASM"
download_group = "tools/asm1"
reader_names = 1
command_examples = "literal"
url = "/bootstrap/asma0/01e-reporting-the-result-name/"
+++

The assembler can write the selected file, but its success line still leaves me to remember which name I supplied. I want that line to identify the result I should inspect.

**Starting source:** `A01D.ASM`. **Save as:** `A01E.ASM`. **Build with:** `ASMKEEP.COM`.

## What this step adds

CMDTEXT prints a zero-terminated string addressed by SI. LODSB fetches each byte; zero returns to the caller. Each other byte goes through DL to DOS function 2. SI advances, AX and DX are scratch, and CLD at startup supplies the forward direction.

The existing TEXT routine prints dollar-terminated messages with DOS function 9. A filename buffer is zero-terminated instead, so passing it to TEXT would use the wrong stopping rule. CMDTEXT handles that representation directly without changing the message routines.

After WRITEOUT has successfully written and closed the output, it prints OKMSG, calls CMDTEXT with RESNAME, prints one space, then uses the existing NUMBER and BYTEMSG routines. The success line becomes OK, the chosen result name, and the byte count. A failed write or close still takes FILEBAD and cannot print a success line.

This changes the report, not the selected file, instruction language, or emitted program bytes. The fixture below includes zero, Control-Z and a high byte as data so its entire result is checked as bytes.


## Enter the source

Copy A01D.ASM to A01E.ASM. Apply the changes in the order shown, working upward through the old source. Use Find to locate each label, including its colon, and confirm that it stands alone on a source line. The locator blocks are existing source: leave them in place and type only the stated insertion or replacement. Blank lines and comment-only lines may differ in your copy.

### Change 1 · `OKMSG:`

Find the unique label `OKMSG:`. Insert the new source immediately before this existing label:

```asm
OKMSG:
```

Insert:

```asm
CMDTEXT:
LODSB
CMP AL,0
JE CMDTEXTEND
MOV DL,AL
MOV AH,2
INT 21H
JMP CMDTEXT
CMDTEXTEND:
RET
```

### Change 2 · `ZWRITEOUT4:`

Find the unique label `ZWRITEOUT4:`, then follow this unchanged source through its last displayed instruction:

```asm
ZWRITEOUT4:
MOV DX,OKMSG
CALL TEXT
```

The edit begins immediately after that unchanged block.

Insert:

```asm
MOV SI,RESNAME
CALL CMDTEXT
MOV DL,32
MOV AH,2
INT 21H
```

## Build this stopping point

```dos
COPY A01E.ASM SOURCE.ASM
CHECK ASMKEEP
COPY RESULT.COM A01E.COM
```

Require the preceding ASM0 to report `OK 02918 bytes` and CHECK to report PASS before preserving the result. Keep the source and executable together.

## Check the addition

Create T01E.ASM:

```asm
DB 65,0,26,255
```

```dos
CHECK A01E T01E.ASM REPORT.COM
```

Require:

```text
OK REPORT.COM 00004 bytes
PASS
```

VIEW.BAS must show REPORT.COM length 4 bytes and these complete contents:

```text
41 00 1A FF
```

The file is an encoding check; inspect it rather than executing it.

Continue with [Remembering an Open Input File](../01f-remembering-an-open-input/index.html).
