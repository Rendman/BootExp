"""Compile RILL only with its published IR implementation; execute every target."""
from common import *
import json,re
assembly,image=build_ir((W/'RILL.IR').read_bytes())
(W/'RILL.ASM').write_bytes(assembly);(W/'RILL.COM').write_bytes(image)
results=[]
def record(name):results.append('PASS '+name)
def good(source,output=b'',status=0,stdin=b'',portable_compiler=False):
 r=run_compiler(source,image,{'RESULT.IR':b'OLD RESULT'})
 assert r.exitcode==0,(source,r.output)
 ir=r.files['RESULT.IR'];assert r.output==f'OK RESULT.IR {len(ir):05}\r\n'.encode()
 if portable_compiler:
  for base,handle in [(0x4000,101),(0x8000,301)]:
   p=Machine({'SOURCE.RIL':source.encode(),'RESULT.IR':b'OLD RESULT'},data_base=base,handle_base=handle).run((W/'RILL.IR').read_bytes(),limit=10_000_000)
   assert (p.exitcode,p.output,p.files)==(r.exitcode,r.output,r.files),(source,'compiler differs across processors')
 targetasm,targetcode=build_ir(ir,'RESULT')
 native=DosMachine(stdin=stdin).run(targetcode);portable=Machine(stdin=stdin).run(ir,limit=10_000_000)
 assert (native.exitcode,native.output)==(status,output),(source,native.exitcode,native.output,status,output)
 assert (portable.exitcode,portable.output)==(native.exitcode,native.output),(source,'target semantics differ')
 return ir

def bad(source,code,files=None):
 f={'RESULT.IR':b'OLD RESULT'};f.update(files or {})
 r=run_compiler(source,image,f)
 assert r.exitcode==1,(source,r.output)
 assert re.fullmatch(rb'ERROR \d{5} CODE '+f'{code:05}'.encode()+rb'\r\n',r.output),(source,r.output,code)
 assert r.files['RESULT.IR']==b'OLD RESULT',(source,'source error overwrote result')

assert len(image)<=8192 and len(assembly)<=32768
record(f'published IR86 -> ASM86 directly builds RILL.COM ({len(image)} bytes)')
for source,out in [('fn main() {}',b''),('fn main(){putc(72);putc(73);}',b'HI'),(' // a comment\nfn\tmain( ) { // line\n putc(65);\n} // end',b'A')]:
 good(source,out,portable_compiler=True);record('header, whitespace, comments, and portable compiler agreement')
for value in [0,1,9,10,255,256,32767,32768,65535]:
 good(f'fn main(){{exit({value});}}',status=value&255);record(f'decimal word {value}')
for expr,val in [('7-3+2',6),('65535+1',0),('0-1',65535),('-(1+2)',65533),('1-(2-3)',2),('--7',7),('5 + -2',3),('9-3-2',4)]:
 good(f'fn main(){{exit({expr});}}',status=val&255);record('arithmetic '+expr)
source='fn main(){ let mut x=48; while x<51 {putc(x); x=x+1;} }'
good(source,b'012',portable_compiler=True);record('mutable storage and loop')
for op in ['==','!=','<','<=','>','>=']:
 for a,b in [(0,1),(1,0),(1,1),(65535,1),(32768,32767)]:
  yes={'==':a==b,'!=':a!=b,'<':a<b,'<=':a<=b,'>':a>b,'>=':a>=b}[op]
  good(f'fn main(){{if {a}{op}{b} {{putc(89);}} else {{putc(78);}}}}',b'Y' if yes else b'N')
  record(f'unsigned condition {a}{op}{b}')
for n in [0,1,65535]:
 good(f'fn main(){{if {n}{{putc(89);}}else{{putc(78);}}}}',b'Y' if n else b'N');record(f'value condition {n}')
good('fn main(){if 0 {putc(78);} putc(65);}',b'A');record('if without else')
good('fn main(){let mut x=0; while x<3 { if x==1 {putc(49);} else {if x==2 {putc(50);} else {putc(48);}} x=x+1;}}',b'012',portable_compiler=True);record('nested control-flow labels and saved contexts')
good('fn main(){if 1 {exit(7);} putc(88);}',status=7);record('exit terminates inside a block')
for stream in [b'',b'Q',bytes(range(256)),b'A\r\n\0\xff']:
 src='fn main(){let mut c=0; let mut s=0; c=getc(); s=status(); while s==0 {if c==65535 {exit(0);} putc(c); s=status(); if s!=0 {exit(1);} c=getc(); s=status();} exit(1);}'
 good(src,stream,stdin=stream);record('byte input, EOF, and persistent service status '+str(len(stream)))
# Exact spelling is checked in both encoded halves of a reserved word.
for word in ['mainz','maim','mai','mainaa']:
 bad('fn '+word+'(){}',2);record('reject header '+word)
for word in ['putcat','putfoo','put','putccc','getcat','getfoo','statux','statusx']:
 source='fn main(){'+(f'putc({word}());' if word.startswith(('get','sta')) else word+'(65);')+'}'
 r=run_compiler(source,image,{'RESULT.IR':b'OLD RESULT'})
 assert r.exitcode==1 and r.files['RESULT.IR']==b'OLD RESULT',(word,r.output)
 record('reject keyword lookalike '+word)
for source,code in [('',2),('main(){}',2),('fn main(){',4),('fn main(){} junk',2),('fn main(){let x=0;}',2),('fn main(){let mut x=0;let mut x=1;}',4),('fn main(){x=1;}',4),('fn main(){putc(x);}',4),('fn main(){putc();}',4),('fn main(){putc(1*2);}',2),('fn main(){let mut x=1+2;}',2),('fn main(){putc(65536);}',3),('fn main(){putc(9999999999);}',3),('fn main(){putc(0x41);}',2),('fn main(){putc(1==1);}',2),('fn main(){if (1==1){}}',2),('fn main(){if 1 {let mut x=0;}}',4),('fn main(){/}',2),('fn main(){let mut xx=0;}',4),('fn other(){}',2),('fn main(){return;}',4)]:
 bad(source,code);record('reject unsupported or malformed source '+repr(source[:45]))
for byte in [0,1,8,11,27,127,128,255]:
 bad(b'fn main(){'+bytes([byte])+b'}',2);record('reject source byte '+str(byte))
good('fn main(){}\x1aignored bytes');record('Control-Z text termination')
good('fn main(){exit('+'('*6+'1'+')'*6+');}',status=1);record('exact combined parser depth')
bad('fn main(){exit('+'('*7+'1'+')'*7+');}',5);record('parser depth overflow')
good('fn main(){'+'if 1{'*7+'}'*8);record('nested block boundary')
bad('fn main(){'+'if 1{'*8+'}'*9,5);record('nested block overflow')
good('fn main(){'+'putc(65);'*59+'}',b'A'*59);record('1021-byte result within output bound')
bad('fn main(){'+'putc(65);'*60+'}',5);record('output capacity preserves old result')
prefix='fn main(){} //'
good(prefix+'x'*(4096-len(prefix)));record('exact 4096-byte source')
bad(prefix+'x'*(4097-len(prefix)),5);record('source capacity preserves old result')
good('fn main(){'+''.join(f'let mut {chr(97+i)}={i};' for i in range(26))+'exit(z);}',status=25);record('all twenty-six variables')
bad(None,1);record('missing input preserves old result')
# Binding failures are injected only in the validation environment.
class Broken(DosMachine):
 def __init__(self,operation):super().__init__({'SOURCE.RIL':b'fn main(){}','RESULT.IR':b'OLD RESULT'});self.operation=operation
 def interrupt(self,c,intno,_):
  from unicorn.x86_const import UC_X86_REG_AH,UC_X86_REG_AX
  if intno==0x21 and c.reg_read(UC_X86_REG_AH)==self.operation:
   c.reg_write(UC_X86_REG_AX,123);self.carry(True);return
  return super().interrupt(c,intno,_)
for operation in [0x3d,0x3f,0x3e,0x3c,0x40]:
 r=Broken(operation).run(image)
 assert r.exitcode in [1,4],(operation,r.output)
 if operation!=0x40:assert r.files['RESULT.IR']==b'OLD RESULT',(operation,'changed old result')
 record(f'normalized binding failure {operation:02X}')
(Q/'test-results.txt').write_text('\n'.join(results)+'\n')
(Q/'build-facts.json').write_text(json.dumps({'binary_bytes':len(image),'assembly_bytes':len(assembly),'checks':len(results)},indent=2)+'\n')
print(f'PASS {len(results)} RILL bootstrap, language, portability, resource, rejection, and binding checks')
