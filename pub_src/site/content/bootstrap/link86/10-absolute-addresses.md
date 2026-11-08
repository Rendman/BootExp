+++
title = "10 \u00b7 Taking an address from another module"
weight = 10
description = "Resolve A records into loaded word addresses. Keep relative displacements and absolute addresses distinct even though each occupies two output bytes."
download = "L10.RIL"
download_group = "tools/link86"
reader_names = 1
+++

Resolve A records into loaded word addresses. Keep relative displacements and absolute addresses distinct even though each occupies two output bytes.

A occupies two bytes and contains the target loaded address itself. MAIN has twelve bytes, placing TEXT at 010CH. The MOV DX immediate must therefore be 0C 01. The runtime of this linked example comes from its authored DOS instructions, not from the linker.

## Enter the source

Copy L09.RIL to L10.RIL. Apply these edits from the bottom of the unchanged old file upward. Physical positions are locators, not source to type. Keep all other source.

### Edit 1

Unchanged source immediately before the edit:

```rill
        if p==65535{fail(3);}
        value=256+get16(table,p+32);
        if get16(table,p+34)==2{value=value+firstsize;}
```

Remove old physical positions 256–256:

```rill
        value=value-(256+pc+2);
```

Replace with:

```rill
        if kind==82{value=value-(256+pc+2);}
```

The following old source remains:

```rill
    }
    emit(value&255);emit(value>>8);return 0;
```

### Edit 2

Unchanged source immediately before the edit:

```rill
    return 0;
}
```

Remove old physical positions 250–250:

```rill
fn reference(){
```

Replace with:

```rill
fn reference(kind){
```

The following old source remains:

```rill
    scan();validname();let mut p=find();finish();let mut value=0;
    if pass==2{
```

### Edit 3

Unchanged source immediately before the edit:

```rill
            }else{
                if same("END"){finish();done=1;}
                else{
```

Remove old physical positions 126–126:

```rill
                    if same("B"){bytesrecord();}else{if same("P"){definition();}else{if same("R"){reference();}else{fail(1);}}}
```

Replace with:

```rill
                    if same("B"){bytesrecord();}else{if same("P"){definition();}else{if same("R"){reference(82);}else{if same("A"){reference(65);}else{fail(1);}}}}
```

The following old source remains:

```rill
                }
            }
```

## Build and preserve the tool

```dos
COPY L10.RIL SOURCE.RIL
CHECK R0
COPY RESULT.IR SOURCE.IR
CHECK I0
COPY RESULT.ASM SOURCE.ASM
CHECK A0
COPY RESULT.COM L10.COM
```

Require compiler `OK RESULT.IR 0000022300`, translator `OK RESULT.ASM 0000046715 text bytes`, assembler `OK RESULT.COM 10536 bytes`, and each PASS before the following copy. VIEW.BAS must show L10.COM length 10536 and these first thirty-two bytes:

```text
FC 81 FC FE FF 74 03 E9 D5 28 E8 2D 25 B4 4C CD 21 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
```

## Check the accepted input

Create M10.OBJ as plain ASCII:

```text
OBJ1
B BA
A TEXT
B B4 09 CD 21 B8 00 4C CD 21
END
```

Create U10.OBJ:

```text
OBJ1
P TEXT 0000
B 48 49 0D 0A 24
END
```

```dos
COPY M10.OBJ MAIN.OBJ
COPY U10.OBJ UTIL.OBJ
CHECK L10
```

Require:

```text
OK RESULT.COM 00017 bytes
PASS
```

VIEW.BAS must show RESULT.COM length 17 and these complete bytes:

```text
BA 0C 01 B4 09 CD 21 B8 00 4C CD 21 48 49 0D 0A 24
```

```dos
COPY RESULT.COM TRY.COM
CHECK TRY
```

TRY displays HI followed by CR/LF and reports PASS.

## A rejection check

```dos
COPY RESULT.COM HOLD.COM
```

Create X10.OBJ:

```text
OBJ1
B BA
A LOST
B B4 09 CD 21 B8 00 4C CD 21
END
```

```dos
COPY X10.OBJ MAIN.OBJ
CHECK L10
```

Require:

```text
LINK ERROR 00001 00003 CODE 00003
FAIL
```

```dos
COMP HOLD.COM RESULT.COM <NO.TXT
```

COMP must report no differences. An unexpected PASS fails the rejection. Require a fresh successful run before preserving any new output.

Preserve L10.COM as LINK86.COM and L10.RIL as LINK86.RIL. The reference describes the complete accepted format.
