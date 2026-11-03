"""Read and type into our own QEMU DOS test console."""
import socket,time,sys
from pathlib import Path
MON=sys.argv[1];TEXT=sys.argv[2] if len(sys.argv)>2 else ''
s=socket.socket(socket.AF_UNIX);s.connect(MON);s.settimeout(2);s.recv(4096)
def command(text):
 s.sendall((text+'\n').encode());time.sleep(.06)
 try:return s.recv(16384)
 except TimeoutError:return b''
keys={':':'shift-semicolon','\\':'backslash',' ':'spc','\n':'ret','"':'shift-apostrophe',',':'comma','.':'0x34','/':'slash','(':'shift-9',')':'shift-0','=':'equal','$':'shift-4'}
for ch in TEXT:
 key=keys.get(ch,ch.lower())
 command('sendkey '+key+' 1')
time.sleep(.1)
path=Path(__file__).resolve().parents[1]/'qa/console.bin'
# The monitor requires a filesystem supporting native file operations.
command('pmemsave 0xb8000 4000 "/tmp/bootexp-console.bin"')
raw=Path('/tmp/bootexp-console.bin').read_bytes();path.write_bytes(raw)
print('\n'.join(raw[i:i+160:2].decode('cp437') for i in range(0,4000,160)))
