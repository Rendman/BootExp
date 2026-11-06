+++
title = "The first IR86 translator reference"
weight = 34
description = "A processor-independent contract, followed by the separate 8086/DOS binding."
download = "IR86.ASM"
download_group = "tools/ir86"
reader_names = 1
+++

This reference describes the first IR32 translator milestone. The [streaming IR contract](../060-the-streaming-ir-contract/index.html) supplies procedures, literal data, and allocated blocks used by the complete RILL toolchain. Keep the prompted and fixed-file builders separately named.

IR86 defines a virtual machine and a runtime-service interface. A backend implements that contract for a processor and environment. The language does not specify CPU registers, processor flags, interrupts, segments, or a native calling convention. The backend constructed in this collection emits assembly accepted by ASM0 and supplies a DOS binding.

## Values and storage

The virtual accumulator **A** holds an unsigned sixteen-bit word. Arithmetic wraps modulo 65536, independently of the processor's native arithmetic width. Signed comparisons interpret the same bits as two's-complement values from -32768 through 32767. A byte is eight bits. The initial value of A is unspecified; load it before use. These are IR data definitions, not requirements for a sixteen-bit processor.

Declared storage is a consecutive sequence of bytes without alignment padding. WORD stores its low byte first: this byte order is part of the IR contract. A backend on another byte order must preserve it. LDB and FETCHB return zero-extended byte values. STB and PUTB store the low eight bits of A and retain the complete A value.

A pointer identifies declared storage; its numeric representation is chosen by the backend. Obtain it with ADDR. Pointers may be saved, compared for equality, and advanced by valid byte offsets within declared storage. Do not assume an absolute address, inspect a pointer's bit pattern, depend on signed pointer ordering, or access memory outside declared storage. Zero is not a valid storage pointer. The backend need not detect an invalid access.

Code labels and storage names share a namespace, but have different uses. Branches and CALL require code labels. ADDR and named memory accesses require storage. Wrong-kind references, an invalid pointer, or RET without an active call are invalid program behavior; the small translator does not prove all such properties.

## Text form

- Each nonempty line is one operation followed by whitespace-separated arguments. Semicolon begins a comment. Case is ignored and tabs act as spaces.
- Names contain one through fourteen letters, digits, or underscores, beginning with a letter or underscore. Operation spellings may also be names.
- Numbers are unsigned decimal, or hexadecimal ending in H and beginning with a decimal digit: 0FFH is valid. Values are 0–65535; BYTE initializers narrow this to 0–255. Tokens may not exceed sixteen characters.
- Numeric tokens are values, not expressions. No signs, quoted strings, character constants, commas, macros, includes, or segment directives are defined. LIT takes a number; ADDR forms a named pointer.
- BYTE, WORD, and BUFFER declarations precede the first executable label, LABEL MAIN. Subsequent LABEL operations define code positions. A declaration after MAIN or executable operation before MAIN is rejected.
- MAIN is required. The normal end of a program terminates with status zero if control can fall through its last operation. HALT, EXIT, JMP, and RET are already terminal operations.

Normal CR/LF, bare CR, bare LF, a final line without a terminator, and Control-Z end-of-input are recognized by the text reader. Empty and comment-only lines have no runtime effect.

## Expression and call semantics

PUSH saves A on an abstract stack; POP retrieves the most recent saved word. A binary operation consumes one saved **left** operand and uses A as its **right** operand. SUB therefore computes left minus A.

The expression stack is empty at a label, transfer, call, return, service boundary, termination, and end of source. A comparison consumes its left operand before checking the empty boundary. READ and WRITE consume both their arguments before that check. Every source statement is checked, including unreachable code. The current translator supports thirty-two saved words within a basic block.

CALL passes A to a named procedure; RET returns its A value. Named storage holds persistent state. There is no implicit parameter list or local-variable frame. A procedure's own expressions must be balanced. No physical registers are part of this calling contract, and no processor call-stack layout is promised.

## Data and value operations

| Form | Stack effect | Defined action |
|---|---|---|
| BYTE name n | None | Declare one initialized byte |
| WORD name n | None | Declare one initialized word in IR byte order |
| BUFFER name count | None | Declare 1–256 consecutive zero bytes |
| LABEL name | Empty | Define a code position; the first is MAIN |
| LIT n | Unchanged | A = n |
| LD name | Unchanged | A = word in named storage |
| ST name | Unchanged | Store A as a word; retain A |
| LDB name | Unchanged | Load a byte and zero-extend it into A |
| STB name | Unchanged | Store the low byte; retain A |
| ADDR name | Unchanged | A = pointer to named storage |
| FETCH / FETCHB | Unchanged | Replace the pointer in A with its word/byte value |
| PUT / PUTB | Consume one | Pop a pointer and store A's word/byte there; retain A |
| PUSH | Add one | Save A |
| POP | Consume one | Replace A with the saved word |

Slashes in tables separate alternatives. Type one operation per line. Width belongs to the operation, not an inferred declaration type. A word access requires two valid consecutive bytes.

## Arithmetic and comparisons

ADD, SUB, AND, OR, and XOR each consume one saved left word and put the word result in A. ADD and SUB wrap modulo 65536; the others operate on all sixteen bits. There is no multiply, divide, remainder, shift, floating-point, or overflow-trapping operation. Such computations can be expressed by explicit procedures within the available operations.

| Form | Condition or result |
|---|---|
| NOP | No observable operation |
| JMP name | Transfer unconditionally |
| JZ name / JNZ name | Transfer if A is zero / nonzero; retain A |
| EQ name / NE name | Compare left and A for equality / inequality |
| ULT name / ULE name | Unsigned left less than / less than or equal to A |
| UGT name / UGE name | Unsigned left greater than / greater than or equal to A |
| SLT name / SLE name | Signed left less than / less than or equal to A |
| SGT name / SGE name | Signed left greater than / greater than or equal to A |
| CALL name | Call a procedure with A |
| RET | Return its A value |
| HALT | Terminate with program status zero |
| EXIT | Terminate with program status A modulo 256 |

Comparisons consume one saved word, require the remaining expression stack to be empty, and branch on their stated relation. They retain the **right operand** in A; they do not produce a Boolean word. All other transfers and terminations require an already empty expression stack. The conditions describe values, not hardware flags.

## Portable runtime services

Services operate on the program's byte streams and file environment. They set a persistent status word: **zero means success, one means failure**. STATUS copies that word into A and does not clear it. Its initial value is zero. Arithmetic, comparisons, loads, stores, and procedures without a service do not change it. A service inside a procedure can change it.

| Service | Arguments | Value returned in A |
|---|---|---|
| PUTC | Low eight bits of A | 1 after writing a byte, otherwise 0 |
| GETC | None | Byte 0–255, or 65535 for EOF/error |
| OPEN | A = pointer to zero-terminated ASCII name | Opaque readable handle, or 0 |
| CREATE | A = pointer to name | Opaque writable handle, or 0 |
| READ | Saved handle, then saved buffer pointer; A = requested count | Actual count; 0 for EOF or failure |
| WRITE | Same argument order as READ | Actual count, including partial progress |
| CLOSE | A = handle | 0; inspect STATUS |
| STATUS | None | Most recent service status, 0 or 1 |

All services except STATUS are empty-expression boundaries after consuming their arguments. STATUS is an ordinary value operation and may be used within an expression.

PUTC performs no newline conversion. GETC's EOF is successful: A is 65535 and STATUS is zero. An input error returns 65535 with STATUS one. Every byte value, including 255, remains distinct from EOF. Terminal buffering and echoing belong to the environment; redirected byte streams provide reproducible input.

OPEN opens an existing file for reading. CREATE prepares a write-only file and replaces its contents with an empty sequence on success. Handles are opaque tokens: save and pass them, test for zero, but do not perform arithmetic on them or treat them as operating-system descriptors. CLOSE invalidates a token after success. Its numeric value may be reused for a new file. Remaining program resources are released on termination.

READ returns a short count successfully when fewer bytes are available. Zero with STATUS zero is EOF; zero with STATUS one is failure. WRITE succeeds only for the requested complete count; a short write returns its partial count with STATUS one. Other file-service errors return zero with STATUS one. Zero-count READ and WRITE validate the handle, do not access the buffer, and return zero successfully; WRITE does not change the file in that case.

File names resolve in the binding's file environment. Available name forms, file availability, terminal policy, and resource capacity are environment properties. The examples use ordinary ASCII names IN.TXT and OUT.TXT. An error is reported through the normalized status, not an environment error number. A failure after creation can leave a partial output file.

## Current translator and target profile

This section describes the **8086/DOS implementation**, separately from the language above. Another backend must preserve the language and service results while choosing its own representation and environmental requirements.

Run CHECK IRKEEP or CHECK IR86. At `IR source name:` enter a one-to-eight-character DOS base name of letters, digits, or underscores. The tool reads NAME.IR and writes NAME.ASM in the current directory. Use ordinary disk names, excluding DOS devices such as CON and NUL even with an extension. These prompt restrictions do not define the IR runtime file-name interface.

Success prints `OK NAME.ASM nnnnn text bytes` and returns zero. Failure prints `IR ERROR nnnnn CODE n` and returns one. CHECK reports PASS or FAIL immediately. The line number is one-based physical input, or zero before reading. Source rejection leaves old assembly untouched; a write/close failure may leave partial output. Require a fresh OK, then a separate ASM0 OK before using NAME.COM.

This backend maps A to AX and uses a native stack for expression words and return addresses. The generated DOS header clears direction and checks the normal full-segment entry SP=FFFEH. Its failure status seven and its segment arrangement are target requirements, not language semantics. DS, ES, and SS retain the DOS program segment. Keep the upper 4 KB clear for native stack use; native call depth is not dynamically checked.

User names are prefixed U_. Conditional transfers use an opposite short condition around a near JMP, with I0001-style skip labels. I_ENTRY belongs to the entry header. R_ names and storage belong to the runtime. The backend appends that runtime after the program's terminating path.

The final DOS runtime reserves 448 machine bytes and 42 definitions. Its eight slots map opaque tokens to private descriptors. A slot stores the descriptor plus one, reserving zero for an unused entry, and a permission bit distinguishes readable and writable handles. R_FIND validates and translates a token. The program cannot obtain the descriptor through any IR operation.

The binding uses DOS handle reads and writes for byte streams, preserving all byte values under redirection. It converts service errors, EOF, short writes, and close results to the portable interface. Zero-count paths are handled explicitly. Ordinary DOS disk names are required in this environment, and resource exhaustion can occur before the runtime's maximum capacity is reached.

### Translation records

The native translator reuses the published ASM0 readers and table search. A fourteen-byte record contains an eight-byte zero-padded operation name, argument class, expression effect, this backend's machine-byte count, padding, and a template pointer. Machine-byte counts and templates are backend data, not definitions of IR meaning.

EXPAND substitutes @ with a saved name, # with a checked numeric spelling, and ? with a generated branch number. Runtime fragments are emitted as assembly text. ASM0 alone encodes the instructions. Each appended fragment remains separately identifiable in the translator's data, so a new service need not replace unrelated text.

FLOW handles ordinary operations, push, consume-one, empty boundary, consume-one-then-empty, terminal boundary, and consume-two-then-empty effects (codes 0 through 6). There is no hardware-flag state in the IR parser. SIZEADD and NEWDEF account for the selected backend, including its reserved runtime. OUTTEXT advances its text cursor; EMITCHAR preserves its byte argument and counts generated lines. WRITEOUT writes the accepted text only after validation.

### Implementation limits

| Resource | Current limit |
|---|---|
| Physical input | 4,000 lines, 120 characters per line |
| Tokens / names | 16 / 14 characters |
| BUFFER declaration | 1–256 bytes |
| Expression temporaries | 32 words within a basic block |
| Assembly text | 32,768 bytes including CR/LF |
| Generated assembly | 4,000 lines and 256 definitions |
| Generated machine image | 8,192 bytes, including header and runtime |
| Open files in this binding | At most eight opaque handles; services still report environment failures |
| Native memory arrangement | Full 64 KB DOS segment, normal entry stack |

The final header and runtime consume 43 of the definition entries, leaving 213 for user definitions and conditional skip labels. Duplicates and undefined names are diagnosed by ASM0. These finite implementation limits do not make the language's operations processor instructions.

### Diagnostics

| Code | Meaning |
|---|---|
| 1 | Syntax/context: unknown operation, extra token, misplaced statement/declaration, overlong token, or bad tool base name |
| 2 | Numeric spelling or word overflow |
| 3 | Malformed/overlong name or missing/incorrect first MAIN label |
| 4 | Byte/buffer range, expression underflow, or nonempty control boundary |
| 5 | Input, text, line, definition, image, or expression capacity exceeded |
| 6 | Translator file failure, short write, or invalid source byte |
| 7 | Native translator entry stack differs from its target requirement |

A runtime service failure is different: it sets the portable STATUS word in the generated program. The translator's diagnostic codes concern building that program. ASM0's later line reports refer to generated assembly, not directly to IR source lines.

## Complete DOS binding source

The following fragment is appended by this backend. It implements the services above; it is not a standalone executable to run. Its physical registers, interrupt numbers, and descriptor representation do not occur in IR programs.

```asm
R_OK:
MOV DX,0
MOV [R_STATUS],DX
RET
R_ERROR:
MOV DX,1
MOV [R_STATUS],DX
RET
R_FAIL:
MOV AX,0
JMP R_ERROR

R_PUTC:
MOV [R_BYTE],AL
MOV BX,1
MOV CX,1
MOV DX,R_BYTE
MOV AH,40H
INT 21H
JAE R_PUTCOUNT
JMP R_FAIL
R_PUTCOUNT:
CMP AX,1
JE R_PUTGOOD
JMP R_ERROR
R_PUTGOOD:
JMP R_OK

R_GETC:
MOV BX,0
MOV CX,1
MOV DX,R_BYTE
MOV AH,3FH
INT 21H
JAE R_GETCOUNT
MOV AX,65535
JMP R_ERROR
R_GETCOUNT:
CMP AX,0
JNE R_GETBYTE
MOV AX,65535
JMP R_OK
R_GETBYTE:
MOV AL,[R_BYTE]
MOV AH,0
JMP R_OK

R_OPEN:
MOV DX,3D00H
JMP R_FILE

R_CREATE:
MOV DX,3C00H
JMP R_FILE

R_FILE:
MOV [R_MODE],DX
MOV [R_NAME],AX
CALL R_FREE
CMP BX,0
JNE R_HAVESLOT
JMP R_FAIL
R_HAVESLOT:
MOV DX,[R_NAME]
MOV CX,0
MOV AX,[R_MODE]
INT 21H
JAE R_FILEGOOD
JMP R_FAIL
R_FILEGOOD:
INC AX
MOV DX,[R_MODE]
CMP DX,3C00H
JNE R_READSLOT
ADD AX,8000H
R_READSLOT:
MOV BX,[R_SLOT]
MOV [BX],AX
MOV AX,[R_NUMBER]
JMP R_OK
R_FREE:
MOV BX,R_HANDLES
MOV CX,1
R_NEXTSLOT:
MOV AX,[BX]
CMP AX,0
JE R_SLOTFOUND
ADD BX,2
INC CX
CMP CX,9
JB R_NEXTSLOT
MOV BX,0
RET
R_SLOTFOUND:
MOV [R_SLOT],BX
MOV [R_NUMBER],CX
RET

R_FIND:
CMP BX,1
JB R_BADHANDLE
CMP BX,8
JA R_BADHANDLE
DEC BX
ADD BX,BX
ADD BX,R_HANDLES
MOV [R_SLOT],BX
MOV BX,[BX]
CMP BX,0
JE R_BADHANDLE
MOV AX,1
CMP BX,8000H
JB R_HANDLEKIND
AND BX,7FFFH
MOV AX,2
R_HANDLEKIND:
DEC BX
RET
R_BADHANDLE:
MOV AX,0
RET

R_READ:
MOV [R_COUNT],AX
MOV [R_BUFFER],DX
CALL R_FIND
CMP AX,1
JE R_READVALID
JMP R_FAIL
R_READVALID:
MOV CX,[R_COUNT]
CMP CX,0
JNE R_READMORE
MOV AX,0
JMP R_OK
R_READMORE:
MOV DX,[R_BUFFER]
MOV AH,3FH
INT 21H
JAE R_READGOOD
JMP R_FAIL
R_READGOOD:
JMP R_OK

R_WRITE:
MOV [R_COUNT],AX
MOV [R_BUFFER],DX
CALL R_FIND
CMP AX,2
JE R_WRITEVALID
JMP R_FAIL
R_WRITEVALID:
MOV CX,[R_COUNT]
CMP CX,0
JNE R_WRITEMORE
MOV AX,0
JMP R_OK
R_WRITEMORE:
MOV DX,[R_BUFFER]
MOV AH,40H
INT 21H
JAE R_WRITECOUNT
JMP R_FAIL
R_WRITECOUNT:
MOV DX,[R_COUNT]
CMP AX,DX
JE R_WRITEGOOD
JMP R_ERROR
R_WRITEGOOD:
JMP R_OK

R_CLOSE:
MOV BX,AX
CALL R_FIND
CMP AX,0
JNE R_CLOSEVALID
JMP R_FAIL
R_CLOSEVALID:
MOV AH,3EH
INT 21H
JAE R_CLOSEGOOD
JMP R_FAIL
R_CLOSEGOOD:
MOV BX,[R_SLOT]
MOV AX,0
MOV [BX],AX
JMP R_OK

R_STATUS:
DW 0

R_BYTE:
DB 0

R_MODE:
DW 0
R_NAME:
DW 0
R_SLOT:
DW 0
R_NUMBER:
DW 0
R_HANDLES:
DW 0,0,0,0,0,0,0,0

R_COUNT:
DW 0
R_BUFFER:
DW 0
```

For this binding consult Intel Corporation, *The 8086 Family User's Manual*, October 1979, and the MS-DOS 3.10 programmer's reference supplied with the machine, particularly INT 21H handle services and process termination. These document the implementation target; the portable service contract above remains the interface used by IR source.
