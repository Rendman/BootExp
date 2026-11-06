+++
title = "14 · Complete seed programs"
weight = 14
description = "A terminated greeting, a byte copied through memory, and a short loop."
download = "ASMA0.ZIP"
+++

These programs use the completed ASMA0 seed. Its fixed input is SOURCE.ASM and its output is RESULT.COM. Preserve each accepted output under the program's own filename before another assembly. Run an output only after a fresh OK and PASS and a VIEW.BAS inspection.

## HELLO

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

DOS function 9 prints the bytes ending at the dollar marker. DB supplies numeric ASCII values because the seed has no quoted-string syntax. Carriage return and line feed are explicit.

```dos
COPY HELLO.ASM SOURCE.ASM
CHECK ASMA0
```

Require `OK RESULT.COM 00020 bytes` and PASS. VIEW.BAS must report length 20 and these complete bytes:

```text
BA 0C 01 B4 09 CD 21 B8 00 4C CD 21 48 65 6C 6C 6F 0D 0A 24
```

```dos
COPY RESULT.COM HELLO.COM
CHECK HELLO
```

It displays "Hello\r\n" and the checker reports PASS. Here `\r\n` denotes carriage return and line feed.

For a separate rejection, copy the source to BAD.ASM and replace the first `INT 21H` with `INT 256`. Copy BAD.ASM to SOURCE.ASM and run CHECK ASMA0. Require `ERROR 00003 CODE 4` and FAIL. The accepted RESULT.COM must remain unchanged. An unexpected PASS fails this test. Restore the accepted source before building again.

## MEMORY

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

BX holds the source byte address. A byte register supplies the width for the [BX] load and direct [COPY] store. The second direct load demonstrates that COPY received M. Both objects belong to the program segment selected by DS.

```dos
COPY MEMORY.ASM SOURCE.ASM
CHECK ASMA0
```

Require `OK RESULT.COM 00024 bytes` and PASS. VIEW.BAS must report length 24 and these complete bytes:

```text
BB 16 01 8A 07 88 06 17 01 8A 16 17 01 B4 02 CD 21 B8 00 4C CD 21 4D 00
```

```dos
COPY RESULT.COM MEMORY.COM
CHECK MEMORY
```

It displays "M" and the checker reports PASS. Here `\r\n` denotes carriage return and line feed.

For a separate rejection, copy the source to BAD.ASM and replace the first `MOV AL,[BX]` with `MOV AX,AL`. Copy BAD.ASM to SOURCE.ASM and run CHECK ASMA0. Require `ERROR 00002 CODE 1` and FAIL. The accepted RESULT.COM must remain unchanged. An unexpected PASS fails this test. Restore the accepted source before building again.

## COUNT

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

DL starts at ASCII zero and advances after each output. CMP leaves the unsigned flags tested by JB. AGAIN is close enough for the seed's short conditional encoding.

```dos
COPY COUNT.ASM SOURCE.ASM
CHECK ASMA0
```

Require `OK RESULT.COM 00017 bytes` and PASS. VIEW.BAS must report length 17 and these complete bytes:

```text
B2 30 B4 02 CD 21 42 80 FA 33 72 F6 B8 00 4C CD 21
```

```dos
COPY RESULT.COM COUNT.COM
CHECK COUNT
```

It displays "012" and the checker reports PASS. Here `\r\n` denotes carriage return and line feed.

For a separate rejection, copy the source to BAD.ASM and replace the first `JB AGAIN` with `JB 400H`. Copy BAD.ASM to SOURCE.ASM and run CHECK ASMA0. Require `ERROR 00007 CODE 4` and FAIL. The accepted RESULT.COM must remain unchanged. An unexpected PASS fails this test. Restore the accepted source before building again.

The completed seed source and its matching self-builds are the handoff to the separate ASM86A collection. Keep ASMA0.COM and ASMA0.ASM with their tested examples.
