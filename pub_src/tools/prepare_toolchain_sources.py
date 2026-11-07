"""Arrange authored RILL source and authored backend string tables, never translate a language."""
from pathlib import Path
import json
from build_ir86_wide import OPS,HEADER,RUNTIME
from rill_local_capacity import extend,fixtures
ROOT=Path(__file__).resolve().parents[1];W=ROOT/'workbench/toolchain'
def quote(s):return json.dumps(s,ensure_ascii=True).replace('\\u0000','\\0')
def dos(p,s):p.write_bytes(s.replace('\r\n','\n').replace('\n','\r\n').encode('ascii'))
s=(ROOT/'tools/ir86_port.ril').read_text()+'\nfn initops() {\n'
for n,(c,d,t) in OPS.items():s+=f'    op({quote(n)},{c},{d},{quote(t.replace(chr(10),chr(13)+chr(10)))});\n'
s+='    return 0;\n}\nfn header() { outstr('+quote(HEADER.replace('\n','\r\n'))+'); return 0; }\nfn runtime() {\n'
rt=RUNTIME.replace('\n','\r\n')
for i in range(0,len(rt),240):s+='    outstr('+quote(rt[i:i+240])+');\n'
s+='    return 0;\n}\n';dos(W/'IR86.RIL',s)
compiler=extend((ROOT/'tools/rill_self.ril').read_text())
dos(W/'RILL.RIL',compiler)
dos(W/'RC44.RIL',compiler)
for name,source in fixtures().items():dos(W/name,source)
print('Prepared authored RILL translator and backend data tables')

# Opcode metadata is authored data from the published assembler's table.
text=(ROOT/'workbench/asm86a/ASM86A.ASM').read_text()
rows=text.split('OPTAB:\n',1)[1].split('\n\n',1)[0].splitlines()
s=(ROOT/'tools/asm86a_port.ril').read_text()+'\nfn initops() {\n'
for row in rows:
 b=bytes(int(x) for x in row.removeprefix('DB ').split(','));n=b[:6].split(b'\0')[0].decode()
 s+=f'    opentry({quote(n)},{b[6]},{b[7]});\n'
s+='    return 0;\n}\n';dos(W/'ASM86A.RIL',s)
