+++
title = "01 \u00b7 A message from assembly"
weight = 1
description = "A short DOS program, built with the BASIC assembler."
download = "AS01.ASM"
download_group = "tools/asm0"
reader_names = 1
url = "/bootstrap/asm86/01-a-message-from-assembly/"
+++

The name `ASM0` will be its first report. For now that is all this program does. I want to assemble it with BOOTASM, return to DOS, and check that the message routine and the exit work.

## How it works

The source uses the same MOV, CALL, RET, and INT forms accepted by BOOTASM. DX receives the offset of HELLOMSG. DOS function 09H displays its bytes until it reaches the dollar-sign code 36; the 13 and 10 move the cursor to the next line. The dollar sign is a terminator, not part of the displayed message.

TEXT is a small subroutine with DX as its input. It changes AH and the flags DOS leaves behind; DOS may also return a value in AL. It does not save AX, because the caller has no AX value to retain. CALL pushes a two-byte return offset and RET takes it back. GOOD then uses function 4CH with a zero return code.

The labels name offsets beginning at 0100H. Neither ORG nor a segment directive is needed or accepted. Each DB item is an ASCII character code, and the BASIC assembler writes the machine bytes without a file header.

## Source changes

Enter this complete source as `AS01.ASM`. The labels and instruction lines are actual source; there are no printed margin numbers.

```asm
; ASM86 construction checkpoint. Plain BOOTASM source.
START:
CLD
MOV DX,HELLOMSG
CALL TEXT
GOOD:
MOV AX,4C00H
INT 21H

TEXT:
MOV AH,9
INT 21H
RET

HELLOMSG:
DB 65,83,77,48,13,10,36
```

## Build and stop

Use the BASIC assembler prepared in the workbench guide:

```dos
COPY AS01.ASM SOURCE.ASM
GWBASIC BOOTASM.BAS
```

Require `OK RESULT.COM 24 bytes`; BASIC may add spaces around the count. If the build reports an error, stop and compare the edited source. Use `SYSTEM` to return to DOS, then `COPY RESULT.COM AS01.COM`. Save this source and executable as a working stopping point.

```dos
CHECK AS01
```

The display, apart from DOS command echo and the checker's separating blank line, is:

```text
ASM0
PASS
```

I save `AS01.ASM` with its executable. It is a small assembly program I can trace from its first instruction to its return to DOS.

## If the result differs

Check the decimal character bytes, the dollar-sign terminators, and the order of saved registers. A RET must match a CALL; the top-level exit uses DOS function 4CH.
