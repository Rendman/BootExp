+++
title = "IR86 language reference"
weight = 900
description = "The accepted language and its bounded implementation."
download = "IR86.ASM"
download_group = "tools/ir86"
reader_names = 1
aliases = ["/bootstrap/ir86/28-reference/"]
+++

IR words are unsigned sixteen-bit values with wrapping arithmetic and byte-addressed storage. A backend preserves this meaning on its target processor. Procedures use named parameter and local slots. File and allocated-block handles are opaque tokens; STATUS is persistent, zero for success, one for failure. READ and WRITE return the actual count; a positive short read is data. Compiler sources use fixed filenames.

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

Classes: 0 has no operand; 1 a word; 2 a name; 3 a storage name and size; 4 a procedure name, parameter count, and local count; 5 a call name and argument count; 6 a quoted string. Stack actions: 0 leaves saved operands alone, 1 saves A, 2 consumes one saved word, 3 consumes two, and 4 requires an empty boundary. INVOKE consumes its declared arguments. PROC allows up to sixteen parameters and local words.

The 8086/DOS backend emits assembly from the operation templates and runtime binding printed during construction. The translator streams 4096-byte blocks, bounds a physical line to 1023 characters, and uses checked two-word source/output counters. ASM86 supplies symbols, label resolution, native encodings, and the 61184-byte target image bound.
