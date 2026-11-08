+++
title = "10 \u00b7 Publishing accepted files"
weight = 10
description = "Add existence, deletion, and rename for recoverable publication. Temporary ownership and the previous accepted result remain distinct states."
download = "RB10.IR"
download_group = "tools/rillboot"
reader_names = 1
aliases = ["/bootstrap/rb/010-allocated-workspace/", "/bootstrap/rb/043-rb-checked-decimal-words/", "/bootstrap/rill/043-rb-checked-decimal-words/"]
url = "/bootstrap/rb/010-publishing-accepted-files/"
+++

Add existence, deletion, and rename for recoverable publication. Temporary ownership and the previous accepted result remain distinct states.

Retain every earlier language feature. This checkpoint edits the complete compiler; it does not replace it with a helper-only driver.

## Enter the source

Copy RB09.IR to RB10.IR. Apply the following edits from the bottom of the old file upward, using the old physical positions and unchanged context. Keep all other source.

### Edit at old physical position 1768

Unchanged source before the edit:

```ir
RETURN

PROC BUILTIN 0 5
```

Remove:

```ir
LITS "PUTC\01\0POP\nPUTC\0STATUS\00\0STATUS\0OPEN\01\0POP\nOPEN\0CREATE\01\0POP\nCREATE\0CLOSE\01\0POP\nCLOSE\0READ\03\0POP\nREAD\0WRITE\03\0POP\nWRITE\0LOAD8\01\0POP\nFETCHB\0EXIT\01\0POP\nEXIT\0\0"
```

Insert in its place:

```ir
LITS "PUTC\01\0POP\nPUTC\0STATUS\00\0STATUS\0OPEN\01\0POP\nOPEN\0CREATE\01\0POP\nCREATE\0CLOSE\01\0POP\nCLOSE\0READ\03\0POP\nREAD\0WRITE\03\0POP\nWRITE\0EXISTS\01\0POP\nEXISTS\0DELETE\01\0POP\nDELETE\0RENAME\02\0POP\nRENAME\0LOAD8\01\0POP\nFETCHB\0EXIT\01\0POP\nEXIT\0\0"
```

The following old source remains:

```ir
SETLOCAL 0
LABEL BUILTINNEXT
```

## Build and check

```dos
COPY RB10.IR SOURCE.IR
CHECK IRKEEP
COPY RESULT.ASM SOURCE.ASM
CHECK ASMAKEEP
```

Require fresh OK and PASS reports before each following copy. The assembler must report `OK RESULT.COM 21004 bytes`. Save RESULT.COM as RB10.COM. VIEW.BAS must show length 21004.

Create TRB10.RIL:

```rill
bytes b[1];
fn main(){
 b[0]=65;
 delete("OLD.TXT");if status(){return 1;}
 let mut h=create("TEMP.TXT");if status(){return 1;}
 if write(h,b,1)!=1{return 1;}
 close(h);if status(){return 1;}
 rename("TEMP.TXT","OLD.TXT");if status(){return 1;}
 if exists("TEMP.TXT"){return 1;}
 return exists("OLD.TXT")!=1;
}
```

```dos
COPY TRB10.RIL SOURCE.RIL
```

```dos
CHECK RB10
```

Require:

```text
OK RESULT.IR 0000000989
PASS
```

Inspect RESULT.IR with VIEW.BAS. Require length 989 bytes and these complete bytes:

```text
42 55 46 46 45 52 20 56 5F 42 20 30 30 30 30 31
0D 0A 50 52 4F 43 20 46 5F 4D 41 49 4E 20 30 30
30 30 30 20 31 36 0D 0A 41 44 44 52 20 56 5F 42
0D 0A 50 55 53 48 0D 0A 4C 49 54 20 30 30 30 30
30 0D 0A 41 44 44 0D 0A 50 55 53 48 0D 0A 4C 49
54 20 30 30 30 36 35 0D 0A 50 55 54 42 0D 0A 4C
49 54 53 20 22 4F 4C 44 2E 54 58 54 22 0D 0A 50
55 53 48 0D 0A 50 4F 50 0D 0A 44 45 4C 45 54 45
0D 0A 53 54 41 54 55 53 0D 0A 4A 5A 20 42 5F 30
30 30 30 31 0D 0A 4C 49 54 20 30 30 30 30 31 0D
0A 52 45 54 55 52 4E 0D 0A 4A 4D 50 20 42 5F 30
30 30 30 32 0D 0A 4C 41 42 45 4C 20 42 5F 30 30
30 30 31 0D 0A 4C 41 42 45 4C 20 42 5F 30 30 30
30 32 0D 0A 4C 49 54 53 20 22 54 45 4D 50 2E 54
58 54 22 0D 0A 50 55 53 48 0D 0A 50 4F 50 0D 0A
43 52 45 41 54 45 0D 0A 53 45 54 4C 4F 43 41 4C
20 30 30 30 30 30 0D 0A 53 54 41 54 55 53 0D 0A
4A 5A 20 42 5F 30 30 30 30 33 0D 0A 4C 49 54 20
30 30 30 30 31 0D 0A 52 45 54 55 52 4E 0D 0A 4A
4D 50 20 42 5F 30 30 30 30 34 0D 0A 4C 41 42 45
4C 20 42 5F 30 30 30 30 33 0D 0A 4C 41 42 45 4C
20 42 5F 30 30 30 30 34 0D 0A 4C 4F 43 41 4C 20
30 30 30 30 30 0D 0A 50 55 53 48 0D 0A 41 44 44
52 20 56 5F 42 0D 0A 50 55 53 48 0D 0A 4C 49 54
20 30 30 30 30 31 0D 0A 50 55 53 48 0D 0A 50 4F
50 0D 0A 57 52 49 54 45 0D 0A 50 55 53 48 0D 0A
4C 49 54 20 30 30 30 30 31 0D 0A 43 4E 45 0D 0A
4A 5A 20 42 5F 30 30 30 30 35 0D 0A 4C 49 54 20
30 30 30 30 31 0D 0A 52 45 54 55 52 4E 0D 0A 4A
4D 50 20 42 5F 30 30 30 30 36 0D 0A 4C 41 42 45
4C 20 42 5F 30 30 30 30 35 0D 0A 4C 41 42 45 4C
20 42 5F 30 30 30 30 36 0D 0A 4C 4F 43 41 4C 20
30 30 30 30 30 0D 0A 50 55 53 48 0D 0A 50 4F 50
0D 0A 43 4C 4F 53 45 0D 0A 53 54 41 54 55 53 0D
0A 4A 5A 20 42 5F 30 30 30 30 37 0D 0A 4C 49 54
20 30 30 30 30 31 0D 0A 52 45 54 55 52 4E 0D 0A
4A 4D 50 20 42 5F 30 30 30 30 38 0D 0A 4C 41 42
45 4C 20 42 5F 30 30 30 30 37 0D 0A 4C 41 42 45
4C 20 42 5F 30 30 30 30 38 0D 0A 4C 49 54 53 20
22 54 45 4D 50 2E 54 58 54 22 0D 0A 50 55 53 48
0D 0A 4C 49 54 53 20 22 4F 4C 44 2E 54 58 54 22
0D 0A 50 55 53 48 0D 0A 50 4F 50 0D 0A 52 45 4E
41 4D 45 0D 0A 53 54 41 54 55 53 0D 0A 4A 5A 20
42 5F 30 30 30 30 39 0D 0A 4C 49 54 20 30 30 30
30 31 0D 0A 52 45 54 55 52 4E 0D 0A 4A 4D 50 20
42 5F 30 30 30 31 30 0D 0A 4C 41 42 45 4C 20 42
5F 30 30 30 30 39 0D 0A 4C 41 42 45 4C 20 42 5F
30 30 30 31 30 0D 0A 4C 49 54 53 20 22 54 45 4D
50 2E 54 58 54 22 0D 0A 50 55 53 48 0D 0A 50 4F
50 0D 0A 45 58 49 53 54 53 0D 0A 4A 5A 20 42 5F
30 30 30 31 31 0D 0A 4C 49 54 20 30 30 30 30 31
0D 0A 52 45 54 55 52 4E 0D 0A 4A 4D 50 20 42 5F
30 30 30 31 32 0D 0A 4C 41 42 45 4C 20 42 5F 30
30 30 31 31 0D 0A 4C 41 42 45 4C 20 42 5F 30 30
30 31 32 0D 0A 4C 49 54 53 20 22 4F 4C 44 2E 54
58 54 22 0D 0A 50 55 53 48 0D 0A 50 4F 50 0D 0A
45 58 49 53 54 53 0D 0A 50 55 53 48 0D 0A 4C 49
54 20 30 30 30 30 31 0D 0A 43 4E 45 0D 0A 52 45
54 55 52 4E 0D 0A 4C 49 54 20 30 0D 0A 52 45 54
55 52 4E 0D 0A 50 52 4F 43 20 4D 41 49 4E 20 30
20 30 0D 0A 49 4E 56 4F 4B 45 20 46 5F 4D 41 49
4E 20 30 0D 0A 52 45 54 55 52 4E 0D 0A
```

This is a complete IR program. Translate it with IRKEEP, assemble its accepted output with ASMAKEEP, and save RESULT.COM as TRY.COM. Require fresh OK and PASS before both copies. First create OLD.TXT with `ECHO old>OLD.TXT`.

VIEW.BAS must report length 1370. CHECK TRY reports PASS.

Inspect OLD.TXT with VIEW.BAS: require length 1 and bytes `41`.

## Check the new boundary

Use this separate rejected source:

```rill
fn main(){putc(65536);}
```

Copy it to SOURCE.RIL and run CHECK RB10. Require:

```text
ERROR 0000000001 CODE 00003
FAIL
```

An unexpected PASS fails this check. Keep a copy of the accepted result before testing; it must remain unchanged.

