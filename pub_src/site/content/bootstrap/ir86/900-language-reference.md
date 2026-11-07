+++
title = "IR86 language reference"
weight = 900
description = "The accepted language and its bounded implementation."
download = "IR86.ASM"
download_group = "tools/ir86"
reader_names = 1
aliases = ["/bootstrap/ir86/060-the-streaming-ir-contract/", "/bootstrap/ir86/28-reference/"]
+++

IR86 defines a virtual accumulator A, sixteen-bit words, an expression stack, and byte-addressed storage. Arithmetic wraps modulo 65536; comparisons and division are unsigned. A backend preserves those rules on its target processor. The language does not expose physical registers, processor flags, segments, interrupts, or operating-system descriptor values.

## Source and names

Put one operation on each line. Names and operation spellings are folded to uppercase. A name begins with a letter or underscore, continues with letters, digits, or underscores, and has at most 29 characters. A semicolon begins a comment outside a quoted string. Empty lines are allowed. Numeric operands are unsigned decimal words or hexadecimal words ending in H; hexadecimal spelling starts with a digit, as in 0FFFFH. A word must fit 0 through 65535.

The native translator reads SOURCE.IR and publishes RESULT.ASM. Compiler sources use those same fixed work files. Keep the input unchanged throughout a run. Source text accepts CR/LF, bare CR, bare LF, and a final line without a terminator; Control-Z ends the source.

## Values, storage, and expressions

| Form | Meaning |
|---|---|
| `WORD name value` | Declare a global word initialized to the numeric value |
| `BUFFER name bytes` | Declare that many zero-filled bytes in the output image |
| `LIT value` | Put the numeric word in A |
| `LD name`, `ST name` | Load or store the named word |
| `ADDR name` | Put the named storage's byte pointer in A |
| `FETCH`, `FETCHB` | Read a word or zero-extended byte at the pointer in A |
| `PUSH`, `POP` | Save A, or restore the most recently saved word to A |
| `PUT`, `PUTB` | Pop a destination pointer and store A as a word or low byte |
| `LITS "text"` | Put a pointer to zero-terminated literal bytes in A |

Keep WORD and BUFFER declarations before procedure bodies so control cannot fall into their storage. LITS supplies its own branch around inline literal data. Quoted literals preserve case and accept `\n`, `\r`, `\t`, `\0`, `\\`, and `\"`. Unknown escapes and unterminated strings are errors. Ordinary pointer access is unchecked; word access needs two live bytes and uses the canonical low-byte-first representation.

A binary operation takes its left operand from the expression stack and its right operand from A, consumes that saved word, and puts the result in A:

- ADD, SUB, and MUL wrap to a word.
- DIV and MOD produce the unsigned quotient and remainder. A zero divisor terminates the program with status two in this backend.
- AND, OR, and XOR operate on corresponding bits.
- SHL and SHR use the low four bits of the right operand as the count; SHR inserts zeroes.
- CEQ, CNE, CULT, CULE, CUGT, and CUGE produce exactly zero or one for equality, inequality, and unsigned ordering.

## Control and procedures

LABEL names a branch destination and requires an empty expression stack. JMP always transfers; JZ transfers when A is zero, and JNZ when A is nonzero. These transfers require no saved expression words. RETURN and EXIT also require an empty expression stack. EXIT terminates the program with the low byte of A as its status.

`PROC name parameters locals` declares a procedure with up to sixteen word parameters and sixty-four local words. Slot numbers are zero-based. PARAM reads a parameter; LOCAL reads a local; SETLOCAL stores A in a local. PADDR and LADDR produce byte pointers to those cells. A pointer to a parameter or local must not outlive its call. Initialize a local before reading it.

Push arguments from left to right, then use `INVOKE name count`. INVOKE consumes that many saved words while preserving older expression operands. `CALL name` calls an argument-free procedure. RETURN returns A to the caller and releases the callee's frame. Each INVOKE count must match its callee's declaration. Keep the expression stack balanced within each procedure; this profile allows at most 256 saved expression words, subject to its native stack guard. The translator checks local/parameter indices and stack depth, while the assembler resolves names; it does not perform a complete procedure-signature or control-flow analysis.

A complete program supplies MAIN with no parameters. The backend invokes it at entry and uses its returned low byte as the DOS status. Its native frame guard terminates with status two when the reserved stack would be exceeded.

## Portable services

Services take their last argument in A and any preceding arguments on the expression stack. Their handles are opaque tokens, not pointers or native descriptors.

| Operation | Arguments, result, and effect |
|---|---|
| PUTC | Low byte in A; write one byte to standard output |
| STATUS | Return the persistent service status: zero for success, one for failure |
| OPEN, CREATE | Terminated filename pointer in A; return a readable or writable handle; CREATE creates or truncates a file |
| READ, WRITE | Saved handle and buffer pointer, count in A; consume both saved words and return actual progress |
| CLOSE | Handle in A; retire it after a successful close |
| EXISTS | Filename pointer in A; return one if it can be opened and closed, zero for file-not-found; check STATUS for other failures |
| DELETE | Filename pointer in A; remove the file |
| RENAME | Saved old-name pointer, new-name pointer in A; consume the saved word and rename to an absent destination |
| ALLOC | Nonzero byte extent in A, at most 65535; return an opaque block handle |
| FREEBLOCK | Block handle in A; release the owned block |
| GET8, GET16 | Saved block handle, byte offset in A; consume the handle and return a checked byte or word |
| SET8, SET16 | Saved block handle and byte offset, value in A; consume both saved words and perform a checked store |

Check STATUS immediately after a service. Ordinary arithmetic, direct pointer loads/stores, and STATUS itself do not replace it. PUTC and file/block operations do. READ returns zero at EOF; zero can also accompany failure, so a count alone is insufficient. A short positive read contains data. A short write reports failure and its actual count. A valid-handle zero-count READ or WRITE performs no memory access and does not truncate a file. Transferred bytes preserve zero, 255, and Control-Z.

The binding has eight file slots and sixteen block slots. Checked block access validates both the handle and the entire byte/word extent. It does not turn ordinary pointers into checked handles or make general pointer arithmetic safe.

## Operation records

The construction's records use these argument classes and stack actions:

| Operation | Argument class | Stack action |
|---|---:|---:|
| `EXIT` | 0 | 4 |
| `LABEL` | 2 | 0 |
| `LIT` | 1 | 0 |
| `ADDR` | 2 | 0 |
| `WORD` | 3 | 4 |
| `BUFFER` | 3 | 4 |
| `LD` | 2 | 0 |
| `ST` | 2 | 0 |
| `FETCH` | 0 | 0 |
| `FETCHB` | 0 | 0 |
| `PUSH` | 0 | 1 |
| `POP` | 0 | 2 |
| `PUT` | 0 | 2 |
| `PUTB` | 0 | 2 |
| `ADD` | 0 | 2 |
| `AND` | 0 | 2 |
| `OR` | 0 | 2 |
| `XOR` | 0 | 2 |
| `SUB` | 0 | 2 |
| `MUL` | 0 | 2 |
| `DIV` | 0 | 2 |
| `MOD` | 0 | 2 |
| `SHL` | 0 | 2 |
| `SHR` | 0 | 2 |
| `CEQ` | 0 | 2 |
| `CNE` | 0 | 2 |
| `CULT` | 0 | 2 |
| `CULE` | 0 | 2 |
| `CUGT` | 0 | 2 |
| `CUGE` | 0 | 2 |
| `JZ` | 2 | 4 |
| `JNZ` | 2 | 4 |
| `JMP` | 2 | 4 |
| `CALL` | 2 | 0 |
| `PROC` | 4 | 0 |
| `RETURN` | 0 | 4 |
| `INVOKE` | 5 | 0 |
| `LOCAL` | 1 | 0 |
| `SETLOCAL` | 1 | 0 |
| `LADDR` | 1 | 0 |
| `PARAM` | 1 | 0 |
| `PADDR` | 1 | 0 |
| `LITS` | 6 | 0 |
| `PUTC` | 0 | 0 |
| `OPEN` | 0 | 0 |
| `CREATE` | 0 | 0 |
| `CLOSE` | 0 | 0 |
| `STATUS` | 0 | 0 |
| `READ` | 0 | 3 |
| `WRITE` | 0 | 3 |
| `DELETE` | 0 | 0 |
| `EXISTS` | 0 | 0 |
| `ALLOC` | 0 | 0 |
| `FREEBLOCK` | 0 | 0 |
| `RENAME` | 0 | 2 |
| `GET8` | 0 | 2 |
| `GET16` | 0 | 2 |
| `SET8` | 0 | 3 |
| `SET16` | 0 | 3 |

Classes: 0 has no source operand; 1 a numeric word; 2 a name; 3 a storage name followed by an initializer for WORD or a byte count for BUFFER; 4 a procedure name, parameter count, and local count; 5 a call name and argument count; 6 a quoted string. Stack actions: 0 preserves saved words, 1 saves A, 2 consumes one saved word, 3 consumes two, and 4 requires an empty expression stack. INVOKE additionally consumes its declared arguments; PROC also requires an empty expression stack at entry and establishes the current frame bounds.

## The 8086/DOS profile

The operation templates and runtime binding emit 8086/8088 assembly for ASM86. The translator streams 4096-byte input and output blocks, bounds a physical line to 1023 characters, and uses checked two-word source/output counters. ASM86 supplies symbol storage, label resolution, instruction encodings, and the 61184-byte target-image bound. The main segment and its upper stack reservation are backend choices, not physical-register operations in the IR language.

A pre-existing IRTX.TMP or IRRES.BAK prevents a new publication. Source rejection preserves an accepted RESULT.ASM; a failed publication can leave recovery files. Success reports `OK RESULT.ASM nnnnnnnnnn text bytes` and returns zero. Failure reports `IR ERROR llllllllll CODE n` and returns nonzero. Require a fresh successful translation and assembly before executing a generated program.
