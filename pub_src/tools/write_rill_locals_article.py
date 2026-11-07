"""Print the four edits after RC43's first self-build, with measured checks."""
from pathlib import Path
from difflib import SequenceMatcher
import json
from compiler_publication import publish
ROOT=Path(__file__).resolve().parents[1];W=ROOT/'workbench/toolchain';Q=ROOT/'qa/toolchain'
facts=json.loads((Q/'local-capacity.json').read_text())
def fence(kind,s):return '```'+kind+'\n'+s.replace('\r\n','\n').rstrip('\n')+'\n```\n\n'
t='''+++
title = "More Local Storage"
weight = 46
description = "Give each function sixty-four local slots while keeping sixteen parameters."
download = "RC44.RIL"
download_group = "rc"
+++

Begin after the first compiler self-build comparisons. Keep the matching RC43 compiler copies and RC43.RIL separately. R0 is still the tested sixteen-local compiler from that exercise. Copy RC43.RIL to RC44.RIL and make the four edits below, from the bottom upward. Everything else stays in place.

The final compiler accepts sixty-four simultaneously live local words and sixteen parameters per function. IR86 already accepts that frame. RILL0, RILLBOOT, and RC43 retain their sixteen-local bounds.

## The record and frame bounds

A name record occupies forty bytes. The 512 global/procedure records occupy bytes 0 through 20479. Eighty parameter/local records occupy bytes 20480 through 23679: sixteen parameter names plus sixty-four live local names. Allocate 23680 bytes and check that allocation before using the table. Record initialization and lexical restoration keep their earlier jobs.

PROC now reserves sixty-four local words for every compiled function, even a function using fewer. That is 128 bytes of local storage per active call, plus its parameters, return state and expression temporaries. The native stack guard still applies; this change does not promise a fixed recursion depth. Parameters retain their separate sixteen-word bound.

## Enter the source

'''
old=(W/'RC43.RIL').read_text().splitlines();new=(W/'RC44.RIL').read_text().splitlines();changes=[]
ops=[op for op in SequenceMatcher(None,old,new,autojunk=False).get_opcodes() if op[0]!='equal']
assert len(ops)==4
for i,(_,a,b,c,d) in enumerate(reversed(ops),1):
 context=old[max(0,a-3):a];after=old[b:b+2]
 t+=f'### Edit {i}\n\nUnchanged source immediately before the edit:\n\n'+fence('rill','\n'.join(context))
 t+=f'Remove this source at old physical positions {a+1}–{b} in RC43.RIL:\n\n'+fence('rill','\n'.join(old[a:b]))
 t+='Replace it with:\n\n'+fence('rill','\n'.join(new[c:d]))
 t+='The following old source remains in place:\n\n'+fence('rill','\n'.join(after))
 changes.append(dict(a1=a,a2=b,old=old[a:b],new=new[c:d],context=context,after=after))
t+='## Build with the tested compiler\n\n'+fence('dos','COPY RC44.RIL SOURCE.RIL\nCHECK R0\nCOPY RESULT.IR SOURCE.IR\nCHECK IWKEEP\nCOPY RESULT.ASM SOURCE.ASM\nCHECK ASMAKEEP\nCOPY RESULT.COM RC44.COM')
t+=f'Require compiler `OK RESULT.IR {facts["boot_ir_bytes"]:010}`, translator `OK RESULT.ASM {facts["boot_assembly_bytes"]:010} text bytes`, assembler `OK RESULT.COM {facts["boot_binary_bytes"]:05} bytes`, and each PASS before the following copy. VIEW.BAS must show RC44.COM length {facts["boot_binary_bytes"]}.\n\n'
t+='The preceding compiler built RC44.COM with sixteen-slot frames for its own functions. RC44 nevertheless emits sixty-four-slot frames. Let it compile its own source before establishing the new comparison baseline:\n\n'+fence('dos','COPY RC44.RIL SOURCE.RIL\nCHECK RC44\nCOPY RESULT.IR SOURCE.IR\nCHECK IWKEEP\nCOPY RESULT.ASM SOURCE.ASM\nCHECK ASMAKEEP\nCOPY RESULT.COM R0.COM\nCOPY RC44.RIL RILL.RIL')
t+=f'Require compiler `OK RESULT.IR {facts["ir_bytes"]:010}`, translator `OK RESULT.ASM {facts["assembly_bytes"]:010} text bytes`, assembler `OK RESULT.COM {facts["binary_bytes"]:05} bytes`, and each PASS before copying. R0 is now the final compiler, with sixty-four-slot frames both in its own implementation and in its generated programs. Its length is {facts["binary_bytes"]} bytes.\n\n'
t+='Compile RILL.RIL with this R0 through IWKEEP and ASMAKEEP, saving the accepted executable as R1.COM. Repeat with R1, saving R2.COM. Require each fresh OK and PASS. Then compare:\n\n'+fence('dos','ECHO N>NO.TXT\nCOMP R0.COM R1.COM <NO.TXT\nCOMP R0.COM R2.COM <NO.TXT')+'Both comparisons must report no differences. These are the compiler copies carried into the toolchain collection.\n\n'
t+='## Fill the local and parameter regions\n\nCreate TLOCAL.RIL:\n\n'+fence('rill',(W/'TLOCAL.RIL').read_text())
def acceptance(name):
 f=facts[name]
 return fence('dos',f'COPY {name} SOURCE.RIL\nCHECK R0\nCOPY RESULT.IR SOURCE.IR\nCHECK IWKEEP\nCOPY RESULT.ASM SOURCE.ASM\nCHECK ASMAKEEP\nCOPY RESULT.COM TRY.COM\nCHECK TRY')+f'Require compiler `OK RESULT.IR {f["ir_bytes"]:010}`, translator `OK RESULT.ASM {f["assembly_bytes"]:010} text bytes`, and assembler `OK RESULT.COM {f["binary_bytes"]:05} bytes`, with PASS before each following copy. TRY must return zero and report PASS; it needs no display routine. VIEW.BAS must show {f["binary_bytes"]} bytes and these first thirty-two bytes:\n\n'+fence('text',f['hex'])
t+=acceptance('TLOCAL.RIL')
t+='## Reject one more live local\n\nCopy TLOCAL.RIL to XLOCAL.RIL. Just before `return (a0!=0)|(a15!=15);`, insert:\n\n'+fence('rill','let mut extra=0;')+fence('dos','COPY XLOCAL.RIL SOURCE.RIL\nCHECK R0')+f'Require `{facts["error"]}` and FAIL. The accepted RESULT.IR must remain unchanged; keep a copy for comparison before this check.\n\n'
t+='## Reuse slots at a closing brace\n\nCreate TSCOPE.RIL using the following skeleton. At each comment, copy the eight declaration lines for v0 through v63 from TLOCAL.RIL; the comments are placement markers. There are two sibling scopes, each filling all sixty-four slots.\n\n'+fence('rill','''let mut result=0;
fn reuse(){
{
// Copy the eight declaration lines here.
v63=17;result=result+v63;
}
{
// Copy the same eight declaration lines here.
v63=29;result=result+v63;
}
return 0;
}
fn main(){
let mut v63=7;
{let mut v63=9;if v63!=9{return 1;}}
reuse();
return (result!=46)|(v63!=7);
}''')
t+='The complete disk source has the declarations in place. It checks both slot reuse between sibling scopes and restoration of an outer binding after a shadowing block.\n\n'+acceptance('TSCOPE.RIL')
t+='Keep the sixteen-parameter limit. A procedure with seventeen parameters is still rejected with capacity code five. The following toolchain construction uses this completed RILL.RIL and the matching R0/R1/R2 copies.\n'
page='134-more-local-storage.md'
publish('rc',page,t,aliases=[])
p=Q/'article-patches.json';patches=json.loads(p.read_text());patches=[s for s in patches if s['family']!='rill-local-extension']
patches.append(dict(family='rill-local-extension',number=44,collection='rc',page=page,base='RC43.RIL',kind='rill',changes=changes,source='RC44.RIL'))
p.write_text(json.dumps(patches,indent=2)+'\n')
print('Rendered the post-self-build local-storage extension')
