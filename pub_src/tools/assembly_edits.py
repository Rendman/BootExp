"""Print label-based assembly edits for editors without source line numbers."""
from difflib import SequenceMatcher
import re

LABEL=re.compile(r'^[A-Z][A-Z0-9_]*:$')

def code_lines(lines):
 return [line.strip() for line in lines if line.strip() and not line.lstrip().startswith(';')]

def fence(lines):return '```asm\n'+'\n'.join(lines)+'\n```\n\n'

def source_note(previous,current,builder):
 start=f'`{previous}`' if previous else 'new listing'
 return f'**Starting source:** {start}. **Save as:** `{current}`. **Build with:** `{builder}`.\n\n'

def patch(previous,lines,complete_error_exits=False):
 previous=code_lines(previous);lines=code_lines(lines)
 edits=[op for op in SequenceMatcher(None,previous,lines,autojunk=False).get_opcodes() if op[0]!='equal']
 if complete_error_exits:
  # Show both complete error paths when a new path would otherwise reuse
  # an unprinted, textually identical JMP from the old path.
  edits=[(tag,a,b+1,c,d+1) if tag=='insert' and previous[a:b+1]==['JMP ERROR'] and lines[d:d+1]==['JMP ERROR']
         else (tag,a,b,c,d) for tag,a,b,c,d in edits]
 if not edits:return 'The instructions and data are retained without edits. This stopping point proves the executable handoff.\n\n',[]
 text=('Apply the changes in the order shown, working upward through the old source. '
       'Use Find to locate each label, including its colon, and confirm that it stands alone on a source line. '
       'The locator blocks are existing source: leave them in place and type only the stated insertion or replacement. '
       'Blank lines and comment-only lines may differ in your copy.\n\n')
 working=list(previous);changes=[]
 for number,(_,a,b,c,d) in enumerate(reversed(edits),1):
  old=previous[a:b];new=lines[c:d];source='\n'.join(working)
  # Later edits may temporarily duplicate a moved data label. Anchor this
  # earlier edit at a label that is still unique at the actual editing step.
  labels=[i for i in range(min(a,len(previous)-1),-1,-1)
          if LABEL.fullmatch(previous[i]) and working.count(previous[i])==1]
  candidates=[i for i in labels if source.count(previous[i])==1] or labels
  assert candidates,('No unique existing label for edit',old,new)
  start=candidates[0];anchor=previous[start][:-1]
  before=previous[start:a]
  placement='before_label' if start==a and not old else 'at_label' if start==a else 'after_context'
  assert working[a:b]==old
  if before:assert working[start:a]==before
  text+=f'### Change {number} · `{anchor}:`\n\n'
  if placement=='before_label':
   text+=f'Find the unique label `{anchor}:`. Insert the new source immediately before this existing label:\n\n'+fence([anchor+':'])
  elif placement=='at_label':
   text+=f'Find the unique label `{anchor}:`. The old block below starts at that label.\n\n'
  else:
   text+=f'Find the unique label `{anchor}:`, then follow this unchanged source through its last displayed instruction:\n\n'+fence(before)
   text+='The edit begins immediately after that unchanged block.\n\n'
  if old:text+=('Replace this existing source:\n\n' if new else 'Remove this existing source:\n\n')+fence(old)
  if new:text+=('With:\n\n' if old else 'Insert:\n\n')+fence(new)
  end_anchor=None
  if old and b<len(previous) and LABEL.fullmatch(previous[b]) and working.count(previous[b])==1:
   end_anchor=previous[b][:-1]
   text+=f'Keep the following `{end_anchor}:` label and the source after it in place.\n\n'
  changes.append(dict(a1=a,a2=b,anchor=anchor,placement=placement,landmark=[anchor+':'] if placement=='before_label' else [],
                      context=before,old=old,new=new,after=[],end_anchor=end_anchor))
  working[a:b]=new
 assert working==lines,'Labelled edits do not reproduce the intended source'
 return text,changes
