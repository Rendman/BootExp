+++
title = "IR86 language and translator reference"
weight = 28
description = "Every operation, its stack contract, the assembly interface, resource bounds, and diagnostics."
download = "IR86.ASM"
+++

This reference describes the completed IR86.COM, assembled from IR86.ASM by the completed ASM86. Earlier construction checkpoints accept only their introduced operations. IR86 translates text into text; ASM86 encodes that assembly into an 8086/8088 DOS `.COM` file.

## Invocation and results

Run CHECK IRKEEP, or CHECK IR86 if using the final tool under its original name. At `IR source name:` supply one through eight letters, digits, or underscores, without path or extension. IR86 reads NAME.IR and, after successful validation, writes NAME.ASM in the current directory. Use ordinary disk names; DOS device names are excluded from the workbench even with an extension.

Success prints `OK NAME.ASM nnnnn text bytes` and returns zero; CHECK prints PASS. The count includes every CR/LF byte. Failure prints `IR ERROR nnnnn CODE n` and returns one; CHECK prints FAIL. The first number is the one-based physical input line, or zero before a source line has been read. Output is not created for a rejected source. An I/O error during final creation, writing, or closing can leave partial output; require a fresh OK.

Then run CHECK ASMKEEP and enter NAME. Require its own OK and PASS before using NAME.COM. ASM86 reports undefined or duplicate names and resolves all addresses. An older machine file can remain after an assembly failure and must not be mistaken for new output.

## Source grammar and program shape

- Each nonempty line contains one operation followed by its whitespace-separated arguments. Commas, colons, quoted strings, character constants, and expressions are not argument syntax.
- Semicolon starts a comment. Tabs become spaces and ASCII case is ignored. Normal line endings are CR/LF; bare CR, bare LF, a final unterminated line, and Control-Z end-of-input are also recognized.
- Names contain one through fourteen letters, digits, or underscores, starting with a letter or underscore. The translator prefixes U_ when emitting a name. Register and operation spellings may be names. Names for storage and code share one namespace.
- Numeric tokens are unsigned decimal or hexadecimal ending in H, beginning with a decimal digit: use 0FFH, not FFH. Values range from zero through 65535. A numeric token, like any token, may not exceed sixteen characters. LIT does not take a label; ADDR forms a named address.
- BYTE, WORD, and BUFFER declarations precede the first executable label. That label must be LABEL MAIN. Subsequent LABEL operations identify code locations. There are no segment, alignment, import, external, macro, or include directives.
- An executable statement before MAIN or a declaration after MAIN is rejected. Missing MAIN is rejected at end of source. The translator checks name spelling; ASM86 checks duplicate definitions and undefined references. Neither tool proves that a branch or memory access uses a name of the intended kind.

The generated header clears direction, requires entry SP=FFFEH, and jumps over declarations to U_MAIN. A failed entry-stack check returns DOS status seven without an IR source diagnostic. If the final statement can fall through, the translator appends a zero-status HALT. A final HALT, EXIT, JMP, or RET needs no appended exit. A label does not prevent execution from falling into its body.

## Accumulator and expression stack

AX holds one sixteen-bit accumulator. PUSH saves its current word; POP restores the most recently saved word. Binary operations consume a saved left operand and use AX as their right operand. Arithmetic wraps modulo 65536. The same bit pattern can be interpreted as signed or unsigned when a comparison explicitly selects its ordering.

The expression stack has at most thirty-two saved words within a basic block. It must be empty at every label, branch, procedure call, return, DOS operation, termination, and end of source. A comparison consumes its left word before checking that boundary. Every source statement is checked, including unreachable statements; this is a linear stack discipline, not a reachability analysis.

The emitted stack uses SS:SP. CALL return addresses share that stack, so expression words cannot be procedure arguments or cross a call. AX and named storage carry values between procedures. A procedure may use its own balanced expressions. There is no automatic local frame, parameter list, or runtime recursion-depth check. Keep native call nesting modest and the upper 4 KB clear for stack use.

## Storage and value operations

Here `name` is a checked name, `n` an unsigned word, and `count` a byte-buffer length. A stack change of -1 requires an existing saved word; zero leaves its depth unchanged.

| Source | Stack change | Meaning |
|---|---|---|
| BYTE name n | 0 | Declare one byte, initialized from 0–255 |
| WORD name n | 0 | Declare one word, low byte first |
| BUFFER name count | 0 | Declare 1–256 consecutive zero bytes |
| LABEL name | Empty required | Define the current code position; first code label is MAIN |
| LIT n | 0 | AX = n |
| LD name | 0 | AX = word at DS:U_name |
| ST name | 0 | Store AX as a word at DS:U_name; retain AX |
| LDB name | 0 | Load one byte and zero-extend it into AX |
| STB name | 0 | Store AL as one byte; retain AX |
| ADDR name | 0 | AX = offset U_name |
| FETCH | 0 | AX = word at the address in AX |
| FETCHB | 0 | AX = zero-extended byte at the address in AX |
| PUT | -1 | Pop an address, store AX there as a word, retain AX |
| PUTB | -1 | Pop an address, store AL there as a byte, retain AX |
| PUSH | +1 | Save AX |
| POP | -1 | Replace AX with the saved top word |

Declarations occupy bytes in the emitted image and have no automatic alignment. A word access needs two consecutive bytes; an unaligned word is permitted by the processor. Operation width is explicit and is not inferred from declaration names. FETCH and PUT use BX as a scratch address register. The programmer is responsible for valid pointers and sufficient storage.

All pointers are offsets in DS. There are no far pointers, segment transfers, allocator, or runtime memory checks. The header requires a full segment, but unused memory is not automatically initialized. An explicitly chosen working area must be initialized and kept clear of the loaded image, the PSP, and the high stack.

## Arithmetic and bit operations

Each operation below consumes one saved left word, leaves the result in AX, and uses BX and arithmetic flags as scratch. Slashes in the tables separate alternatives; type one operation per line.

| Operation | Result |
|---|---|
| ADD | left + AX, modulo 65536 |
| SUB | left - AX, modulo 65536 |
| AND | Bitwise AND of left and AX |
| OR | Bitwise OR of left and AX |
| XOR | Bitwise XOR of left and AX |

No multiply, divide, remainder, shift, floating-point, or overflow-trapping operation is defined. These would require additional target support or explicit routines. Unsigned literal 65535 supplies the signed bit pattern -1; 32768 supplies -32768. There is no signed literal syntax.

## Transfers and comparisons

| Source | Stack condition | Effect |
|---|---|---|
| NOP | Unchanged | Emit one native NOP |
| JMP name | Empty | Near transfer to U_name |
| JZ name | Empty | Transfer if AX is zero; retain AX |
| JNZ name | Empty | Transfer if AX is nonzero; retain AX |
| EQ name / NE name | Consume one, then empty | Compare left with AX for equality or inequality |
| ULT name / ULE name | Consume one, then empty | Unsigned left less than / less than or equal to AX |
| UGT name / UGE name | Consume one, then empty | Unsigned left greater than / greater than or equal to AX |
| SLT name / SLE name | Consume one, then empty | Signed left less than / less than or equal to AX |
| SGT name / SGE name | Consume one, then empty | Signed left greater than / greater than or equal to AX |
| CALL name | Empty | Near procedure call; AX carries a value by convention |
| RET | Empty | Near return; AX is retained |
| HALT | Empty | Terminate with DOS status zero |
| EXIT | Empty | Terminate with the low byte of AX as the DOS status |

Comparisons branch; they do not produce a Boolean value in AX. They retain the right operand there and use BX and flags as scratch. Signed ordering uses two's-complement values from -32768 through 32767; unsigned ordering uses zero through 65535. Equality has the same meaning for both.

Every conditional transfer uses a nearby opposite short condition around a near JMP. The target remains U_name for ASM86 to resolve. A generated skip name such as I0001 is reserved to the translator and counts toward the assembler's symbol limit. Conditional targets can span the bounded image without exceeding short-branch reach.

## DOS interface

| Source | Stack condition | Effect |
|---|---|---|
| TOBX / TOCX / TODX | Unchanged | Copy AX into BX, CX, or DX |
| FROMBX / FROMCX / FROMDX | Unchanged | Copy BX, CX, or DX into AX |
| DOS | Empty | Execute INT 21H with the prepared registers |
| JC name / JNC name | Empty | Branch on carry set / clear from the immediately preceding DOS |

JC or JNC must be the next nonempty statement after DOS. Comments and blank lines are permitted between them. Another operation or label consumes the pending carry context, and a carry branch consumes it too. This prevents an unrelated computation from accidentally supplying the tested flags.

AX supplies AH's service number and any AL parameter. BX, CX, and DX supply the service's documented arguments. DOS result registers are available through AX and the FROM operations. Ordinary IR computations use BX as scratch where stated; procedures and DOS may change other registers. Prepare DOS arguments after computations which could disturb them and save needed results in named storage.

There is no segment-register or SP bridge. Use services compatible with the common program segment and check the DOS manual for each call's arguments, results, and carry convention. The translator does not validate a service number or a handle. An INT 21H service which terminates the program does not return to the following IR operation.

## Translation representation

The native translator uses the published ASM86 reader, scanner, numeric reader, table search, and DOS reporting conventions. A fourteen-byte instruction record contains an eight-byte zero-padded name, argument class, expression/control effect, emitted machine-byte count, a padding byte, and a word template pointer.

EXPAND reads zero-terminated assembly text. @ inserts the saved name from 2500H; # inserts the checked numeric spelling from 2520H; ? inserts the current four-digit branch number. It saves the template cursor while a substitution is emitted. Templates contain source text only; ASM86 alone supplies machine encodings.

Argument classes are zero=no arguments, one=numeric value, two=name reference, three=label definition, four=byte declaration, five=word declaration, six=buffer declaration, and seven=conditional target. Effects are zero=ordinary, one=push, two=consume, three=empty boundary, four=consume then empty, five=terminal empty boundary, six=DOS boundary, and seven=carry boundary. FLOW uses these effects independently of argument spelling.

NAMEARG and NUMARG preserve the line cursor while copying their saved tokens. VALUE preserves SI but uses the other work registers. OUTTEXT advances SI; EMITCHAR preserves AX and BX, updates OUTPTR, counts generated line feeds, and changes flags. FOUR preserves all word registers while emitting its digits. SIZEADD updates TARGETSIZE from the record count or a buffer's length. NEWDEF bounds generated definitions. WRITEOUT uses the checked output pointer to write the buffered text. ERROR reports LINENO and terminates without returning.

## Resource bounds

| Resource | Bound or requirement | Reason |
|---|---|---|
| Input physical lines | 4,000 | Bounded source processing and reports |
| Input physical width | 120 characters, including comments and tabs | Fixed line buffer |
| Token width | 16 characters | Fixed token and numeric-spelling buffers |
| IR name width | 14 characters | U_ must fit ASM86's name limit |
| Numeric value | 0–65535 | Unsigned word; BYTE narrows it to 0–255 |
| BUFFER count | 1–256 bytes | Compact, inspectable declarations |
| Expression words | 32 within a basic block | Bounded temporary use and simple stack checking |
| Assembly-text bytes | 32,768, including CR/LF | Buffer at 6000H–DFFFH |
| Generated assembly lines | 4,000 | ASM86's source bound |
| Generated definitions | 256 total | Includes I_ENTRY, every user definition, and conditional skip labels |
| Generated machine image | 8,192 bytes | Includes header, declarations, code, and any appended HALT |
| Program memory | Full 64 KB segment, entry SP=FFFEH | Fixed translator buffers and generated-program memory convention |
| Stack reservation | Upper 4 KB kept free | Separates native calls and expression words from data |

With no conditional skip labels, at most 255 user definitions fit beside I_ENTRY. Duplicate definitions still consume the translator's accounting and are then rejected by ASM86. Generated template lines fit within ASM86's physical-width bound. No new assembler instruction form or executable format is required.

## Diagnostics

| Code | Meaning |
|---|---|
| 1 | Syntax or context: unknown operation, extra token, misplaced declaration/executable statement, token too long, or invalid source base name |
| 2 | Numeric spelling or value above 65535 |
| 3 | Malformed or overlong name, or missing/incorrect initial MAIN label |
| 4 | Byte/buffer range, expression underflow, nonempty control boundary, or carry branch without its DOS context |
| 5 | Input, output-text, generated-line, definition, target-image, or expression-depth capacity exceeded |
| 6 | DOS file failure, short write, or invalid source byte |
| 7 | Translator entry stack differs from FFFEH |

The line report counts physical input lines, including blank and comment lines. End-of-source checks refer to the last completed physical line. ASM86's separate diagnostics refer to physical lines in the generated .ASM file, which need not correspond one for one with .IR lines.

For instruction encodings and signed conditions consult Intel Corporation, *The 8086 Family User's Manual*, October 1979. For handles, console services, and process termination consult the MS-DOS 3.10 programmer's reference supplied with the machine, particularly INT 21H functions 02H, 09H, 0AH, 3CH–3FH, 40H, and 4CH. Check each service's documented result and carry behavior rather than treating all DOS calls alike.
