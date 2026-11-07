"""Package the single IR construction and both continuing compiler milestones."""
from pathlib import Path
import json,zipfile,shutil
from publication_names import ROOT
Q=ROOT/'qa/toolchain'
for group,family,prefix,work,complete,archive in [('ir86','ir-extensions','IR','ir86','IR86.ASM','IR86.ZIP'),('rill','rill-initial-series','R','rill','RILL.IR','RILL.ZIP'),('rb','rill-seed-series','RB','toolchain','RILLBOOT.IR','RB.ZIP')]:
 W=ROOT/'workbench'/work;D=ROOT/'site/static/downloads'/group;D.mkdir(exist_ok=True,parents=True)
 cases=json.loads((Q/(family+'.json')).read_text());files=[complete,'VIEW.BAS','CHECK.BAT','README.TXT']
 if group!='ir86':
  shutil.copyfile(ROOT/'workbench/ir86/IR86.ASM',W/'IRWIDE.ASM');files.append('IRWIDE.ASM')
 if group=='rb':shutil.copyfile(ROOT/'workbench/rill/RILL.IR',W/'RILL.IR');files.append('RILL.IR')
 for helper in ['VIEW.BAS','CHECK.BAT']:shutil.copyfile(ROOT/'workbench/bootasm'/helper,W/helper)
 lines=['BOOTSTRAP EXPERIMENT - '+('RILL0' if group=='rill' else 'RILLBOOT' if group=='rb' else 'IR86'),'',
 'Read the matching workbench and construction articles in order.',
 'Use your own DOS 3.10 and period BASIC interpreter.',
 'VIEW.BAS inspects lengths and bytes. CHECK.BAT checks program status.',
 'Require each fresh OK and PASS before copying a result to the next tool.',
 'Sources are ASCII with DOS line endings and 8.3 filenames.',
 'No executable, interpreter, or outside compiler is included.','']
 if group=='ir86':lines+=['ASM86 builds all native checkpoints. SOURCE.ASM -> RESULT.COM.',f'IR01.ASM through IR{len(cases):02}.ASM form one continuing translator.',f'IR86.ASM is identical to IR{len(cases):02}.ASM.', 'The translator uses SOURCE.IR -> RESULT.ASM.', 'Preserve IRKEEP.COM and an identical IWKEEP.COM for later workbenches.']
 elif group=='rill':lines+=[f'R01.IR through R{len(cases):02}.IR construct the small compiler.',f'RILL.IR is identical to R{len(cases):02}.IR.', 'Translate SOURCE.IR with IRKEEP; assemble SOURCE.ASM with ASMAKEEP.', 'The compiler uses SOURCE.RIL -> RESULT.IR. Preserve RLKEEP.COM.', 'Continue this same compiler source in the RILLBOOT collection.']
 else:lines+=['Begin by copying the completed small RILL.IR to RB01.IR.',f'RB01.IR through RB{len(cases):02}.IR extend that working compiler.',f'RILLBOOT.IR is identical to RB{len(cases):02}.IR.', 'Use IRKEEP and ASMAKEEP. Preserve RILLBOOT.COM for the RILL compiler.', 'Every continuation accepts the preceding language subset.']
 lines+=['','Early helper output can be an incomplete fragment; inspect its bytes.', 'Execute only programs identified as complete in their article.', 'Source rejection preserves accepted output. A failed publication may', 'leave temporary or backup files; inspect those before a new run.','']
 (W/'README.TXT').write_bytes('\r\n'.join(lines).encode('ascii'))
 for c in cases:
  n=c['number'];name=f'{prefix}{n:02}';src=name+'.ASM' if group=='ir86' else c['source'];files.append(src)
  if group!='ir86':files.append(name+'.ASM')
  if c.get('fixture') is not None:
   fixture=('T'+f'{n:02}' if group!='rb' else f'TRB{n:02}')+('.IR' if group=='ir86' else '.RIL')
   (W/fixture).write_bytes((c['fixture'].replace('\r\n','\n').rstrip('\n')+'\n').replace('\n','\r\n').encode())
   files.append(fixture)
  if c.get('bad') is not None:
   reject=('X'+f'{n:02}' if group!='rb' else f'XRB{n:02}')+('.IR' if group=='ir86' else '.RIL')
   (W/reject).write_bytes((c['bad'].rstrip('\n')+'\n').replace('\n','\r\n').encode());files.append(reject)
 for name in files:shutil.copyfile(W/name,D/name)
 with zipfile.ZipFile(D/archive,'w',zipfile.ZIP_DEFLATED) as z:
  for name in files:
   info=zipfile.ZipInfo(name,(1986,1,1,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;z.writestr(info,(W/name).read_bytes())
 keep=set(files)|{archive}
 if group=='ir86':keep|={'IR86.RIL','IRWIDE.ASM'}
 if group=='rill':keep|={'RILL.RIL','RILLBOOT.IR'}
 for stale in D.iterdir():
  if stale.is_file() and stale.name not in keep:stale.unlink()
 manifest=ROOT/'qa'/('compiler_collections/rb-files.json' if group=='rb' else group+'/package-files.json')
 manifest.write_text(json.dumps(files,indent=2)+'\n')
 if group=='rb':
  snap=ROOT/'workbench/rb';snap.mkdir(exist_ok=True)
  for name in files:shutil.copyfile(W/name,snap/name)
 print('Packaged',group,len(files),'source files')
