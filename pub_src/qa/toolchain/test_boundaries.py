from common import *
from portable import Machine,InvalidIR
import re
compiler=(W/'RILL.COM').read_bytes();translator=(W/'IR86.COM').read_bytes();native_ir=(ROOT/'workbench/ir86/IRWIDE.COM').read_bytes();logs=[]
def accepted(source):
 r=run(compiler,source,'RIL',{'RESULT.IR':b'OLD'});assert r.exitcode==0,(source[:100],r.output)
 assert b'\n' not in r.files['RESULT.IR'].replace(b'\r\n',b''),'non-DOS IR output'
 return r.files['RESULT.IR']
def rejected(source,category):
 r=run(compiler,source,'RIL',{'RESULT.IR':b'OLD'});assert r.exitcode==1 and r.files['RESULT.IR']==b'OLD' and re.search(rb'CODE 0*'+str(category).encode()+rb'\r\n',r.output),(source[:100],r.output)
 return r
for source in ['fn main(){return "\\z";}','fn main(){return "open\nclose";}','fn main(){return "open\rclose";}']:rejected(source,2);logs.append('PASS reject invalid string escape or raw newline')
for trans in [native_ir,translator]:
 for source in ['PROC MAIN 0 0\nLIT 1\nPUSH\nLIT 2\nPUSH\nLIT 3\nEQ X\nLABEL X\nLIT 0\nRETURN\n','PROC MAIN 0 0\nLIT 65536\nRETURN\n']:
  r=run(trans,source,files={'RESULT.ASM':b'OLD'});assert r.exitcode==1 and r.files['RESULT.ASM']==b'OLD',r.output
 logs.append('PASS native/RILL translator rejects leftover branch operands and word overflow')
source=''.join(f'let mut g{i}=0;\n' for i in range(511))+'fn main(){return 0;}';accepted(source);rejected(source.replace('fn main','let mut extra=0;\nfn main'),5);logs.append('PASS exact 512 global/procedure records and overflow')
source='fn main(){'+''.join(f'let mut v{i}={i};' for i in range(64))+'return v63;}';accepted(source);rejected(source.replace('return v63;','let mut extra=0;return v63;'),5);logs.append('PASS exact sixty-four active locals and overflow')
args=','.join('a'+str(i) for i in range(16));vals=','.join(str(i) for i in range(16));accepted(f'fn f({args}){{return a15;}}fn main(){{return f({vals});}}');rejected(f'fn f({args},extra){{return 0;}}fn main(){{return 0;}}',5);logs.append('PASS sixteen parameters and overflow')
accepted('fn main(){let mut abcdefghijklmnopqrstuvwx=7;return abcdefghijklmnopqrstuvwx;}');rejected('fn main(){let mut abcdefghijklmnopqrstuvwxy=7;return 0;}',4);logs.append('PASS complete 24-character names and rejection of character 25')
accepted('// comment\n'*65536+'fn main(){return 0;}');r=rejected('// comment\n'*65536+'bad',2);assert b'ERROR 0000065537' in r.output,r.output;logs.append('PASS streamed source beyond 65535 lines and full decimal error line')
(Q/'boundary-results.txt').write_text('\n'.join(logs)+'\n');print('PASS',len(logs),'compiler and IR boundary checks')
