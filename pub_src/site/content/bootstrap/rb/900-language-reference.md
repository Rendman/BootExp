+++
title = "RILLBOOT language reference"
weight = 900
description = "The accepted language and its bounded implementation."
download = "RILLBOOT.IR"
download_group = "tools/rillboot"
reader_names = 1
aliases = ["/bootstrap/rb/132-the-rill-systems-language/", "/bootstrap/rill/132-the-rill-systems-language/"]
+++

Words range from 0 through 65535; arithmetic wraps and ordering is unsigned. Names begin with a letter or underscore, continue with letters, digits, or underscores, and are folded to uppercase with complete spelling, up to 24 characters. Source uses decimal word literals, ASCII text, // comments ending at LF or EOF, and brace-enclosed bodies. Use DOS CR/LF disk text. Local bindings use `let mut name=expression;`, assignment, lexical braces, `if`/`else`, `while`, and `return expression;`. Expressions have parentheses, +, -, and unsigned comparisons. Addition/subtraction bind more tightly than comparisons; each level associates left to right. Zero is false and any nonzero word is true. return; and normal fall-through return zero. Each expression and block has a checked nesting limit of sixteen. At most sixteen local word slots are live in a procedure.

RILLBOOT adds `*`, `/`, `%`, `&`, `|`, `>>`, logical `!`, zero-terminated string literals and escapes, global mutable words with literal initializers, global `bytes name[size];` buffers, indexed bytes, procedure parameters, and recursive calls. Calls evaluate arguments from left to right. Declarations may occur after calls; final acceptance rejects an undefined procedure or inconsistent arity. The table has 512 global/procedure records and 32 active local records. Each procedure has at most sixteen parameters and sixteen live local words.

Builtin calls are putc, status, exit, load8, open, create, close, read, write, exists, delete, rename, alloc, free, get8, get16, set8, and set16. The first three and load8 take respectively 1, 0, 1, and 1 arguments; file read/write and block stores take 3; rename and block loads take 2; other services take 1. Handles are opaque. read returns zero at EOF; a failure can also return zero, so check status immediately. A short positive read contains data; require exact write progress. File transfers preserve all byte values, including Control-Z. The native binding supplies eight file slots and sixteen allocated-block slots.

RILLBOOT omits ^, <<, unary -, ~, explicit address-of, getc, load16, store8, and store16 because the compiler source does not need them. The RILL-written compiler adds the operators and pointer wrappers required by its tool successors.

Both milestones use the same 40-byte symbol record layout, 4096-byte file blocks, checked two-word text counters, scanner, parser state, and RILL.TMP/RILL.BAK publication. Source rejection preserves an accepted RESULT.IR; a failed publication may leave recovery files.
