+++
title = "17 \u00b7 Reserving a byte buffer"
weight = 17
description = "Emit bounded, zero-filled storage without a string syntax."
download = "IR17.ASM"
+++

BUFFER names a run of consecutive bytes which pointer operations can traverse.

## How it works

BUFFER takes a name and a count from one through 256. NUMV retains that count. ZEROBUFFER first expands the name definition, then emits DB rows of at most sixteen zero values. CX counts bytes still required and BP counts the current row. OUTTEXT and EMITCHAR preserve those counters.

Grouping the zeroes keeps each assembly line short and avoids spending one source line per byte. The final row may be partial. Each row ends with CR/LF, and no extra alignment byte is inserted.

The count is deliberately bounded so a declaration remains easy to inspect. Larger working areas can be addressed explicitly within the allocated segment, but that requires a memory plan; BUFFER itself reserves bytes in the emitted image. The test crosses a row boundary and fetches its initial zero byte.

## Source changes

Copy `IR16.ASM` to `IR17.ASM`. Make these edits **from the bottom of the old file upward**, in the order printed. Physical line positions count blank lines and are only locators. The nearby label and unchanged context identify each place; retain everything else.

### Change 1: following `T_PUTB:`

Unchanged code immediately before the edit:

```asm
T_PUTB:
DB 80,79,80,32,66,88,13,10,77,79,86,32,91,66,88,93
DB 44,65,76,13,10,0
```

Insert after old physical line 986, before the following old line.

Insert this source:

```asm

T_BUFFER:
DB 0
```

### Change 2: following `T_NOP:`

Unchanged code immediately before the edit:

```asm

T_NOP:
DB 78,79,80,13,10,0
```

Remove these exact old lines (physical positions 912–914 in `IR16.ASM`):

```asm

T_LABEL:
DB 85,95,64,58,13,10,0
```

No replacement source is needed.

### Change 3: following `T_HALT:`

Unchanged code immediately before the edit:

```asm
DB 77,79,86,32,65,88,44,52,67,48,48,72,13,10,73,78
DB 84,32,50,49,72,13,10,0

```

Insert after old physical line 909, before the following old line.

Insert this source:

```asm
T_LABEL:
DB 85,95,64,58,13,10,0

```

### Change 4: following `LAST:`

Unchanged code immediately before the edit:

```asm
LAST:
DB 0

```

Insert after old physical line 898, before the following old line.

Insert this source:

```asm
ZEROSTART:
DB 68,66,32,48,0

ZERONEXT:
DB 44,48,0

```

### Change 5: following `SPACE:`

Unchanged code immediately before the edit:

```asm
SPACE:
DB 32,36

```

Insert after old physical line 874, before the following old line.

Insert this source:

```asm
CRLF:
DB 13,10,0

```

### Change 6: following `OPTAB:`

Unchanged code immediately before the edit:

```asm
DW T_PUT
DB 80,85,84,66,0,0,0,0,0,2,3,0
DW T_PUTB
```

Insert after old physical line 808, before the following old line.

Insert this source:

```asm
DB 66,85,70,70,69,82,0,0,6,0,0,0
DW T_BUFFER
```

### Change 7: following `STACKBAD:`

Unchanged code immediately before the edit:

```asm
MOV AX,4
JMP ERROR

```

Insert after old physical line 752, before the following old line.

Insert this source:

```asm
ZEROBUFFER:
MOV SI,T_LABEL
CALL EXPAND
MOV CX,[NUMV]
ZEROLINE:
MOV SI,ZEROSTART
CALL OUTTEXT
MOV BP,1
ZEROMORE:
DEC CX
JE ZEROEND
CMP BP,16
JE ZEROBREAK
MOV SI,ZERONEXT
CALL OUTTEXT
INC BP
JMP ZEROMORE
ZEROBREAK:
MOV SI,CRLF
CALL OUTTEXT
JMP ZEROLINE
ZEROEND:
MOV SI,CRLF
CALL OUTTEXT
RET

```

### Change 8: following `ARGNAME:`

Unchanged code immediately before the edit:

```asm
CMP AX,255
JBE ARGDONE
JMP ARGRANGE
```

Insert after old physical line 661, before the following old line.

Insert this source:

```asm
ARGBUFFER:
CMP AL,6
JNE ARGDONE
MOV AX,[NUMV]
CMP AX,1
JB ARGRANGE
CMP AX,256
JA ARGRANGE
```

### Change 9: following `ARGNAME:`

Unchanged code immediately before the edit:

```asm
CALL NUMARG
MOV AL,[CLASS]
CMP AL,4
```

Remove these exact old lines (physical positions 657–657 in `IR16.ASM`):

```asm
JNE ARGDONE
```

Put this source in their place:

```asm
JNE ARGBUFFER
```

### Change 10: following `STATLAST:`

Unchanged code immediately before the edit:

```asm
CALL FINISH
CALL CONTEXT
CALL FLOW
```

Insert after old physical line 515, before the following old line.

Insert this source:

```asm
MOV AL,[CLASS]
CMP AL,6
JNE STATORDINARY
CALL ZEROBUFFER
RET
STATORDINARY:
```

### Change 11: following `STATWORD:`

Unchanged code immediately before the edit:

```asm
RET
STATWORD:
MOV BX,OPTAB
```

Remove these exact old lines (physical positions 485–485 in `IR16.ASM`):

```asm
MOV CX,23
```

Put this source in their place:

```asm
MOV CX,24
```

## Build the checkpoint

```dos
CHECK ASMKEEP
```

Enter `IR17` at ASM86's `Source name:` prompt. Require `OK 02628 bytes` followed by PASS. This builds `IR17.COM` directly with the completed assembler. Save the source and executable before running the test.

Create `T17.IR` with `COPY CON T17.IR`, enter this text, and finish with Ctrl-Z and Enter. The Ctrl-Z keystroke ends console input; it is not a printed language token.

```ir
BUFFER DATA 17
LABEL MAIN
ADDR DATA
FETCHB
EXIT
```

```dos
CHECK IR17
```

Enter `T17` at `IR source name:`. Apart from DOS echo and the checker's separating blank line, require:

```text
IR source name: T17
OK T17.ASM 00207 text bytes
PASS
```

Run `TYPE T17.ASM`. Its complete text must be:

```asm
CLD
CMP SP,0FFFEH
JE I_ENTRY
MOV AX,4C07H
INT 21H
I_ENTRY:
JMP U_MAIN
U_DATA:
DB 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
DB 0
U_MAIN:
MOV AX,U_DATA
MOV BX,AX
MOV AL,[BX]
MOV AH,0
MOV AH,4CH
INT 21H
```

Assemble that generated source with `CHECK ASMKEEP`, entering `T17`. Require `OK 00045 bytes` and PASS. The text-byte count above includes CR/LF and is distinct from this machine-image count.

Run `GWBASIC VIEW.BAS`, enter `T17.COM`, and require length **45 bytes** with these hexadecimal bytes. Use `SYSTEM` afterward to return to DOS.

```text
FC 81 FC FE FF 74 05 B8 07 4C CD 21 E9 11 00 00
00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
B8 0F 01 8B D8 8A 07 B4 00 B4 4C CD 21
```

`T17.COM` is a complete program. Run `CHECK T17`. It returns zero and the checker reports PASS.

## A rejection check

Enter this separate input as `X17.IR` using COPY CON and the same end-of-input keystroke:

```ir
BUFFER DATA 0
LABEL MAIN
HALT
```

Run `CHECK IR17` and enter `X17`. Require this diagnostic and FAIL:

```text
IR ERROR 00001 CODE 4
FAIL
```

An unexpected PASS is a failed rejection test. Require a fresh OK before using assembly output; a source error leaves an older .ASM untouched.

## If the result differs

Check the table effect and target-size fields separately. A saved expression word must be consumed before a label or control boundary. Compare the generated source and its byte count before executing the target.
