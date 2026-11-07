+++
title = "12 \u00b7 Checked workspace access"
weight = 12
description = "Access allocated blocks through checked byte offsets. A canonical word needs two valid bytes; the symbol record layout stays unchanged."
download = "RB12.IR"
download_group = "tools/rillboot"
reader_names = 1
+++

Access allocated blocks through checked byte offsets. A canonical word needs two valid bytes; the symbol record layout stays unchanged.

Retain every earlier language feature. This checkpoint edits the complete compiler; it does not replace it with a helper-only driver.

## Enter the source

Copy RB11.IR to RB12.IR. Apply the following edits from the bottom of the old file upward, using the old physical positions and unchanged context. Keep all other source.

### Edit at old physical position 1768

Unchanged source before the edit:

```ir
RETURN

PROC BUILTIN 0 5
```

Remove:

```ir
LITS "PUTC\01\0POP\nPUTC\0STATUS\00\0STATUS\0OPEN\01\0POP\nOPEN\0CREATE\01\0POP\nCREATE\0CLOSE\01\0POP\nCLOSE\0READ\03\0POP\nREAD\0WRITE\03\0POP\nWRITE\0EXISTS\01\0POP\nEXISTS\0DELETE\01\0POP\nDELETE\0RENAME\02\0POP\nRENAME\0ALLOC\01\0POP\nALLOC\0FREE\01\0POP\nFREEBLOCK\0LOAD8\01\0POP\nFETCHB\0EXIT\01\0POP\nEXIT\0\0"
```

Insert in its place:

```ir
LITS "PUTC\01\0POP\nPUTC\0STATUS\00\0STATUS\0OPEN\01\0POP\nOPEN\0CREATE\01\0POP\nCREATE\0CLOSE\01\0POP\nCLOSE\0READ\03\0POP\nREAD\0WRITE\03\0POP\nWRITE\0EXISTS\01\0POP\nEXISTS\0DELETE\01\0POP\nDELETE\0RENAME\02\0POP\nRENAME\0ALLOC\01\0POP\nALLOC\0FREE\01\0POP\nFREEBLOCK\0GET8\02\0POP\nGET8\0GET16\02\0POP\nGET16\0SET8\03\0POP\nSET8\0SET16\03\0POP\nSET16\0LOAD8\01\0POP\nFETCHB\0EXIT\01\0POP\nEXIT\0\0"
```

The following old source remains:

```ir
SETLOCAL 0
LABEL BUILTINNEXT
```

## Build and check

```dos
COPY RB12.IR SOURCE.IR
CHECK IRKEEP
COPY RESULT.ASM SOURCE.ASM
CHECK ASMAKEEP
```

Require fresh OK and PASS reports before each following copy. The assembler must report `OK RESULT.COM 21111 bytes`. Save RESULT.COM as RB12.COM. VIEW.BAS must show length 21111.

Create TRB12.RIL:

```rill
fn main(){
 let mut h=alloc(100);if status(){return 1;}
 set16(h,98,4660);if status(){free(h);return 1;}
 let mut n=get16(h,98);
 set8(h,0,65);putc(get8(h,0));
 free(h);return n!=4660;
}
```

```dos
COPY TRB12.RIL SOURCE.RIL
```

```dos
CHECK RB12
```

Require:

```text
OK RESULT.IR 0000000656
PASS
```

Inspect RESULT.IR with VIEW.BAS. Require length 656 bytes and these complete bytes:

```text
50 52 4F 43 20 46 5F 4D 41 49 4E 20 30 30 30 30
30 20 31 36 0D 0A 4C 49 54 20 30 30 31 30 30 0D
0A 50 55 53 48 0D 0A 50 4F 50 0D 0A 41 4C 4C 4F
43 0D 0A 53 45 54 4C 4F 43 41 4C 20 30 30 30 30
30 0D 0A 53 54 41 54 55 53 0D 0A 4A 5A 20 42 5F
30 30 30 30 31 0D 0A 4C 49 54 20 30 30 30 30 31
0D 0A 52 45 54 55 52 4E 0D 0A 4A 4D 50 20 42 5F
30 30 30 30 32 0D 0A 4C 41 42 45 4C 20 42 5F 30
30 30 30 31 0D 0A 4C 41 42 45 4C 20 42 5F 30 30
30 30 32 0D 0A 4C 4F 43 41 4C 20 30 30 30 30 30
0D 0A 50 55 53 48 0D 0A 4C 49 54 20 30 30 30 39
38 0D 0A 50 55 53 48 0D 0A 4C 49 54 20 30 34 36
36 30 0D 0A 50 55 53 48 0D 0A 50 4F 50 0D 0A 53
45 54 31 36 0D 0A 53 54 41 54 55 53 0D 0A 4A 5A
20 42 5F 30 30 30 30 33 0D 0A 4C 4F 43 41 4C 20
30 30 30 30 30 0D 0A 50 55 53 48 0D 0A 50 4F 50
0D 0A 46 52 45 45 42 4C 4F 43 4B 0D 0A 4C 49 54
20 30 30 30 30 31 0D 0A 52 45 54 55 52 4E 0D 0A
4A 4D 50 20 42 5F 30 30 30 30 34 0D 0A 4C 41 42
45 4C 20 42 5F 30 30 30 30 33 0D 0A 4C 41 42 45
4C 20 42 5F 30 30 30 30 34 0D 0A 4C 4F 43 41 4C
20 30 30 30 30 30 0D 0A 50 55 53 48 0D 0A 4C 49
54 20 30 30 30 39 38 0D 0A 50 55 53 48 0D 0A 50
4F 50 0D 0A 47 45 54 31 36 0D 0A 53 45 54 4C 4F
43 41 4C 20 30 30 30 30 31 0D 0A 4C 4F 43 41 4C
20 30 30 30 30 30 0D 0A 50 55 53 48 0D 0A 4C 49
54 20 30 30 30 30 30 0D 0A 50 55 53 48 0D 0A 4C
49 54 20 30 30 30 36 35 0D 0A 50 55 53 48 0D 0A
50 4F 50 0D 0A 53 45 54 38 0D 0A 4C 4F 43 41 4C
20 30 30 30 30 30 0D 0A 50 55 53 48 0D 0A 4C 49
54 20 30 30 30 30 30 0D 0A 50 55 53 48 0D 0A 50
4F 50 0D 0A 47 45 54 38 0D 0A 50 55 53 48 0D 0A
50 4F 50 0D 0A 50 55 54 43 0D 0A 4C 4F 43 41 4C
20 30 30 30 30 30 0D 0A 50 55 53 48 0D 0A 50 4F
50 0D 0A 46 52 45 45 42 4C 4F 43 4B 0D 0A 4C 4F
43 41 4C 20 30 30 30 30 31 0D 0A 50 55 53 48 0D
0A 4C 49 54 20 30 34 36 36 30 0D 0A 43 4E 45 0D
0A 52 45 54 55 52 4E 0D 0A 4C 49 54 20 30 0D 0A
52 45 54 55 52 4E 0D 0A 50 52 4F 43 20 4D 41 49
4E 20 30 20 30 0D 0A 49 4E 56 4F 4B 45 20 46 5F
4D 41 49 4E 20 30 0D 0A 52 45 54 55 52 4E 0D 0A
```

This is a complete IR program. Translate it with IRKEEP, assemble its accepted output with ASMAKEEP, and save RESULT.COM as TRY.COM. Require fresh OK and PASS before both copies. VIEW.BAS must report length 1230. CHECK TRY displays `A` and reports PASS.

## Check the new boundary

Use this separate rejected source:

```rill
fn main(){putc(65536);}
```

Copy it to SOURCE.RIL and run CHECK RB12. Require:

```text
ERROR 0000000001 CODE 00003
FAIL
```

An unexpected PASS fails this check. Keep a copy of the accepted result before testing; it must remain unchanged.

```dos
COPY RB12.COM RILLBOOT.COM
```

RILLBOOT.IR is this final source. Continue with the [compiler written in RILL](../../rc/index.html).
