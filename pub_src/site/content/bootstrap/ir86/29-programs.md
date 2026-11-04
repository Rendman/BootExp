+++
title = "Three complete programs"
weight = 29
description = "Console output, a procedure-driven counter, and a byte-pointer loop."
download = "IR86.ZIP"
+++

These complete programs use the finished IR86 and ASM86. Save each under its indicated .IR name. Run `CHECK IRKEEP` and enter its base name; require the stated text-byte count and PASS. Then run `CHECK ASMKEEP` with the same base name and require the machine-byte count and PASS. Only then execute the new program.

## HELLO: two console characters

Save `HELLO.IR`:

```ir
LABEL MAIN
LIT 72
TODX
LIT 200H
DOS
LIT 73
TODX
LIT 200H
DOS
HALT
```

TODX supplies each character code to DOS function 02H. LIT 200H sets AH to two; DOS displays DL. The second character is prepared after the first DOS call because result registers may have changed. HALT returns zero.

Require `OK HELLO.ASM 00197 text bytes` from IR86, then `OK 00040 bytes` from ASM86. `CHECK HELLO` displays `HI` and reports PASS.

Copy HELLO.IR to BADHELLO.IR and change its first TODX to TODX EXTRA. Translate BADHELLO with CHECK IRKEEP. Require IR ERROR 00003 CODE 1 and FAIL.

## COUNT: a procedure and an unsigned loop

Save `COUNT.IR`:

```ir
WORD DIGIT 48
LABEL MAIN
LABEL AGAIN
LD DIGIT
CALL PUTCHAR
LD DIGIT
PUSH
LIT 1
ADD
ST DIGIT
LD DIGIT
PUSH
LIT 51
ULT AGAIN
HALT
LABEL PUTCHAR
TODX
LIT 200H
DOS
RET
```

DIGIT is named word storage. CALL passes its value in AX to PUTCHAR, whose TODX and DOS sequence displays it. After the call, main reloads DIGIT rather than depending on AX. The comparison consumes the saved left word and branches while the updated digit is less than 51. The expression stack is empty at every label, call, and transfer.

Require `OK COUNT.ASM 00383 text bytes` from IR86, then `OK 00068 bytes` from ASM86. `CHECK COUNT` displays `012` and reports PASS.

Copy COUNT.IR to BADCOUNT.IR and remove the PUSH immediately before LIT 51. Translate BADCOUNT with CHECK IRKEEP. ULT then has no left operand: require IR ERROR 00013 CODE 4 and FAIL.

## BYTES: walk a zero-terminated message

Save `BYTES.IR`:

```ir
BYTE TEXT0 79
BYTE TEXT1 75
BYTE TEXT2 0
WORD POINTER 0
LABEL MAIN
ADDR TEXT0
ST POINTER
LABEL AGAIN
LD POINTER
FETCHB
JZ DONE
TODX
LIT 200H
DOS
LD POINTER
PUSH
LIT 1
ADD
ST POINTER
JMP AGAIN
LABEL DONE
HALT
```

The BYTE declarations are consecutive, and TEXT2 is the zero terminator. POINTER retains an offset. FETCHB converts one byte to an unsigned word; JZ stops at its terminator. Pointer addition happens after DOS and the updated offset is stored before the loop transfers. The word POINTER itself is separate storage, not a second copy of the text.

Require `OK BYTES.ASM 00451 text bytes` from IR86, then `OK 00076 bytes` from ASM86. `CHECK BYTES` displays `OK` and reports PASS.

Copy BYTES.IR to BADBYTES.IR and change TEXT0 to 1TEXT in the first BYTE declaration. Translate BADBYTES with CHECK IRKEEP. Require IR ERROR 00001 CODE 3 and FAIL.

All three programs require the full-segment entry arrangement documented in the reference. They leave DS, ES, and SS at their DOS entry values and rely only on the accepted 8086/8088 instruction forms. The file-copy program in the pipeline installment is a separate example of handle-based input and output.
