+++
title = "RILL language and compiler reference"
weight = 31
description = "The exact grammar, word semantics, portable services, and limits of the first implementation."
download = "RILL.IR"
+++

RILL has a small structured source language. Its compiler is written in the published IR86 language and emits IR86 source. IR86 and ASM86 then build the executable. RILL.IR is the compiler implementation; a .RIL file is a program supplied to it. The complete source does not contain native assembly escapes.

## Program and declaration form

```rill
fn main() {
    let mut x = 65;
    putc(x);
}
```

Exactly one `fn main()` is required. It has no arguments or result annotation. All declarations precede executable statements in its outer body. Each declaration is `let mut name = number;`, with a required unsigned decimal literal initializer. Names are single lowercase letters a through z. There is one flat set of twenty-six variables; duplicate declarations and undeclared uses are rejected. The required mut spelling identifies the one supported kind of binding.

Values are unsigned sixteen-bit words. Addition and subtraction wrap modulo 65536. Unary minus computes zero minus its operand in that same word domain: -1 is 65535. This does not select signed comparisons. No pointer, register, flag, or operating-system descriptor is a RILL source value in this implementation.

Keywords are lowercase and must be spelled completely. Whitespace may separate tokens, but not letters within a keyword or the characters of a two-character comparison. Comments begin with // and continue through the next line ending or source termination. There are no string literals, character literals, numeric radix prefixes, type annotations, or expression initializers in declarations.

## Grammar

The notation below describes forms rather than text to type. Braces and punctuation in quotes are source characters; alternatives are separated by a vertical bar. Repetition may occur zero or more times.

```text
program     = "fn" "main" "(" ")" "{" declarations statements "}"
declarations= repeated declaration
declaration = "let" "mut" name "=" number ";"
statements  = repeated statement
statement   = name "=" expression ";"
            | "putc" "(" expression ")" ";"
            | "exit" "(" expression ")" ";"
            | "if" condition block [ "else" block ]
            | "while" condition block
block       = "{" statements "}"
condition   = expression [ relation expression ]
relation    = "==" | "!=" | "<" | "<=" | ">" | ">="
expression  = primary repeated ( ("+" | "-") primary )
primary     = number | name | "(" expression ")" | "-" primary
            | "getc" "(" ")" | "status" "(" ")"
name        = one lowercase letter
number      = one or more decimal digits, value 0 through 65535
```

Binary + and - have equal precedence and associate left to right. Unary minus binds more tightly; parentheses select grouping. Every expression has one word value. Assignment replaces its variable and requires a semicolon. An empty block is valid; a stray semicolon is not an empty statement.

A condition without a relation is false at zero and true at every nonzero word. All ordering relations are **unsigned**. A comparison is allowed only at the outer level of an if or while condition. It does not yield a Boolean word for arithmetic. Thus `if x < 10 {}` is valid, while `putc(x < 10);` and `if (x < 10) {}` are rejected. Arithmetic parentheses inside a condition are valid.

An else belongs to its explicitly closed preceding if block. Both branches require braces; there is no else-if abbreviation. A while condition is evaluated before every iteration, so its body may execute zero times. There is no break or continue. exit terminates the entire program. Reaching the end of main returns zero.

## Runtime operations

| Source form | Defined action |
|---|---|
| `putc(expression);` | Write the low eight bits of the word; update service status |
| `getc()` | Return the next byte, or 65535 for EOF or error |
| `status()` | Return persistent service status: zero success, one failure |
| `exit(expression);` | Terminate with status equal to the word modulo 256 |

PUTC performs no newline conversion. Write 13 and 10 explicitly for a DOS CR/LF. getc() returns every byte value from zero through 255 without confusing 255 with EOF. EOF has status zero; an input error has status one. Arithmetic, assignment, conditions, and status() itself do not reset the status. Store the byte before reading status() when both results are needed.

putc is a statement and its count is discarded. Inspect status() to detect a failed output. The language does not automatically turn a service failure into program failure. The echo example checks both input and output explicitly. Terminal buffering and echo belong to the environment; redirected byte streams give reproducible checks.

The compiler emits the corresponding IR operations. No DOS interrupt number, hardware flag, or physical register is part of these source interfaces. File-opening services are used by the compiler's own IR implementation; this RILL subset exposes only the operations in the table.

## Deliberate language limits

Only main is a function. There are no user-defined procedures, parameters, automatic local frames, nested declarations, arrays, pointer operations, ownership rules, or memory-safety analysis. A single flat variable set keeps declaration checking separate from block parsing. Literal-only initializers allow declarations to be emitted before the IR MAIN label without buffering a second code stream.

There are no multiplication, division, remainder, shift, bitwise, floating-point, logical-and, or logical-or operators. Keeping two binary arithmetic operators makes their precedence and saved-operand discipline visible. Comparisons belong to structured control conditions so the generated IR expression stack is empty at every branch. Calls to unknown names are rejected rather than assumed to be library functions.

These are exact language restrictions, not statements about the capabilities of the processor or IR86. Unsupported source is an error; the compiler does not ignore it or pass it through as assembly.

## Compiler files and reports

The compiler reads SOURCE.RIL and, after full acceptance and successful source close, creates or truncates RESULT.IR. COPY selects a source program and preserves the accepted result under a distinct base name. Fixed work filenames keep filename-entry code out of the parser.

Success is `OK RESULT.IR nnnnn` with zero status. The number is the complete CR/LF IR text length. Failure is `ERROR nnnnn CODE nnnnn` with status one. The first number is LINE, initially one and advanced when LF is consumed. A failed console write exits with status four and may prevent the full report. CHECK must immediately print PASS or FAIL.

| Category | Meaning |
|---|---|
| 1 | Input open/read/close or result create/write/close failed |
| 2 | Syntax, punctuation, keyword suffix, invalid source byte, or unsupported form |
| 3 | Decimal literal exceeds 65535 |
| 4 | Variable/name context, duplicate declaration, undeclared use, or overlong word |
| 5 | Source, generated text, parser-depth, or saved-state capacity exceeded |

A missing primary may report category four because the primary parser tries the variable form after excluding its other alternatives. The report identifies where recognition stopped; look just before that token for a missing delimiter or operand. Every source statement is checked, including statements after exit and blocks which would not execute.

A source or input error leaves an older RESULT.IR untouched. A result I/O failure after CREATE can leave a partial file. Require a fresh OK and PASS before translating any result. IR86 and ASM86 have their own diagnostics and must each succeed independently.

## Implementation capacities

| Resource | Bound and reason |
|---|---|
| Source read | 4096 actual bytes, including whitespace and comments before termination |
| Generated IR | 1024 bytes, including CR/LF; fixed buffer checked before each store |
| Word spelling | At most six lowercase letters, enough for every defined keyword |
| Variables | Twenty-six single-letter mutable words |
| Active parser levels | Eight combined BODY and FACTOR calls, including the main body and current primary |
| Saved compiler state | Thirty-two words in FRAMES, checked before a save and restore |
| Numeric values | Unsigned 0–65535; no overflow during conversion |

BODY and FACTOR share DEPTH. For example, the main body plus six parenthesized primaries and the innermost primary fills eight active levels; one further parenthesis is rejected. A deeply nested block leaves less room for parentheses within it. These explicit bounds keep parser state and native calls modest. A long left-associative sum does not add one recursive level per term.

Printable ASCII, tab, CR, and LF are accepted by NEXT. Control-Z ends source text. A file NUL or any other control/high byte is rejected. CR is whitespace; line numbering counts LF. Leading zeroes in a number are allowed and do not change its radix. The byte-input operation of a compiled program is separate and preserves all byte values.

## Compiler helper interfaces

All compiler calls obey IR86: A carries the explicit input/result and the expression stack is empty across CALL. Work cells may change unless a row says they must survive. FRAMES saves names, pending operators, and block targets across recursive calls. It is separate from the emitted program's expression stack.

| Helper | Interface and state |
|---|---|
| CHAR | Input A; DEST zero selects console, one selects OUTBUF. Changes A, VALUE, and buffer OUTCOUNT |
| DIVIDE | Dividend A, nonzero STEP; remainder A and quotient COUNT. Changes VALUE |
| PAIR | Two nonzero packed ASCII bytes in A. Changes WORK, STEP, VALUE, COUNT, and A |
| NUMBER | Input A; prints five decimal digits. Changes WORK, PLACE, STEP, VALUE, COUNT, and A |
| NAMEWORD | Input A stored at PLACE; PLACE advances by two. Changes VALUE |
| SOURCENAME / RESULTNAME | Fill NAMEBUF with a terminated fixed name; change PLACE and VALUE |
| NEXT | Advance CH; update LINE, READTOTAL, and COUNT; check INPUT handle service status |
| LEX | Set TOK, SUFFIX, and numeric TOKENVAL; retain following byte in CH; changes formatting work cells |
| EXPECT | Required token A and WANTTAIL; compare both token groups, clear WANTTAIL, then LEX |
| ENDTOKEN | Expected suffix A for a selected word; check it and call LEX |
| VARADDRESS / USEVAR | Check TOK as a variable; return table pointer / declared letter; update VARNAME |
| SAVE / RESTORE | Save A / return latest saved word; update SAVECNT; SAVE also uses VALUE |
| EXPR / FACTOR | Consume an expression / primary and emit its IR; pending state belongs in FRAMES |
| BODY / BLOCK | Consume statements through } / require { first; update shared DEPTH |
| NEWLABEL | Advance LABELNO and return its number in A |
| DEFLABEL / JUMPLABEL | Input label number A; emit its definition / jump, using BRANCH and formatting cells |
| CONDITION | False target A; consume a condition, preserving target in BRANCH until emitted |
| WRITEFILE | Create, write, and close RESULT.IR; reuse INPUT after successful source close |

Formatting and scanning share WORK, PLACE, STEP, VALUE, and COUNT because their active lifetimes do not overlap. NUMBER calls CHAR, which preserves WORK, PLACE, and STEP. A scanner calls NEXT, which changes COUNT only after the current digit or letter calculation has finished. TOKENVAL temporarily holds an already parsed relation after the right expression is complete. READTOTAL becomes the error category only on a terminal failure path. VARNAME temporarily holds a restored end target only between label-output calls, before it is saved again. These shared cells must not replace FRAMES for state needed across a recursive parse.

The word scanner encodes lowercase letters as digits one through twenty-six in base 32, split into groups of at most three. This is exact, not a hash. TOK adds 32768 for a multi-letter word; a single-letter variable keeps its ASCII code. SUFFIX holds the second group. fn, if, and punctuation have an empty suffix; main has suffix fourteen. Both groups are checked before a reserved spelling is consumed. Numeric TOK is 65535 and paired comparisons are 200–203, outside the word codes.

## First backend profile

The compiler source uses only the published processor-independent IR operations and runtime services. Its DOS build is 5,173 bytes; its generated assembly text is 24,676 bytes. It uses 255 definitions including the IR86 header, generated comparison skips, and runtime, within ASM86's 256-entry table. No extension of BOOTASM, ASM86, or IR86 is needed.

The native environment must satisfy IR86's documented full-segment entry check and high-stack reservation. The compiler's bounded data is part of its image. Its result is IR text, which must still pass IR86 and ASM86 before execution. The finite current image, text, and definition budgets describe this implementation and backend; they do not give RILL source programs physical register or address semantics.
