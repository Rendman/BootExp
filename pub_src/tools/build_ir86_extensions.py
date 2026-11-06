"""Arrange gradual native IR86 checkpoints from authored assembly routines."""
from pathlib import Path
import json
from build_ir86_wide import source,OPS,PARTS,near
ROOT=Path(__file__).resolve().parents[1];W=ROOT/'workbench/toolchain';Q=ROOT/'qa/toolchain'
ENTRY='START:\nCLD\nCMP SP,0FFFEH\nJNE NEAR MEMORYBAD\n'
EXIT='MOV AX,4C00H\nINT 21H\nMEMORYBAD:\nMOV AX,7\nJMP ERROR\n'
read=ENTRY+'CALL OPENFILE\nREADNEXT:\nCALL READLINE\nCMP AX,0\nJE READDONE\nMOV SI,0C800H\n'
readend='JMP READNEXT\nREADDONE:\nCALL CLOSEFILE\n'+EXIT
show=read+'SHOWBYTE:\nLODSB\nCMP AL,0\nJE SHOWEND\nMOV DL,AL\nMOV AH,2\nINT 21H\nJMP SHOWBYTE\nSHOWEND:\nMOV DX,NEWLINE\nCALL TEXT\n'+readend
tokens=read+'SHOWTOKEN:\nCALL SCAN\nMOV AX,[TOKLEN]\nCMP AX,0\nJE READNEXT\nPUSH SI\nMOV SI,0CC00H\nMOV DL,91\nMOV AH,2\nINT 21H\nTOKENBYTE:\nLODSB\nCMP AL,0\nJE TOKENEND\nMOV DL,AL\nMOV AH,2\nINT 21H\nJMP TOKENBYTE\nTOKENEND:\nMOV DL,93\nMOV AH,2\nINT 21H\nPOP SI\nJMP SHOWTOKEN\n'+readend
copy=ENTRY+'CALL PREFLIGHT\nCALL OPENFILE\nCALL CREATEOUT\nCOPYBYTE:\nCALL NEXTBYTE\nCMP AX,0\nJE COPYDONE\nMOV AL,[CHAR]\nCALL EMITCHAR\nJMP COPYBYTE\nCOPYDONE:\nCALL CLOSEFILE\nCALL FLUSH\nCALL CLOSEOUT\nCALL COMMIT\nMOV DX,OKMSG\nCALL TEXT\nMOV AX,[TOTALLO]\nMOV DX,[TOTALHI]\nCALL NUMBER32\nMOV DX,BYTEMSG\nCALL TEXT\n'+EXIT
lookup=read+'CALL SCAN\nMOV BX,IRTAB\nMOV CX,2\nMOV AX,16\nCALL LOOK\nCMP BX,0\nJE SYNTAXBAD\nADD BX,10\nMOV AL,[BX]\nMOV AH,0\nPUSH AX\nCALL FINISH\nPOP AX\nMOV DX,0\nCALL NUMBER32\nMOV DX,NEWLINE\nCALL TEXT\n'+readend
specs=[
('A bounded input reader','Read a fixed source through the inherited line reader and checked source counters.','ABC\n','',show),
('Tokens without a complete source buffer','Fold token spellings while preserving the raw line for quoted data.','lit 7\n','',tokens),
('Publishing streamed assembly text','Copy a byte stream through a checked output block and recoverable publication.','ABC\r\n','',copy),
('An operation record','Look up the complete mnemonic and inspect its argument-class field.','LIT\n','LIT HALT',lookup),
('The first text translator','Expand names and literal operands into a complete native assembly file.','LABEL MAIN\nLIT 0\nHALT\n','LABEL LIT HALT NOP EXIT',None),
('Declared storage','Give named byte and word storage fixed sizes and materialize larger buffers with RESB.','WORD X 0\nBYTE Y 65\nBUFFER B 300\nLABEL MAIN\nHALT\n','WORD BYTE BUFFER',None),
('Addresses and indirect storage','Keep byte addresses and canonical word loads independent of physical registers.','WORD X 65\nLABEL MAIN\nADDR X\nFETCHB\nEXIT\n','LD ST LDB STB ADDR FETCH FETCHB',None),
('Saved expression operands','Check push/pop depth and apply word arithmetic before a control boundary.','LABEL MAIN\nLIT 7\nPUSH\nLIT 7\nSUB\nEXIT\n','PUSH POP ADD SUB AND OR XOR PUT PUTB',None),
('Conditions without extra skip definitions','Use fixed native conditional bridges while keeping branch semantics in the virtual machine.','LABEL MAIN\nLIT 7\nPUSH\nLIT 7\nEQ GOOD\nLIT 1\nEXIT\nLABEL GOOD\nHALT\n','JMP JZ JNZ EQ NE ULT ULE UGT UGE SLT SLE SGT SGE',None),
('Calls and returns','Keep a return address separate from a procedure result in A.','LABEL MAIN\nCALL VALUE\nPUSH\nLIT 65\nEQ GOOD\nLIT 1\nEXIT\nLABEL GOOD\nHALT\nLABEL VALUE\nLIT 65\nRET\n','CALL RET',None),
('Counted console output','Bind PUTC and persistent STATUS to checked byte output.','LABEL MAIN\nLIT 65\nPUTC\nHALT\n','PUTC STATUS',None),
('Input bytes and EOF','Distinguish every byte from EOF without exposing a native status flag.','LABEL MAIN\nGETC\nPUTC\nHALT\n','GETC',None),
('Opening an opaque file','Give OPEN an ordinary terminated filename and return a checked handle.','WORD NAME 65\nLABEL MAIN\nADDR NAME\nOPEN\nSTATUS\nJZ GOOD\nLIT 1\nEXIT\nLABEL GOOD\nHALT\n','OPEN',None),
('Creating a counted file','Create writable handles through the same opaque slot table.','WORD NAME 65\nLABEL MAIN\nADDR NAME\nCREATE\nSTATUS\nJZ GOOD\nLIT 1\nEXIT\nLABEL GOOD\nHALT\n','CREATE',None),
('Reading into a buffer','Consume a saved handle and pointer, return actual progress, and refill after short reads.','WORD NAME 65\nWORD H 0\nBUFFER B 1\nLABEL MAIN\nADDR NAME\nOPEN\nST H\nLD H\nPUSH\nADDR B\nPUSH\nLIT 1\nREAD\nPUSH\nLIT 1\nEQ GOOD\nLIT 1\nEXIT\nLABEL GOOD\nHALT\n','READ',None),
('Writing a bounded block','Check both service status and actual write progress.','WORD NAME 65\nWORD H 0\nBYTE B 65\nLABEL MAIN\nADDR NAME\nCREATE\nST H\nLD H\nPUSH\nADDR B\nPUSH\nLIT 1\nWRITE\nPUSH\nLIT 1\nEQ GOOD\nLIT 1\nEXIT\nLABEL GOOD\nHALT\n','WRITE',None),
('Closing a handle','Retire an owned handle only after a successful close.','WORD NAME 65\nLABEL MAIN\nADDR NAME\nOPEN\nCLOSE\nSTATUS\nEXIT\n','CLOSE',None),
('Procedure frames and arguments','Name parameter and local slots in IR; leave native frame offsets to the backend.','PROC MAIN 0 0\nLIT 7\nPUSH\nLIT 9\nPUSH\nINVOKE TWICE 1\nADD\nPUSH\nLIT 25\nCEQ\nPUSH\nLIT 1\nSUB\nRETURN\nPROC TWICE 1 1\nPARAM 0\nPUSH\nLIT 2\nMUL\nSETLOCAL 0\nLOCAL 0\nRETURN\n','PROC RETURN INVOKE LOCAL SETLOCAL LADDR PARAM SETPARAM PADDR MUL CEQ',None),
('Word arithmetic and comparison values','Define multiply, unsigned quotient/remainder, masked shifts, and zero-or-one relations.','PROC MAIN 0 0\nLIT 65535\nPUSH\nLIT 255\nDIV\nPUSH\nLIT 257\nCNE\nRETURN\n','NEG NOT DIV MOD SHL SHR CEQ CNE CULT CULE CUGT CUGE CSLT CSLE CSGT CSGE',None),
('Quoted literal data','Preserve case and escape bytes while branching around inline constant storage.','PROC MAIN 0 0\nLITS "Hi"\nFETCHB\nPUTC\nLIT 0\nRETURN\n','LITS',None),
('File publication services','Normalize existence, deletion, and rename without exposing DOS error values.','PROC MAIN 0 0\nLITS "A"\nEXISTS\nPUSH\nLIT 1\nCNE\nRETURN\n','EXISTS DELETE RENAME',None),
('Allocated block handles','Allocate byte extents beyond the main image and release owned blocks.','WORD H 0\nPROC MAIN 0 0\nLIT 40960\nALLOC\nST H\nSTATUS\nJNZ BAD\nLD H\nFREEBLOCK\nSTATUS\nRETURN\nLABEL BAD\nLIT 1\nRETURN\n','ALLOC FREEBLOCK',None),
('Checked block access','Validate an opaque block and byte extent before reading or writing a word.','WORD H 0\nPROC MAIN 0 0\nLIT 40960\nALLOC\nST H\nLD H\nPUSH\nLIT 40958\nPUSH\nLIT 4660\nSET16\nLD H\nPUSH\nLIT 40958\nGET16\nPUSH\nLIT 4660\nCNE\nPUSH\nLD H\nFREEBLOCK\nPOP\nRETURN\n','GET8 GET16 SET8 SET16',None)]
def runtime(level):
 selected=[]
 for n in ['RESULT','PUTC','GETC','OPEN','CREATE','FILE','FIND','READ','WRITE','CLOSE','STATUS','BYTE','FILEDATA','TRANSFERDATA']:
  at={'RESULT':11,'PUTC':11,'GETC':12,'OPEN':13,'CREATE':14,'FILE':13,'FIND':15,'READ':15,'WRITE':16,'CLOSE':17,'STATUS':11,'BYTE':11,'FILEDATA':13,'TRANSFERDATA':15}[n]
  if level>=at:selected.append(PARTS[n])
 ext=(ROOT/'tools/ir86_wide_runtime.asm').read_text()
 if level>=21:selected.append(ext[:ext.index('R_ALLOC:')])
 if level>=22:
  if level==22:selected.append(ext[ext.index('R_ALLOC:'):ext.index('R_BLOCKPTR:')]+ext[ext.index('R_FREEBLOCK:'):ext.index('R_STACKFAIL:')])
  else:selected.append(ext[ext.index('R_ALLOC:'):ext.index('R_STACKFAIL:')])
 selected.append('R_STACKFAIL:\nMOV AX,4C02H\nINT 21H\n')
 if level>=22:selected.append('R_WANT:\nDW 0\nR_MEMVALUE:\nDW 0\nR_BLOCKS:\nRESW 32\n')
 return near('\n'.join(selected))
def build():
 active={};cases=[]
 for n,(title,why,fixture,adds,driver) in enumerate(specs,1):
  for name in adds.split():active[name]=OPS[name]
  if n==23:text=source()
  else:text=source(active,runtime(n),driver,frames=n>=18,strings=n>=20)
  filename=f'IW{n:02}.ASM';(W/filename).write_bytes(text.replace('\n','\r\n').encode('ascii'))
  (W/f'TIW{n:02}.IR').write_bytes(fixture.replace('\r\n','\n').replace('\n','\r\n').encode())
  cases.append(dict(number=n,title=title,why=why,source=filename,fixture=fixture,diagnostic=n<=4,raw=n==3))
 (Q/'ir-extensions.json').write_text(json.dumps(cases,indent=2)+'\n');print('Prepared 23 native IR86 extension checkpoints')
if __name__=='__main__':build()
