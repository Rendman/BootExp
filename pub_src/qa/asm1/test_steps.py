"""Build each new stopping point with ASM0 and execute its actual DOS interface."""
from pathlib import Path
import sys,json
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'tools'));sys.path.insert(0,str(ROOT/'qa/asm86'))
from asm1_steps import STEPS,prepare,sources
from machine import AssemblerMachine,assemble
from unicorn.x86_const import UC_X86_REG_AH,UC_X86_REG_AX
prepare()
W=ROOT/'workbench/asm1';Q=ROOT/'qa/asm1'
builder=(ROOT/'workbench/asm0/ASM86.COM').read_bytes()
records=[];facts=[]
for definition in STEPS:
 s=dict(definition);name=s['id'];source=(W/(name+'.ASM')).read_bytes()
 assert all(len(row)<=120 for row in source.splitlines()),name
 built=assemble(builder,source);assert built.exitcode==0,(name,built.output)
 image=built.files['RESULT.COM'];(W/(name+'.COM')).write_bytes(image)
 s.update(binary_bytes=len(image),binary_hex=image[:32].hex(' ').upper())
 if s['mode']=='probe':
  for tail in [' in.asm out.com','\tIN.ASM\tOUT.COM',' ABCDEFGH.ASM IJKLMNOP.COM']:
   r=AssemblerMachine(command_line=tail).run(image)
   assert r.exitcode==0 and r.output==b'' and r.operations==[],(name,tail,r.output)
  for tail in ['', ' ONLY.ASM',' A B C',' TOO_LONG9.ASM OUT.COM',' A..ASM B.COM',' A. B.COM',' .ASM B.COM',r' C:\IN.ASM OUT.COM',' "IN.ASM" OUT.COM']:
   r=AssemblerMachine(command_line=tail).run(image)
   assert r.exitcode==1 and b'ERROR 00000 CODE 9' in r.output and not r.operations,(name,tail,r.output)
 else:
  fixture='T'+name[1:]+'.ASM';raw=(W/fixture).read_bytes();result=s.get('result','RESULT.COM')
  tail='' if s['mode']=='fixed' else f' {fixture.lower()} {result.lower()}'
  files={'SOURCE.ASM':raw if s['mode']=='fixed' else b'UNKNOWN\r\n',fixture:raw,result:b'OLD'}
  r=AssemblerMachine(files,command_line=tail).run(image)
  expected=bytes.fromhex(s['expected'])
  assert r.exitcode==0 and r.files[result]==expected,(name,r.output,r.files)
  report=f'OK {result} {len(expected):05} bytes\r\n' if name in ['A01E','A01F'] else f'OK {len(expected):05} bytes\r\n'
  assert r.output==report.encode(),(name,r.output,report)
  s.update(target_bytes=len(expected),target_hex=expected.hex(' ').upper())
  if s['mode']=='selected':
   for tail in [f' {fixture}',f' {fixture} {fixture.lower()}',f' {fixture} ASMA.TMP',f' RESULT.BAK {result}']:
    bad=AssemblerMachine(files,command_line=tail).run(image)
    assert bad.exitcode==1 and b'ERROR 00000 CODE 9' in bad.output and not bad.operations,(name,tail,bad.output)
    assert bad.files[result]==b'OLD'
 if name=='A01F':
  # Ask ASM0 for label addresses as ordinary emitted words. Its original
  # machine-code prefix must remain identical to the published executable.
  labelled=assemble(builder,source+b'\r\nDW INPUTOPEN,INPUTCLOSED,INOPEN\r\n')
  assert labelled.exitcode==0,labelled.output
  data=labelled.files['RESULT.COM'];assert data[:-6]==image
  opened,closed,flag=[int.from_bytes(data[i:i+2],'little') for i in range(len(data)-6,len(data),2)]
  assert r.cpu.mem_read(r.base+flag,1)==b'\0'
  for key,offset in [('open',opened-256+4),('close',closed-256)]:
   block=image[offset:offset+6]
   assert block==bytes([0xb0,1 if key=='open' else 0,0x88,0x06])+flag.to_bytes(2,'little'),block
   s[key+'_offset']=offset;s[key+'_hex']=block.hex(' ').upper()
  s['flag_address']=flag
  class FailedInputClose(AssemblerMachine):
   def interrupt(self,c,number,context):
    if number==0x21 and c.reg_read(UC_X86_REG_AH)==0x3e:
     c.reg_write(UC_X86_REG_AX,6);self.carry(True);return
    return super().interrupt(c,number,context)
  failed=FailedInputClose(files,command_line=' T01F.ASM CLOSED.COM').run(image)
  assert failed.exitcode==1 and b'CODE 6' in failed.output and failed.files['CLOSED.COM']==b'OLD'
  assert failed.cpu.mem_read(failed.base+flag,1)==b'\x01'

 facts.append(s);records.append('PASS '+name+': ASM0 build and focused '+s['mode']+' checks')
 print(records[-1],flush=True)
# Restoring XOR at the final small step reproduces the established endpoint.
endpoint=(ROOT/'workbench/asm86/A01.ASM').read_bytes()
built=assemble(builder,endpoint);assert built.exitcode==0,built.output
assert built.files['RESULT.COM']==(ROOT/'workbench/asm86/A01.COM').read_bytes()
r=AssemblerMachine({'SOURCE.ASM':b'XOR AL,AL\r\nXOR AX,BX\r\nXOR AL,80H\r\nXOR AX,1234H\r\n'}).run(built.files['RESULT.COM'])
assert r.exitcode==0 and r.files['RESULT.COM']==bytes.fromhex('32C033C380F08081F03412'),r.output
rejected=AssemblerMachine({'SOURCE.ASM':b'XOR AX,BL\r\n','RESULT.COM':b'OLD'}).run(built.files['RESULT.COM'])
assert rejected.exitcode==1 and rejected.files['RESULT.COM']==b'OLD'
records.append('PASS A01: separate XOR step retains the established executable and checks register/immediate bytes and width rejection')
(Q/'intro.json').write_text(json.dumps(facts,indent=2)+'\n')
(Q/'intro-results.txt').write_text('\n'.join(records)+'\n')
print(records[-1])
