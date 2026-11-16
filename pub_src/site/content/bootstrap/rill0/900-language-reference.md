+++
title = "RILL0 language reference"
weight = 900
description = "The accepted language and its bounded implementation."
download = "RILL0.IR"
download_group = "tools/rill0"
reader_names = 1
aliases = ["/bootstrap/rill/31-reference/"]
url = "/bootstrap/rill/900-language-reference/"
+++

Words range from 0 through 65535; arithmetic wraps and ordering is unsigned. Names begin with a letter or underscore, continue with letters, digits, or underscores, and are folded to uppercase with complete spelling, up to 24 characters. Source uses decimal word literals, ASCII text, // comments ending at LF or EOF, and brace-enclosed bodies. Use DOS CR/LF disk text. Local bindings use `let mut name=expression;`, assignment, lexical braces, `if`/`else`, `while`, and `return expression;`. Expressions have parentheses, +, -, and unsigned comparisons. Addition/subtraction bind more tightly than comparisons; each level associates left to right. Zero is false and any nonzero word is true. return; and normal fall-through return zero. Each expression and block has a checked nesting limit of sixteen. At most sixteen local word slots are live in a procedure.

## Command-line filenames

```dos
CHECK RILL0 INPUT.RIL OUTPUT.IR
```

DOS supplies the names in the PSP command tail. The native entry binding copies them into owned zero-terminated storage before file services. The language-level interface supplies argument counts and ordinary string pointers through portable services. CHECK.BAT forwards the arguments and reports status immediately. No arguments select SOURCE.RIL and RESULT.IR. Use unquoted 8.3 disk names in the current directory: letters, digits, underscore and hyphen, with an optional extension. Paths, switches, excess arguments and overlong names are rejected. Keep selected files distinct from each other and from RILL.TMP and RILL.BAK. Those temporary/backup names remain reserved.

Success reports the selected result name. Rejected source preserves that accepted result; recovery rules apply to the selected name. Early diagnostic writers may deliberately retain a temporary file for inspection, as stated in their lesson.

There is exactly one argument-free `fn main(){...}`. Its builtin calls are putc(value), status(), and exit(value). No strings, globals, user procedures, multiply, divide, bit operators, or byte-input intrinsic are accepted. RILLBOOT adds the syntax needed to compile the compiler while retaining these implementations.

Both milestones use the same 40-byte symbol record layout, 4096-byte file blocks, checked two-word text counters, scanner, parser state, and RILL.TMP/RILL.BAK publication. Source rejection preserves an accepted RESULT.IR; a failed publication may leave recovery files.
