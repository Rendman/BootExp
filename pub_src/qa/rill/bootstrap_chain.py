"""Execute canonical BASIC -> ASM86 -> IR86 -> RILL -> IR86 -> ASM86 -> program."""
from common import *
import runpy
# The preceding chain executes BASIC to recreate the assembler, self-assembles it,
# and assembles the translator before any tool binary is consumed here.
runpy.run_path(str(ROOT/'qa/ir86/bootstrap_chain.py'),run_name='__main__')
assembly,image=build_ir((W/'RILL.IR').read_bytes())
if (W/'R29.COM').exists():assert image==(W/'R29.COM').read_bytes()
(W/'RILL.ASM').write_bytes(assembly);(W/'RILL.COM').write_bytes(image)
r=run_compiler((W/'HELLO.RIL').read_bytes(),image)
assert r.exitcode==0,r.output
_,program=build_ir(r.files['RESULT.IR'],'HELLO')
child=DosMachine().run(program)
assert child.exitcode==0 and child.output==b'HI',child.output
text=f'PASS canonical BOOTASM.BAS recreates ASM86; ASM86 self-assembles and builds IR86.\nPASS that IR86 translates RILL.IR and that ASM86 builds RILL.COM ({len(image)} bytes).\nPASS the IR-written RILL compiler translates HELLO.RIL to IR; IR86 and ASM86 build its executable.\nPASS the resulting COM displays HI and returns zero; no host compiler supplies an artifact.\n'
(Q/'bootstrap-results.txt').write_text(text);print(text)
