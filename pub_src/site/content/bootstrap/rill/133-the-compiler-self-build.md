+++
title = "The compiler self-build"
weight = 133
description = "Compare two compiler generations made from the same RILL source."
download = "RILL.RIL"
download_group = "toolchain"
+++

RC43.RIL is the complete RILL compiler, saved as RILL.RIL. The IR-written seed built its first executable. VIEW.BAS must report **26625 bytes** for that RILL-written compiler. Preserve RC43.COM as R0.COM.

## Build the first native self-copy

```dos
COPY RILL.RIL SOURCE.RIL
CHECK R0
COPY RESULT.IR SOURCE.IR
CHECK IWKEEP
COPY RESULT.ASM SOURCE.ASM
CHECK ASMAKEEP
COPY RESULT.COM R1.COM
```

Each copy follows its own fresh OK and PASS. In particular, never copy an older result after an error. Use VIEW.BAS to check both lengths before comparing:

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

Require each OK and PASS and no COMP differences. R0, R1, and R2 must all have length 26625. This is a compiler written in RILL compiling the same RILL compiler source, through the published IR translator and assembler.

## A rejected input must stay rejected

Create BAD.RIL:

```rill
fn main(){return missing(1);}
```

```dos
COPY BAD.RIL SOURCE.RIL
CHECK R2
```

Require `ERROR 0000000001 CODE 00004` and FAIL. The accepted RESULT.IR must remain unchanged. An unexpected PASS fails the check. Restore RILL.RIL as SOURCE.RIL before another self-build.

The compiler seed remains a reproducible predecessor. Keep its IR source, the native IR bridge, and the original native assembler on a separate labeled disk.
