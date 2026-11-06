+++
title = "30 \u00b7 ASM86 reference"
weight = 30
description = "The accepted language, fixed encodings, storage layout, and failure contract."
download = "ASM86.ASM"
download_group = "tools/asm86"
reader_names = 1
+++

ASM86 is a two-pass 8086/8088 assembler for a single DOS COM image starting at 0100H. It reads SOURCE.ASM and publishes RESULT.COM. It has no filename prompt. Its preceding builder is ASM1, whose language and storage contract are documented in the separate [ASM1 reference](../../asma0/13-reference/index.html).

## Source and values

Names and mnemonics are case-insensitive outside strings. Names begin with a letter or underscore and continue with letters, digits, or underscores. A label occupies a statement of its own and ends with a colon. Blank lines and semicolon comments are accepted. Semicolons inside quoted DB text are ordinary data. Register names, including segment registers, cannot be definitions.

Decimal integers and hexadecimal integers ending in H must fit 0 through 65535. Begin a hexadecimal spelling with a digit, as in 0FFFFH. Expressions support unary + and -, parentheses, addition, subtraction, labels, constants, and `$`, the current location. Addition and subtraction wrap as sixteen-bit words; byte contexts subsequently require 0 through 255. Thus DW -1 is valid but DB -1 is not. Unary signs and parentheses consume the bounded expression nesting allowance. There is no multiplication, division, bitwise expression operator, or floating-point notation.

A forward reference is allowed in a fixed-size operand. Values affecting layout must resolve during pass one. EQU is a single definition of an earlier-resolved absolute word; forward or cyclic EQU definitions are rejected. An EQU name may itself be referenced forward in an ordinary fixed-size operand.

```asm
SIZE EQU 8
START:
DB "Hello; world",13,10
DB "Say ""yes""",0
DW START,$-START
RESB SIZE
RESW 2
```

DB accepts comma-separated numeric values and double-quoted byte strings, including empty strings. Doubled quotes represent one quote; case is preserved. DW accepts numeric expressions, not strings. RESB and RESW materialize zero bytes in the file; they do not allocate additional DOS memory. Their count must be known on pass one and fit the remaining output profile before emission. No ORG, include files, macros, conditional assembly, object records, relocation records, linker, or multi-segment output is supplied. Keeping one origin and fixed instruction lengths makes two-pass addresses reproducible.

CR/LF, bare CR, bare LF, a final unterminated line, and a final source Control-Z are accepted. Control-Z ends source input. Ordinary source bytes must be ASCII; strings are still subject to the physical-line bound. The complete source stays unchanged between passes. Definition and length checks detect some changes, but cannot detect every same-size edit.

## Registers and memory operands

Byte registers are AL, CL, DL, BL, AH, CH, DH, BH. Word registers are AX, CX, DX, BX, SP, BP, SI, DI. Segment registers are ES, CS, SS, DS. Segment registers are accepted only by the documented MOV forms, not ordinary arithmetic or PUSH/POP.

| Address within brackets | Default segment |
|---|---|
| BX, SI, DI | DS |
| BP | SS |
| BX+SI, BX+DI | DS |
| BP+SI, BP+DI | SS |
| Direct expression with no base registers | DS |

A register combination may have an added or subtracted word expression. Write the base registers in the order shown, followed by the displacement: `[BX+SI+4]`, `[BP-2]`, `[SI+TABLE]`. There is no SP-based addressing, scaled index, BX+BP, SI+DI, register subtraction, or extra third address register. These restrictions follow the 8086 addressing fields.

A written displacement is always a sixteen-bit displacement, even when zero. A bare BP uses mode 01 with displacement byte zero because mode 00/rm 110 means a direct address. Other bare register combinations use mode 00. A direct address uses mode 00/rm 110 and a word address. Thus statement sizes never depend on displacement shortening.

BYTE and WORD qualify memory when no ordinary register supplies width. A conflicting qualifier is rejected. Segment selection precedes brackets, after any size qualifier:

```asm
MOV AX,[BP+4]
MOV [BP-2],AX
MOV BYTE [DI],65
ADD WORD [BX+SI+4],1
MOV AX,ES:[BX]
MOV WORD SS:[BP-2],1234H
```

The overrides ES:, CS:, SS:, and DS: select supported memory operands. BP still defaults to SS when no override is written. A COM program normally enters with CS=DS=ES=SS; a program that changes segment registers must preserve its own storage conventions. Overrides are not accepted on LEA, which forms an offset rather than reading memory, or as arbitrary prefixes on string operations.

## Accepted instruction families

Here r8/r16 mean an ordinary byte/word register; r/m means a register or supported memory operand of that width. An immediate is an assembly-time expression. Two memory operands are never accepted.

| Family | Accepted forms |
|---|---|
| MOV | ordinary register with register, memory, or immediate; memory with ordinary register or width-qualified immediate; segment register with r16 or word memory in either direction, except CS as destination |
| ADD, OR, ADC, SBB, AND, SUB, XOR, CMP | ordinary register with register or memory; memory with ordinary register; register or width-qualified memory with immediate |
| TEST | ordinary register with r/m, r/m with ordinary register, or r/m with immediate; memory width required when not inferred |
| INC, DEC, PUSH, POP | ordinary word register only |
| NEG, NOT, MUL, IMUL, DIV, IDIV | one r/m8 or r/m16 operand; explicit width for memory |
| SHL/SAL, SHR, SAR, ROL, ROR, RCL, RCR | r/m8 or r/m16, count 1 or CL; explicit width for memory |
| LEA | r16, supported memory address; no segment override |
| CALL, JMP | direct word target, ordinary word register, or near word memory operand |
| RET | no operand, or immediate word argument-release count |
| INT | immediate byte |
| NOP, CLD | no operands |
| LODSB, LODSW, STOSB, STOSW, MOVSB, MOVSW | no operands; REP allowed only with these six spellings |

IMUL and IDIV use the original single-operand accumulator conventions. Multiplication and division register pairs, flags, divide faults, segment defaults, and string-register effects are CPU behavior, not hidden assembler services. Consult Intel, *The 8086 Family User's Manual*, October 1979, instruction descriptions and encoding tables.

There is no PUSH immediate, later-CPU near conditional opcode, two- or three-operand IMUL, immediate shift count other than one, far call/jump, general prefix syntax, or complete Intel instruction vocabulary. These omissions keep the accepted language and implementation bounded. The processor may have other forms that this assembler does not accept.

Immediate arithmetic keeps the full-width group encoding; it does not select a sign-extended byte optimization. Ordinary word-register INC/DEC and register-immediate MOV retain ASM0's encodings. Existing published ASM0, IR86, and RILL-generated assembly produce identical bytes. Newly reserved segment-register names mean this is not a promise about every possible old source using such names as labels.

## Conditional transfers

JB, JAE, JE, JNE, JBE, JA, JL, JGE, JLE, and JG are supported. JC aliases JB; JNC aliases JAE; JZ aliases JE; JNZ aliases JNE. Unsigned and signed comparisons use different condition families. Ordinary Jcc remains short: the target minus the address after the instruction must be between -128 and +127.

Write NEAR explicitly for a distant conditional:

```asm
JNE NEAR DEST
```

This always emits five bytes: JE short +3, then E9 followed by the near relative word. For a start at 0100H and target 0200H the bytes are `74 03 E9 FB 00`; the word displacement is 0200H minus 0105H. A false original condition skips the near JMP; a true condition takes it. The near displacement is word arithmetic within the same code segment.

There is no generated skip-label definition and no extra symbol-table record. Size is five bytes in both passes. There is no automatic branch relaxation: removing NEAR requests a short instruction and can fail its range check. The Z labels visible in the assembler's own implementation are explicit source labels used by its small preceding builder; they are separate from the label-free output expansion above.

## Capacity and memory

| Resource | ASM86 bound |
|---|---|
| Executable produced by ASM1 | 6422 bytes |
| Input/output blocks | 4096 bytes each |
| Definitions | 8192 |
| Name length | 31 characters |
| Physical-line content | 1023 characters |
| Ordinary token content | 63 characters |
| Source lines and consumed bytes | Checked 32-bit counts |
| Expression nesting | At most 16 factor levels |
| Maximum emitted image | 61184 bytes |

The image occupies offsets 0100H through EFFFH at most. F000H is a valid end label, but no additional byte may be emitted there. F000H–FFFFH is reserved for the generated program's stack. This is a chosen COM execution profile; allocated assembler workspace does not enlarge a target's code segment. Empty output is valid for inspection only.

ASM1 retains the old instruction grammar plus ordinary-word/segment MOV excluding CS destination and ES overrides on the old MOV memory forms. It has no quoted data, EQU, RESB/RESW, new expressions, general addressing, or NEAR conditional qualifier. Its own source fits unchanged ASM0's 256-definition, 4000-line, 120-character, 8192-byte limits. The full ASM86 source uses only ASM1's language. New accepted source forms are not prerequisites for building their implementation.

| Main-segment offsets | ASM86 use |
|---|---|
| 0000H–00FFH | PSP |
| 0100H–BFFFH | Resident code and static state |
| C000H–C7FFH | Reserved; descriptors and scalar state are in the loaded image |
| C800H–CBFFH | Physical line and zero |
| CC00H–CC3FH | Token and zero |
| CC40H–CFFFH | Saved name and reserved parser workspace |
| D000H–DFFFH | Input block |
| E000H–EFFFH | Output block |
| F000H–FFFFH | Stack |

Unused gaps are reserved. The full resident ceiling is BFFFH. It is separate from the size of the image streamed to disk. The seed's single-segment map belongs to the [ASM1 reference](../../asma0/13-reference/index.html).

ASM86 keeps CS, DS, and SS at its original main segment, checks normal COM entry SP=FFFEH, and retains 1000H paragraphs using DOS function 4AH. It allocates eight A00H-paragraph symbol pages and one 200H-paragraph hash block using function 48H. Partial allocations are recorded and released with function 49H. The main segment plus these blocks is 392 KiB, excluding DOS, environment, and allocation-control overhead. Allocation is checked rather than inferred from the machine's nominal RAM.

Each page holds 1024 forty-byte records. IDs 1 through 8192 select page `(ID-1)/1024` and offset `((ID-1) modulo 1024)*40`; zero is the empty marker. No record crosses a page. A record has a 32-byte zero-padded name, word value, word next-ID link, word pass-seen flags, and word kind (zero label, one EQU). All inserted fields are initialized. Unused allocated memory is never assumed zero.

The hash starts at zero, rotates the word left five bits, and XORs each uppercase name byte. Its low twelve bits choose one of 4096 word buckets. Every candidate is compared through its complete zero-terminated spelling. A collision is merely another candidate. Unresolved pass-one operand references do not allocate placeholder records. Pass two checks definition kind/value, one occurrence per definition, total seen definitions, and final image length.

SYMPTR deliberately returns ES selecting a page and BX the record offset. RECORDWRITE temporarily selects record and hash storage. Their callers restore ES to the main segment before ordinary string or file-publication work. An offset without its page segment is not a complete pointer. Allocation helpers and normal symbol-definition/value operations restore ES on return. Newly allocated RAM, bucket heads, record padding, reader cursors, and handle flags are explicitly initialized.

## Files, passes, and errors

Pass one reads and validates while counting output and recording definitions. Pass two reopens the same disk source, resets its reader and counters, resolves references, and streams ASMA.TMP. A short successful DOS read is consumed completely and followed by another refill; only a zero read is file EOF. Nonempty output flushes check carry and the exact written count. Short writes fail. A zero-length write is not used as a flush.

A pre-existing ASMA.TMP or RESULT.BAK is an error before output creation. The assembler owns only the temporary file it created. Source failure closes owned handles and deletes that temporary file, preserving an older RESULT.COM. Flush and close must succeed before publication.

Publication renames an old RESULT.COM to RESULT.BAK, renames ASMA.TMP to RESULT.COM, then deletes the backup. If the second rename fails, it attempts restoration. Failed restoration retains recovery files and prints a notice. Failed backup deletion also prevents OK. DOS rename is not atomic replacement; power loss can still require manual recovery. Inspect recovery files before renaming or deleting them.

Success prints `OK RESULT.COM nnnnn bytes` and exits zero. Failure prints `ERROR llllllllll CODE n` and exits one. The seed prints five line digits; the full tool prints ten. Line zero identifies startup/file setup before a physical line is read; an EOF or publication error can retain the last source line. CHECK immediately prints PASS for zero or FAIL for nonzero.

| Code | Meaning |
|---|---|
| 1 | Statement, token, operand, width, or delimiter error |
| 2 | Invalid or overflowing numeric literal |
| 3 | Invalid, duplicate, unresolved, or inconsistent definition/reference |
| 4 | Byte, short-branch, or shift-count range |
| 5 | Symbol, physical-line, source-count, nesting, or image capacity |
| 6 | DOS file, read, write, close, rename, or cleanup failure |
| 7 | Main-segment or allocated-memory failure |
| 8 | Reserved temporary or backup name already present |

Cleanup failure can accompany an earlier category and a recovery notice. The printed category alone does not prove every file operation succeeded. Require a fresh OK and PASS before using output. Microsoft, *MS-DOS 3.10 Programmer's Reference Manual*, November 1984, documents handle operations 3CH–41H, memory functions 48H–4AH, and rename 56H.
