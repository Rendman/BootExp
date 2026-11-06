"""Authored status checks for helpers; retain output only where it is the helper's job."""
import re

def refine(entries,language):
 for e in entries:
  key=e['key'].upper();body=e['body']
  if body is None:continue
  if key in ['ERROR','FAIL']:
   e['body']='LIT 2\nPUSH\nINVOKE ERROR 1\nLIT 0\nRETURN\n' if language=='ir' else 'fail(2);return 0;'
   e['expected']='ERROR 0000000001 CODE 00002\r\n';e['accept_exit']=1
  elif e['expected'].isdigit() and key not in ['PRINTNUM','PRINT32']:
   value=int(e['expected'])
   if language=='ir':
    end='CALL PRINTNUM\nLIT 0\nRETURN\n';assert body.endswith(end),key
    e['body']=body[:-len(end)]+f'PUSH\nLIT {value}\nCNE\nRETURN\n'
   else:
    e['body']=re.sub(r'printnum\((.*)\);return 0;$',lambda m:f'return ({m[1]})!={value};',body)
    assert e['body']!=body,key
   e['expected']='';e['check_value']=value
  elif key=='SETIDENT':
   e['body']='LITS "ABC"\nCALL SETIDENT\nLIT 1\nST TOK\nLITS "ABC"\nCALL ISWORD\nPUSH\nLIT 1\nCNE\nRETURN\n' if language=='ir' else 'setident("ABC");tok=1;return isword("ABC")!=1;'
   e['expected']='';e['check_value']='ABC'
  elif e['fragment'] is not None or e['complete']:
   if language=='ir':e['body']=body.replace('LITS "OK RILL.TMP\\r\\n"\nCALL PRINT\n','')
   else:e['body']=body.replace('print("OK RILL.TMP\\r\\n");','')
   e['expected']=''
  # Missing-file behavior belongs to the first input lesson, not every consumer.
  if e['code']==1 and e['bad'] is None and key!='NEXT':e['code']=None
