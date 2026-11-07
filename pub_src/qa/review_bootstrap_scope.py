"""Read-only successor-usage audit. Never translates a bootstrap language or emits code."""
from pathlib import Path
import collections,json,re,sys
ROOT=Path(__file__).resolve().parents[1];W=ROOT/'workbench';Q=ROOT/'qa'

def assembly(paths):
 used=collections.defaultdict(set);sizes=[]
 for p in paths:
  labels=set();width=0
  for line in p.read_text().splitlines():
   width=max(width,len(line));s=line.split(';',1)[0].strip()
   if not s:continue
   if s.endswith(':'):labels.add(s[:-1]);continue
   words=s.split();op='EQU' if len(words)>1 and words[1]=='EQU' else words[0]
   used[op].add(str(p.relative_to(ROOT)))
  sizes.append({'source':str(p.relative_to(ROOT)),'definitions':len(labels),'physical_line_width':width,'source_bytes':p.stat().st_size})
 return used,sizes

def ir(paths):
 used=collections.defaultdict(set)
 for p in paths:
  for line in p.read_text().splitlines():
   s=line.strip()
   if s and not s.startswith(';'):used[s.split()[0]].add(str(p.relative_to(ROOT)))
 return used

def table(path):
 s=path.read_text().split('OPTAB:\n',1)[1].split('\n\n',1)[0];out=set()
 for row in s.splitlines():
  if row.startswith('DB '):out.add(bytes(int(n) for n in row[3:].split(',')[:6]).split(b'\0')[0].decode('ascii'))
 return out

TOKEN=re.compile(r'//[^\n]*|"(?:[^"\\]|\\.)*"|[A-Za-z_][A-Za-z_0-9]*|\d+|==|!=|<=|>=|<<|>>|[^\s]')
def rill(paths):
 calls=collections.defaultdict(set);operators=collections.defaultdict(set);stats=[]
 for p in paths:
  text=p.read_text();tokens=[m[0] for m in TOKEN.finditer(text) if not m[0].startswith('//')]
  definitions=re.findall(r'^fn (\w+)\(([^)]*)\)',text,re.M);defined={n for n,_ in definitions}
  source=str(p.relative_to(ROOT))
  for i,t in enumerate(tokens):
   if t in ['^','<<','>>','~','!','&','|','-']:operators[t].add(source)
   if t in ['-','&'] and (i==0 or tokens[i-1] in ['(','=','return',',',';','{','+','-','*','/','!=','==','&','|','if','while']):operators['unary '+t].add(source)
   if i+1<len(tokens) and tokens[i+1]=='(' and re.fullmatch(r'[A-Za-z_]\w*',t) and t not in defined|{'if','while','return'}:calls[t].add(source)
  literals=[]
  for t in tokens:
   if t.startswith('"'):literals.append(len(bytes(t[1:-1],'ascii').decode('unicode_escape')))
  stats.append({'source':source,'global_and_procedure_names':len(defined)+len(re.findall(r'^(?:let mut|bytes) ',text,re.M)), 'largest_parameter_list':max((len([v for v in args.split(',') if v.strip()]) for _,args in definitions),default=0),'longest_string_bytes':max(literals,default=0)})
 return calls,operators,stats

def profile(name,accepted,paths,kind='asm'):
 if kind=='asm':used,stats=assembly(paths)
 else:used=ir(paths);stats=[]
 return {'tool':name,'consumers':[str(p.relative_to(ROOT)) for p in paths],'accepted':sorted(accepted),'observed':sorted(used),'not_observed_candidates':sorted(set(accepted)-set(used)), 'witnesses':{k:sorted(v) for k,v in sorted(used.items())},'resources':stats}

names=set(json.loads((Q/'asm86/checkpoints.json').read_text())[-1]['names'])
result={'status':'REVIEW PENDING','meaning':'Usage candidates are not deletion proofs. Complete successor construction, self-builds, runtime bindings, failure behavior and readability must also be checked. Required teaching stages are retained; their code must evolve into the following implementation.','profiles':[]}
result['profiles'].append(profile('BOOTASM',names-{'OR'},sorted((W/'asm86').glob('AS[0-9][0-9].ASM'))))
result['profiles'].append(profile('ASM0',names,[W/f'asm86a/A{n:02}.ASM' for n in range(1,13)]+[W/'asm86/ASM86.ASM']))
result['profiles'].append(profile('ASM1',table(W/'asm86a/ASMA0.ASM'),[W/'asm86a'/c['source'] if 'source' in c else W/'asm86a'/f'A{c["number"]:02}.ASM' for c in json.loads((Q/'asm86a/checkpoints.json').read_text()) if c['number']>12]+[W/'asm86a/ASMA0.ASM']))
# The assembler stays a builder until the RILL-written assembler exists. Include emitted code,
# not merely the assembly used to implement the native translator.
generated=[W/'toolchain/RILLBOOT.ASM',W/'toolchain/RILL0.ASM',Q/'toolchain/generated/IR86.ASM',Q/'toolchain/generated/ASM86A.ASM']
for p in generated:
 if not p.exists():raise SystemExit('Run the native seed/compiler/port builds before auditing: '+str(p))
result['profiles'].append(profile('ASM86',table(W/'asm86a/ASM86A.ASM'),[W/'toolchain'/c['source'] for c in json.loads((Q/'toolchain/ir-extensions.json').read_text())]+generated))
wide_consumers=[W/'rill'/c['source'] for c in json.loads((Q/'toolchain/rill-initial-series.json').read_text())]+[W/'toolchain'/c['source'] for c in json.loads((Q/'toolchain/rill-seed-series.json').read_text())]+[W/'toolchain/RILL0.IR',W/'toolchain/IR86.IR',W/'toolchain/ASM86A.IR']
result['profiles'].append(profile('Native IR86',json.loads((Q/'toolchain/wide-ops.json').read_text()),wide_consumers,kind='ir'))
calls,operators,stats=rill(sorted((W/'toolchain').glob('RC[0-9][0-9].RIL')))
seed=(W/'rill/RILLBOOT.IR').read_text()
accepted={n.lower() for n in re.findall(r'([A-Z][A-Z0-9_]*)\\0[0-9]\\0',seed)}
seed_extras=[]
for description,token,label in [('bitwise XOR','^','BINXOR'),('left shift','<<','BINSHL'),('unary minus','unary -','PRIMARYNEG'),('bitwise complement','~','PRIMARYNOT'),('explicit address-of','unary &','PRIMARYADDR')]:
 if token not in operators and re.search(r'^LABEL '+label+r'$',seed,re.M):seed_extras.append(description)
result['compiler_seed']={'tool':'RILLBOOT','immediate_successor':'RILL.RIL and all RC construction sources','required_intrinsics':sorted(calls),'not_observed_intrinsics':sorted(accepted-set(calls)),'not_observed_syntax':seed_extras,'successor_resources':stats[-1] if stats else {},'final_source_resources':rill([W/'toolchain/RILL.RIL'])[2][0]}
result['final_compiler_consumers']={'tools':rill([W/'toolchain/IR86.RIL',W/'toolchain/ASM86A.RIL'])[2],'intrinsics':sorted(rill([W/'toolchain/IR86.RIL',W/'toolchain/ASM86A.RIL'])[0])}
patches=json.loads((Q/'toolchain/ladder-article-patches.json').read_text())
seed_first=next(p for p in patches if p['family']=='rill-seed-series')
one_ir=(W/'ir86/IR86.ASM').read_bytes()==(W/'ir86/IRWIDE.ASM').read_bytes()
result['required_evolution']=[{'from':'native IR86','status':'PASS' if one_ir else 'FAIL','evidence':'One native construction grows from its first translator through frames, strings and workspace; both retained aliases are identical.'},{'from':'RILL0','current_base':seed_first['base'],'required_base':'RILL0.IR','status':'PASS' if seed_first['base']=='RILL0.IR' else 'FAIL','evidence':'Printed continuation edits start from the accepted RILL0 source; each continuation remains a complete compiler.'}]
failures=[p['tool'] for p in result['profiles'] if p['not_observed_candidates']]
if result['compiler_seed']['not_observed_intrinsics'] or seed_extras:failures.append('RILLBOOT')
if any(e['status']!='PASS' for e in result['required_evolution']):failures.append('source evolution')
result['status']='PASS' if not failures else 'REWORK REQUIRED'
(Q/'bootstrap-scope-review.json').write_text(json.dumps(result,indent=2)+'\n')
lines=['Bootstrap scope review: '+result['status'],'Required first IR86 and RILL0 remain on the path and must evolve, not become optional.']
for p in result['profiles']:lines.append(p['tool']+' accepted mnemonics not observed in successor implementations: '+', '.join(p['not_observed_candidates']))
lines+=['RILLBOOT intrinsics not used by the RILL compiler construction: '+', '.join(result['compiler_seed']['not_observed_intrinsics']),'RILLBOOT syntax not used by that construction: '+', '.join(seed_extras)]
for e in result['required_evolution']:lines.append(e['from']+' evolution: '+e['status']+'; '+e['evidence'])
lines.append('Each accepted operation has a successor-source witness. Native execution and exact rebuild checks are recorded separately.')
(Q/'bootstrap-scope-results.txt').write_text('\n'.join(lines)+'\n');print('\n'.join(lines))
if '--strict' in sys.argv:raise SystemExit(0 if result['status']=='PASS' else 1)
