"""Render native-measured seed examples using only the seed's accepted syntax."""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1];W=ROOT/'workbench/asma0';C=ROOT/'site/content/bootstrap/asma0'
def fence(k,s):return '```'+k+'\n'+s.rstrip('\n')+'\n```\n\n'
t='''+++
title = "14 · Complete seed programs"
weight = 14
description = "A terminated greeting, a byte copied through memory, and a short loop."
download = "ASMA0.ZIP"
+++

These programs use the completed ASMA0 seed. Its fixed input is SOURCE.ASM and its output is RESULT.COM. Preserve each accepted output under the program's own filename before another assembly. Run an output only after a fresh OK and PASS and a VIEW.BAS inspection.

'''
notes={'HELLO':'DOS function 9 prints the bytes ending at the dollar marker. DB supplies numeric ASCII values because the seed has no quoted-string syntax. Carriage return and line feed are explicit.', 'MEMORY':'BX holds the source byte address. A byte register supplies the width for the [BX] load and direct [COPY] store. The second direct load demonstrates that COPY received M. Both objects belong to the program segment selected by DS.', 'COUNT':'DL starts at ASCII zero and advances after each output. CMP leaves the unsigned flags tested by JB. AGAIN is close enough for the seed\'s short conditional encoding.'}
for r in json.loads((ROOT/'qa/asma0/examples.json').read_text()):
 name=r['name'];t+='## '+name+'\n\nSave '+name+'.ASM:\n\n'+fence('asm',(W/(name+'.ASM')).read_text())+notes[name]+'\n\n'
 t+=fence('dos',f'COPY {name}.ASM SOURCE.ASM\nCHECK ASMA0')+f'Require `OK RESULT.COM {r["binary_bytes"]:05} bytes` and PASS. VIEW.BAS must report length {r["binary_bytes"]} and '+('these complete bytes' if r['binary_bytes']<=32 else 'these first thirty-two bytes')+':\n\n'+fence('text',r['hex'])
 t+=fence('dos',f'COPY RESULT.COM {name}.COM\nCHECK {name}')+'It displays '+json.dumps(r['output'])+' and the checker reports PASS. Here `\\r\\n` denotes carriage return and line feed.\n\n'
 t+='For a separate rejection, copy the source to BAD.ASM and replace the first `'+r['bad_before']+'` with `'+r['bad_after']+'`. Copy BAD.ASM to SOURCE.ASM and run CHECK ASMA0. Require '+f'`ERROR {r["bad_line"]:05} CODE {r["bad_code"]}` and FAIL. The accepted RESULT.COM must remain unchanged. An unexpected PASS fails this test. Restore the accepted source before building again.\n\n'
t+='The completed seed source and its matching self-builds are the handoff to the separate ASM86A collection. Keep ASMA0.COM and ASMA0.ASM with their tested examples.\n'
(C/'14-programs.md').write_text(t)
