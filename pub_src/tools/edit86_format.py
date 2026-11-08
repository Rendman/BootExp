"""Lay out authored RILL text; this does not translate or encode a language."""
import re
def layout(text):
 # Protect literals and comments while putting statement and brace boundaries
 # on their own lines. No lexical spelling or token order is changed.
 tokens=re.findall(r'"(?:\\.|[^"\\])*"|//[^\n]*|[^"/]+|/(?!/)',text)
 level=0;line='';lines=[]
 def emit():
  nonlocal line
  if line.strip():lines.append('    '*level+line.strip())
  line=''
 for part in tokens:
  if part.startswith('"'):line+=part;continue
  if part.startswith('//'):
   emit();lines.append('    '*level+part);continue
  for ch in part:
   if ch=='{':line+='{';emit();level+=1
   elif ch=='}':emit();level-=1;lines.append('    '*level+'}')
   elif ch==';':line+=';';emit()
   elif ch=='\n':
    if line and not line.endswith(' '):line+=' '
   else:line+=ch
 emit();assert level==0
 return '\n'.join(lines)+'\n'
