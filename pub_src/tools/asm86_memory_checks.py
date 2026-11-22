"""Reader diagnostics made as labelled edits to copies of A13, A14 and A15.

The construction checkpoints are deliberately unchanged. These are authored
assembly test drivers; this module only arranges source, never machine bytes.
"""
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
WORK = ROOT / 'workbench/asm86'
QA = ROOT / 'qa/asm86'


def message(label, text):
    return label + ':\nDB ' + ','.join(str(b) for b in (text + '\r\n$').encode('ascii')) + '\n'


EQUAL = '''PROBEEQUAL:
CMP AX,DX
JE PROBEEQUALOK
JMP PROBEFAIL
PROBEEQUALOK:
RET
PROBEFAIL:
MOV AX,CS
MOV ES,AX
CALL MEMFREE
MOV DX,PROBEFAILMSG
CALL TEXT
MOV AX,4C01H
INT 21H
'''

MEMORY = '''PROBEBASE:
MOV BX,0FFFFH
MOV AH,48H
INT 21H
JB PROBEBASEOK
JMP PROBEFAIL
PROBEBASEOK:
MOV [PROBEFREE],BX
RET

PROBEDIRTY:
PUSH AX
PUSH BX
PUSH CX
MOV AX,0A5A5H
MOV CX,4096
PROBEDIRTYLOOP:
MOV ES:[BX],AX
ADD BX,2
DEC CX
JNE PROBEDIRTYLOOP
POP CX
POP BX
POP AX
RET

PROBEMEM:
MOV AX,[MEMCOUNT]
MOV DX,9
CALL PROBEEQUAL
MOV AX,ES
MOV DX,CS
CALL PROBEEQUAL
MOV AX,[HASHSEG]
MOV ES,AX
MOV BX,0
MOV CX,4096
PROBEZERO:
MOV AX,ES:[BX]
MOV DX,0
CALL PROBEEQUAL
ADD BX,2
DEC CX
JNE PROBEZERO
MOV SI,MEMSEGS
MOV BP,8
MOV DI,1
PROBEPAGES:
MOV BX,SI
MOV AX,[BX]
MOV ES,AX
MOV BX,0
MOV AX,DI
MOV ES:[BX],AX
MOV BX,40958
ADD AX,100H
MOV ES:[BX],AX
ADD SI,2
INC DI
DEC BP
JNE PROBEPAGES
MOV SI,MEMSEGS
MOV BP,8
MOV DI,1
PROBEPAGECHECK:
MOV BX,SI
MOV AX,[BX]
MOV ES,AX
MOV BX,0
MOV AX,ES:[BX]
MOV DX,DI
CALL PROBEEQUAL
MOV BX,40958
MOV AX,ES:[BX]
ADD DX,100H
CALL PROBEEQUAL
ADD SI,2
INC DI
DEC BP
JNE PROBEPAGECHECK
MOV AX,[HASHSEG]
MOV ES,AX
MOV BX,0
MOV AX,ES:[BX]
MOV DX,0
CALL PROBEEQUAL
MOV AX,CS
MOV ES,AX
MOV DX,PROBEALLOK
CALL TEXT
RET

PROBEFREED:
MOV AX,[MEMCOUNT]
MOV DX,[PROBELIMIT]
CMP DX,0
JNE PROBEFREECOUNT
MOV DX,9
PROBEFREECOUNT:
CALL PROBEEQUAL
MOV AL,[CLEANFAIL]
MOV AH,0
MOV DX,0
CALL PROBEEQUAL
MOV AX,ES
MOV DX,CS
CALL PROBEEQUAL
MOV SI,MEMSEGS
MOV CX,9
PROBEDESC:
MOV BX,SI
MOV AX,[BX]
MOV DX,0
CALL PROBEEQUAL
ADD SI,2
DEC CX
JNE PROBEDESC
MOV BX,0FFFFH
MOV AH,48H
INT 21H
JB PROBEFREEQUERY
JMP PROBEFAIL
PROBEFREEQUERY:
MOV AX,BX
MOV DX,[PROBEFREE]
CALL PROBEEQUAL
MOV DX,PROBEFREEOK
CALL TEXT
RET

PROBEFREE:
DW 0
PROBELIMIT:
DW 0
'''+message('PROBEALLOK', 'MEMORY CLEAR AND PAGES PASS')+message('PROBEFREEOK', 'MEMORY RELEASE PASS')

PAGES = '''EARLYTEST:
MOV DI,PROBECASES
MOV BP,8
PROBECASE:
MOV BX,DI
MOV AX,[BX]
PUSH AX
ADD BX,2
MOV DX,[BX]
ADD BX,2
MOV AX,[BX]
MOV [PROBEOFF],AX
MOV BX,MEMSEGS
ADD BX,DX
MOV AX,[BX]
MOV [PROBESEG],AX
POP AX
CALL SYMPTR
MOV AX,BX
MOV DX,[PROBEOFF]
CALL PROBEEQUAL
MOV AX,ES
MOV DX,[PROBESEG]
CALL PROBEEQUAL
MOV AX,[RECORDPTR]
MOV DX,[PROBEOFF]
CALL PROBEEQUAL
ADD DI,6
DEC BP
JNE PROBECASE
MOV AX,CS
MOV ES,AX
MOV DX,PROBEPAGEOK
CALL TEXT
RET

PROBECASES:
DW 1,0,0
DW 2,0,40
DW 1023,0,40880
DW 1024,0,40920
DW 1025,2,0
DW 1026,2,40
DW 8191,14,40880
DW 8192,14,40920
PROBEOFF:
DW 0
PROBESEG:
DW 0
'''+message('PROBEPAGEOK', 'PAGE BOUNDARIES PASS')

RECORDS = '''EARLYTEST:
CALL PROBERECPAGE
MOV BX,39
MOV AL,5AH
MOV ES:[BX],AL
MOV BX,80
MOV AL,6BH
MOV ES:[BX],AL
MOV BX,40
MOV CX,40
MOV AL,0A5H
PROBERECDIRTY:
MOV ES:[BX],AL
INC BX
DEC CX
JNE PROBERECDIRTY
MOV AX,[HASHSEG]
MOV ES,AX
MOV BX,8188
MOV AX,55AAH
MOV ES:[BX],AX
MOV BX,8190
MOV AX,8192
MOV ES:[BX],AX
MOV AX,CS
MOV ES,AX
MOV SI,PROBELONG
MOV DI,4080H
CALL COPYZ
MOV AX,1026
MOV [SYMID],AX
MOV AX,1234H
MOV [DEFVALUE],AX
MOV AX,8192
MOV [HEADID],AX
MOV AX,1
MOV [DEFTYPE],AX
MOV AX,8190
MOV [BUCKET],AX
MOV AX,[SYMID]
CALL RECORDWRITE
MOV SI,PROBEEXPECT1
CALL PROBERECORD
CALL PROBERECPAGE
MOV BX,76
MOV AX,0FFFFH
MOV ES:[BX],AX
MOV AX,CS
MOV ES,AX
MOV SI,PROBESHORT
MOV DI,4080H
CALL COPYZ
MOV AX,0BEEFH
MOV [DEFVALUE],AX
MOV AX,1025
MOV [HEADID],AX
MOV AX,0
MOV [DEFTYPE],AX
MOV AX,[SYMID]
CALL RECORDWRITE
MOV SI,PROBEEXPECT2
CALL PROBERECORD
MOV AX,CS
MOV ES,AX
MOV DX,PROBERECOK
CALL TEXT
RET

PROBERECPAGE:
MOV BX,MEMSEGS
ADD BX,2
MOV AX,[BX]
MOV ES,AX
RET

PROBERECORD:
CALL PROBERECPAGE
MOV BX,40
MOV CX,40
PROBERECBYTE:
LODSB
MOV AH,0
MOV DL,ES:[BX]
MOV DH,0
CALL PROBEEQUAL
INC BX
DEC CX
JNE PROBERECBYTE
MOV BX,39
MOV AL,ES:[BX]
MOV AH,0
MOV DX,5AH
CALL PROBEEQUAL
MOV BX,80
MOV AL,ES:[BX]
MOV AH,0
MOV DX,6BH
CALL PROBEEQUAL
MOV AX,[HASHSEG]
MOV ES,AX
MOV BX,8190
MOV AX,ES:[BX]
MOV DX,1026
CALL PROBEEQUAL
MOV BX,8188
MOV AX,ES:[BX]
MOV DX,55AAH
CALL PROBEEQUAL
MOV BX,0
MOV AX,ES:[BX]
MOV DX,0
CALL PROBEEQUAL
RET

PROBELONG:
DB 65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80
DB 81,82,83,84,85,86,87,88,89,90,65,66,67,68,69,0
PROBESHORT:
DB 81,0
PROBEEXPECT1:
DB 65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80
DB 81,82,83,84,85,86,87,88,89,90,65,66,67,68,69,0
DW 1234H,8192,0,1
PROBEEXPECT2:
DB 81,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
DB 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
DW 0BEEFH,1025,0,0
'''+message('PROBERECOK', 'RECORD FIELDS AND GUARDS PASS')


def replace_once(source, old, new):
    assert source.count(old) == 1, old
    return source.replace(old, new, 1)


def diagnostic(number, source):
    """Keep the reader's routines, changing only the documented diagnostic hooks."""
    source = source.replace('\r\n', '\n').split('\x1a')[0].rstrip() + '\n'
    if number == 13:
        source = replace_once(source, 'CALL MEMINIT\n', 'CALL MEMINIT\nCALL PROBEMEM\n')
        source = replace_once(source, 'CALL COMMIT\nCALL MEMFREE\n',
                              'CALL COMMIT\nCALL MEMFREE\nCALL PROBEFREED\n')
        source = replace_once(source, 'MEMSHRUNK:\n', 'MEMSHRUNK:\nCALL PROBEBASE\n')
        source = replace_once(source, 'MOV CX,4096\nMOV AX,0\nMEMCLEAR:',
                              'CALL PROBEDIRTY\nMOV CX,4096\nMOV AX,0\nMEMCLEAR:')
        source = replace_once(source, 'ALLOCBLOCK:\n', '''ALLOCBLOCK:
MOV AX,[PROBELIMIT]
CMP AX,0
JE PROBEALLOCATE
MOV DX,[MEMCOUNT]
CMP AX,DX
JNE PROBEALLOCATE
MOV BX,0FFFFH
PROBEALLOCATE:
''')
        source = replace_once(source, 'ERROR:\nMOV [ERRCODE],AL\nCALL CLEANUP\n', '''ERROR:
MOV [ERRCODE],AL
CALL CLEANUP
MOV AX,[PROBELIMIT]
CMP AX,0
JNE PROBEEXPECTED
JMP PROBEFAIL
PROBEEXPECTED:
MOV AL,[ERRCODE]
MOV AH,0
MOV DX,7
CALL PROBEEQUAL
CALL PROBEFREED
''')
        extra = MEMORY
        source = replace_once(source, 'CMDINIT:\n', extra + EQUAL + message('PROBEFAILMSG', 'MEMORY TEST FAILED') + '\nCMDINIT:\n')
    else:
        start, end = source.index('EARLYTEST:\n'), source.index('CMDINIT:\n')
        extra = PAGES if number == 14 else RECORDS
        source = source[:start] + extra + EQUAL + message('PROBEFAILMSG', 'MEMORY TEST FAILED') + '\n' + source[end:]
    return source


def prepare():
    for number in (13, 14, 15):
        text = diagnostic(number, (WORK / f'A{number}.ASM').read_text())
        (WORK / f'M{number}.ASM').write_bytes(text.replace('\n', '\r\n').encode('ascii'))


def article(number):
    """Print the same numbered-label edits checked by the execution tests."""
    from assembly_edits import patch
    facts = json.loads((QA / 'memory-checks.json').read_text())[str(number)]
    source = (WORK / f'A{number}.ASM').read_text()
    target = diagnostic(number, source)
    edits, _ = patch(source.splitlines(), target.splitlines())
    edits = edits.replace('### Change ', '### Diagnostic edit ')
    text = '## Check the new memory routines\n\n'
    text += ('The small T input below checks that ordinary assembly still works. '
             'For a direct check of the added routines, make a separate diagnostic copy. '
             'Keep the accepted construction source and executable for the next article.\n\n')
    text += f'Copy `A{number}.ASM` to `M{number}.ASM`. '
    text += f'The [complete diagnostic source](../../../downloads/tools/asm86/M{number}.ASM) is also available. '
    text += 'Apply the edits to your own typed source to check your routines; the download is a reference copy. '
    text += 'These edits use labels and existing source as locators; no physical line numbers are needed.\n\n'
    if number == 13:
        text += ('The diagnostic fills all 8192 bucket bytes with A5H just before MEMCLEAR, '
                 'then verifies every word became zero. It writes different markers at both '
                 'ends of each symbol page, reads them back after all eight pages have been '
                 'written, and checks the hash block was not aliased. Before allocation it '
                 'asks DOS for the largest free block; after MEMFREE it requires the same '
                 'answer, zero saved segment descriptors, and no cleanup failure. '
                 'DOS function 48H with BX=FFFFH must fail and return the largest available '
                 'paragraph count in BX; the request cannot fit in conventional memory.\n\n')
    elif number == 14:
        text += ('The case table gives each ID an independently expected page-word offset '
                 'and record offset. It checks ES, BX and RECORDPTR directly; it never uses '
                 'SYMPTR to calculate its expected answer or to read back a write.\n\n'
                 '| ID | Symbol page | Record offset |\n|---|---|---|\n'
                 '| 1 | 0 | 0 |\n| 2 | 0 | 40 |\n| 1023 | 0 | 40880 |\n'
                 '| 1024 | 0 | 40920 |\n| 1025 | 1 | 0 |\n| 1026 | 1 | 40 |\n'
                 '| 8191 | 7 | 40880 |\n| 8192 | 7 | 40920 |\n\n')
    else:
        text += ('The test fills record 1026 with A5H and places guard bytes before and '
                 'after it. It writes a 31-character spelling, value 1234H, link 8192 and '
                 'kind 1 into bucket offset 8190. It independently selects page 1, offset '
                 '40 and compares all forty bytes against a literal expected record. '
                 'It then overwrites the spelling with Q, changes the fields and dirties '
                 'the pass flags; every name-padding and flag byte must become zero. '
                 'Both runs verify the guards, the bucket head, its neighbor and bucket zero. '
                 'The long spelling exercises the record writer directly; it does not extend '
                 'the seed parser\'s accepted identifier length.\n\n')
    text += edits
    text += f'### Build and run M{number}\n\n```dos\nCHECK ASM1 M{number}.ASM M{number}.COM\nCHECK M{number} T{number}.ASM RESULT.COM\n```\n\n'
    text += f'Require `OK M{number}.COM {facts["binary_bytes"]:05} bytes` and PASS from the build. The diagnostic run must show:\n\n```text\n'
    text += facts['output'].replace('\r\n', '\n') + 'PASS\n```\n\n'
    text += 'MEMORY TEST FAILED, an unexpected error, or a missing diagnostic message fails this check.\n\n'
    if number == 13:
        text += '''### Stop partway through allocation

In M13.ASM find this exact declaration:

```asm
PROBELIMIT:
DW 0
```

Change only its word to `DW 2` and save the copy as F13.ASM. The third allocation now requests FFFFH paragraphs, so DOS must reject it after two successful page allocations. The ordinary ERROR and CLEANUP path must free both pages before the diagnostic compares the largest free block with its saved value.

```dos
CHECK ASM1 F13.ASM F13.COM
CHECK F13 T13.ASM RESULT.COM
```

The build must succeed with the same size as M13.COM. The run must display:

```text
MEMORY RELEASE PASS
ERROR 00000 CODE 7
FAIL
```

FAIL is the intended process status for this forced allocation error. Require MEMORY RELEASE PASS as well: CODE 7 alone does not demonstrate cleanup. An existing RESULT.COM must remain unchanged. Repeat with limits 1 through 8 to exercise every partially completed allocation count. Do not carry any of these diagnostic edits into A14.ASM.

'''
    text += f'Continue the construction from your accepted A{number}.ASM, not M{number}.ASM.\n\n'
    return text


if __name__ == '__main__':
    prepare()
