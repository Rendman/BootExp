+++
title = "The RILL language reference"
weight = 44
description = "The language used to write and rebuild the compiler, IR86, and ASM86."
download = "RILL.RIL"
download_group = "tools/rill"
reader_names = 1
+++

RILLBOOT builds the first RILL compiler from RC43.RIL. After its self-build comparisons, RC44 extends the local capacity. RILL.RIL is that completed RC44 source; R0 and its next two compiler generations reproduce it. RILL adds the word operators and pointer wrappers used by the later tools.

## Program structure

A program contains global mutable words, global byte buffers, and procedures. Exactly one argument-free main procedure is required. Declarations and procedure definitions may be interspersed at top level; duplicate global names are errors. A normal procedure fall-through returns zero.

```rill
let mut count=0;
bytes text[32];
fn twice(n) { return n*2; }
fn main() {
    let mut answer=twice(21);
    if answer==42 { putc(65); }
    return 0;
}
```

Names begin with a letter or underscore and continue with letters, digits, or underscores. The scanner folds ASCII case, so answer and ANSWER denote the same name. Complete spellings are compared. The name bound is 24 characters, leaving space for generated IR and assembler prefixes. Reserved statement words and intrinsic spellings have their defined parsing roles; use distinct names for program bindings.

Global word initializers are decimal literals from 0 through 65535. A global byte-buffer size is a nonzero decimal literal. Local declarations use `let mut name=expression;` and may appear within blocks. A local name is unavailable during its own initializer. Duplicate active declarations at the same lexical level are rejected; a nested block may shadow an outer binding. Leaving a block restores earlier names and reuses its local slots.

## Procedures and control

Procedures have zero through sixteen named word parameters and return one word. Parameters are mutable private cells. Calls may precede definitions; all call counts must agree and every called procedure must be defined before final acceptance. Arguments evaluate from left to right. Older expression operands survive a nested call.

`return expression;` returns a word; `return;` returns zero. `if expression { ... }` optionally has `else { ... }`. `while expression { ... }` reevaluates its condition at the entrance. Zero is false; any other word is true. Braces make scopes. Every source statement is parsed, including unreachable statements after return. There is no break, continue, for statement, nested procedure definition, variadic argument list, module system, or implicit library declaration.

The final compiler reserves sixty-four local words per call, even when the function uses fewer. Parameters remain separately bounded at sixteen. A call owns its local state. Recursion therefore works within the native stack bound. A pointer to a parameter or local must not outlive that call. The compiler uses no global scratch cell as a substitute for a pending recursive operator or branch target.

## Words and expressions

All ordinary values are sixteen-bit words. Arithmetic wraps modulo 65536. Decimal literals are checked before narrowing; 65536 is not zero. There is no implicit signed type or floating point.

Precedence, from lowest to highest, is:

| Level | Operations |
|---|---|
| 1 | Bitwise OR `\|` |
| 2 | Bitwise XOR `^` |
| 3 | Bitwise AND `&` |
| 4 | `==`, `!=`, `<`, `<=`, `>`, `>=` |
| 5 | `<<`, `>>` |
| 6 | `+`, `-` |
| 7 | `*`, `/`, `%` |
| Primary | Literals, names, indexing, calls, parentheses, unary `-`, `~`, `!`, and address `&name` |

Binary operations are left-associative within a level. Division and remainder are unsigned. Shift counts use the low four bits; right shift inserts zeroes. Comparisons are unsigned and produce exactly zero or one. `!` tests zero; `~` complements all word bits. Bitwise AND/OR evaluate both operands; they are not short-circuit boolean operators. Use nested if statements when a right-hand operation must be skipped.

Division by zero and native frame exhaustion terminate a program with status two. These checks are not a general arithmetic or memory-safety system. There is no pointer type checker, ownership checker, cast syntax, or structure/record syntax.

## Byte storage and strings

A bare global buffer name produces its first-byte pointer. `buffer[index]` reads one zero-extended byte; assigning to it stores the low byte. Indices are byte offsets and are unchecked. A program must keep ordinary pointer access within live declared storage. Word access uses explicit load16/store16 and canonical low-byte-first representation; there is no hidden multiplication of a pointer offset by two.

`&name` produces the byte address of a global word, parameter, or live local. It does not turn an allocated-block handle into a pointer. Quoted strings produce pointers to zero-terminated program-lifetime bytes. Case is preserved; valid escapes are `\n`, `\r`, `\t`, `\0`, `\\`, and `\"`. Raw line breaks, unknown escapes, and unterminated strings are rejected. A string can contain an embedded zero, but an ordinary terminated-string walk stops at it.

## Portable intrinsic calls

| Call | Result and requirements |
|---|---|
| putc(byte), status() | Write the low byte; read the persistent service status |
| open(name), create(name) | Opaque readable/writable file handle; name is a terminated byte pointer |
| read(handle,pointer,count), write(handle,pointer,count) | Actual progress; check status and exact write count |
| close(handle) | Retire the owned handle after successful close |
| exists(name), delete(name), rename(old,new) | Closed-file existence, removal, and rename to an absent destination |
| load8(pointer), load16(pointer) | Read ordinary byte-addressed storage |
| store8(pointer,value), store16(pointer,value) | Write ordinary byte-addressed storage |
| alloc(bytes), free(block) | Allocate/release an opaque block; nonzero extent, at most 65535 bytes |
| get8(block,offset), get16(block,offset) | Checked byte/word read from an allocated block |
| set8(block,offset,value), set16(block,offset,value) | Checked byte/word store in an allocated block |
| exit(word) | Terminate with the low byte as status |

PUTC and file/block services normalize STATUS to zero or one. Ordinary computations, pointer loads/stores, and status() itself do not replace it. Check service status immediately. A successful read returns zero at EOF; a failed read can also return zero, so check STATUS. Transferred bytes retain every value, including zero, 255, and Control-Z. The native binding has eight file slots and sixteen block slots; values remain opaque. A short positive read must be consumed before refilling. Zero-count valid-handle transfers perform no memory access and do not truncate a file.

## Compiler resources and publication

| Resource | Bound and reason |
|---|---|
| Global/procedure records | 512, including pending procedure names; one bounded block keeps lookup and scope representation visible |
| Name spelling | 24 folded ASCII characters, with complete comparison |
| Parameters per procedure | 16 private word cells |
| Simultaneously live local words | 64; slots are reused when a lexical block ends |
| Active local-name records | 80, accommodating parameters and live local bindings |
| Lexical block and expression recursion | At most 16 each, with native stack guard still applying |
| Quoted token spelling | At most 510 bytes including its quotes; escapes count as source spelling |
| Input and output blocks | 4096 bytes each; no complete-source or complete-IR output buffer |
| Source line and emitted-text counts | Checked paired words; reports print the full decimal count |

The global and local record regions share a 23680-byte opaque block. Records are initialized explicitly; new allocated memory may contain arbitrary bytes. Fixed bounds make this first systems compiler practical on the reference machine, and the complete toolchain fits them.

SOURCE.RIL is reopenable disk text, terminated by EOF or Control-Z. Printable ASCII, tab, CR, and LF are accepted; other control/high bytes are rejected. Source line numbering counts LF. A // comment ends at LF or EOF; use CR/LF for ordinary disk text. A compiled program's file transfers are a separate byte interface and preserve every value.

Accepted IR streams through RILL.TMP. Existing RILL.TMP or RILL.BAK prevents a full compiler run. Parsing and pending-procedure checks, source close, final write, and output close precede the rename publication as RESULT.IR. Ordinary source rejection preserves the previous result. Failed publication can retain recovery files; inspect them before another run. A fresh OK and PASS is required at every tool boundary.

Success is `OK RESULT.IR nnnnnnnnnn`, with the actual complete byte count and exit zero. Failure is `ERROR llllllllll CODE ccccc`, with exit one. Codes are one for file I/O/publication, two for syntax/source bytes, three for numeric-literal overflow, four for binding/arity context, and five for a source-count, table, string, or parser capacity. An error report shows where recognition stopped, which can be just after the missing delimiter.

The backend remains a DOS COM image with at most 61184 emitted bytes and a reserved upper stack area. Allocated workspace does not enlarge the near code segment. Assembly text may be much larger than the executable because neither the compiler nor translator retains a complete output file in memory.
