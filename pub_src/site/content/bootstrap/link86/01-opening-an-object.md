+++
title = "01 \u00b7 Opening the first object"
weight = 1
description = "Open MAIN.OBJ read-only and close its owned handle. Fixed work files keep console parsing out of the linker."
download = "L01.RIL"
download_group = "tools/link86"
reader_names = 1
+++

Open MAIN.OBJ read-only and close its owned handle. Fixed work files keep console parsing out of the linker.

## Enter the source

Create L01.RIL as plain text:

```rill
// LINK86 construction checkpoint.
let mut input=0;
let mut inopen=0;
fn main(){openunit();closein();return 0;}

fn openunit(){input=open("MAIN.OBJ");if status(){fail(6);}inopen=1;return 0;}

fn closein(){close(input);if status(){fail(6);}inopen=0;return 0;}

fn fail(code){if inopen{close(input);}exit(1);return 0;}
```

## Build and preserve the tool

```dos
COPY L01.RIL SOURCE.RIL
CHECK R0
COPY RESULT.IR SOURCE.IR
CHECK I0
COPY RESULT.ASM SOURCE.ASM
CHECK A0
COPY RESULT.COM L01.COM
```

Require compiler `OK RESULT.IR 0000000852`, translator `OK RESULT.ASM 0000006386 text bytes`, assembler `OK RESULT.COM 01305 bytes`, and each PASS before the following copy. VIEW.BAS must show L01.COM length 1305 and these first thirty-two bytes:

```text
FC 81 FC FE FF 74 03 E9 C6 04 E8 1E 01 B4 4C CD 21 00 00 00 00 55 8B EC 81 EC 80 00 81 FC 00 F0
```

## Check the accepted input

Create M01.OBJ as plain ASCII:

```text
OBJ1
END
```

```dos
COPY M01.OBJ MAIN.OBJ
CHECK L01
```

CHECK must report PASS. This checkpoint creates no linked output. Its input handling is checked by its return status; its retained executable was inspected above.

## A rejection check

```dos
COPY RESULT.COM HOLD.COM
```

```dos
REN MAIN.OBJ HOLD.OBJ
CHECK L01
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
