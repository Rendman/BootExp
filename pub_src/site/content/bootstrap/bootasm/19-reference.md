+++
title = "BOOTASM reference"
weight = 19
description = "Every accepted form, its limits, and its encoding."
download = "BOOTASM.BAS"
+++

This reference describes the completed `BOOTASM.BAS`. Earlier checkpoints accept only the features introduced by their construction installments.

## Files and invocation

At DOS run `GWBASIC BOOTASM.BAS`. At the source prompt enter a base name of one through eight letters, digits, or underscores, without path or extension. The assembler reads `name.ASM` twice and writes `name.COM` after both passes succeed. The files are in the current work directory. Use ordinary disk filenames; the character check does not reject DOS device names such as CON or NUL. Device names are excluded from the workbench to keep this small validator simple.

`OK name.COM n bytes` reports success and the exact byte count. `ERROR line n : diagnostic` reports a rejected source line. BASIC may insert additional spaces around numeric values. `BASIC error n at m` reports an interpreter or file error at BASIC line m. Assembly errors leave existing output untouched. A file error during the final write may leave incomplete output. Always require a fresh OK report.

The assembler finishes at the BASIC `Ok` prompt; use `SYSTEM` before running a DOS program. Assembly failures do not supply a dependable DOS return code. Observe the printed report, rather than using CHECK.BAT to judge BASIC itself.

## Source spelling

- One instruction or directive per line. Empty lines and comment-only lines are allowed.
- A semicolon starts a comment. Tabs are treated as spaces. Letter case is ignored.
- A label definition occupies a line by itself: `NAME:`. It names the next byte's loaded offset, including the 0100H origin. Labels do not emit bytes.
- Names contain one through sixteen letters, digits, or underscores, starting with a letter or underscore. Register names are reserved. Duplicate definitions are errors. Several different names may refer to the same position.
- Numbers are unsigned decimal, or hexadecimal with an `H` suffix. A number must start with a decimal digit: `0FFH`, not `FFH`. Values range from 0 through 65,535.
- A value is one number or one label. Forward references are allowed. No signs, expressions, character literals, quoted strings, EQU, ORG, END, INCLUDE, macros, or segment directives are accepted. DOS supplies the fixed 0100H origin.
- Commas separate operands and data items. Operand spaces are ignored by the small parser; keep each name or number together for clarity.

DB takes one or more byte values separated by commas. DW takes one or more word values. Words are stored low byte first. A named address may be used in DW or an immediate word operand. DB rejects values above 255, including labels whose address does not fit in a byte. No alignment or padding is inserted.

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

The CPU's other addressing forms and segment overrides are outside this assembler's syntax. Use BX or a direct offset and explicit register arithmetic. The accepted memory forms belong only to MOV; arithmetic with memory operands and immediate-to-memory MOV are omitted to keep operand parsing small.

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

### The BASIC routines

| Entry | Inputs | Outputs and state changed |
|---|---|---|
| 1000 | Raw line S$ | Cleaned S$; I, C |
| 2000 | Value text T$ | N; Q$, BA, NI, D; for labels also the 2200 scratch state |
| 2200 | Label text T$, PS | N; validator and lookup scratch state |
| 3000 | Byte X, PS, P | Advances P; writes B%(P) only on pass two; preserves N |
| 3100 | Word N | Emits low and high bytes; changes X and P; preserves N |
| 4000 | M$, A$ | Dispatches one source statement; effects of selected routine |
| 4100 | A$, M$ | Emits DB/DW items; DA$, DI, DW, T$, numeric scratch, X, P |
| 4200 / 4300 | MOV operands | RD, WD, register and numeric scratch, emitted bytes |
| 4390 / 4400 / 4500 | Arithmetic mnemonic match and operands | OP, RD, WD, register and numeric scratch, emitted bytes |
| 4600 / 4700 | MOV memory operands, saved register state | RM, MA, N, T$, numeric scratch, X, P |
| 4800 | Bracketed operand T$ | RM, MA; T$, numeric scratch; preserves RD and WD |
| 4900 | Fixed opcode X, A$ | Rejects an extra operand or emits X |
| 5000 | A$ | A1$, A2$, I |
| 5100 | INT argument A$ | Value-reader scratch, X, P |
| 5200 | Single register A$, M$ | T$, R, W, RI, X, P |
| 5500 | Near-transfer argument A$, M$ | Value-reader scratch, RV, N, X, P |
| 5600 | Short-branch argument A$, BC | Value-reader scratch, RV, C$, X, P |
| 6000 | Register text T$ | R (or -1), W if matched, RI |
| 7000 | Label T$, PS, P | Enters SY$/SV in pass one; SC and validator/lookup scratch |
| 7100 | Label text T$ | Validates; K, C$, register-reader scratch; preserves T$ |
| 7200 | T$, SC, SY$ | SI (or -1), K |
| 8000 | Filename F$ | Validates; FI, FC$, C$ |
| 9000 / 9500 | Assembly diagnostic E$ or BASIC ERR/ERL | Reports, closes files, and ends the program |

Variables are shared BASIC program state. Callers save values which their callees may change: RD and WD preserve a destination while another operand is read; DA$ and DI preserve a data list while the number reader scans an item. The dispatcher is called through GOSUB, so its selected subroutine returns before the main source loop continues. None of these routines recursively calls itself.

## Capacity and storage

| Item | Limit or requirement | Reason |
|---|---|---|
| Output image | 4,096 bytes | Bounds the BASIC byte array and keeps initial programs small |
| Byte-array storage | 8,192 bytes | One BASIC integer per output byte |
| Labels | 128, each at most 16 characters | Bounds the symbol arrays and string storage |
| Symbol values | 128 ordinary BASIC numeric entries, 512 bytes | Addresses use nonnegative values; no signed-integer address conversion |
| Source lines | 2,000 | Bounds work per pass and gives a clear diagnostic |
| Source line width | 120 characters before normalization | Limits the line a reader must enter and inspect |
| Numeric values | 0 through 65,535 | An unsigned word; byte contexts impose 255 |
| Image origin | 0100H | Fixed DOS `.COM` load offset |
| Image address range at full size | 0100H through 10FFH | 4,096 loaded bytes; an end label may name 1100H |
| BASIC working space | Use the normal roughly 60 KB BASIC workspace | Source, strings, symbol entries, arrays, and BASIC's own runtime share it |
| BASIC subroutine nesting | At most eight active GOSUB calls in this implementation | Fixed, shallow call paths; no recursive parsing |
| Executable stack | Near CALL and each PUSH consume two bytes | The program must balance returns and saved words; nested calls add their demands |

The 640 KB installed in the PC does not give GW-BASIC a 640 KB program workspace. Its program-and-data area is much smaller. BOOTASM streams the source twice instead of retaining it, and buffers only the bounded output. It uses neither a heap in the assembled programs nor a separate object format.

The emitted program shares one segment for code, data, and stack. DOS initializes the segment registers to its program segment and supplies a stack near the top of available space; its precise position depends on the memory granted to the program. The examples leave SS and SP alone. BOOTASM checks its file-size bound, not a program's runtime memory accesses or stack depth. Reserve any working data in the source, keep stack usage modest, and do not write into the PSP or outside the program's allocated storage.

An empty source is accepted as a zero-byte output for inspection. It is not a runnable `.COM` program. Bytes emitted by DB and DW are not checked for safe execution.

## Diagnostics

| Diagnostic | What to check |
|---|---|
| Bad filename | Base name length and permitted characters |
| Too many source lines / Source line too long | The physical input limits, including comments |
| Missing value / Bad number / Number too large | An absent item, malformed digits, or a value above 65,535 |
| Byte out of range | A byte operand above 255 |
| Unknown instruction | Spelling or an unsupported instruction/directive |
| Unexpected operand | An argument after a fixed instruction |
| Two operands required | Missing, misplaced, or extra comma |
| Register required / Word register required | The accepted register forms |
| Register sizes differ | A byte register paired with a word register |
| Bad label / Reserved label | Name spelling or use of a register name |
| Duplicate label / Undefined label | Repeated definition or missing definition |
| Too many labels | The 128-entry table is full |
| Bad memory operand | Missing closing bracket; other malformed offsets may report Bad label or Bad number |
| Branch out of range | A conditional target outside -128 through +127 bytes from the following instruction |
| Program too large | Output exceeds 4,096 bytes |

## Printed references

For the processor's register layout, instruction encodings, and flag definitions, consult Intel Corporation, *The 8086 Family User's Manual*, October 1979, Chapter 2, especially the instruction-set descriptions and encoding tables. It describes the full processor; BOOTASM accepts only the forms listed here.

For BASIC file records, consult the GW-BASIC reference manual supplied with the interpreter, entries for OPEN, CLOSE, FIELD, LSET, PUT, GET, LOF, KILL, and ON ERROR. For DOS console output and termination, consult the MS-DOS 3.10 programmer's reference supplied for the machine, INT 21H functions 02H, 09H, and 4CH. Check the printing date and interpreter version of the manuals on your workbench.
