+++
title = "Complete portable programs"
weight = 35
description = "Byte streams, a procedure-driven counter, and pointers to declared storage."
download = "IR86.ZIP"
+++

These complete programs use the finished IR86 and ASM86. Save each under its indicated .IR name. Run `CHECK IRKEEP` and enter its base name; require the stated text-byte count and PASS. Then run `CHECK ASMKEEP` with the same base name and require the machine-byte count and PASS. Only then execute the new program.

## HELLO: two output bytes

Save `HELLO.IR`:

```ir
LABEL MAIN
LIT 72
PUTC
LIT 73
PUTC
HALT
```

PUTC writes the low byte of virtual A to the output stream. Its result is a count, so each new character is loaded explicitly. HALT returns zero. The IR source contains no physical register or operating-system service number.

Require `OK HELLO.ASM 02594 text bytes` from IR86, then `OK 00480 bytes` from ASM86. `CHECK HELLO` displays `HI` and reports PASS.

Copy HELLO.IR to BADHELLO.IR and change its first PUTC to PUTC EXTRA. Translate BADHELLO with CHECK IRKEEP. Require IR ERROR 00003 CODE 1 and FAIL.

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
PUTC
RET
```

DIGIT is persistent word storage. CALL passes its value in virtual A to PUTCHAR, which uses PUTC. Main reloads DIGIT after the call. ULT consumes the saved left operand and tests the updated value against 51. Every control boundary has an empty expression stack.

Require `OK COUNT.ASM 02800 text bytes` from IR86, then `OK 00512 bytes` from ASM86. `CHECK COUNT` displays `012` and reports PASS.

Copy COUNT.IR to BADCOUNT.IR and remove the PUSH immediately before LIT 51. Require IR ERROR 00013 CODE 4 and FAIL.

## BYTES: walk declared byte storage

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
PUTC
LD POINTER
PUSH
LIT 1
ADD
ST POINTER
JMP AGAIN
LABEL DONE
HALT
```

The BYTE declarations are consecutive; TEXT2 is the zero terminator. POINTER retains a pointer formed by ADDR. FETCHB returns an unsigned byte value, and JZ stops at zero. Pointer advancement uses a byte offset within this declared sequence. No numeric address is assumed.

Require `OK BYTES.ASM 02868 text bytes` from IR86, then `OK 00520 bytes` from ASM86. `CHECK BYTES` displays `OK` and reports PASS.

Copy BYTES.IR to BADBYTES.IR and change TEXT0 to 1TEXT in its first declaration. Require IR ERROR 00001 CODE 3 and FAIL.

## ECHOIR: copy an input byte stream

Save `ECHOIR.IR`:

```ir
WORD CHARACTER 0
LABEL MAIN
LABEL AGAIN
GETC
ST CHARACTER
STATUS
JNZ FAILURE
LD CHARACTER
PUSH
LIT 65535
EQ DONE
LD CHARACTER
PUTC
STATUS
JNZ FAILURE
JMP AGAIN
LABEL DONE
HALT
LABEL FAILURE
LIT 1
EXIT
```

GETC returns each byte or the distinct EOF value 65535. CHARACTER saves the result before STATUS is read. The equality branch consumes its left value, so CHARACTER is reloaded before PUTC. Both services are checked. A byte value 255 is data, not EOF.

Create KEY.TXT with `ECHO IR86 echo.>KEY.TXT`, then run `CHECK ECHOIR <KEY.TXT`. It copies the line including its CR/LF.

Require `OK ECHOIR.ASM 02930 text bytes` from IR86, then `OK 00536 bytes` from ASM86. `CHECK ECHOIR <KEY.TXT` displays `IR86 echo.` and reports PASS.

Copy ECHOIR.IR to BADECHOIR.IR and change GETC to GETC EXTRA. Require IR ERROR 00004 CODE 1 and FAIL.

These sources use only the virtual machine and portable runtime contract. The 8086/DOS binding has the environment requirements documented separately in the reference. The pipeline installment supplies a complete file-copy example.
