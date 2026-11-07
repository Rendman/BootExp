+++
title = "RILLBOOT language reference"
weight = 900
description = "The accepted language and its bounded implementation."
download = "RILLBOOT.IR"
download_group = "tools/rillboot"
reader_names = 1
aliases = ["/bootstrap/rb/132-the-rill-systems-language/", "/bootstrap/rill/132-the-rill-systems-language/"]
+++

Words range from 0 through 65535; arithmetic wraps and ordering is unsigned. Names are folded to uppercase with complete spelling, up to 24 characters. Local bindings use `let mut name=expression;`, assignment, lexical braces, `if`/`else`, `while`, and `return expression;`. Expressions have parentheses, +, -, and unsigned comparisons. Each expression and block has a checked nesting limit of sixteen. At most sixteen local word slots are live in a procedure.

RILLBOOT adds *, /, %, &, |, >>, logical !, zero-terminated string literals and escapes, global mutable words with literal initializers, global `bytes name[size];` buffers, indexed bytes, procedure parameters, and recursive calls. Calls evaluate arguments from left to right. Declarations may occur after calls; final acceptance rejects an undefined procedure or inconsistent arity. The table has 512 global/procedure records and 32 active local records. Each procedure has at most sixteen parameters and sixteen live local words.

Builtin calls are putc, status, exit, load8, open, create, close, read, write, exists, delete, rename, alloc, free, get8, get16, set8, and set16. The first three and load8 take respectively 1, 0, 1, and 1 arguments; file read/write and block stores take 3; rename and block loads take 2; other services take 1. Handles are opaque. Check status immediately after a service and check exact progress for a write.

RILLBOOT omits ^, <<, unary -, ~, explicit address-of, getc, load16, store8, and store16 because the compiler source does not need them. The RILL-written compiler adds the operators and pointer wrappers required by its tool successors.

Both milestones use the same 40-byte symbol record layout, 4096-byte file blocks, checked two-word text counters, scanner, parser state, and RILL.TMP/RILL.BAK publication. Source rejection preserves an accepted RESULT.IR; a failed publication may leave recovery files.
