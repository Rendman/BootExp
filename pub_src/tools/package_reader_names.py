"""Publish canonical reader filenames while retaining established download URLs."""
import json,zipfile
from publication_names import ROOT,SERIES,filename,names,reader_text
bundles=[('bootasm','BOOTASM.ZIP'),('asm86','ASM86.ZIP'),('asma0','ASMA0.ZIP'),('asm86a','ASM86A.ZIP'),('ir86','IR86.ZIP'),('rill','RILL.ZIP'),('rb','RB.ZIP'),('rc','RC.ZIP'),('toolchain','TOOLCHN.ZIP'),('link86','LINK86.ZIP'),('edit86','EDIT86.ZIP')]
manifest={}
for group,oldzip in bundles:
 canonical=SERIES[group][0].lower() if group in SERIES else group
 D=ROOT/'site/static/downloads/tools'/canonical;D.mkdir(parents=True,exist_ok=True)
 old=ROOT/'site/static/downloads'/group;files=[];origins={}
 with zipfile.ZipFile(old/oldzip) as z:
  for original in z.namelist():
   if group=='rc' and original in ['IR86.RIL','ASM86A.RIL','TMAKE.BAT']:continue
   new=filename(original);assert new not in files,(group,new)
   raw=z.read(original)
   if original in ['README.TXT','TMAKE.BAT']:raw=reader_text(group,original,raw.decode('ascii')).encode('ascii')
   (D/new).write_bytes(raw);files.append(new);origins[new]=original
 archive=D/filename(oldzip);same=False
 if archive.exists():
  with zipfile.ZipFile(archive) as z:same=z.namelist()==files and all(z.read(n)==(D/n).read_bytes() for n in files)
 if not same:
  with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED) as z:
   for name in files:
    info=zipfile.ZipInfo(name,(1986,1,1,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;z.writestr(info,(D/name).read_bytes())
 keep=set(files)|{archive.name}
 if group=='ir86':keep|={'IR86.RIL','IRWIDE.ASM'}
 if group=='rill':keep|={'RILL.RIL','RILLBOOT.IR'}
 for stale in D.iterdir():
  if stale.is_file() and stale.name not in keep:stale.unlink()
 manifest[canonical]=dict(legacy_group=group,legacy_archive=oldzip,archive=archive.name,files=origins)
# Keep established direct-source links available alongside the native IR86 cover source.
for group,source in [('ir86','IR86.RIL'),('ir86','IRWIDE.ASM'),('rill','RILL.RIL'),('rillboot','RILLBOOT.IR')]:
 (ROOT/'site/static/downloads/tools'/group/source).write_bytes((ROOT/'site/static/downloads/toolchain'/source).read_bytes())
(ROOT/'qa/reader-packages.json').write_text(json.dumps(manifest,indent=2)+'\n')
print('Published canonical reader sources: BOOTASM, ASM0, ASM1, ASM86, IR86, RILL0, RILLBOOT, RILL and toolchain')
