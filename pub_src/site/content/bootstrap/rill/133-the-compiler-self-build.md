+++
title = "The compiler self-build"
weight = 45
description = "Establish the compiler frame convention and compare two matching generations."
download = "RILL.RIL"
download_group = "tools/rill"
aliases = ["/bootstrap/rill/133-the-compiler-self-build/"]
reader_names = 1
url = "/bootstrap/rc/133-the-compiler-self-build/"
+++

RC43.RIL is the completed RILL compiler, saved as RILL.RIL. Its record, local-declaration and procedure routines already support sixty-four local slots and sixteen parameters. The IR-written seed built RC43.COM; preserve it as RBOOT.COM. VIEW.BAS must report **26617 bytes**.

## Let RILL establish its own frames

RILLBOOT reserves sixteen local slots in the programs it compiles. RILL reserves sixty-four. RBOOT therefore uses sixteen-slot frames in its own implementation but emits sixty-four-slot frames. Compile the unchanged compiler source once with RBOOT to establish R0 using the RILL frame convention:

```dos
COPY RILL.RIL SOURCE.RIL
CHECK RBOOT
COPY RESULT.IR SOURCE.IR
CHECK IWKEEP
COPY RESULT.ASM SOURCE.ASM
CHECK ASMAKEEP
COPY RESULT.COM R0.COM
```

Require compiler `OK RESULT.IR 0000049992`, translator `OK RESULT.ASM 0000103091 text bytes`, assembler `OK RESULT.COM 26617 bytes`, and each PASS before the following copy. VIEW.BAS must show R0.COM length 26617. RBOOT and R0 need not have identical bytes: their builders reserve different frames. All comparisons below start with R0.

## Build the first matching self-copy

```dos
COPY RILL.RIL SOURCE.RIL
CHECK R0
COPY RESULT.IR SOURCE.IR
CHECK IWKEEP
COPY RESULT.ASM SOURCE.ASM
CHECK ASMAKEEP
COPY RESULT.COM R1.COM
```

Each copy follows its own fresh OK and PASS. Use VIEW.BAS to check both lengths before comparing:

```dos
ECHO N>NO.TXT
COMP R0.COM R1.COM <NO.TXT
```

Require no differences. NO.TXT answers N if COMP asks whether to compare more files. A successful comparison is separate from the preceding tools' success reports.

## Let that copy do the same job

```dos
COPY RILL.RIL SOURCE.RIL
CHECK R1
COPY RESULT.IR SOURCE.IR
CHECK IWKEEP
COPY RESULT.ASM SOURCE.ASM
CHECK ASMAKEEP
COPY RESULT.COM R2.COM
COMP R0.COM R2.COM <NO.TXT
```

Require each OK and PASS and no COMP differences. R0, R1, and R2 must all have length 26617. This is the same RILL source compiled through the published IR translator and assembler. Preserve these matching copies for the toolchain collection.

## A rejected input must stay rejected

Create BAD.RIL:

```rill
fn main(){return missing(1);}
```

```dos
COPY BAD.RIL SOURCE.RIL
CHECK R2
```

With a final CR/LF after the source line, require `ERROR 0000000002 CODE 00004` and FAIL. The accepted RESULT.IR must remain unchanged. An unexpected PASS fails the check. Restore RILL.RIL as SOURCE.RIL before another self-build.

Keep the compiler seed, native IR bridge, original native assembler and their sources on a separate labeled disk.
