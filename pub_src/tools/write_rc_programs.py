"""Print the complete programs verified with the RILL-written compiler."""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
def fence(k,s):return '```'+k+'\n'+s.rstrip('\n')+'\n```\n\n'
t='''+++
title = "Complete RC programs"
weight = 48
description = "Recursion, checked allocated storage, and counted files through the RILL-written compiler."
download = "RC.ZIP"
download_group = "rc"
+++

Use R0.COM, the completed RC compiler built by RILLBOOT. Keep IWKEEP and ASMAKEEP as the translator and assembler. These programs use the same language accepted by the RB seed; their IR and executable bytes must agree through both compilers.

'''
for c in json.loads((ROOT/'qa/compiler_collections/rc-examples.json').read_text()):
 name=c['name'];t+='## '+c['title']+'\n\n'+c['why']+'\n\nSave '+name+'.RIL:\n\n'+fence('rill',c['source'])
 t+=fence('dos',f'COPY {name}.RIL SOURCE.RIL\nCHECK R0\nCOPY RESULT.IR SOURCE.IR\nCHECK IWKEEP\nCOPY RESULT.ASM SOURCE.ASM\nCHECK ASMAKEEP')
 t+=f'Require compiler `OK RESULT.IR {c["ir_bytes"]:010}`, translator `OK RESULT.ASM {c["assembly_bytes"]:010} text bytes`, and assembler `OK RESULT.COM {c["binary_bytes"]:05} bytes`, each with PASS **before** the following copy. VIEW.BAS must report length {c["binary_bytes"]} and these first thirty-two bytes:\n\n'+fence('text',c['hex'])
 t+=fence('dos',f'COPY RESULT.COM {name}.COM')
 if c.get('files'):t+='Create IN.TXT with `ECHO A short copy.>IN.TXT`. '
 t+='CHECK '+name+' '+('displays '+json.dumps(c['output'])+' and ' if c['output'] else '')+'reports PASS. '
 if c.get('result_file'):t+='COMP IN.TXT OUT.TXT must report no differences; answer N to the compare-more-files question. An empty input and every possible byte value must also copy unchanged. '
 t+='\n\nFor a separate rejection, save BAD.RIL:\n\n'+fence('rill',c['bad'])+fence('dos','COPY BAD.RIL SOURCE.RIL\nCHECK R0')+f'Require `{c["error"]}` and FAIL. The accepted RESULT.IR must remain unchanged. An unexpected PASS fails the check. Restore the accepted source before building again.\n\n'
(ROOT/'site/content/bootstrap/rc/048-programs.md').write_text(t)

# Both compiler implementations accept one shared language contract.
reference=(ROOT/'site/content/bootstrap/rb/132-the-rill-systems-language.md').read_text().split('## Program structure',1)[1]
header='+++\ntitle = "The RC language reference"\nweight = 44\ndescription = "The complete language used by the compiler, IR86, and ASM86A implementations."\ndownload = "RILL.RIL"\ndownload_group = "rc"\n+++\n\nRC constructs RILL.RIL, a compiler written in the same language it accepts. RILLBOOT builds its first executable; R0 and the next two compiler generations reproduce it. The language contract is the same as the completed RB compiler seed. ASM86A.RIL and IR86.RIL use this same language.\n\n## Program structure'
(ROOT/'site/content/bootstrap/rc/044-reference.md').write_text(header+reference)
