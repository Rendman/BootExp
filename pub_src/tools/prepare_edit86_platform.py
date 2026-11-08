"""Arrange published editor compiler/IR extensions and authored target services."""
from pathlib import Path
import json,re
ROOT=Path(__file__).resolve().parents[1];W=ROOT/'workbench/edit86';T=ROOT/'workbench/toolchain'
def dos(name,s):(W/name).write_bytes(s.replace('\r\n','\n').replace('\n','\r\n').encode('ascii'))
s=(T/'RILL.RIL').read_text();a=s.index('fn builtin() {');b=s.index('fn resolveoptional()',a);old=s[a:b]
first=old[:old.index('\n    let mut i = 0;')]
loop=old[old.index('    let mut i = 0;'):]
table='VBEGIN\\00\\0VBEGIN\\0VEND\\00\\0VEND\\0VPOS\\01\\0POP\\nVPOS\\0VWRITE\\02\\0POP\\nVWRITE\\0KEY\\00\\0KEY\\0BLOCKMOVE\\05\\0POP\\nBMOVE\\0BLOCKLOAD\\04\\0POP\\nBLOAD\\0BLOCKREAD\\04\\0POP\\nBREAD\\0\\0'
replacement=first+'\n    let mut hit = findbuiltin(p); if hit { return hit; }\n    return findbuiltin("'+table+'");\n}\nfn findbuiltin(p) {\n'+loop
s=s[:a]+replacement+s[b:];dos('RILLED.RIL',s)
s=(T/'IR86.RIL').read_text()
s=s.replace('    if delta == 4 { if depth { fail(4); } }', '    if delta == 4 { if depth { fail(4); } }\n    if delta == 5 { if depth < 4 { fail(4); } depth = depth-4; }\n    if delta == 6 { if depth < 3 { fail(4); } depth = depth-3; }')
a=s.index('fn initops() {');s=s[:a]+s[a:].replace('    return 0;\n}', '''    op("VBEGIN",0,0,"CALL R_VBEGIN\\r\\n");
    op("VEND",0,0,"CALL R_VEND\\r\\n");
    op("VPOS",0,0,"CALL R_VPOS\\r\\n");
    op("VWRITE",0,2,"POP DX\\r\\nCALL R_VWRITE\\r\\n");
    op("KEY",0,0,"CALL R_KEY\\r\\n");
    op("BMOVE",0,5,"POP DI\\r\\nPOP DX\\r\\nPOP CX\\r\\nPOP BX\\r\\nCALL R_BMOVE\\r\\n");
    op("BLOAD",0,6,"POP DX\\r\\nPOP CX\\r\\nPOP BX\\r\\nCALL R_BLOAD\\r\\n");
    op("BREAD",0,6,"POP DX\\r\\nPOP CX\\r\\nPOP BX\\r\\nCALL R_BREAD\\r\\n");
    return 0;
}''',1)
s=s.rstrip();assert s.endswith('return 0;\n}')
s=s[:-len('return 0;\n}')]+'''editorruntime(); return 0;
}
fn editorruntime() {
    let mut file=open("EDITRT.ASM"); if status() { fail(6); }
    while 1 {
        let mut count=read(file,inbuf,4096); if status() { close(file); fail(6); }
        if count==0 { close(file); if status() { fail(6); } return 0; }
        let mut i=0; while i<count { outchar(inbuf[i]); i=i+1; }
    }
    return 0;
}
''';dos('IRED.RIL',s)
dos('EDITRT.ASM',(ROOT/'tools/edit86_runtime.asm').read_text())
print('Prepared RILL/IR console extensions and the authored 8086/DOS service binding')
