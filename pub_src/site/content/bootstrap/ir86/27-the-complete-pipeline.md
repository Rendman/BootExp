+++
title = "33 \u00b7 The complete translation pipeline"
weight = 33
description = "Use the portable file interface, then build and run its DOS binding."
download = "IR86.ASM"
download_group = "tools/ir86"
reader_names = 1
+++

The completed translator is the saved IR32 program. This installment adds no translator source. It follows a portable file-copy program through the current backend and assembler to an executable.

## Preserve the translator

```dos
COPY IR32.ASM IR86.ASM
CHECK ASMKEEP
```

Enter IR86. Require `OK 06407 bytes` and PASS, then preserve the result:

```dos
COPY IR86.COM IRKEEP.COM
```

ASMKEEP is the completed ASM0 from the workbench. Its executable comes from BOOTASM and directly assembles this translator. The runtime binding is emitted as source by IR86 and assembled by the same ASM0.

## A portable file copier

Save COPYFILE.IR:

```ir
BYTE IN0 73
BYTE IN1 78
BYTE IN2 46
BYTE IN3 84
BYTE IN4 88
BYTE IN5 84
BYTE IN6 0
BYTE OUT0 79
BYTE OUT1 85
BYTE OUT2 84
BYTE OUT3 46
BYTE OUT4 84
BYTE OUT5 88
BYTE OUT6 84
BYTE OUT7 0
WORD INPUT 0
WORD OUTPUT 0
WORD COUNT 0
WORD WRITTEN 0
BUFFER DATA 1
LABEL MAIN
ADDR IN0
OPEN
ST INPUT
STATUS
JNZ FAILURE
ADDR OUT0
CREATE
ST OUTPUT
STATUS
JNZ FAILURE
LABEL AGAIN
LD INPUT
PUSH
ADDR DATA
PUSH
LIT 1
READ
ST COUNT
STATUS
JNZ FAILURE
LD COUNT
JZ FINISH
LD OUTPUT
PUSH
ADDR DATA
PUSH
LD COUNT
WRITE
ST WRITTEN
STATUS
JNZ FAILURE
LD WRITTEN
PUSH
LD COUNT
NE FAILURE
JMP AGAIN
LABEL FINISH
LD INPUT
CLOSE
STATUS
JNZ FAILURE
LD OUTPUT
CLOSE
STATUS
JNZ FAILURE
HALT
LABEL FAILURE
LIT 1
EXIT
```

IN0 and OUT0 begin consecutive, zero-terminated filename bytes. INPUT and OUTPUT hold opaque tokens, not operating-system descriptors. COUNT and WRITTEN retain service results before STATUS is inspected. DATA is the transfer buffer.

OPEN requests readable input. CREATE requests writable output and replaces its contents. Each service is followed by an ordinary STATUS/JNZ check. No physical register or interrupt number appears in the program.

READ takes two saved arguments: the handle, then the buffer pointer. A supplies the requested count. Its returned count is stored before STATUS is read; a zero count with successful status means EOF. WRITE uses the same argument order. Both its status and its actual count are checked. The comparison cannot destroy the stored service status.

CLOSE releases each handle and its status is checked. FAILURE returns one; the environment releases remaining program resources on termination. Failure after creation can leave partial output. The copier treats all file bytes as data, including zero and Control-Z.

## Translate and assemble

Run CHECK IRKEEP and enter COPYFILE. Require `OK COPYFILE.ASM 03855 text bytes` and PASS. TYPE COPYFILE.ASM shows how this backend represents the virtual operations and appends its runtime.

Run CHECK ASMKEEP and enter COPYFILE. Require `OK 00687 bytes` and PASS. This second OK confirms assembly and address resolution; the translator's OK alone is insufficient.

## Exercise the binding

Use COPY CON IN.TXT to enter this sentence, finishing with Ctrl-Z and Enter:

```text
An IR86 file copy.
```

Then run:

```dos
CHECK COPYFILE
TYPE OUT.TXT
COMP IN.TXT OUT.TXT
```

Require PASS, the same sentence, and the COMP matching-files report with no differing bytes. Answer N when asked whether to compare more files. DOS 3.10 may report `Eof mark not found` for a file without its text marker; the comparison must still report `Files compare ok`.

For the missing-input test, use HOLD.TXT only if that name is free:

```dos
REN IN.TXT HOLD.TXT
CHECK COPYFILE
REN HOLD.TXT IN.TXT
```

Require FAIL. The earlier OUT.TXT is not replaced because input is opened before output is created. An unexpected PASS is a failed rejection check.

This same IR program can be given to another backend with the defined file services and corresponding input files. Only the generated code and binding implementation change. If a DOS result differs, inspect the generated call sequences and the private handle lookup; do not add register setup to the IR source.
