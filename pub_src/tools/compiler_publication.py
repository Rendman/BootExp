"""Publish separate compiler collections while retaining earlier article addresses."""
from project_paths import directory_name
from publication_names import write_page
from pathlib import Path
import json,re
ROOT=Path(__file__).resolve().parents[1]
CONTENT=ROOT/'site/content/bootstrap'
def publish(collection,page,text,weight=None,download=None,aliases=None):
 if weight is not None:text=re.sub(r'(?m)^weight = \d+$',f'weight = {weight}',text,count=1)
 if collection not in ['rb','rc','toolchain']:
  dest=CONTENT/directory_name(collection)/page;write_page(dest,text);return
 if download is not None:text=re.sub(r'(?m)^download = .*$',f'download = "{download}"',text,count=1)
 group='toolchain' if download=='TOOLCHN.ZIP' else collection
 text=re.sub(r'(?m)^download_group = .*$',f'download_group = "{group}"',text,count=1)
 if 'download_group =' not in text.split('+++')[1]:text=text.replace('+++\n\n',f'download_group = "{group}"\n+++\n\n',1)
 routes=aliases if aliases is not None else ['/bootstrap/rill/'+Path(page).stem+'/']
 if routes:text=text.replace('+++\n\n',f'aliases = {json.dumps(routes)}\n+++\n\n',1)
 for route in routes:
  parts=Path(route.removeprefix('/bootstrap/').strip('/')).parts
  old=CONTENT/directory_name(parts[0])/Path(*parts[1:])
  old=old.with_suffix('.md')
  if old!=CONTENT/directory_name(collection)/page:old.unlink(missing_ok=True)
 dest=CONTENT/directory_name(collection)/page;dest.parent.mkdir(parents=True,exist_ok=True);write_page(dest,text)
