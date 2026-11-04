+++
title = "ASM86 reference"
weight = 31
description = "The native assembler's source grammar, byte encodings, memory contract, and diagnostics."
download = "ASM86.ASM"
+++

This reference describes the completed AS29/ASM86 source. Earlier construction checkpoints accept only their introduced features. ASM86 is implemented using BOOTASM's assembly language and accepts the forms below; it is not a complete 8086 assembler.

## Files and invocation

Run `CHECK ASM86` and enter a base name of one through eight letters, digits, or underscores when `Source name:` appears. Supply no extension or path. ASM86 uppercases the name, reads `NAME.ASM` twice from the current directory, and creates `NAME.COM` only after both passes succeed. Use ordinary disk filenames; DOS device names, including CON and NUL, are excluded from the workbench because the small character validator does not recognize devices.

A successful assembly prints `OK nnnnn bytes` and returns DOS status zero; CHECK prints PASS. The count is always five decimal digits. A failure prints `ERROR nnnnn CODE n` and returns status one; CHECK prints FAIL. The first number is the physical source line, starting at one, or zero before source reading begins. Observe the status immediately; another program may replace it.

A source rejection leaves existing output unchanged. An input/output error during the final create, write, or close can leave an empty or partial file. Only a fresh OK report authorizes use of that output. An empty source creates a zero-byte file for inspection, never execution. ASM86 does not judge whether bytes defined by DB or DW form a safe program.

## Source grammar

- Each line is empty, a comment, one standalone label definition, or one instruction/directive. A label may have spaces before its colon and a comment afterward; it cannot share a line with an instruction.
- A semicolon starts a comment. Letter case is ignored, tabs become spaces, and other printable ASCII characters are retained for parsing. CR/LF is the normal line ending; bare CR, bare LF, a final line without a newline, and Control-Z end-of-input are also recognized.
- Names contain one through sixteen letters, digits, or underscores, starting with a letter or underscore. Register names are reserved. Definitions are unique, case independently; different names may denote the same offset. A definition names the next byte's loaded offset, including the 0100H origin, and emits no bytes.
- Values are one unsigned decimal number, one hexadecimal number ending in H, or one label. Numeric spelling begins with a decimal digit: use `0FFH`, not `FFH`. Numeric values range from zero through 65535. Forward labels are resolved on pass two.
- Commas separate operands and data items. Spaces may surround tokens, commas, and brackets, but may not split a number or name. Unlike BOOTASM's operand cleanup, this token reader does not join separated characters.
- There are no signs, arithmetic expressions, quoted strings, character constants, EQU, ORG, END, INCLUDE, macros, segment directives, or object files. These would require more parsing and representations than this small construction uses. DOS supplies the 0100H origin.

DB requires one or more byte values separated by commas. DW requires one or more word values. A byte must fit zero through 255; a word fits zero through 65535 and is stored low byte first. No alignment or padding is inserted. A named loaded address fits a word; DB rejects a label address above 255 on pass two.

## Registers and memory

| Encoding number | Byte register | Word register |
|---|---|---|
| 0 | AL | AX |
| 1 | CL | CX |
| 2 | DL | DX |
| 3 | BL | BX |
| 4 | AH | SP |
| 5 | CH | BP |
| 6 | DH | SI |
| 7 | BH | DI |

For a register operand, its name determines the width. Both registers in a two-register instruction must have the same width. An immediate must fit the destination: no silent truncation is performed.

The only memory forms are `[BX]` and `[value]`, where value is a number or a label. Memory uses DS. `[BX]` uses the offset in BX; `[TEXT]` uses the offset named TEXT. A register supplies the transfer width. An instruction reading or writing a word accesses two consecutive bytes, so the program must provide storage for both.

The CPU's other addressing forms and segment overrides are outside ASM86's syntax. Use BX or a direct offset and explicit register arithmetic. The accepted memory forms belong only to MOV; arithmetic with memory operands and immediate-to-memory MOV are omitted to keep operand parsing small.

## Accepted instructions

Here `r8` is any byte register, `r16` any ordinary word register, `r` a register of either width, `imm` a value fitting that register, and `mem` one of the two memory forms. Every byte count below is fixed for the chosen form.

| Source form | Bytes | Effect or restriction |
|---|---|---|
| `MOV r8,imm` | 2 | Load a byte constant or value |
| `MOV r16,imm` | 3 | Load a word constant or address |
| `MOV r,r` | 2 | Copy equal-width registers |
| `MOV r,[BX]` / `MOV [BX],r` | 2 | Load or store at DS:BX |
| `MOV r,[value]` / `MOV [value],r` | 4 | Load or store at a direct DS offset |
| `ADD r,r` / `SUB r,r` / `CMP r,r` | 2 | Equal-width registers; CMP does not store the subtraction |
| `AND r,r` / `OR r,r` / `XOR r,r` | 2 | Equal-width bitwise operations |
| `ADD/SUB/CMP/AND/OR/XOR r8,imm` | 3 | Full byte immediate |
| `ADD/SUB/CMP/AND/OR/XOR r16,imm` | 4 | Full word immediate; no 83H shortening |
| `INC r16` / `DEC r16` | 1 | Change by one; carry flag preserved |
| `PUSH r16` / `POP r16` | 1 | Transfer a word through SS:SP |
| `INT value` | 2 | Interrupt number 0 through 255 |
| `CALL value` | 3 | Near relative call; pushes return offset |
| `JMP value` | 3 | Near relative jump |
| `JB/JAE/JE/JNE/JBE/JA value` | 2 | Short conditional branch, unsigned comparisons |
| `JL/JGE/JLE/JG value` | 2 | Short conditional branch, signed comparisons |
| `NOP` | 1 | 90H |
| `RET` | 1 | C3H; near return without an immediate |
| `CLD` | 1 | FCH; clear direction flag |
| `LODSB` | 1 | ACH; DS:SI to AL, then adjust SI |
| `STOSB` | 1 | AAH; AL to ES:DI, then adjust DI |

Slash-separated mnemonic names in this table denote alternatives, not literal source syntax. Write `ADD AX,1`, for example. No other instruction names or aliases are accepted. In particular, write JE and JNE rather than JZ and JNZ; use JB and JAE to test carry rather than JC and JNC.

### Encoding rules

For MOV immediate, use B0H plus the byte register number or B8H plus the word register number, followed by the immediate in the selected width.

For register-to-register MOV, use 8AH for bytes or 8BH for words. The ModR/M byte is `192 + 8*destination + source`. For memory loads use the same opcode; for stores use 88H or 89H. The memory ModR/M byte is `8*register + 7` for [BX], or `8*register + 6` followed by a word offset for a direct address.

The arithmetic group numbers are ADD=0, OR=1, AND=4, SUB=5, XOR=6, CMP=7. For a register source the opcode is `8*group + 2 + width`, where width is zero for byte or one for word. The ModR/M byte uses the same register rule as MOV. For immediate arithmetic the opcode is 80H or 81H and ModR/M is `192 + 8*group + destination`; the full-width immediate follows.

Near CALL is E8H and near JMP is E9H. Their displacement is `target - (instruction offset + 3)`, represented as a 16-bit word. Conditional branches subtract `instruction offset + 2` and require -128 through +127 in pass two. No branch relaxation occurs.

| Branch | Opcode | Flags required |
|---|---|---|
| JB | 72H | CF=1 |
| JAE | 73H | CF=0 |
| JE | 74H | ZF=1 |
| JNE | 75H | ZF=0 |
| JBE | 76H | CF=1 or ZF=1 |
| JA | 77H | CF=0 and ZF=0 |
| JL | 7CH | SF differs from OF |
| JGE | 7DH | SF equals OF |
| JLE | 7EH | ZF=1 or SF differs from OF |
| JG | 7FH | ZF=0 and SF equals OF |

CF is carry, ZF is zero, SF is sign, and OF is signed overflow. CMP sets the flags as though subtracting its source from its destination. The branch must test the intended flags before another instruction changes them. An out-of-range conditional transfer must be written explicitly as an opposite short condition around a near JMP.

## Native routine interfaces

The program retains DOS's common CS, DS, ES, and SS segment. CLD at entry establishes forward string operations. Flags are scratch state across routines unless a particular caller tests a DOS carry result immediately. There is no recursive parsing. Shared fields retain operand state while SCAN, LOOK, or VALUE changes working registers.

| Entry | Inputs and results | Scratch and preserved state |
|---|---|---|
| GETNAME | Console line to FNAME and EXTP | Working registers and flags; validates 1–8 characters |
| OPENFILE / CLOSEFILE | FNAME to HANDLE / HANDLE to DOS close | AX, BX, DX and DOS flags as used; failure does not return |
| NEXTBYTE | HANDLE to AX=count, CHAR=byte if count is one | AX, BX, CX, DX, flags; preserves SI, DI, BP |
| READLINE | HANDLE and reader fields to text at 2200H; AX=1 line or 0 EOF | Working registers, LINENO, ENDED, SKIPLF |
| SCAN | SI=line cursor to token at 2300H and TOKLEN | AX, DI, SI, flags; retains cursor at separator/end |
| LOOK | BX=table, CX=count, AX=stride to BX=record or zero | Preserves SI; other work registers and STRIDE are scratch |
| REGISTER | Current token to AX=0–15 or FFFFH | LOOK scratch; preserves source cursor SI |
| VALIDNAME | Current token to accepted spelling or code 3 | Preserves SI; AL and flags are scratch |
| VALUE | Current token to AX=unsigned word | Preserves SI; AX, BX, CX, DX, DI, BP and flags are scratch |
| SYMBOLVALUE / DEFINE | Token and PASS to address / stored or checked definition | LOOK and name-reader scratch; preserves line cursor |
| OPERAND / MEMORY | SI to KIND, WIDTH, REG, VAL | Parser work registers; KIND 1=register, 2=memory, 3=value |
| STATEMENT | SI=start of line to parsed and emitted statement | Parser and encoding state; TYPE and OP select handler |
| TWOOPERANDS | Operand text to encoded MOV or arithmetic | K1, W1, R1, V1 save the first operand; second uses KIND, WIDTH, REG, VAL |
| SAMEWIDTH | W1 and WIDTH to equal-width acceptance | AL, DL, flags |
| TIMES8 | AL to eight times AL modulo 256 | AL and flags only |
| BYTEVALUE / EMITWORD | AX to one checked byte / two bytes | EMITWORD preserves AX; changes output position |
| EMIT | AL to one counted byte, buffered only on pass two | Preserves AX and BX; changes flags, PC, OUTPTR |
| COPYZ | DS:SI zero string to ES:DI including its zero | AL, SI, DI, flags |
| TEXT | DS:DX dollar-terminated display string | AX and DOS flags |
| NUMBER | AX to five displayed decimal digits | Preserves all word registers; flags are scratch |
| ERROR | AX=code, LINENO=line to report and status one | Does not return; DOS closes process handles |

The instruction table has 31 eight-byte records: six zero-padded name bytes, a class byte, and a parameter byte. Classes are data=1, fixed=2, MOV=3, arithmetic=4, single-register=5, INT=6, near transfer=7, and short transfer=8. The register table has sixteen four-byte records: two name characters, zero, and a code. Word register codes have eight added; the low three bits are the CPU register encoding.

A symbol record occupies twenty bytes: up to sixteen name characters and a zero, padding through byte seventeen, then its loaded offset at bytes eighteen and nineteen. Pass one rejects duplicates and records addresses; pass two requires every definition to retain its address. Fixed-length encodings keep those addresses stable. Undefined references are provisional zeroes on pass one and errors on pass two. Byte-range and conditional-branch checks therefore cannot accept an unresolved final address.

## Resource and memory contract

| Item | Bound or requirement | Reason |
|---|---|---|
| Native output | 8,192 bytes, loaded at 0100H–20FFH | Fixed output buffer and reserved low image area |
| End label at full size | 2100H | Position after the last emitted byte |
| Physical source lines | 4,000 per pass | Bounds reading and the line report |
| Physical line width | 120 characters, including comments and tabs | Bounded line buffer; one extra byte holds zero |
| Tokens / names | 16 characters | Bounded token buffer and compact symbol records |
| Symbols | 256 records, 5,120 bytes | Fits 3000H–43FFH without a heap |
| Numeric value | 0–65535 | Unsigned word; byte contexts narrow it to 0–255 |
| Program memory | Full 64 KB segment, entry SP=FFFEH | Fixed buffers and a high stack; smaller allocations are rejected |
| Stack reservation | Upper 4 KB kept free; calls are shallow and nonrecursive | Keeps stack clear of all fixed buffers; each CALL/PUSH consumes two bytes |
| Source handles | One input at a time, reopened each pass | No source copy or seek state in memory |
| Output handles | One, after both source passes | Avoids replacing a good file for a source error |

The workbench guide gives the exact buffer map. These bounds belong to ASM86, not to the CPU. BOOTASM accepts 256 labels, at most 4,096 output bytes, and at most 2,000 source lines. The completed ASM86 source and image fit those bounds.

ASM86 checks emitted length, source bounds, symbol bounds, and its own entry stack. It does not check the assembled program's later memory accesses, stack depth, or DOS-call correctness. An emitted program shares code, data, and stack in one segment and must respect its own allocated storage. PUSH SP has the original 8086/8088 behavior: the pushed value reflects the decremented SP. Avoid treating it as an ordinary saved-register value.

## Error codes

| Code | Meaning and likely cause |
|---|---|
| 1 | Syntax: unknown instruction, punctuation, extra operand, token too long, wrong register width/class, or bad base name |
| 2 | Numeric spelling or overflow: malformed numeric digits or a value above 65535 |
| 3 | Symbol/value: malformed name, missing value, reserved register name, undefined reference, duplicate definition, or changed definition address |
| 4 | Range: byte above 255 or conditional displacement outside -128 through +127 |
| 5 | Capacity: image, symbol count, source-line count, or physical-line width exceeds its bound |
| 6 | File/text: DOS open/read/create/write/close failure, short write, or invalid source character |
| 7 | Memory: entry SP differs from FFFEH |

A token beginning with a digit follows numeric checks; another token follows name checks. Thus a signed literal such as -1 reports a symbol error, while 65536 reports a numeric error. The report identifies the class of failure rather than attempting to guess the intended source. Physical line numbers count blank and comment lines too.

## Printed references

Consult Intel Corporation, *The 8086 Family User's Manual*, October 1979, Chapter 2 and the instruction encoding tables. For the file and console interfaces consult the MS-DOS 3.10 programmer's reference supplied for the machine, INT 21H functions 02H, 09H, 0AH, 3CH, 3DH, 3EH, 3FH, 40H, and 4CH. Check the exact manual printing against your DOS distribution. Those manuals describe more facilities than this assembler accepts.
