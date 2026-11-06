"""Independent byte expectations and complete programs for the RILL-written tools."""
from common import *
import ast,json,re
logs=[];image=(W/'ASM86A.COM').read_bytes()
def good(source,expected=None):
 r=run(image,source,'ASM',{'RESULT.COM':b'OLD'});assert r.exitcode==0,(source[:100],r.output)
 b=r.files['RESULT.COM']
 if expected is not None:assert b==(bytes.fromhex(expected) if isinstance(expected,str) else expected),(source[:100],b[:50],expected)
 assert not r.allocations and 'ASMA.TMP' not in r.files and 'RESULT.BAK' not in r.files
 return b
def bad(source,category):
 r=run(image,source,'ASM',{'RESULT.COM':b'OLD'});assert r.exitcode==1,(source,r.output)
 assert re.search(rb'CODE 0*'+str(category).encode()+rb'\r\n',r.output),(source,r.output,category)
 assert r.files['RESULT.COM']==b'OLD' and not r.allocations,(source,r.files.keys())
# Authored expected bytes are reused; no host assembler supplies an oracle.
tree=ast.parse((ROOT/'qa/asm86a/test_asm86a.py').read_text())
cases=next(ast.literal_eval(n.value) for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='cases' for t in n.targets))
for source,expect in cases:good(source,expect);logs.append('PASS encoding '+source.splitlines()[0])
rejections=next(ast.literal_eval(n.iter) for n in tree.body if isinstance(n,ast.For) and isinstance(n.target,ast.Tuple) and [getattr(v,'id',None) for v in n.target.elts]==['text','code'])
for source,code in rejections:bad(source+'\n',code);logs.append('PASS rejection '+source.splitlines()[0])
for group,name in [('asm86','ASM86'),('asm86a','ASMA0'),('asm86a','ASM86A'),('ir86','IR86'),('rill','RILL')]:
 p=ROOT/'workbench'/group;good((p/(name+'.ASM')).read_bytes(),(p/(name+'.COM')).read_bytes());logs.append('PASS exact native-source compatibility '+name)
for name in ['HELLO','FRAME','BRIDGE','COPYTEXT']:
 b=good((ROOT/'workbench/asm86a'/(name+'.ASM')).read_bytes(),(ROOT/'workbench/asm86a'/(name+'.COM')).read_bytes());r=run(b)
 expected=next(c['output'].encode() for c in json.loads((ROOT/'qa/asm86a/examples.json').read_text()) if c['name']==name)
 assert r.exitcode==0 and r.output==expected;logs.append('PASS complete native program '+name)
for n in [0,4095,4096,4097,8193,61184]:good(f'RESB {n}\n',bytes(n));logs.append('PASS streamed output '+str(n))
bad('RESB 61185\n',5);bad('RESW 32768\n',5);bad('RESB 61184\nDB 1\n',5)
for count in [8192,8193]:
 source=''.join(f'S{i}:\n' for i in range(count))+f'DW S0,S{count-1}\n'
 if count==8192:good(source,'00010001')
 else:bad(source,5)
 logs.append('PASS symbol boundary '+str(count))
good(';\n'*65536+'DB 1\n','01');logs.append('PASS source beyond 65535 physical lines')
(Q/'assembler-results.txt').write_text('\n'.join(logs)+'\n');print('PASS',len(logs),'assembler encoding, compatibility, execution and capacity checks')
