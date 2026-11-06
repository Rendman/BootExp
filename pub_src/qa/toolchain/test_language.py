from common import *
from portable import Machine
import re
compiler=(W/'RILL.COM').read_bytes();translator=(W/'IR86.COM').read_bytes();assembler=(W/'ASM86A.COM').read_bytes();logs=[]
def compile_program(s):
 r=run(compiler,s,'RIL',{'RESULT.IR':b'OLD'});assert r.exitcode==0,(s[:120],r.output)
 text=r.files['RESULT.IR'];r=run(translator,text);assert r.exitcode==0,(s,r.output)
 r=run(assembler,r.files['RESULT.ASM'],'ASM');assert r.exitcode==0,(s,r.output)
 return text,r.files['RESULT.COM']
programs=[
 ('fn main(){return 0;}',b'',0),
 ('fn main(){return 7+3*4;}',b'',19),
 ('fn main(){return (7+3)*4;}',b'',40),
 ('fn main(){return -1/255;}',b'',1),
 ('fn main(){return 65535%256;}',b'',255),
 ('fn main(){return (1<<4)|(255&3);}',b'',19),
 ('fn main(){return 65535>>15;}',b'',1),
 ('fn main(){return ~65535;}',b'',0),
 ('fn main(){return !0+!1;}',b'',1),
 ('fn main(){return 7+twice(9); } fn twice(n){return n*2;}',b'',25),
 ('fn main(){return f(7,2);} fn f(a,b){a=a+b;return a-b;}',b'',7),
 ('fn main(){return fact(5);} fn fact(n){if n==0{return 1;} return n*fact(n-1);}',b'',120),
 ('fn main(){let mut x=7; {let mut x=9;putc(x+48);}putc(x+48);return 0;}',b'97',0),
 ('bytes msg[4]; fn main(){msg[0]=72;msg[1]=73;putc(msg[0]);putc(msg[1]);return 0;}',b'HI',0),
 ('fn main(){let mut x=7;store16(&x,9);return x;}',b'',9),
 ('fn main(){let mut h=alloc(40960);set16(h,40958,4660);let mut x=get16(h,40958);free(h);return x;}',b'',52),
 ('fn main(){let mut h=alloc(3);set16(h,2,7);let mut s=status();free(h);return s;}',b'',1),
 ('fn main(){let mut s="Hello; text";let mut i=0;while load8(s+i){putc(load8(s+i));i=i+1;}return 0;}',b'Hello; text',0),
 ('fn main(){return 1/0;}',b'',2)]
for source,out,status in programs:
 text,image=compile_program(source);native=run(image);assert (native.output,native.exitcode)==(out,status),(source,native.output,native.exitcode)
 for base in [0x2000,0x4000]:
  portable=Machine(data_base=base,handle_base=131,block_base=701).run(text)
  assert (portable.output,portable.exitcode)==(out,status),(source,'portable',portable.output,portable.exitcode)
 logs.append('PASS native/portable '+source[:65])
for op in ['==','!=','<','<=','>','>=']:
 for a,b in [(1,1),(0,1),(65535,1)]:
  text,image=compile_program(f'fn main(){{return {a}{op}{b};}}');n=run(image);p=Machine().run(text)
  expect={'==':a==b,'!=':a!=b,'<':a<b,'<=':a<=b,'>':a>b,'>=':a>=b}[op]
  assert n.exitcode==p.exitcode==int(expect),(op,a,b,n.exitcode,p.exitcode)
  logs.append(f'PASS value relation {a}{op}{b}')
for source in ['fn main(){return missing(1);}','fn main(){return f(1);}fn f(a,b){return a;}','fn main(){let mut x=x;return x;}','fn main(){let mut x=0;let mut x=1;}','fn main(){return 65536;}','fn main(){return 1+;}','fn main(){return get8(1);}','fn main(a){return a;}']:
 r=run(compiler,source,'RIL',{'RESULT.IR':b'OLD'});assert r.exitcode==1 and r.files['RESULT.IR']==b'OLD',(source,r.output);logs.append('PASS rejection '+source)
# The same compiler implementation executes as IR at unrelated data and handle addresses.
source=(W/'RILL.RIL').read_bytes();boot=(W/'RILL0.IR').read_bytes();r=run(compiler,source,'RIL')
for base in [0x2000,0x4000]:
 p=Machine({'SOURCE.RIL':source},data_base=base,handle_base=131,block_base=701).run(boot,limit=100_000_000)
 assert p.exitcode==0 and p.files['RESULT.IR']==r.files['RESULT.IR'],('portable compiler',base,p.output)
 logs.append(f'PASS RILL-written compiler compiles itself in portable model at {base:04X}')
(Q/'language-results.txt').write_text('\n'.join(logs)+'\n');print('PASS',len(logs),'RILL and IR language/portability checks')
