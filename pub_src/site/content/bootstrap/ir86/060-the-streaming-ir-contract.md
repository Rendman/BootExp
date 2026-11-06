+++
title = "The streaming IR86 contract"
weight = 60
description = "Procedures, expressions, literal data, and opaque services in a processor-independent machine."
download = "IR86.RIL"
download_group = "toolchain"
+++

IR86 defines a virtual accumulator A, sixteen-bit words, an expression stack, named byte-addressed storage, and portable services. A backend maps those operations to a processor and environment. Physical registers, flags, segments, interrupt numbers, and native descriptors are not language values.

The native IRWIDE bridge and the RILL-written IR86 accept this contract. The earlier translator's first construction remains a smaller bootstrap milestone with its own source-name interface and bounds. Keep it as a separately named tool.

## Values and storage

WORD name value declares a canonical low-byte-first word; BYTE declares one byte (initializer 0 through 255); BUFFER name count materializes that many zero bytes. Declarations may occur between procedure bodies. A program must not execute through data. ADDR returns a byte-addressed pointer to the named object. LD/ST and LDB/STB operate on named words/bytes; FETCH/FETCHB and PUT/PUTB operate through pointers. PUT consumes a saved pointer with the value in A. Byte reads zero-extend; byte writes retain the low byte.

Numeric spellings are unsigned decimal or hexadecimal ending in H, within 0 through 65535. Names begin with a letter or underscore and continue with letters, digits, or underscores; case is folded. They have at most 29 characters so the backend's U_ prefix still fits ASM86A. The input line has at most 1023 characters, and an ordinary token at most 63. Semicolons introduce comments outside quoted literals. CR/LF, bare CR or LF, a final unterminated line, and source Control-Z are supported.

A word computation wraps modulo 65536. Pointers address bytes, not words; callers keep ordinary accesses within live storage. The language supplies no physical-register escape or automatic memory-safety system.

## Expressions and branches

LIT loads A. PUSH saves it; POP restores the latest word. ADD, SUB, MUL, DIV, MOD, AND, OR, XOR, SHL, and SHR consume one saved left operand and use A as the right operand. DIV and MOD are unsigned; zero divisors terminate with status two in this profile. Shifts use the low four bits of the count, an explicit word operation independent of processor shift conventions. NEG and NOT act on A alone.

CEQ, CNE, CULT, CULE, CUGT, CUGE, CSLT, CSLE, CSGT, and CSGE consume a saved left operand and produce exactly zero or one. Signed relations interpret the same word bits in two's-complement order; the other ordering relations are unsigned.

JMP branches unconditionally; JZ/JNZ test A without consuming it. EQ/NE and ULT/ULE/UGT/UGE/SLT/SLE/SGT/SGE instead consume a saved left operand and branch to a named target when the relation is true. A branch, label, or return meets with an empty expression stack. Value comparisons may leave older saved operands. The translator checks at most 256 active saved words.

The selected backend uses ASM86A's fixed conditional bridges and no synthetic label per ordinary conditional. The assembly format and machine-byte counts are backend properties. The assembler separately checks target image size, symbols, definitions, byte-operand narrowing, and branch ranges. An accepted IR-to-assembly translation is not a successful executable build until that assembly also passes.

## Procedures and local state

| Form | Meaning |
|---|---|
| PROC name arguments locals | Define a procedure with explicit parameter and local-word counts |
| PARAM index / SETPARAM index | Read or write a zero-based parameter slot |
| LOCAL index / SETLOCAL index | Read or write a zero-based local slot |
| PADDR index / LADDR index | Produce a byte pointer to a live slot |
| INVOKE name count | Consume the most recent count saved words as arguments, left to right; preserve older expression operands |
| RETURN | Return A and release this procedure's frame |

The native profile supports at most 16 parameters and 64 local words per IR procedure. Slots are word objects; a pointer to one is valid only during that call. Local contents are unspecified until assigned. A procedure result is A; arguments are not a hidden global array.

CALL/RET retain the accumulator-passing, unframed helper convention. CALL preserves older caller expression operands while its callee starts with an empty expression stack. Do not use RET to release a PROC frame; use RETURN. A PROC body may contain ordinary labels and unreachable source after a RETURN, but every executed path must obey the frame convention.

```ir
PROC MAIN 0 0
LIT 7
PUSH
LIT 9
PUSH
INVOKE TWICE 1
ADD
PUSH
LIT 25
CNE
RETURN
PROC TWICE 1 1
PARAM 0
PUSH
LIT 2
MUL
SETLOCAL 0
LOCAL 0
RETURN
```

The caller's saved seven survives TWICE. The comparison returns zero when the result is 25, so this complete program exits zero. A runtime guard terminates native frame exhaustion with status two; it is not a general guarantee against invalid pointers.

## Literal strings

LITS "text" produces a pointer to zero-terminated bytes. Case is preserved. Escapes are `\n`, `\r`, `\t`, `\0`, `\\`, and `\"`; raw line breaks and unknown escapes are errors. Embedded zero is data, and an additional zero terminates the literal. Literal storage has program lifetime. In the native backend a jump skips inline bytes; a constant is never executed as instructions.

## File and memory services

Services set persistent STATUS to zero for success or one for failure. Ordinary computations do not change it. STATUS reads it. Failure returns zero except GETC EOF, which is 65535 with success. File names are ordinary terminated strings; workbench names are disk files rather than DOS devices.

| Operation | Inputs and result |
|---|---|
| PUTC / GETC | A byte to output / a byte or EOF in A |
| OPEN / CREATE | Filename pointer in A; readable/writable opaque handle returned |
| READ / WRITE | Saved handle, saved pointer, count in A; actual progress returned |
| CLOSE | Handle in A; retire it only on success |
| EXISTS | Filename pointer; zero absent, one present, 65535 on failure |
| DELETE | Filename pointer; remove the named closed file |
| RENAME | Saved old-name pointer, new-name pointer in A; destination must be absent |
| ALLOC | Nonzero byte extent in A; return an opaque memory-block handle |
| FREEBLOCK | Live block handle in A; invalidate it on success |
| GET8 / GET16 | Saved block handle, byte offset in A; return byte/word |
| SET8 / SET16 | Saved block handle, saved byte offset, value in A; store byte/word |

An allocated-block handle is not a pointer and cannot be used by FETCH or passed as an ordinary file buffer. GET/SET validate the whole access, including a word at the end of a block. New allocated memory is unspecified; initialize records and bucket heads explicitly. This binding has eight live file slots and sixteen live block slots. Slots are bounded so ownership remains understandable; handle values and their native representation are private.

Zero-count READ/WRITE returns zero for a valid handle, without reading memory or issuing a truncating zero-length DOS write. A short successful read is ordinary progress. A short write returns actual progress and failure status in this binding. Check both when a full record is required.

## Files and target profile

The translator reads SOURCE.IR and streams RESULT.ASM through IRTX.TMP, using IRRES.BAK during publication. Reserved recovery names are not silently erased. Syntax/input failure preserves the previous result. Publication failures retain recovery options and return nonzero; require a fresh OK and PASS before assembling.

The main segment must be a normal full COM allocation with entry SP=FFFEH. Code, static data, and native stack stay in that segment. ALLOC uses separate DOS-owned blocks and restores ordinary string-segment conventions before returning. The target image may contain at most 61184 bytes, occupying 0100H–EFFFH; F000H–FFFFH is reserved for stack. More assembler workspace does not make a COM image unlimited.

Source and output use bounded 4096-byte blocks with checked source/output counters. No complete-input or complete-assembly buffer imposes the earlier 32768-byte text ceiling. Generated declarations and inline strings still consume real target image space. The assembler's 8192-symbol and image checks remain part of a successful complete build.
