"""Diagnose short-branch reach using the BASIC-produced symbol addresses.
Only byte lengths are counted; no instruction bytes or COM files are generated.
"""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[2]
source=ROOT/'workbench/asm0/ASM86.ASM'
symbols=json.loads((ROOT/'qa/asm0/basic-ASM86-symbols.json').read_text())
registers={'AL','CL','DL','BL','AH','CH','DH','BH','AX','CX','DX','BX','SP','BP','SI','DI'}
byteset={'AL','CL','DL','BL','AH','CH','DH','BH'}
pc=256
for number,raw in enumerate(source.read_text().splitlines(),1):
 line=raw.split(';')[0].strip()
 if not line:continue
 if line.endswith(':'):
  label=line[:-1];assert pc==symbols[label],(label,pc,symbols[label]);continue
 mnemonic,*rest=line.split(None,1);args=rest[0] if rest else ''
 operands=[v.strip() for v in args.split(',')]
 if mnemonic=='DB':length=len(operands)
 elif mnemonic=='DW':length=2*len(operands)
 elif mnemonic in {'NOP','RET','CLD','LODSB','STOSB','INC','DEC','PUSH','POP'}:length=1
 elif mnemonic in {'CALL','JMP'}:length=3
 elif mnemonic.startswith('J'):
  length=2
  if args in symbols:
   distance=symbols[args]-(pc+2)
   if not -128<=distance<=127:print(number,line,'distance',distance)
 elif mnemonic=='INT':length=2
 elif mnemonic=='MOV':
  a,b=operands
  if '[' in a or '[' in b:length=2 if '[BX]' in (a,b) else 4
  elif b in registers:length=2
  else:length=2 if a in byteset else 3
 elif mnemonic in {'ADD','SUB','CMP','AND','OR','XOR'}:
  length=2 if operands[1] in registers else (3 if operands[0] in byteset else 4)
 else:raise AssertionError(line)
 pc+=length
print('Image size from BASIC-verified addresses:',pc-256)
