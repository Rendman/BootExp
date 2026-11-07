+++
title = "13 \u00b7 ASM1 reference"
weight = 13
description = "The seed language, streaming files, single-segment symbol table, and handoff contract."
download = "ASM1.ASM"
download_group = "tools/asm1"
reader_names = 1
+++

ASM1 is the completed A12 streaming seed. Its first executable is built by the published ASM0; two self-assembly generations must reproduce it. The seed's own implementation uses only ASM0's accepted instructions. The language it accepts includes the segment-access forms below.

## Files and passes

COPY selects the input; the tool has no filename prompt:

```dos
COPY HELLO.ASM SOURCE.ASM
CHECK ASM1
```

Pass one reads and validates while recording definitions and counting output. Pass two closes and reopens the same source, checks label values and the final image length, resolves forward values, and streams ASMA.TMP. Keep SOURCE.ASM unchanged throughout both passes. The checks detect some changes, not every possible same-size edit.

The reader and writer each use a 1024-byte block. A short positive read is consumed and followed by another refill; zero means file EOF. A nonempty flush checks both DOS carry and actual progress. The final partial block and close must succeed before publication. The assembler retains neither the whole source nor the whole emitted image.

A pre-existing ASMA.TMP or RESULT.BAK prevents a completed seed run. After successful output close, an old RESULT.COM is renamed to RESULT.BAK; ASMA.TMP is renamed to RESULT.COM; then the backup is removed. Failed publication attempts restoration and retains recovery files when restoration fails. DOS rename is not atomic replacement. Inspect recovery files before renaming or deleting them.

Source rejection closes owned handles and removes only this run's temporary output, preserving the accepted result. Cleanup failures prevent OK and can print a recovery notice. Always require a fresh OK and PASS before using output.

## Source and values

Each physical line is empty, a semicolon comment, a standalone label ending in a colon, or one statement. A label cannot share its line with an instruction. Case is folded; tabs are whitespace. Normal CR/LF, bare CR or LF, a final unterminated line, and source Control-Z are accepted. The source is ordinary ASCII.

Names begin with a letter or underscore and continue with letters, digits, or underscores, up to sixteen characters. All ordinary and segment register names are reserved. Definitions are unique, and different names may have the same loaded address.

A value is one unsigned decimal literal, one hexadecimal literal ending in H, or a label. It is not an expression. Numeric spelling starts with a digit: write 0FFH rather than FFH. Numbers fit 0 through 65535; a byte context narrows this to 0 through 255. Forward labels resolve during pass two. There are no signs, arithmetic expressions, quoted strings, character constants, EQU, RESB/RESW, ORG, include files, macros, segment directives, object records, or a linker. Keeping the value grammar small makes the seed buildable within ASM0's bounds.

DB and DW accept one or more comma-separated values. DW emits the low byte first. No alignment or padding is inserted. Labels name the next loaded offset, including the fixed 0100H origin, and emit no bytes.

## Registers and accepted forms

Ordinary byte registers are AL, CL, DL, BL, AH, CH, DH, BH. Their encoding numbers are zero through seven. Ordinary word registers AX, CX, DX, BX, SP, BP, SI, DI use the same numbers. ES, CS, SS, and DS are segment registers, with numbers zero through three.

| Family | Accepted forms |
|---|---|
| MOV | Ordinary equal-width register/register; register/immediate; register with [BX] or a direct [value], in either direction |
| Segment MOV | Ordinary word register with ES, CS, SS, or DS in either direction, excluding CS as destination |
| ADD, SUB, CMP, AND, OR, XOR | Ordinary equal-width register/register or register/immediate |
| INC, DEC, PUSH, POP | Ordinary word register only |
| INT | One byte value |
| CALL, JMP | One direct near target value |
| JB, JAE, JE, JNE, JBE, JA | Direct short target, checked for -128 through +127 reach |
| RET, CLD, LODSB, STOSB | No operands; RET has no immediate |

Memory belongs only to the ordinary MOV forms. [BX] and a direct [value] default to DS. The seed also accepts ES: on those memory forms. An ordinary register supplies width; there is no BYTE/WORD qualifier, immediate-to-memory MOV, segment-register/memory MOV, arithmetic on memory, indexed address combination, or displacement expression.

```asm
MOV AX,ES
MOV ES,BX
MOV AX,ES:[BX]
MOV ES:[1234H],DX
```

MOV ES,AX encodes as `8E C0`; MOV AX,ES is `8C C0`. The segment register occupies the ModR/M register field. An ES memory override emits 26H before the ordinary MOV encoding. Other overrides are outside the seed's grammar. Segment-register PUSH/POP, indirect CALL/JMP, RET with an operand, multiply/divide, shifts/rotates, and repeated/word string forms are also outside this language.

Write JE/JNE rather than JZ/JNZ, and JB/JAE rather than JC/JNC. There is no Jcc NEAR qualifier. Spell a distant conditional explicitly as the opposite short condition around a near JMP, with your own label. The source formatter's Z labels are ordinary implementation labels for such bridges.

## Fixed encodings

MOV register-immediate uses B0H plus the byte register number or B8H plus the word number. Register and memory loads use 8AH/8BH; stores use 88H/89H. Register ModR/M is `192 + 8*destination + source`. Memory ModR/M is `8*register+7` for [BX], or `8*register+6` followed by the direct word address.

Arithmetic groups are ADD=0, OR=1, AND=4, SUB=5, XOR=6, CMP=7. Register-source opcodes are `8*group+2+width`, where width is zero for byte and one for word. Immediate arithmetic uses 80H/81H with the full immediate width; there is no sign-extended byte shortening.

CALL uses E8H and JMP E9H, followed by `target-(instruction offset+3)` as a word. Conditional opcodes are JB=72H, JAE=73H, JE=74H, JNE=75H, JBE=76H, JA=77H, JL=7CH, JGE=7DH, JLE=7EH, JG=7FH. Their displacement subtracts `instruction offset+2`. There is no branch relaxation.

## Capacity and memory

| Resource | Bound |
|---|---|
| Seed executable | 3302 bytes, built by ASM0 |
| Definitions | 2048 records |
| Name/token content | 16 characters |
| Physical line content | 120 characters |
| Physical lines per pass | Checked 16-bit count, at most 65535 |
| Input/output blocks | 1024 bytes each |
| Maximum emitted image | 61184 bytes, EF00H |
| Main allocation | Full 64 KB segment; entry SP=FFFEH |

The maximum target occupies 0100H–EFFFH. F000H is a valid end label, with F000H–FFFFH reserved for the generated program's stack. One more emitted byte fails. An empty result is valid for inspection only. The assembler's workspace is separate from this target image; streamed output is not limited to its resident buffer size.

| Main-segment offsets | Use |
|---|---|
| 0000H–00FFH | PSP |
| 0100H–3FFFH | Resident code, constants, and scalar state |
| 4000H–4078H | Physical line and zero |
| 4080H–4090H | Token and zero |
| 4100H–41FFH | Reserved gap |
| 4200H–45FFH | Input block |
| 4600H–49FFH | Output block |
| 4A00H–4FFFH | Reserved gap |
| 5000H–EFFFH | 2048 twenty-byte symbol records |
| F000H–FFFFH | Native stack reservation |

A record holds a terminated name of at most sixteen characters in its initial name area and the loaded word value at byte offset eighteen. Lookup compares through the zero terminator; unused padding is not assumed to be zero. No allocated pages or hash buckets are required. The seed's resident ceiling and the preceding ASM0's 8192-byte output ceiling are separate from the seed's own streamed target limit.

## Reports and ownership

Success is `OK RESULT.COM nnnnn bytes`, exit zero. Failure is `ERROR lllll CODE n`, exit one. The line is zero before source reading, then the current physical line; an EOF/publication failure may retain the last line. CHECK reports PASS or FAIL immediately.

| Code | Meaning |
|---|---|
| 1 | Syntax, statement, width, or operand form |
| 2 | Invalid or overflowing numeric literal |
| 3 | Invalid, duplicate, undefined, or inconsistent symbol |
| 4 | Byte or short-branch range |
| 5 | Symbol, line, source-count, or image capacity |
| 6 | File I/O, publication, or cleanup failure |
| 7 | Main-segment/entry-stack requirement |
| 8 | Reserved temporary or backup name present |

The tool does not prove the safety of an assembled program's memory accesses, stack use, or DOS calls. Intel, *The 8086 Family User's Manual*, October 1979, describes CPU behavior; Microsoft, *MS-DOS 3.10 Programmer's Reference Manual*, November 1984, describes handle operations and rename. The accepted syntax and chosen limits above belong to this seed.
