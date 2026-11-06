+++
title = "The complete RILL toolchain"
weight = 135
description = "Build the compiler, translator, and assembler, then let all three rebuild all three."
download = "TOOLCHN.ZIP"
download_group = "toolchain"
+++

The complete ladder is:

```text
GW-BASIC
  BOOTASM
    ASM86
      ASMA0
        ASM86A
          native streaming IR86
            IR-written RILL compiler seed
              RILL-written compiler, IR86, and ASM86A
                two matching rebuild generations
```

ASMA0 is the streaming-seed collection between ASM86 and ASM86A. RILLBOOT is the compiler seed, not an outside prerequisite. The final three source programs are RILL.RIL, IR86.RIL, and ASM86A.RIL. They share the published language, not a special tool-building escape.

## Reproduce the disk workbench

Begin with the tested native 6422-byte ASM86A preserved as ASMAKEEP.COM. Keep its BASIC/native ladder sources. Copy the source collection to a hard-disk work directory and run:

```dos
TMAKE
```

TMAKE first builds IRWIDE.COM (11577 bytes) with ASMAKEEP. That native translator and assembler build RILLBOOT.COM (21818 bytes) from the authored RILLBOOT.IR. The compiler seed then builds the three RILL implementations. It prints a visible PASS after each successfully completed build and stops at the first nonzero status.

The A/I/R letters below mean assembler, IR translator, and RILL compiler:

| Tool | First RILL build | First rebuild | Second rebuild | Bytes |
|---|---|---|---|---|
| ASM86A | A0.COM | A1.COM | A2.COM | 32404 |
| IR86 | I0.COM | I1.COM | I2.COM | 31472 |
| RILL | R0.COM | R1.COM | R2.COM | 26625 |

Each rebuild generation uses the preceding RILL-written compiler, translator, and assembler for **all three source programs**. The preserved native tools are not silently used in that closed loop. TMAKE.BAT is ordinary DOS batch text; it supplies no executable bytes. Its complete source is:

```dos
ECHO OFF
IF NOT EXIST ASMAKEEP.COM GOTO MISSING
COPY IRWIDE.ASM SOURCE.ASM >NUL
ASMAKEEP
IF ERRORLEVEL 1 GOTO FAILED
COPY RESULT.COM IRWIDE.COM >NUL
COPY RILLBOOT.IR SOURCE.IR >NUL
IRWIDE
IF ERRORLEVEL 1 GOTO FAILED
COPY RESULT.ASM SOURCE.ASM >NUL
ASMAKEEP
IF ERRORLEVEL 1 GOTO FAILED
COPY RESULT.COM RILLBOOT.COM >NUL
COPY RILL.RIL SOURCE.RIL >NUL
RILLBOOT
IF ERRORLEVEL 1 GOTO FAILED
COPY RESULT.IR SOURCE.IR >NUL
IRWIDE
IF ERRORLEVEL 1 GOTO FAILED
COPY RESULT.ASM SOURCE.ASM >NUL
ASMAKEEP
IF ERRORLEVEL 1 GOTO FAILED
COPY RESULT.COM R0.COM >NUL
ECHO PASS RILL INITIAL BUILD
COPY IR86.RIL SOURCE.RIL >NUL
RILLBOOT
IF ERRORLEVEL 1 GOTO FAILED
COPY RESULT.IR SOURCE.IR >NUL
IRWIDE
IF ERRORLEVEL 1 GOTO FAILED
COPY RESULT.ASM SOURCE.ASM >NUL
ASMAKEEP
IF ERRORLEVEL 1 GOTO FAILED
COPY RESULT.COM I0.COM >NUL
ECHO PASS IR86 INITIAL BUILD
COPY ASM86A.RIL SOURCE.RIL >NUL
RILLBOOT
IF ERRORLEVEL 1 GOTO FAILED
COPY RESULT.IR SOURCE.IR >NUL
IRWIDE
IF ERRORLEVEL 1 GOTO FAILED
COPY RESULT.ASM SOURCE.ASM >NUL
ASMAKEEP
IF ERRORLEVEL 1 GOTO FAILED
COPY RESULT.COM A0.COM >NUL
ECHO PASS ASM86A INITIAL BUILD
COPY RILL.RIL SOURCE.RIL >NUL
R0
IF ERRORLEVEL 1 GOTO FAILED
COPY RESULT.IR SOURCE.IR >NUL
I0
IF ERRORLEVEL 1 GOTO FAILED
COPY RESULT.ASM SOURCE.ASM >NUL
A0
IF ERRORLEVEL 1 GOTO FAILED
COPY RESULT.COM R1.COM >NUL
ECHO PASS RILL GENERATION 1
COPY IR86.RIL SOURCE.RIL >NUL
R0
IF ERRORLEVEL 1 GOTO FAILED
COPY RESULT.IR SOURCE.IR >NUL
I0
IF ERRORLEVEL 1 GOTO FAILED
COPY RESULT.ASM SOURCE.ASM >NUL
A0
IF ERRORLEVEL 1 GOTO FAILED
COPY RESULT.COM I1.COM >NUL
ECHO PASS IR86 GENERATION 1
COPY ASM86A.RIL SOURCE.RIL >NUL
R0
IF ERRORLEVEL 1 GOTO FAILED
COPY RESULT.IR SOURCE.IR >NUL
I0
IF ERRORLEVEL 1 GOTO FAILED
COPY RESULT.ASM SOURCE.ASM >NUL
A0
IF ERRORLEVEL 1 GOTO FAILED
COPY RESULT.COM A1.COM >NUL
ECHO PASS ASM86A GENERATION 1
COPY RILL.RIL SOURCE.RIL >NUL
R1
IF ERRORLEVEL 1 GOTO FAILED
COPY RESULT.IR SOURCE.IR >NUL
I1
IF ERRORLEVEL 1 GOTO FAILED
COPY RESULT.ASM SOURCE.ASM >NUL
A1
IF ERRORLEVEL 1 GOTO FAILED
COPY RESULT.COM R2.COM >NUL
ECHO PASS RILL GENERATION 2
COPY IR86.RIL SOURCE.RIL >NUL
R1
IF ERRORLEVEL 1 GOTO FAILED
COPY RESULT.IR SOURCE.IR >NUL
I1
IF ERRORLEVEL 1 GOTO FAILED
COPY RESULT.ASM SOURCE.ASM >NUL
A1
IF ERRORLEVEL 1 GOTO FAILED
COPY RESULT.COM I2.COM >NUL
ECHO PASS IR86 GENERATION 2
COPY ASM86A.RIL SOURCE.RIL >NUL
R1
IF ERRORLEVEL 1 GOTO FAILED
COPY RESULT.IR SOURCE.IR >NUL
I1
IF ERRORLEVEL 1 GOTO FAILED
COPY RESULT.ASM SOURCE.ASM >NUL
A1
IF ERRORLEVEL 1 GOTO FAILED
COPY RESULT.COM A2.COM >NUL
ECHO PASS ASM86A GENERATION 2
ECHO BUILDS COMPLETE - COMPARE THE GENERATIONS
GOTO END
:MISSING
ECHO MISSING TESTED ASMAKEEP.COM
GOTO END
:FAILED
ECHO FAIL - STOP AT THE FIRST TOOL ERROR
:END
```

## Compare the generations

```dos
ECHO N>NO.TXT
COMP A0.COM A1.COM <NO.TXT
COMP A0.COM A2.COM <NO.TXT
COMP I0.COM I1.COM <NO.TXT
COMP I0.COM I2.COM <NO.TXT
COMP R0.COM R1.COM <NO.TXT
COMP R0.COM R2.COM <NO.TXT
```

Every comparison must report no differences, and VIEW.BAS must show the corresponding length in the table. NO.TXT answers N if COMP asks whether to compare more files. Build status and byte comparison are independent observations.

## Use generation two

Create HI.RIL:

```rill
fn main(){putc(72);putc(73);return 0;}
```

```dos
COPY HI.RIL SOURCE.RIL
CHECK R2
COPY RESULT.IR SOURCE.IR
CHECK I2
COPY RESULT.ASM SOURCE.ASM
CHECK A2
COPY RESULT.COM HI.COM
CHECK HI
```

Require OK and PASS before each copy. HI displays HI and reports PASS.

For a rejection, give R2 SOURCE.RIL containing `fn main(){return missing();}`. Require `ERROR 0000000001 CODE 00004` and FAIL. RESULT.IR must remain unchanged. An unexpected PASS fails the check. Restore the accepted source before another run.

Keep the source, preserved native builders, and matching generations separately labeled. A toolchain is established by reproducible successful translations and executable behavior, not by retaining an unexplained binary.
