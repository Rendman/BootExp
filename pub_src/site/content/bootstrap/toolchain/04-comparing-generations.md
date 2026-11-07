+++
title = "Comparing Two Rebuild Generations"
weight = 4
description = "Compare all three tools and use generation two to compile a complete program."
download = "TOOLCHN.ZIP"
download_group = "tools/toolchain"
reader_names = 1
+++

Begin after TMAKE has completed successfully. Keep A0/A1/A2, I0/I1/I2, and R0/R1/R2. Each group must have the same length and identical bytes. These are independent checks of builds that already returned success.

| Tool | Bytes in every generation |
|---|---|
| ASM86 | 30911 |
| IR86 | 29678 |
| RILL | 26617 |

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
