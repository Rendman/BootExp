+++
title = "01 \u00b7 Opening the first object"
weight = 1
description = "Obtain module and result names through the portable argument services, then open the selected first object read-only and close its owned handle."
download = "L01.RIL"
download_group = "tools/link86"
reader_names = 1
+++

Obtain module and result names through the portable argument services, then open the selected first object read-only and close its owned handle.

## Enter the source

Create L01.RIL as plain text:

```rill
// LINK86 construction checkpoint.
let mut input=0;
let mut inopen=0;
fn main(){filearg(1,"MAIN.OBJ");openunit();closein();return 0;}

fn openunit(){input=open(filearg(1,"MAIN.OBJ"));if status(){fail(6);}inopen=1;return 0;}

fn closein(){close(input);if status(){fail(6);}inopen=0;return 0;}

fn fail(code){if inopen{close(input);}exit(1);return 0;}

fn filearg(n,fallback){
    let mut count=argc();
    if count==0{return fallback;}
    if count!=3{exit(1);}
    if filesame(arg(1),arg(2))|filesame(arg(1),arg(3))|filesame(arg(1),"LINK.TMP")|filesame(arg(1),"LINK.BAK")|filesame(arg(2),arg(3))|filesame(arg(2),"LINK.TMP")|filesame(arg(2),"LINK.BAK")|filesame(arg(3),"LINK.TMP")|filesame(arg(3),"LINK.BAK"){exit(1);}
    return arg(n);
}

fn filesame(a,b){
    let mut i=0;
    while load8(a+i)==load8(b+i){
        if load8(a+i)==0{return 1;}i=i+1;
    }
    return 0;
}
```

## Build and preserve the tool

```dos
CHECK R0 L01.RIL RESULT.IR
CHECK I0 RESULT.IR RESULT.ASM
CHECK A0 RESULT.ASM RESULT.COM
COPY RESULT.COM L01.COM
```

Require compiler `OK RESULT.IR 0000002689`, translator `OK RESULT.ASM 0000011874 text bytes`, assembler `OK RESULT.COM 02314 bytes`, and each PASS before the following copy. VIEW.BAS must show L01.COM length 2314 and these first thirty-two bytes:

```text
FC 81 FC FE FF 74 03 E9 59 07 E8 9F 07 81 F8 FF FF 75 03 E9 4D 07 E8 A5 03 B4 4C CD 21 00 00 00
```

## Check the accepted input

Create M01.OBJ as plain ASCII:

```text
OBJ1
END
```

```dos
CHECK L01 M01.OBJ UTIL.OBJ RESULT.COM
```

CHECK must report PASS. This checkpoint creates no linked output. Its input handling is checked by its return status; its retained executable was inspected above.

## A rejection check

```dos
COPY RESULT.COM HOLD.COM
```

```dos
REN MAIN.OBJ HOLD.OBJ
CHECK L01 M01.OBJ UTIL.OBJ RESULT.COM
```

Use an unused HOLD.OBJ name and restore it to MAIN.OBJ after the check.

Require:

```text
FAIL
```

```dos
COMP HOLD.COM RESULT.COM <NO.TXT
```

COMP must report no differences. An unexpected PASS fails the rejection. Require a fresh successful run before preserving any new output.
