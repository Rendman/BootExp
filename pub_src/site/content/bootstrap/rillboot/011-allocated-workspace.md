+++
title = "11 \u00b7 Allocated workspace"
weight = 11
description = "Allocate workspace through an opaque block handle. A block is separate from ordinary pointers into the program image; check status before using it."
download = "RB11.IR"
download_group = "tools/rillboot"
reader_names = 1
aliases = ["/bootstrap/rb/011-checked-workspace-access/", "/bootstrap/rb/044-rb-quoted-source-text/", "/bootstrap/rb/045-rb-consume-an-exact-token/", "/bootstrap/rb/046-rb-compare-the-whole-keyword/", "/bootstrap/rb/047-rb-save-an-explicit-spelling/", "/bootstrap/rb/048-rb-word-fields-in-an-opaque-block/", "/bootstrap/rb/049-rb-byte-fields-in-an-opaque-block/", "/bootstrap/rb/050-rb-write-one-explicit-record-field/", "/bootstrap/rb/051-rb-initialize-a-complete-symbol/", "/bootstrap/rb/052-rb-add-a-global-definition/", "/bootstrap/rb/053-rb-a-separate-local-name-region/", "/bootstrap/rb/054-rb-search-exact-names-from-the-inside-out/", "/bootstrap/rb/055-rb-the-global-namespace/", "/bootstrap/rb/056-rb-resolve-a-current-binding/", "/bootstrap/rb/057-rb-write-a-nonempty-output-block/", "/bootstrap/rb/058-rb-append-one-streamed-byte/", "/bootstrap/rb/059-rb-append-a-text-template/", "/bootstrap/rb/060-rb-print-an-ir-operand/", "/bootstrap/rb/061-rb-terminate-an-emitted-record/", "/bootstrap/rb/062-rb-allocate-a-source-label-number/", "/bootstrap/rb/063-rb-define-one-compiler-label/", "/bootstrap/rb/064-rb-emit-a-label-operand/", "/bootstrap/rb/065-rb-emit-a-saved-symbol-spelling/", "/bootstrap/rb/066-rb-a-table-of-portable-services/", "/bootstrap/rb/067-rb-call-names-and-forward-declarations/", "/bootstrap/rb/068-rb-operator-precedence/", "/bootstrap/rb/069-rb-emit-a-word-operation/", "/bootstrap/rb/070-rb-precedence-with-a-numeric-primary/", "/bootstrap/rb/071-rb-parentheses-strings-and-unary-values/", "/bootstrap/rb/072-rb-variables-and-addressed-storage/", "/bootstrap/rb/073-rb-nested-argument-expressions/", "/bootstrap/rb/074-rb-a-global-word-declaration/", "/bootstrap/rb/075-rb-a-global-byte-extent/", "/bootstrap/rb/076-rb-a-local-slot-and-initializer/", "/bootstrap/rb/077-rb-enter-and-leave-a-lexical-scope/", "/bootstrap/rb/078-rb-statements-and-structured-branches/", "/bootstrap/rb/079-rb-a-named-procedure-definition/", "/bootstrap/rb/080-rb-the-complete-streamed-compiler/", "/bootstrap/rb/081-word-expressions/", "/bootstrap/rb/082-arguments-and-saved-expressions/", "/bootstrap/rb/083-recursive-procedures/", "/bootstrap/rb/084-scopes-and-local-addresses/", "/bootstrap/rb/085-indexed-byte-storage/", "/bootstrap/rb/086-literal-strings/", "/bootstrap/rb/087-opaque-memory-blocks/", "/bootstrap/rb/088-counted-file-transfer/", "/bootstrap/rill/044-rb-quoted-source-text/", "/bootstrap/rill/045-rb-consume-an-exact-token/", "/bootstrap/rill/046-rb-compare-the-whole-keyword/", "/bootstrap/rill/047-rb-save-an-explicit-spelling/", "/bootstrap/rill/048-rb-word-fields-in-an-opaque-block/", "/bootstrap/rill/049-rb-byte-fields-in-an-opaque-block/", "/bootstrap/rill/050-rb-write-one-explicit-record-field/", "/bootstrap/rill/051-rb-initialize-a-complete-symbol/", "/bootstrap/rill/052-rb-add-a-global-definition/", "/bootstrap/rill/053-rb-a-separate-local-name-region/", "/bootstrap/rill/054-rb-search-exact-names-from-the-inside-out/", "/bootstrap/rill/055-rb-the-global-namespace/", "/bootstrap/rill/056-rb-resolve-a-current-binding/", "/bootstrap/rill/057-rb-write-a-nonempty-output-block/", "/bootstrap/rill/058-rb-append-one-streamed-byte/", "/bootstrap/rill/059-rb-append-a-text-template/", "/bootstrap/rill/060-rb-print-an-ir-operand/", "/bootstrap/rill/061-rb-terminate-an-emitted-record/", "/bootstrap/rill/062-rb-allocate-a-source-label-number/", "/bootstrap/rill/063-rb-define-one-compiler-label/", "/bootstrap/rill/064-rb-emit-a-label-operand/", "/bootstrap/rill/065-rb-emit-a-saved-symbol-spelling/", "/bootstrap/rill/066-rb-a-table-of-portable-services/", "/bootstrap/rill/067-rb-call-names-and-forward-declarations/", "/bootstrap/rill/068-rb-operator-precedence/", "/bootstrap/rill/069-rb-emit-a-word-operation/", "/bootstrap/rill/070-rb-precedence-with-a-numeric-primary/", "/bootstrap/rill/071-rb-parentheses-strings-and-unary-values/", "/bootstrap/rill/072-rb-variables-and-addressed-storage/", "/bootstrap/rill/073-rb-nested-argument-expressions/", "/bootstrap/rill/074-rb-a-global-word-declaration/", "/bootstrap/rill/075-rb-a-global-byte-extent/", "/bootstrap/rill/076-rb-a-local-slot-and-initializer/", "/bootstrap/rill/077-rb-enter-and-leave-a-lexical-scope/", "/bootstrap/rill/078-rb-statements-and-structured-branches/", "/bootstrap/rill/079-rb-a-named-procedure-definition/", "/bootstrap/rill/080-rb-the-complete-streamed-compiler/", "/bootstrap/rill/081-word-expressions/", "/bootstrap/rill/082-arguments-and-saved-expressions/", "/bootstrap/rill/083-recursive-procedures/", "/bootstrap/rill/084-scopes-and-local-addresses/", "/bootstrap/rill/085-indexed-byte-storage/", "/bootstrap/rill/086-literal-strings/", "/bootstrap/rill/087-opaque-memory-blocks/", "/bootstrap/rill/088-counted-file-transfer/"]
url = "/bootstrap/rb/011-allocated-workspace/"
+++

Allocate workspace through an opaque block handle. A block is separate from ordinary pointers into the program image; check status before using it.

Retain every earlier language feature. This checkpoint edits the complete compiler; it does not replace it with a helper-only driver.

## Enter the source

Copy RB10.IR to RB11.IR. Apply the following edits from the bottom of the old file upward, using the old physical positions and unchanged context. Keep all other source.

### Edit at old physical position 1768

Unchanged source before the edit:

```ir
RETURN

PROC BUILTIN 0 5
```

Remove:

```ir
LITS "PUTC\01\0POP\nPUTC\0STATUS\00\0STATUS\0OPEN\01\0POP\nOPEN\0CREATE\01\0POP\nCREATE\0CLOSE\01\0POP\nCLOSE\0READ\03\0POP\nREAD\0WRITE\03\0POP\nWRITE\0EXISTS\01\0POP\nEXISTS\0DELETE\01\0POP\nDELETE\0RENAME\02\0POP\nRENAME\0LOAD8\01\0POP\nFETCHB\0EXIT\01\0POP\nEXIT\0\0"
```

Insert in its place:

```ir
LITS "PUTC\01\0POP\nPUTC\0STATUS\00\0STATUS\0OPEN\01\0POP\nOPEN\0CREATE\01\0POP\nCREATE\0CLOSE\01\0POP\nCLOSE\0READ\03\0POP\nREAD\0WRITE\03\0POP\nWRITE\0EXISTS\01\0POP\nEXISTS\0DELETE\01\0POP\nDELETE\0RENAME\02\0POP\nRENAME\0ALLOC\01\0POP\nALLOC\0FREE\01\0POP\nFREEBLOCK\0LOAD8\01\0POP\nFETCHB\0EXIT\01\0POP\nEXIT\0\0"
```

The following old source remains:

```ir
SETLOCAL 0
LABEL BUILTINNEXT
```

## Build and check

```dos
COPY RB11.IR SOURCE.IR
CHECK IRKEEP
COPY RESULT.ASM SOURCE.ASM
CHECK ASMAKEEP
```

Require fresh OK and PASS reports before each following copy. The assembler must report `OK RESULT.COM 21043 bytes`. Save RESULT.COM as RB11.COM. VIEW.BAS must show length 21043.

Create TRB11.RIL:

```rill
fn main(){let mut h=alloc(100);free(h);return status();}
```

```dos
COPY TRB11.RIL SOURCE.RIL
```

```dos
CHECK RB11
```

Require:

```text
OK RESULT.IR 0000000173
PASS
```

Inspect RESULT.IR with VIEW.BAS. Require length 173 bytes and these complete bytes:

```text
50 52 4F 43 20 46 5F 4D 41 49 4E 20 30 30 30 30
30 20 31 36 0D 0A 4C 49 54 20 30 30 31 30 30 0D
0A 50 55 53 48 0D 0A 50 4F 50 0D 0A 41 4C 4C 4F
43 0D 0A 53 45 54 4C 4F 43 41 4C 20 30 30 30 30
30 0D 0A 4C 4F 43 41 4C 20 30 30 30 30 30 0D 0A
50 55 53 48 0D 0A 50 4F 50 0D 0A 46 52 45 45 42
4C 4F 43 4B 0D 0A 53 54 41 54 55 53 0D 0A 52 45
54 55 52 4E 0D 0A 4C 49 54 20 30 0D 0A 52 45 54
55 52 4E 0D 0A 50 52 4F 43 20 4D 41 49 4E 20 30
20 30 0D 0A 49 4E 56 4F 4B 45 20 46 5F 4D 41 49
4E 20 30 0D 0A 52 45 54 55 52 4E 0D 0A
```

This is a complete IR program. Translate it with IRKEEP, assemble its accepted output with ASMAKEEP, and save RESULT.COM as TRY.COM. Require fresh OK and PASS before both copies. VIEW.BAS must report length 1075. CHECK TRY reports PASS.

## Check the new boundary

Use this separate rejected source:

```rill
fn main(){putc(65536);}
```

Copy it to SOURCE.RIL and run CHECK RB11. Require:

```text
ERROR 0000000001 CODE 00003
FAIL
```

An unexpected PASS fails this check. Keep a copy of the accepted result before testing; it must remain unchanged.

