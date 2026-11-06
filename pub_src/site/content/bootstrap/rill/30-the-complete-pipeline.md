+++
title = "30 \u00b7 The complete RILL pipeline"
weight = 30
description = "Carry a structured counter through IR and assembly to a working program."
download = "RILL0.IR"
download_group = "tools/rill0"
reader_names = 1
+++

The compiler source is IR86, and its result is IR86. Keep both translations visible while making a complete program. Begin with the tested R29.COM and preserve the working compiler:

```dos
COPY R29.COM RILL0.COM
COPY RILL0.COM RLKEEP.COM
```

RILL0.COM must have length 5173 bytes in VIEW.BAS. Keep RILL0.IR, IRKEEP.COM, ASMKEEP.COM, CHECK.BAT, and their sources.

## Enter a complete program

Save this as COUNT.RIL:

```rill
fn main() {
    let mut x = 48;
    while x < 51 {
        putc(x);
        x = x + 1;
    }
}
```

x is a mutable unsigned word. The condition is evaluated at the loop entrance on every iteration. Each successful pass prints the low byte of x, then advances x by one. The body has no declarations or hidden parameter frame.

```dos
COPY COUNT.RIL SOURCE.RIL
CHECK RLKEEP
```

Require `OK RESULT.IR 00153` and PASS. TYPE RESULT.IR must show:

```ir
WORD x 00048
LABEL MAIN
LABEL B00001
LD x
PUSH
LIT 00051
UGE B00002
LD x
PUTC
LD x
PUSH
LIT 00001
ADD
ST x
JMP B00001
LABEL B00002
HALT
```

The WORD declaration precedes MAIN. The condition emits UGE to leave the loop when x is not less than 51. PUSH and ADD implement the update; both loop edges have an empty expression stack. B00001 and B00002 are generated names, not physical addresses.

## Translate and assemble

```dos
COPY RESULT.IR COUNT.IR
CHECK IRKEEP
```

Enter COUNT. Require `OK COUNT.ASM 02783 text bytes` and PASS. Run CHECK ASMKEEP, enter COUNT, and require `OK 00511 bytes` and PASS. VIEW.BAS must report COUNT.COM length 511 bytes. Its first sixteen hexadecimal bytes are:

```text
FC 81 FC FE FF 74 05 B8 07 4C CD 21 E9 02 00 30
```

Only after all three tools succeed, run CHECK COUNT. It displays `012` and reports PASS. The saved IR is sufficient input for another conforming backend; the source program makes no native register or DOS call assumptions.

## Observe a rejected program

Copy COUNT.RIL to BADCOUNT.RIL and remove the semicolon from `x = x + 1;`. Copy BADCOUNT.RIL to SOURCE.RIL and run CHECK RLKEEP. Require ERROR 00006 CODE 00002 and FAIL. The closing brace is the token at which the missing semicolon is detected. TYPE RESULT.IR must still show the accepted counter above.

Restore COUNT.RIL as SOURCE.RIL before another successful build. An unexpected PASS fails the rejection check. If the result differs, inspect RESULT.IR first, then COUNT.ASM; do not execute an older COUNT.COM after any build step fails.
