"""Reader acceptance checks for the completed RILL compiler's storage."""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1];W=ROOT/'workbench/toolchain';Q=ROOT/'qa/toolchain'
def fence(kind,s):return '```'+kind+'\n'+s.replace('\r\n','\n').rstrip('\n')+'\n```\n\n'
def render():
 facts=json.loads((Q/'local-capacity.json').read_text())
 t=''
 t+='## Local and parameter capacity\n\nThe completed compiler now combines the record, scope, and frame routines. Create TLOCAL.RIL:\n\n'+fence('rill',(W/'TLOCAL.RIL').read_text())
 def acceptance(name):
  f=facts[name]
  return fence('dos',f'COPY {name} SOURCE.RIL\nCHECK RC43\nCOPY RESULT.IR SOURCE.IR\nCHECK IWKEEP\nCOPY RESULT.ASM SOURCE.ASM\nCHECK ASMAKEEP\nCOPY RESULT.COM TRY.COM\nCHECK TRY')+f'Require compiler `OK RESULT.IR {f["ir_bytes"]:010}`, translator `OK RESULT.ASM {f["assembly_bytes"]:010} text bytes`, and assembler `OK RESULT.COM {f["binary_bytes"]:05} bytes`, with PASS before each following copy. TRY must return zero and report PASS; it needs no display routine. VIEW.BAS must show {f["binary_bytes"]} bytes and these first thirty-two bytes:\n\n'+fence('text',f['hex'])
 t+=acceptance('TLOCAL.RIL')
 t+='## Reject one more live local\n\nCopy TLOCAL.RIL to XLOCAL.RIL. Just before `return (a0!=0)|(a15!=15);`, insert:\n\n'+fence('rill','let mut extra=0;')+fence('dos','COPY XLOCAL.RIL SOURCE.RIL\nCHECK RC43')+f'Require `{facts["error"]}` and FAIL. The accepted RESULT.IR must remain unchanged; keep a copy for comparison before this check.\n\n'
 t+='## Reusing local slots\n\nCreate TSCOPE.RIL using the following skeleton. At each comment, copy the eight declaration lines for v0 through v63 from TLOCAL.RIL; the comments are placement markers. There are two sibling scopes, each filling all sixty-four slots.\n\n'+fence('rill','''let mut result=0;
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
 return t
