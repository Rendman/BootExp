+++
title = "40 \u00b7 Keeping Values Across a Procedure Call"
weight = 40
description = "Evaluate arguments from left to right and save each emitted result."
download = "RB40.IR"
download_group = "tools/rillboot"
aliases = ["/bootstrap/rill/073-rb-nested-argument-expressions/"]
reader_names = 1
+++

## The working parts

Evaluate arguments from left to right and save each emitted result. Check the complete argument count against the intrinsic or procedure record. INVOKE consumes precisely those words and preserves older expression operands.

## Enter the source

Copy RB39.IR to RB40.IR. Apply edits **from the bottom of the old file upward**. Physical positions refer to that unchanged old file; use the printed context to identify each place. Keep all other source.

### Edit 1

Unchanged source immediately before the edit:

```ir
PROC CALLARGS 2 0
LIT 2
PUSH
```

Remove this source at old physical positions 1251–1251 in RB39.IR:

```ir
INVOKE ERROR 1
```

Replace it with:

```ir
LIT 48
SUB
PUSH
LOCAL 0
CNE
JNZ NAMEFAIL
PARAM 1
CALL OUTSTR
CALL NEWLINE
LIT 0
RETURN
LABEL ARGUSER
PARAM 0
PUSH
LIT 32
ADD
CALL TWORD
SETLOCAL 1
PUSH
LIT 3
CEQ
JNZ ARGFUNCTION
LOCAL 1
PUSH
LIT 4
CNE
JNZ NAMEFAIL
LABEL ARGFUNCTION
PARAM 0
PUSH
LIT 34
ADD
CALL TWORD
SETLOCAL 1
PUSH
LIT 65535
CEQ
JNZ ARGFIRST
LOCAL 1
PUSH
LOCAL 0
CNE
JNZ NAMEFAIL
JMP ARGEMIT
LABEL ARGFIRST
PARAM 0
PUSH
LIT 34
ADD
PUSH
LOCAL 0
PUSH
INVOKE WRITEFIELD 2
LABEL ARGEMIT
LITS "INVOKE F_"
CALL OUTSTR
PARAM 0
CALL OUTNAME
LIT 32
CALL OUTCHAR
LOCAL 0
CALL OUTNUM
CALL NEWLINE
```

The following old source remains in place:

```ir
LIT 0
RETURN
```

### Edit 2

Unchanged source immediately before the edit:

```ir

PROC CALLARGS 2 0
LIT 2
```

Insert after old physical line 1249.

Insert:

```ir
SUB
FETCHB
```

The following old source remains in place:

```ir
PUSH
INVOKE ERROR 1
```

### Edit 3

Unchanged source immediately before the edit:

```ir
LOCAL 0
RETURN
```

Remove this source at old physical positions 1248–1248 in RB39.IR:

```ir
PROC CALLARGS 2 0
```

Replace it with:

```ir
PROC CALLARGS 2 3
LIT 0
SETLOCAL 0
LIT 40
PUSH
INVOKE EXPECT 1
LD TOK
PUSH
LIT 41
CEQ
JNZ ARGSEND
LABEL ARGLOOP
LOCAL 0
PUSH
LIT 16
CUGE
JNZ CAPFAIL
LIT 1
PUSH
INVOKE EXPR 1
LITS "PUSH\r\n"
CALL OUTSTR
LOCAL 0
PUSH
LIT 1
ADD
SETLOCAL 0
LD TOK
PUSH
LIT 41
CEQ
JNZ ARGSEND
LIT 44
PUSH
INVOKE EXPECT 1
JMP ARGLOOP
LABEL ARGSEND
CALL LEX
PARAM 1
JZ ARGUSER
PUSH
```

The following old source remains in place:

```ir
LIT 2
PUSH
```

## Build this stopping point

```dos
COPY RB40.IR SOURCE.IR
```

```dos
CHECK IWKEEP
COPY RESULT.ASM SOURCE.ASM
CHECK ASMAKEEP
```

Require IR86 `OK RESULT.ASM 0000055127 text bytes` and PASS **before** the copy. Require assembler `OK RESULT.COM 18735 bytes` and PASS before saving:

```dos
COPY RESULT.COM RB40.COM
```

VIEW.BAS must report RB40.COM length 18735 bytes. Keep this executable and its source together.

## Acceptance check

Create TRB40.RIL with COPY CON or a plain-text editor. Finish COPY CON with Ctrl-Z and Enter:

```rill
putc(65)
```

```dos
COPY TRB40.RIL SOURCE.RIL
```

```dos
CHECK RB40
```

The checker must report PASS. Inspect the emitted file below.

Use VIEW.BAS to inspect RILL.TMP. Require length 28 bytes. The complete bytes must be:

```text
4C 49 54 20 30 30 30 36 35 0D 0A 50 55 53 48 0D
0A 50 4F 50 0D 0A 50 55 54 43 0D 0A
```

This is an IR fragment for inspection. Do not translate it as a complete program or execute any file with its name.

After inspection, delete this deliberately created RILL.TMP before another checkpoint. The file is diagnostic text, not an interrupted accepted compiler build.

## A rejection or boundary check

Create XRB40.RIL:

```rill
get8(1)
```

```dos
COPY XRB40.RIL SOURCE.RIL
CHECK RB40
```

Require:

```text
ERROR 0000000001 CODE 00004
FAIL
```

An unexpected PASS fails the rejection. The pre-existing RESULT.IR must remain unchanged; preserve a copy before the test.

## If the result differs

Compare CALLARGS with the printed addition. Check its arguments and saved state across calls, then inspect the generated text or bytes.
