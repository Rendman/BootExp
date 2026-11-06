from common import *
source=(ROOT/'tools/rill_bootstrap.ir').read_bytes()
(ROOT/'workbench/rill/RILLBOOT.IR').write_bytes(source.replace(b'\r\n',b'\n').replace(b'\n',b'\r\n'))
a,b=ir(source);(W/'RILLBOOT.ASM').write_bytes(a);(W/'RILLBOOT.COM').write_bytes(b);print('Compiler seed',len(a),len(b))
r=run(b,'fn main() { putc(72); putc(73); return 0; }','RIL')
print(r.exitcode,bytes(r.output),r.files.get('RESULT.IR',b'')[:400])
assert r.exitcode==0
_,p=ir(r.files['RESULT.IR']);c=run(p);assert c.exitcode==0 and c.output==b'HI',(c.exitcode,c.output)
print('PASS compiler seed -> IR86 -> ASM86A -> HI')
