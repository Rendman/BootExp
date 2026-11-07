+++
title = "RILL0 language reference"
weight = 900
description = "The accepted language and its bounded implementation."
download = "RILL0.IR"
download_group = "tools/rill0"
reader_names = 1
aliases = ["/bootstrap/rill/01-a-program-in-the-intermediate-language/", "/bootstrap/rill/31-reference/"]
+++

Words range from 0 through 65535; arithmetic wraps and ordering is unsigned. Names are folded to uppercase with complete spelling, up to 24 characters. Local bindings use `let mut name=expression;`, assignment, lexical braces, `if`/`else`, `while`, and `return expression;`. Expressions have parentheses, +, -, and unsigned comparisons. Each expression and block has a checked nesting limit of sixteen. At most sixteen local word slots are live in a procedure.

There is exactly one argument-free `fn main(){...}`. Its builtin calls are putc(value), status(), and exit(value). No strings, globals, user procedures, multiply, divide, bit operators, or byte-input intrinsic are accepted. RILLBOOT adds the syntax needed to compile the compiler while retaining these implementations.

Both milestones use the same 40-byte symbol record layout, 4096-byte file blocks, checked two-word text counters, scanner, parser state, and RILL.TMP/RILL.BAK publication. Source rejection preserves an accepted RESULT.IR; a failed publication may leave recovery files.
