+++
title = "Three complete programs"
weight = 31
description = "Use console output, a data byte, and a counted loop in short runnable examples."
download = "ASM0.ZIP"
download_group = "tools/asm0"
reader_names = 1
url = "/bootstrap/asm86/32-programs/"
+++

I can now build ASM0 with ASM0. I also want it to remain useful for the small jobs that helped me learn assembly. A message, a stored byte, and a counted loop give me familiar results to check with the finished tool.

These are complete DOS .COM programs for the finished ASM0. For HELLO, use COPY HELLO.ASM SOURCE.ASM, run CHECK ASM0, then require the stated OK byte count and PASS before COPY RESULT.COM HELLO.COM. Follow the same pattern for MEMORY and COUNT. Select rejection inputs with COPY in the same way; a rejected source must leave RESULT.COM unchanged.

## HELLO: a terminated message

Save HELLO.ASM:

```asm
MOV DX,MESSAGE
MOV AH,9
INT 21H
MOV AX,4C00H
INT 21H
MESSAGE:
DB 72,101,108,108,111,13,10,36
```

Require `OK 00020 bytes`. `CHECK HELLO` displays `Hello`, moves to a new line, and reports PASS. Function 09H reads DS:DX until the dollar sign; this example's message must not contain that terminator as ordinary text. MOV loads DX without changing the segment. The program returns with code zero.

As a rejection check, change only the first line in a separate BADHELLO.ASM to `MOV DX,MISSING`. Assembling BADHELLO must report `ERROR 00001 CODE 3` and FAIL. Restore the original source before rebuilding HELLO.

## MEMORY: copy a stored byte

Save MEMORY.ASM:

```asm
MOV BX,LETTER
MOV AL,[BX]
MOV [COPY],AL
MOV DL,[COPY]
MOV AH,2
INT 21H
MOV AX,4C00H
INT 21H
LETTER:
DB 77
COPY:
DB 0
```

Require `OK 00024 bytes`. `CHECK MEMORY` displays `M` and reports PASS. The byte moves from LETTER through AL into COPY, then through DL to DOS. The register operand determines the byte width. COPY names actual storage after the exit, so execution does not fall into the data.

In a separate BADMEM.ASM, change the second line to `MOV AL,[SI]`. Assembling it must report `ERROR 00002 CODE 3` and FAIL. The CPU has other addressing forms, but this assembler accepts only BX-based and direct memory offsets.

## COUNT: a loop with a nearby target

Save COUNT.ASM:

```asm
MOV DL,30H
AGAIN:
MOV AH,2
INT 21H
INC DX
CMP DL,33H
JB AGAIN
MOV AX,4C00H
INT 21H
```

Require `OK 00017 bytes`. `CHECK COUNT` displays `012` and reports PASS. INC DX advances the low-byte digit; the values stay far from a carry into DH. CMP sets unsigned comparison flags, and JB consumes them immediately. The backward displacement is F6H, ten bytes back from the end of the branch.

In a separate BADCOUNT.ASM, change only `JB AGAIN` to `JB 400H`. Assembling it must report `ERROR 00007 CODE 4` and FAIL. A conditional branch reaches only -128 through +127 bytes from the following instruction. Write a nearby opposite condition around a near JMP when a longer conditional transfer is required.

All three programs leave the DOS segment registers and entry stack alone. CALL and PUSH would need balanced returns and pops; these examples require no local subroutines or reserved stack storage. Consult the language reference before adding instructions: a CPU manual describes more forms than ASM0 accepts.
