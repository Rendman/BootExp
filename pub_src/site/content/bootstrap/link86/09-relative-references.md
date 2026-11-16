+++
title = "09 \u00b7 Calling into another module"
weight = 9
description = "Resolve R records into near-relative words while streaming. A saved definition supplies the target even when the defining module follows the caller."
download = "L09.RIL"
download_group = "tools/link86"
reader_names = 1
+++

Resolve R records into near-relative words while streaming. A saved definition supplies the target even when the defining module follows the caller.

R occupies two image bytes at the current output position. Its word is target loaded address minus the loaded address just after that word, modulo 65536. MAIN has seven bytes, so VALUE in UTIL loads at 0107H. The call operand begins at 0101H and ends at 0103H: 0107H minus 0103H is 0004H.

## Enter the source

Copy L08.RIL to L09.RIL. Apply these edits from the bottom of the unchanged old file upward. Physical positions are locators, not source to type. Keep all other source.

### Edit 1

Unchanged source immediately before the edit:

```rill
    return 0;
}
```

Insert after old physical line 249.

Insert:

```rill
fn reference(){
    scan();validname();let mut p=find();finish();let mut value=0;
    if pass==2{
        if p==65535{fail(3);}
        value=256+get16(table,p+32);
        if get16(table,p+34)==2{value=value+firstsize;}
        value=value-(256+pc+2);
    }
    emit(value&255);emit(value>>8);return 0;
}
```

The following old source remains:

```rill
fn print(s){
    while load8(s){putc(load8(s));s=s+1;}return 0;
```

### Edit 2

Unchanged source immediately before the edit:

```rill
            }else{
                if same("END"){finish();done=1;}
                else{
```

Remove old physical positions 126–126:

```rill
                    if same("B"){bytesrecord();}else{if same("P"){definition();}else{fail(1);}}
```

Replace with:

```rill
                    if same("B"){bytesrecord();}else{if same("P"){definition();}else{if same("R"){reference();}else{fail(1);}}}
```

The following old source remains:

```rill
                }
            }
```

## Build and preserve the tool

```dos
CHECK R0 L09.RIL RESULT.IR
CHECK I0 RESULT.IR RESULT.ASM
CHECK A0 RESULT.ASM RESULT.COM
COPY RESULT.COM L09.COM
```

Require compiler `OK RESULT.IR 0000024251`, translator `OK RESULT.ASM 0000052358 text bytes`, assembler `OK RESULT.COM 11575 bytes`, and each PASS before the following copy. VIEW.BAS must show L09.COM length 11575 and these first thirty-two bytes:

```text
FC 81 FC FE FF 74 03 E9 86 2B E8 CC 2B 81 F8 FF FF 75 03 E9 7A 2B E8 D2 27 B4 4C CD 21 00 00 00
```

## Check the accepted input

Create M09.OBJ as plain ASCII:

```text
OBJ1
B E8
R VALUE
B B4 4C CD 21
END
```

Create U09.OBJ:

```text
OBJ1
P VALUE 0000
B 33 C0 C3
END
```

```dos
CHECK L09 M09.OBJ U09.OBJ RESULT.COM
```

Require:

```text
OK RESULT.COM 00010 bytes
PASS
```

VIEW.BAS must show RESULT.COM length 10 and these complete bytes:

```text
E8 04 00 B4 4C CD 21 33 C0 C3
```

```dos
COPY RESULT.COM TRY.COM
CHECK TRY
```

TRY calls VALUE in the second module, exits with its zero result and reports PASS. It has no display routine.

## A rejection check

```dos
COPY RESULT.COM HOLD.COM
```

Create X09.OBJ:

```text
OBJ1
B E8
R LOST
B B4 4C CD 21
END
```

```dos
CHECK L09 X09.OBJ U09.OBJ RESULT.COM
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
