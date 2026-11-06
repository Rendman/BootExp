"""Maintain exact type-in patches, working checkpoints, and downloadable sources."""
from publication_names import write_page
from pathlib import Path
import json, re, shutil, zipfile
ROOT=Path(__file__).resolve().parents[1]
WORK=ROOT/'workbench/bootasm'
CONTENT=ROOT/'site/content/bootstrap/bootasm'
DOWNLOAD=ROOT/'site/static/downloads/bootasm'
for p in (WORK,CONTENT,DOWNLOAD): p.mkdir(parents=True,exist_ok=True)
def dos(path,text):
    path.write_bytes((text.rstrip()+'\n').replace('\r\n','\n').replace('\n','\r\n').encode('ascii'))
def lines(text):
    result={}
    for line in text.strip().splitlines():
        n,body=line.split(' ',1); result[int(n)]=body
    return result
stages=[]
DESCRIPTIONS = {
    'Reading a source file': 'From lines of source to an exact sequence of bytes.',
    'Tidying the input': 'Making room for spaces, comments, and lowercase letters.',
    'Hexadecimal numbers': 'Reading base sixteen and catching malformed numbers.',
    'Several bytes on one line': 'A row of data, one comma at a time.',
    'Putting a word on disk': 'Sixteen-bit values, with the low byte first.',
    'Instructions without operands': 'The first mnemonics and their one-byte encodings.',
    'Loading a register': 'Register names, operand sizes, and immediate values.',
    'Making a DOS request': 'Display a character and return control to DOS.',
    'Counting twice': 'One pass to count the bytes, another to collect them.',
    'Giving positions names': 'A symbol table gives each label its address.',
    'Using names as values': 'Resolve forward references without hand-counting offsets.',
    'Copying between registers': 'Copy a value with a register-to-register MOV.',
    'The stack and single-register work': 'Move an index, save a word, and mind the stack.',
    'Arithmetic and comparisons': 'Adding, subtracting, testing bits, and setting flags.',
    'Reading and writing memory': 'Transfer bytes and words through BX or a named address.',
    'Calling and jumping': 'Near transfers, return addresses, and relative displacements.',
    'Short conditional branches': "Let the flags choose a path, within a signed byte's reach.",
}
def stage(title,code,why,explain,fixture,expected,bad,diagnostic,*,remove=(),run=None):
    stages.append(dict(title=title,patch=lines(code),why=why,explain=explain,fixture=fixture,
                       expected=expected,bad=bad,diagnostic=diagnostic,remove=remove,run=run))
VIEW='''10 ON ERROR GOTO 900
20 LINE INPUT "File: "; F$
25 OPEN "I", #1, F$: CLOSE #1
30 OPEN "R", #1, F$, 1
40 FIELD #1, 1 AS B$
50 N=LOF(1)
60 PRINT "Length:"; N
70 IF N=0 THEN CLOSE: END
80 FOR I=1 TO N
90 GET #1, I
100 PRINT RIGHT$("0"+HEX$(ASC(B$)),2); " ";
110 IF I MOD 16=0 THEN PRINT
120 NEXT I
130 IF N MOD 16<>0 THEN PRINT
140 CLOSE
150 END
900 PRINT "Cannot read file. BASIC error"; ERR
910 CLOSE: END
'''
BYTE='''10 ON ERROR GOTO 900
20 LINE INPUT "Decimal byte (0-255): "; T$
30 IF T$="" THEN PRINT "Bad byte": END
40 N=0
50 FOR I=1 TO LEN(T$)
60 D=ASC(MID$(T$,I,1))-48
70 IF D<0 OR D>9 THEN PRINT "Bad byte": END
80 N=N*10+D
90 IF N>255 THEN PRINT "Bad byte": END
100 NEXT I
110 OPEN "O", #1, "BYTE.COM"
120 CLOSE #1
130 OPEN "R", #1, "BYTE.COM", 1
140 FIELD #1, 1 AS B$
150 LSET B$=CHR$(N)
160 PUT #1, 1
170 CLOSE
180 PRINT "Wrote BYTE.COM: 1 byte"
190 END
900 PRINT "BASIC error"; ERR; "at"; ERL
910 CLOSE: END
'''
stage('Reading a source file','''10 ON ERROR GOTO 9500
20 DIM B%(4095)
30 LINE INPUT "Source name (no extension): "; F$
80 OPEN "I", #1, F$+".ASM"
90 P=0: L=0
100 IF EOF(1) THEN 300
110 LINE INPUT #1, S$
120 L=L+1
160 IF S$="" THEN 100
170 I=INSTR(S$+" "," "): M$=LEFT$(S$,I-1)
180 A$=MID$(S$,I+1)
200 GOSUB 4000
210 GOTO 100
300 CLOSE #1
310 OPEN "O", #2, F$+".COM"
320 CLOSE #2
325 KILL F$+".COM"
330 OPEN "R", #2, F$+".COM", 1
340 FIELD #2, 1 AS O$
345 IF P=0 THEN 380
350 FOR I=0 TO P-1
360 LSET O$=CHR$(B%(I)): PUT #2, I+1
370 NEXT I
380 CLOSE: PRINT "OK "; F$; ".COM"; P; "bytes"
390 END
2000 IF T$="" THEN E$="Missing value": GOTO 9000
2020 N=0
2060 FOR NI=1 TO LEN(T$)
2070 D=ASC(MID$(T$,NI,1))-48
2080 IF D<0 OR D>9 THEN E$="Bad number": GOTO 9000
2090 N=N*10+D
2100 IF N>65535 THEN E$="Number too large": GOTO 9000
2110 NEXT NI: RETURN
3000 IF X<0 OR X>255 THEN E$="Byte out of range": GOTO 9000
3010 IF P=4096 THEN E$="Program too large": GOTO 9000
3020 B%(P)=X
3030 P=P+1: RETURN
4000 IF M$="DB" THEN GOSUB 4100: RETURN
4090 E$="Unknown instruction": GOTO 9000
4100 T$=A$: GOSUB 2000
4140 X=N: GOSUB 3000: RETURN
9000 PRINT "ERROR line"; L; ": "; E$
9010 CLOSE: END
9500 PRINT "BASIC error"; ERR; "at"; ERL
9510 CLOSE: END
''',
'A single byte is a useful disk experiment, but a program needs a sequence. We shall read one decimal byte from each source line and keep the result in memory until the whole source has been accepted.',
'''`B%` is an integer array with 4,096 elements, numbered 0 through 4,095. `P` is the number of bytes collected; it is also the index of the next free element. This limit keeps the array to 8,192 bytes of BASIC storage. It deliberately limits our programs, rather than the processor.

Lines 80-210 open `name.ASM` as a sequential input file. `LINE INPUT` reads a whole line without treating commas as input separators. `L` counts physical source lines, including empty ones. At 170, the first space ends the instruction name `M$`; the remainder becomes the argument `A$`. At this checkpoint use uppercase `DB`, one space, and one decimal number.

The dispatcher at 4000 selects the routine for `DB`, meaning *define byte*. Routine 2000 takes a number in `T$` and returns its value in `N`. It changes `NI` and `D`, but leaves the argument string alone. Each digit is checked before it is included; the bound is checked after each multiplication. This avoids accepting BASIC expressions or mistyped suffixes.

Routine 3000 takes a byte in `X`, checks its range and available space, and advances `P`. It preserves `N`. The output loop opens a fresh file only after the source succeeds. Line 345 skips the FOR loop for an empty image: GW-BASIC enters a FOR body once even when its starting value already exceeds its limit. One-character random records write exactly one byte each. `OPEN "O"` followed by `CLOSE` first ensures that the output name exists. `KILL` then removes it before the random file is created, so a shorter assembly cannot leave an old tail. Closing a sequential output file can leave a DOS end-of-file character; removing that file also makes a truly empty result possible. BASIC's `BSAVE` adds a header, which a `.COM` file must not have.

The error exits close all open files. An assembly error leaves any existing `.COM` file unchanged. An input/output error while writing can leave a partial file; only an `OK` report means the write finished.''',
'DB 65\nDB 66\nDB 67','41 42 43','DB 256','Byte out of range')
stage('Tidying the input','''40 GOSUB 8000
125 IF L>2000 THEN E$="Too many source lines": GOTO 9000
130 IF LEN(S$)>120 THEN E$="Source line too long": GOTO 9000
150 GOSUB 1000
180 A$=""
185 FOR J=I+1 TO LEN(S$)
190 C$=MID$(S$,J,1): IF C$<>" " THEN A$=A$+C$
195 NEXT J
1000 FOR I=1 TO LEN(S$)
1010 C=ASC(MID$(S$,I,1))
1020 IF C=9 THEN MID$(S$,I,1)=" "
1030 IF C>=97 AND C<=122 THEN MID$(S$,I,1)=CHR$(C-32)
1040 NEXT I
1050 I=INSTR(S$,";"): IF I>0 THEN S$=LEFT$(S$,I-1)
1060 IF LEFT$(S$,1)=" " THEN S$=MID$(S$,2): GOTO 1060
1070 IF RIGHT$(S$,1)=" " THEN S$=LEFT$(S$,LEN(S$)-1): GOTO 1070
1080 RETURN
8000 IF LEN(F$)<1 OR LEN(F$)>8 THEN E$="Bad filename": GOTO 9000
8005 FC$="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_"
8010 FOR FI=1 TO LEN(F$)
8020 C$=MID$(F$,FI,1)
8030 IF INSTR(FC$,C$)=0 THEN E$="Bad filename": GOTO 9000
8040 NEXT FI: RETURN
''',
'Indentation and a note in the margin should not spoil a source line. We can improve that without changing the byte writer.',
'''Routine 1000 takes `S$` and returns a cleaned line in the same variable. It changes `I`, `C`, and individual characters. ASCII lowercase letters are 32 greater than their uppercase partners; tabs become spaces. A semicolon begins a comment, and the loops at 1060-1070 remove spaces from the ends. They also handle a line containing only spaces.

The argument builder at 180-195 removes spaces from operands. There are no quoted strings in this language, so there is no quoted space to preserve. Write each number as one token even though this small parser ignores operand spaces. The mnemonic still ends at the first space.

The source is limited to 2,000 physical lines of at most 120 characters each. Both limits keep a typing error from becoming an unmanageable job. The filename routine takes `F$`, uses `FI`, `FC$`, and `C$`, and allows only a one-to-eight-character base name made of letters, digits, and underscores. Paths and extensions are excluded so the input and output names stay predictable.''',
'; Three letters\n  db 65 ; first\n\n\tdb 66\nDB 67','41 42 43','DB -1','Bad number')
stage('Hexadecimal numbers','''2020 Q$=T$: BA=10
2030 IF RIGHT$(Q$,1)="H" THEN BA=16: Q$=LEFT$(Q$,LEN(Q$)-1)
2040 IF Q$="" THEN E$="Bad number": GOTO 9000
2050 N=0
2060 FOR NI=1 TO LEN(Q$)
2070 D=INSTR("0123456789ABCDEF",MID$(Q$,NI,1))-1
2080 IF D<0 OR D>=BA THEN E$="Bad number": GOTO 9000
2090 N=N*BA+D
''',
'Machine-code tables are easier to read in hexadecimal. The byte writer need not change; only the reader of numbers needs another base.',
'''A hexadecimal digit describes four bits. The digits run from 0 through 9 and then A through F, meaning ten through fifteen. Thus `41H` is four sixteens plus one, or decimal 65. The suffix `H` selects base sixteen; no suffix selects base ten.

The number routine now copies `T$` into `Q$` and chooses `BA`, its base. The suffix is removed from the copy. `INSTR` finds a digit in the ordered digit string; subtracting one gives its value, or -1 if it is absent. The range test rejects a hexadecimal letter in a decimal number. Multiplication by `BA` moves the preceding digits one place left.

`N` may reach 65,535, because other callers will need words. The byte emitter still rejects anything above 255. Write hexadecimal constants with a leading decimal digit, such as `0FFH`; this spelling will distinguish numbers from names.''',
'DB 41H\nDB 66\nDB 0FFH','41 42 FF','DB 1GH','Bad number')
stage('Several bytes on one line','''4100 IF A$="" THEN E$="Missing value": GOTO 9000
4110 DA$=A$
4120 DI=INSTR(DA$+",",","): T$=LEFT$(DA$,DI-1)
4130 GOSUB 2000
4140 X=N: GOSUB 3000
4150 DA$=MID$(DA$,DI+1)
4160 IF DA$<>"" THEN 4120
4170 IF RIGHT$(A$,1)="," THEN E$="Missing value": GOTO 9000
4180 RETURN
''',
'A row of character codes ought to occupy a row of source. We shall let DB accept a comma-separated list, using the number routine for each item.',
'''Routine 4100 keeps the unprocessed part in `DA$`. Searching `DA$+","` guarantees that a separator can be found even for the final item. `DI` locates it, `T$` receives the item, and the existing routines read and store it. `MID$` then removes the item and its comma.

`DA$` and `DI` belong to this loop. The number reader changes `Q$`, `BA`, `NI`, `D`, and `N`, but does not alter them. The emitter preserves them as well. The test at 4170 rejects a comma at the end; two adjacent commas produce an empty item and the same diagnostic. No string constants or repetition syntax are being added.''',
'DB 41H,42H,43H,0','41 42 43 00','DB 1,','Missing value')
stage('Putting a word on disk','''3100 X=N-256*INT(N/256): GOSUB 3000
3110 X=INT(N/256): GOSUB 3000
3120 RETURN
4000 IF M$="DB" OR M$="DW" THEN GOSUB 4100: RETURN
4110 DA$=A$: DW=0
4115 IF M$="DW" THEN DW=1
4140 IF DW=0 THEN X=N: GOSUB 3000 ELSE GOSUB 3100
''',
'The processor uses 16-bit quantities as well as bytes. A define-word directive gives us a direct way to check their order on disk.',
'''`DW` means *define word*. A word holds 0 through 65,535. The 8088 stores its low byte first. The word `1234H` is therefore written as `34 12`, not `12 34`.

Routine 3100 takes `N` and emits two bytes through 3000. `INT(N/256)` is the high byte; subtracting 256 times that value leaves the low byte. This arithmetic avoids BASIC's signed integer division and logical operators for unsigned values above 32,767. Routine 3100 changes `X` and `P` and preserves `N`.

`DW` in line 4110 is an ordinary numeric flag, distinct from the text in `M$`. It selects one or two bytes for every item. Do not confuse a word in the file with a BASIC integer variable: BASIC integers are signed.''',
'DW 1234H,65535\nDB 0','34 12 FF FF 00','DW 65536','Number too large')
stage('Instructions without operands','''4010 X=-1
4012 IF M$="NOP" THEN X=144
4014 IF M$="RET" THEN X=195
4016 IF M$="CLD" THEN X=252
4018 IF M$="LODSB" THEN X=172
4020 IF M$="STOSB" THEN X=170
4022 IF X>=0 THEN GOSUB 4900: RETURN
4900 IF A$<>"" THEN E$="Unexpected operand": GOTO 9000
4910 GOSUB 3000: RETURN
''',
'A mnemonic is a name for an instruction. Five instructions with fixed one-byte encodings let us add names without yet designing an operand parser.',
'''The dispatcher sets `X` to -1, meaning that no fixed instruction has matched. A match replaces it with an opcode, the byte which tells the processor what to do. Routine 4900 checks that there is no argument before passing `X` to the emitter. It changes `P`, preserving the source arguments.

`NOP` performs no operation. `RET` takes a return address from the stack. `CLD` clears the direction flag so string instructions advance their indexes. `LODSB` loads AL from DS:SI, then advances or retreats SI according to that flag. `STOSB` stores AL at ES:DI and adjusts DI. DS and ES are segment registers; SI and DI are index registers. These last instructions are included for explicit byte-by-byte work, rather than repeated string operations.

At this checkpoint we are checking encodings only. In particular, a stray RET or string instruction is not a complete test program: the stack, segment registers, and indexes must have suitable values. Inspect this fixture without running it.''',
'NOP\nRET\nCLD\nLODSB\nSTOSB','90 C3 FC AC AA','NOP 1','Unexpected operand')
stage('Loading a register','''4024 IF M$="MOV" THEN GOSUB 4200: RETURN
4200 GOSUB 5000: T$=A1$: GOSUB 6000
4210 IF R<0 THEN E$="Register required": GOTO 9000
4220 RD=R: WD=W
4226 T$=A2$: GOSUB 2000
4230 X=176+8*WD+RD: GOSUB 3000
4240 IF WD=0 THEN X=N: GOSUB 3000: RETURN
4250 GOSUB 3100: RETURN
5000 I=INSTR(A$,",")
5010 IF I<2 OR I=LEN(A$) THEN E$="Two operands required": GOTO 9000
5020 A1$=LEFT$(A$,I-1): A2$=MID$(A$,I+1)
5030 IF INSTR(A2$,",")>0 THEN E$="Two operands required": GOTO 9000
5040 RETURN
6000 R=-1: W=0
6010 IF LEN(T$)<>2 THEN RETURN
6020 FOR RI=0 TO 7
6030 IF T$=MID$("ALCLDLBLAHCHDHBH",2*RI+1,2) THEN R=RI: RETURN
6040 NEXT RI
6050 W=1
6060 FOR RI=0 TO 7
6070 IF T$=MID$("AXCXDXBXSPBPSIDI",2*RI+1,2) THEN R=RI: RETURN
6080 NEXT RI: RETURN
''',
'A DOS service takes its request in registers. We shall first teach MOV to load a constant, with the register name determining its size.',
'''A register is a small working store inside the processor. AX, CX, DX, BX, SP, BP, SI, and DI are 16-bit registers, numbered zero through seven in that order for these encodings. AL, CL, DL, BL, AH, CH, DH, and BH are the corresponding encoding order for 8-bit registers. AL and AH are the low and high halves of AX; the same rule holds for CX, DX, and BX. The other four word registers have no byte halves accessible by those names.

Routine 5000 splits `A$` into destination `A1$` and source `A2$`, rejecting a missing or extra comma. It changes `I` but no numeric value. Routine 6000 takes a register name in `T$`, returns its number in `R` and width in `W` (zero for byte, one for word), and uses `RI` as its loop index. `R=-1` means no register matched; in that case `W` has no meaning.

The MOV routine saves the destination number and width in `RD` and `WD` before reading the source number. The opcode is B0H plus the register number for a byte, or B8H plus the number for a word. The immediate value follows it. *Immediate* means the value is part of the instruction. MOV does not alter the arithmetic flags.

A word register accepts a value up to 65,535; a byte register accepts at most 255. No automatic truncation is performed. This fixture checks encodings and must not be executed.''',
'MOV AL,41H\nMOV AX,1234H\nMOV DX,65535','B0 41 B8 34 12 BA FF FF','MOV AL,256','Byte out of range')
stage('Making a DOS request','''4026 IF M$="INT" THEN GOSUB 5100: RETURN
5100 T$=A$: GOSUB 2000
5110 X=205: GOSUB 3000
5120 X=N: GOSUB 3000: RETURN
''',
'We can load registers, but a complete program must also ask DOS to do something and then return control to it. INT supplies that connection.',
'''`INT n` performs a software interrupt. Its encoding is CDH followed by the interrupt number, which must fit in a byte. Routine 5100 takes the argument in `A$`, reads it through `T$`, emits the fixed opcode and then the number, and advances `P`. It changes `T$`, `N`, `X`, and the numeric reader's scratch variables.

DOS uses interrupt 21H. For function 02H, put 2 in AH and a character code in DL; DOS displays the character. Function 4CH terminates a program, with the return code in AL. Loading AX with 4C00H sets both the function and a zero return code in one instruction.

DOS loads a `.COM` file at offset 0100H in a segment. Its first 256 bytes hold the Program Segment Prefix, or PSP, maintained by DOS. At entry CS, DS, ES, and SS identify this segment. The stack normally begins near its upper end. Our test does not change those segment registers or depend on uninitialized general registers. BASIC must return to the DOS prompt before the new program can be run.''',
'MOV DL,42H\nMOV AH,2\nINT 21H\nMOV AX,4C00H\nINT 21H','B2 42 B4 02 CD 21 B8 00 4C CD 21','INT 256','Byte out of range',run='B')
stage('Counting twice','''70 FOR PS=1 TO 2
305 NEXT PS
3020 IF PS=2 THEN B%(P)=X
''',
'A source file can be read once to count its bytes and again to collect them. We shall establish those two passes while all operands are still numeric.',
'''The new FOR loop begins before opening the source and ends after closing it. Each pass resets `P` and `L` at line 90. `PS` is one for the counting pass and two for the collecting pass. Routine 3000 performs the same range and capacity checks in either pass, but only pass two stores bytes in the array.

Nothing is written to disk until both passes finish. The file is reopened rather than retained in a string array, saving BASIC memory. The same instruction always has the same length; no instruction shortening is attempted. Those choices make the second pass reproduce the first pass's positions.

The output loop uses the second pass's byte count. There is still only one OK report and one output file. Do not edit the source while an assembly is running. The test below must produce exactly the same result as a one-pass assembly.''',
'MOV AX,4C00H\nINT 21H','B8 00 4C CD 21','DB 256','Byte out of range',run='')
stage('Giving positions names','''22 DIM SY$(255), SV(255)
65 SC=0
158 IF RIGHT$(S$,1)=":" THEN T$=LEFT$(S$,LEN(S$)-1): GOSUB 7000: GOTO 100
7000 GOSUB 7100: GOSUB 7200
7010 IF PS=2 THEN RETURN
7020 IF SI>=0 THEN E$="Duplicate label": GOTO 9000
7030 IF SC=256 THEN E$="Too many labels": GOTO 9000
7040 SY$(SC)=T$: SV(SC)=256+P: SC=SC+1
7050 RETURN
7100 IF LEN(T$)<1 OR LEN(T$)>16 THEN E$="Bad label": GOTO 9000
7110 C$=LEFT$(T$,1)
7120 IF INSTR("ABCDEFGHIJKLMNOPQRSTUVWXYZ_",C$)=0 THEN E$="Bad label": GOTO 9000
7130 FOR K=1 TO LEN(T$)
7140 C$=MID$(T$,K,1)
7150 IF INSTR("ABCDEFGHIJKLMNOPQRSTUVWXYZ_0123456789",C$)=0 THEN E$="Bad label": GOTO 9000
7160 NEXT K
7170 GOSUB 6000: IF R>=0 THEN E$="Reserved label": GOTO 9000
7180 RETURN
7200 SI=-1
7205 IF SC=0 THEN RETURN
7210 FOR K=0 TO SC-1
7220 IF SY$(K)=T$ THEN SI=K: RETURN
7230 NEXT K: RETURN
''',
'The counting pass knows where each source line will lie. We can give a position a name without emitting another byte.',
'''A label is written alone on a line, followed by a colon. Its value is the address of the next byte: 256 plus `P`. A label may precede code or data, and several different labels may name the same position. The colon is a definition mark and is not part of the name.

Routine 7100 checks `T$`. Names contain one to sixteen uppercase letters, digits, or underscores; the first character cannot be a digit. Normalization makes lowercase spelling equivalent. Register names are reserved because they would be ambiguous in operands. The validator changes `K`, `C$`, and the register reader's scratch variables; it preserves `T$`.

Routine 7200 searches the first `SC` entries and returns the matching index `SI`, or -1. Routine 7000 enters a definition only in pass one, using parallel arrays `SY$` for names and `SV` for values. A repeated name is an error, even if its value would be unchanged. The table holds 256 names, a deliberate storage bound. The arrays run from zero through 255; the full-table test prevents a write beyond that allocation. Pass two validates definitions without entering them again.

At this checkpoint names are recorded, but numeric operands are still required. A label line should make no difference to the bytes collected.''',
'START:\nDB 41H\nFINISH:\nDB 42H','41 42','AGAIN:\nDB 1\nAGAIN:','Duplicate label')
stage('Using names as values','''2010 IF LEFT$(T$,1)<"0" OR LEFT$(T$,1)>"9" THEN GOSUB 2200: RETURN
2200 GOSUB 7100: GOSUB 7200
2210 IF SI>=0 THEN N=SV(SI): RETURN
2220 IF PS=1 THEN N=0: RETURN
2230 E$="Undefined label": GOTO 9000
''',
'A recorded address can replace a hand-counted constant. We shall allow a name wherever a whole numeric value is accepted, including a name defined farther down the source.',
'''The numeric reader now examines the first character before parsing digits. A token beginning with a decimal digit is numeric; everything else must pass the label validator. This is why an all-letter hexadecimal number needs a leading zero: write `0ABH`, not `ABH`.

Routine 2200 uses the same name search as a definition. A known name returns its value in `N`. An unknown name returns zero during pass one, because all accepted forms have fixed lengths. In pass two every definition has been seen; an unknown name is then an error.

The routine changes the validator's and searcher's scratch variables, but preserves the DB list's `DA$` and `DI`. A named address in DW is useful because an address normally exceeds one byte. DB still rejects a named value above 255. There is no expression evaluator: `TEXT+1`, a minus sign, or an EQU definition is outside this language.

Our test places the word before the byte it names. The word takes two bytes, so TEXT is at 0102H. Inspect the bytes; this is data, not a program.''',
'DW TEXT\nTEXT:\nDB 41H','02 01 41','DW MISSING','Undefined label')
stage('Copying between registers','''4222 T$=A2$: GOSUB 6000
4224 IF R>=0 THEN GOSUB 4300: RETURN
4300 IF WD<>W THEN E$="Register sizes differ": GOTO 9000
4310 X=138+WD: GOSUB 3000
4320 X=192+8*RD+R: GOSUB 3000
4330 RETURN
''',
'A constant is not the only source for MOV. Copying one register to another gives us a first encounter with the byte which describes operands.',
'''The source is tried as a register before it is tried as a number or name. The saved `RD` and `WD` describe the destination; `R` and `W` describe the source. The widths must agree. MOV AX,AL would not say which half to extend, and this assembler refuses it.

For this direction of MOV, the opcode is 8AH for a byte or 8BH for a word. A second byte, called ModR/M, describes the operands. Bits 7-6 are 11 for register operands, contributing 192. Bits 5-3 hold the destination register number, contributing eight times `RD`. Bits 2-0 hold the source register number `R`.

Routine 4300 takes those four saved and current register values, emits the opcode and ModR/M byte, and changes `X` and `P`. It preserves the register values. For MOV AX,BX, the second byte is C3H: 192 plus zero plus three. This fixture checks encodings only.''',
'MOV AX,BX\nMOV DL,AL\nMOV CH,BH','8B C3 8A D0 8A EF','MOV AX,AL','Register sizes differ')
stage('The stack and single-register work','''4028 IF M$="INC" OR M$="DEC" OR M$="PUSH" OR M$="POP" THEN GOSUB 5200: RETURN
5200 T$=A$: GOSUB 6000
5210 IF R<0 OR W<>1 THEN E$="Word register required": GOTO 9000
5220 X=64+R
5230 IF M$="DEC" THEN X=72+R
5240 IF M$="PUSH" THEN X=80+R
5250 IF M$="POP" THEN X=88+R
5260 GOSUB 3000: RETURN
''',
'Indexes must move, and a routine sometimes needs to put a word aside. Four families of one-byte instructions cover these small jobs.',
'''INC adds one and DEC subtracts one, with 16-bit wraparound. They update arithmetic flags but preserve the carry flag. PUSH decrements SP by two and stores a word at SS:SP. POP reads a word there and advances SP by two. PUSH and POP do not change the arithmetic flags.

The opcodes start at 40H, 48H, 50H, and 58H respectively; the register number is added to the starting value. Routine 5200 takes the one argument in `A$`, checks it through 6000, chooses the base, and sends the byte to 3000. It changes `T$`, `R`, `W`, `RI`, `X`, and `P`.

Only word-register forms are accepted. The processor has other INC and DEC forms, but supporting them would require more operand rules. Avoid PUSH SP: on the 8086/8088 it stores the already-decremented SP, unlike later processors. POP SP replaces the stack pointer itself. Never experiment with either form without understanding the resulting stack. Ordinary PUSH and POP pairs must be balanced before a RET.

This fixture is for byte inspection only; its register values have not been initialized.''',
'INC BX\nDEC CX\nPUSH AX\nPOP DX','43 49 50 5A','INC AL','Word register required')
stage('Arithmetic and comparisons','''4030 I=INSTR("ADD OR  AND SUB XOR CMP ",M$+" ")
4032 IF I>0 THEN IF (I-1) MOD 4=0 THEN GOSUB 4390: RETURN
4390 OP=VAL(MID$("014567",(I-1)/4+1,1)): GOTO 4400
4400 GOSUB 5000: T$=A1$: GOSUB 6000
4410 IF R<0 THEN E$="Register required": GOTO 9000
4420 RD=R: WD=W
4430 T$=A2$: GOSUB 6000
4440 IF R>=0 THEN GOSUB 4500: RETURN
4450 T$=A2$: GOSUB 2000
4460 X=128+WD: GOSUB 3000
4470 X=192+8*OP+RD: GOSUB 3000
4480 IF WD=0 THEN X=N: GOSUB 3000: RETURN
4490 GOSUB 3100: RETURN
4500 IF WD<>W THEN E$="Register sizes differ": GOTO 9000
4510 X=8*OP+2+WD: GOSUB 3000
4520 X=192+8*RD+R: GOSUB 3000
4530 RETURN
''',
'To work on a character or count, a program needs arithmetic and tests. The same operand machinery serves six closely related instruction families.',
'''ADD and SUB alter the destination by addition or subtraction. CMP sets the subtraction flags without storing the answer. AND, OR, and XOR perform bit-by-bit logical operations. All these forms set flags; logical operations clear carry and overflow and leave auxiliary carry undefined. Arithmetic carries beyond the selected width are not stored in the destination.

The mnemonic table uses four characters per entry, including spaces. A matching name must begin at an entry boundary. The matching position selects an operation number from `014567`: ADD=0, OR=1, AND=4, SUB=5, XOR=6, CMP=7. These are the processor's group numbers, not consecutive entries invented by the assembler. `OP` preserves that choice while the operands are read.

For a register source, routine 4500 emits `8*OP+2+WD` and a register ModR/M byte. For an immediate source, 4400 emits 80H for a byte or 81H for a word. The ModR/M byte has the operation number in its middle field and the destination register in its low field. The immediate follows in the destination's width. We deliberately omit the shorter sign-extended 83H form to keep size decisions fixed.

Both routines take their operands from `A$` through 5000. They change the operand-reader scratch variables, `RD`, `WD`, `R`, `W`, `N`, `X`, and `P`; they preserve `OP`. Memory arithmetic and signed literal syntax are omitted. To represent a negative bit pattern, use its unsigned hexadecimal value, such as 0FFFFH for a word containing all one bits. This fixture is only for inspection.''',
'ADD AX,BX\nSUB CX,1\nCMP AL,41H\nXOR DX,DX\nAND AL,0DFH\nOR BL,20H','03 C3 81 E9 01 00 80 F8 41 33 D2 80 E0 DF 80 CB 20','ADD AX,AL','Register sizes differ')
stage('Reading and writing memory','''4205 IF LEFT$(A1$,1)="[" THEN GOSUB 4700: RETURN
4221 IF LEFT$(A2$,1)="[" THEN GOSUB 4600: RETURN
4600 T$=A2$: GOSUB 4800
4610 X=138+WD: GOSUB 3000
4620 X=8*RD+RM: GOSUB 3000
4630 IF RM=6 THEN N=MA: GOSUB 3100
4640 RETURN
4700 T$=A2$: GOSUB 6000
4710 IF R<0 THEN E$="Register required": GOTO 9000
4720 RD=R: WD=W: T$=A1$: GOSUB 4800
4730 X=136+WD: GOSUB 3000
4740 X=8*RD+RM: GOSUB 3000
4750 IF RM=6 THEN N=MA: GOSUB 3100
4760 RETURN
4800 IF RIGHT$(T$,1)<>"]" THEN E$="Bad memory operand": GOTO 9000
4810 T$=MID$(T$,2,LEN(T$)-2)
4820 MA=0: RM=7
4830 IF T$="BX" THEN RETURN
4840 RM=6: GOSUB 2000: MA=N
4850 RETURN
''',
'Registers hold working values; a source buffer belongs in memory. We shall add just two ways to name a memory location.',
'''Square brackets mean the contents of memory. `MOV AL,[BX]` loads the byte at DS:BX; `MOV [BX],AL` stores it. `MOV AX,[ITEM]` loads a word at the named offset, and `MOV [ITEM],AX` stores a word there. A word accesses two consecutive bytes. Without brackets, ITEM means the address itself. The register operand determines whether to transfer a byte or a word.

Routine 4800 takes the bracketed text in `T$`. It checks the closing bracket and removes both brackets. `[BX]` returns `RM=7` with no displacement. Every other accepted operand is a numeric or named direct offset, returning `RM=6` and `MA` as its value. It changes the value reader's scratch variables; it preserves `RD` and `WD`.

The ModR/M mode bits are 00. In that mode, r/m=7 means [BX], while r/m=6 is the special direct-address form followed by a low-byte-first 16-bit offset. Routine 4600 uses the load opcode 8AH or 8BH. Routine 4700 first finds the source register, then uses store opcode 88H or 89H. Both place the register number in the middle field and emit the direct offset only when `RM=6`.

The CPU also supports combinations such as [BX+SI] and other segment choices. BOOTASM does not parse them. Fetch or store through BX and adjust BX explicitly, or use a direct label. Memory-to-memory MOV and immediate-to-memory MOV are also excluded. This keeps size and direction unambiguous without BYTE PTR or WORD PTR syntax.

The fixture uses the harmless direct offset 0200H for encoding checks. It is not intended to run.''',
'MOV AL,[BX]\nMOV [BX],AL\nMOV AX,[200H]\nMOV [200H],AX','8A 07 88 07 8B 06 00 02 89 06 00 02','MOV [BX],1','Register required')
stage('Calling and jumping','''4034 IF M$="JMP" OR M$="CALL" THEN GOSUB 5500: RETURN
5500 T$=A$: GOSUB 2000
5510 RV=N-(256+P+3)
5520 X=233: IF M$="CALL" THEN X=232
5530 GOSUB 3000: N=RV
5540 IF N<0 THEN N=N+65536
5550 GOSUB 3100: RETURN
''',
'A routine can now do useful work, but we need to reach it and return. Near CALL and JMP share the same address calculation.',
'''A near transfer stays in the current code segment. JMP replaces the instruction pointer; CALL first pushes the address of the following instruction. RET uses that saved word. Each ordinary call uses two stack bytes until its return, in addition to any words the routine pushes itself. There is no automatic check for stack collision or unmatched pushes.

The opcode is E9H for JMP and E8H for CALL. Both are followed by a 16-bit relative displacement. `P` is a file offset, so the current instruction's loaded address is `256+P`. The following instruction lies three bytes farther on. Routine 5500 subtracts that address from the destination to obtain `RV`, emits the opcode, and writes the displacement as a word. A negative displacement is represented by adding 65,536. The 16-bit instruction pointer wraps when that word is added.

The routine takes the destination from `A$`; it changes `T$`, the numeric-reader scratch variables, `RV`, `N`, `X`, and `P`. Every JMP is three bytes; there is no automatic short-JMP selection. Far transfers and indirect calls are omitted because all our code shares one segment.

In the test, CALL occupies offsets 0100H-0102H. SAY begins at 0108H, so the displacement is five. The routine displays C and returns to the termination code.''',
'CALL SAY\nMOV AX,4C00H\nINT 21H\nSAY:\nMOV DL,43H\nMOV AH,2\nINT 21H\nRET','E8 05 00 B8 00 4C CD 21 B2 43 B4 02 CD 21 C3','CALL LOST','Undefined label',run='C')
stage('Short conditional branches','''4036 I=INSTR("JB  JAE JE  JNE JBE JA  JL  JGE JLE JG  ",M$+" ")
4038 IF I>0 THEN IF (I-1) MOD 4=0 THEN BC=(I-1)/4: GOSUB 5600: RETURN
5600 T$=A$: GOSUB 2000
5610 RV=N-(256+P+2)
5620 IF PS=2 THEN IF RV<-128 OR RV>127 THEN E$="Branch out of range": GOTO 9000
5630 C$=MID$("234567CDEF",BC+1,1)
5640 X=112+INSTR("0123456789ABCDEF",C$)-1: GOSUB 3000
5650 X=RV-256*INT(RV/256): GOSUB 3000
5660 RETURN
''',
'A comparison becomes useful when it can select the next instruction. The 8088 gives these conditional transfers a signed one-byte reach, so the assembler must check the distance.',
'''The supported unsigned conditions are JB (below), JAE (above or equal), JE (equal), JNE (not equal), JBE (below or equal), and JA (above). For signed comparisons use JL, JGE, JLE, and JG. JE and JNE work for either interpretation. The processor stores bit patterns; the branch instruction chooses how the comparison flags are interpreted.

The opcode table selects 72H through 77H and 7CH through 7FH. These conditions test carry, zero, sign, and overflow as shown in the reference. CMP must be near enough in the execution path that intervening instructions have not changed the flags it set. MOV, PUSH, POP, CALL, RET, and the branches do not themselves alter arithmetic flags; a called routine may do so.

Routine 5600 subtracts `256+P+2`, the address after this two-byte instruction, from the destination. Pass one does not check the reach of an unresolved name. Pass two requires a result from -128 through +127 inclusive. Subtracting `256*INT(RV/256)` converts a negative displacement to its unsigned byte pattern without BASIC's signed logical operators. The routine changes `T$`, the value-reader scratch variables, `RV`, `C$`, `X`, and `P`; `BC` retains the selected condition.

There is no automatic long conditional branch on an 8088. To reach a distant destination, branch on the opposite condition to a nearby label, then use a near JMP. That sequence belongs in the source, where its size and meaning are visible.

The executable test starts DL at the character 0, displays it, advances to the next character, and repeats until DL reaches the character 3. DOS function 02H leaves DL available for this loop; AH is loaded each time.''',
'MOV DL,30H\nAGAIN:\nMOV AH,2\nINT 21H\nINC DX\nCMP DL,33H\nJB AGAIN\nMOV AX,4C00H\nINT 21H','B2 30 B4 02 CD 21 42 80 FA 33 72 F6 B8 00 4C CD 21','JE 400H','Branch out of range',run='012')

# Public source files are ASCII text with CRLF and period-compatible filenames.
dos(WORK/'BYTE.BAS',BYTE);dos(WORK/'VIEW.BAS',VIEW)
program={}; manifest=[]
for index,s in enumerate(stages,2):
    previous=program.copy()
    for n in s['remove']: program.pop(n,None)
    program.update(s['patch'])
    if len(s['patch'])>50: raise ValueError((s['title'],len(s['patch'])))
    code='\n'.join(f'{n} {body}' for n,body in sorted(program.items()))
    name=f'BA{index:02}.BAS';dos(WORK/name,code)
    fixture=f'T{index:02}'
    dos(WORK/(fixture+'.ASM'),s['fixture'])
    dos(WORK/(f'X{index:02}.ASM'),s['bad'])
    record={k:v for k,v in s.items() if k not in ('patch','remove')}
    record.update(number=index,source=name,fixture=fixture,patch_lines=len(s['patch']),total_lines=len(program),expected=s['expected'])
    manifest.append(record)
    # List exact changes, grouped only to distinguish replacements from additions.
    changes='\n'.join(f'{n} {body}' for n,body in sorted(s['patch'].items()))
    changed=[str(n) for n in s['patch'] if n in previous]
    if previous:
        inst=f'Load the preceding checkpoint, `BA{index-1:02}.BAS`. Keep its working copy. '
        if changed: inst+='Replace lines '+', '.join(sorted(changed,key=int))+'. '
        inst+='Insert the other numbered lines in their numeric positions; leave all unlisted lines in place.'
        # Exact old context is a compact locator table, avoiding repeated type-in code.
        anchors=[]
        for n in sorted(s['patch']):
            if n in previous: continue
            lower=[k for k in previous if k<n]; upper=[k for k in previous if k>n]
            pair=(max(lower) if lower else None,min(upper) if upper else None)
            if pair not in anchors: anchors.append(pair)
        if anchors:
            inst+=' New-line locations in the preceding listing: '+ '; '.join(f'{a or "start"} / {b or "end"}' for a,b in anchors)+'. Each pair gives the existing lines on either side.'
    else: inst='Start a new BASIC program with `NEW`. Type the complete numbered listing below.'
    example=s['fixture'].replace('\t','    ')
    context=''
    if previous:
        nearby=set()
        for n in s['patch']:
            if n in previous: nearby.add(n)
            lower=[k for k in previous if k<n]; upper=[k for k in previous if k>n]
            if lower: nearby.add(max(lower))
            if upper: nearby.add(min(upper))
        context='\nThe following lines are **context from the preceding checkpoint**, not another block to type. Compare them to locate the replacements and insertion gaps:\n\n```text\n'+'\n'.join(f'{n} {previous[n]}' for n in sorted(nearby))+'\n```\n'
    body=f'''+++
title = "{index:02}. {s['title']}"
weight = {index}
description = "{DESCRIPTIONS[s['title']]}"
checkpoint = "{name}"
+++

{s['why']}

## At the keyboard

{inst}

BASIC line numbers are part of the source. Enter a whole numbered line when replacing it.

```basic
{changes}
```

{context}
Save the result before running it:

```basic
SAVE "{name}",A
```

Keep this filename for the stopping point; it is not a second program to type.

## How it works

{s['explain']}

## A visible check

At DOS, create `{fixture}.ASM` with the following exact source. `COPY CON {fixture}.ASM` accepts text from the keyboard; finish with Ctrl-Z and Enter. Ctrl-Z is the end-of-input keystroke, not a character to include in a source line. A text editor which saves plain ASCII is also suitable.

```asm
{example}
```

From DOS start the checkpoint:

```dos
GWBASIC {name}
```

At its source-name prompt enter `{fixture}` without an extension. The success report must name `{fixture}.COM` and report **{len(bytes.fromhex(s['expected']))} bytes**. After the program ends at BASIC's `Ok` prompt, inspect the file:

```basic
RUN "VIEW.BAS"
```

At `File:` enter `{fixture}.COM`. The viewer must report length {len(bytes.fromhex(s['expected']))} and these bytes (spaces and line wrapping are immaterial):

```text
{s['expected']}
```

'''
    if s['run'] is not None:
        body+=f'''This fixture is a complete program. Return to DOS with `SYSTEM`, then run it through the shared status check:

```dos
CHECK {fixture}
```

'''
        if s['run']: body+=f'It must display `{s["run"]}`, followed on a new line by `PASS` from the batch file. '
        else: body+='It must display `PASS` from the batch file. '
        body+='`FAIL` means the program returned a nonzero status. The checker is printed in the workbench section.\n\n'
    else: body+='This is an encoding or data fixture. Inspect it with the viewer; **do not execute it**.\n\n'
    badline=len(s['bad'].splitlines())
    body+=f'''## An error worth catching

Create `X{index:02}.ASM` containing:

```asm
{s['bad']}
```

Reload `{name}` and run it with source name `X{index:02}`. Expect `ERROR line {badline} : {s['diagnostic']}`; BASIC may print extra spaces around the line number. There must be no `OK` report. On a fresh workbench there must be no `X{index:02}.COM`. If an older file exists, it is left unchanged and must not be mistaken for a new result.

## If the result differs

Check the changed line numbers first, then compare the test source with the listing above. A BASIC error names a BASIC line; `ERROR line` names a line in the assembly input. A missing source file produces a BASIC file error. Keep the preceding checkpoint until both the byte check and rejection check agree.
'''
    write_page((CONTENT/f'{index:02}-{re.sub("[^a-z0-9]+","-",s["title"].lower()).strip("-")}.md'),body)

dos(WORK/'BOOTASM.BAS','\n'.join(f'{n} {body}' for n,body in sorted(program.items())))
(ROOT/'qa/checkpoints.json').write_text(json.dumps(manifest,indent=2))
print('Prepared BOOTASM source checkpoints and construction articles.')
