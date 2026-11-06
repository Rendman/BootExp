from common import *
compiler=(W/'RILL.COM').read_bytes()
for name in ['IR86','ASM86A']:
 r=run(compiler,(W/(name+'.RIL')).read_bytes(),'RIL');print(name,'compile',r.exitcode,bytes(r.output),flush=True)
 assert r.exitcode==0,r.output
 (W/(name+'.IR')).write_bytes(r.files['RESULT.IR']);a,b=ir(r.files['RESULT.IR']);(Q/'generated').mkdir(exist_ok=True);(Q/'generated'/(name+'.ASM')).write_bytes(a);(W/(name+'.COM')).write_bytes(b);print(name,len(a),len(b),flush=True)
 if name=='IR86':
  r=run(b,'PROC MAIN 0 0\nLIT 72\nPUTC\nLIT 73\nPUTC\nLIT 0\nRETURN\n');print(bytes(r.output));assert r.exitcode==0
  child=run(asm(r.files['RESULT.ASM']));assert child.output==b'HI' and child.exitcode==0
