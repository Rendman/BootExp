"""Publish separate compiler collections while retaining earlier article addresses."""
from pathlib import Path
import json,re
ROOT=Path(__file__).resolve().parents[1]
CONTENT=ROOT/'site/content/bootstrap'
def publish(collection,page,text,weight=None,download=None):
 if weight is not None:text=re.sub(r'(?m)^weight = \d+$',f'weight = {weight}',text,count=1)
 if collection not in ['rb','rc']:
  dest=CONTENT/collection/page;dest.write_text(text);return
 if download is not None:text=re.sub(r'(?m)^download = .*$',f'download = "{download}"',text,count=1)
 group='toolchain' if download=='TOOLCHN.ZIP' else collection
 text=re.sub(r'(?m)^download_group = .*$',f'download_group = "{group}"',text,count=1)
 if 'download_group =' not in text.split('+++')[1]:text=text.replace('+++\n\n',f'download_group = "{group}"\n+++\n\n',1)
 alias='/bootstrap/rill/'+Path(page).stem+'/'
 text=text.replace('+++\n\n',f'aliases = [{json.dumps(alias)}]\n+++\n\n',1)
 (CONTENT/'rill'/page).unlink(missing_ok=True)
 dest=CONTENT/collection/page;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_text(text)
