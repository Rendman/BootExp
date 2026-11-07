"""Four authored source edits following the first compiler self-build."""

# 512 global records occupy 20480 bytes; 80 local records occupy 3200.
EDITS = [
    ('table = alloc(22000);', 'table = alloc(23680);'),
    ('if localcount >= 32 { fail(5); }', 'if localcount >= 80 { fail(5); }'),
    ('outnum(argc); outstr(" 16\\r\\n");', 'outnum(argc); outstr(" 64\\r\\n");'),
    ('if nextlocal >= 16 { fail(5); }', 'if nextlocal >= 64 { fail(5); }'),
]

def extend(source):
    for old, new in EDITS:
        assert source.count(old) == 1, old
        source = source.replace(old, new)
    return source

def fixtures():
    args = ','.join(f'a{i}' for i in range(16))
    vals = ','.join(str(i) for i in range(16))
    rows = [''.join(f'let mut v{i}={i};' for i in range(j, j+8)) for j in range(0,64,8)]
    checks = '\n'.join('if '+(' | '.join(f'(v{i}!={i})' for i in range(j,j+8)))+' {return 1;}' for j in range(0,64,8))
    accepted = f'fn check({args}){{\n'+'\n'.join(rows)+'\n'+checks+'\nreturn (a0!=0)|(a15!=15);\n}\n'+f'fn main(){{return check({vals});}}\n'
    rejected = accepted.replace('return (a0!=0)', 'let mut extra=0;\nreturn (a0!=0)')
    # Each sibling scope fills all 64 slots. Main separately checks shadowing.
    scope = 'let mut result=0;\nfn reuse(){\n'
    for value in [17,29]:
        scope += '{\n'+'\n'.join(rows)+f'\nv63={value};result=result+v63;\n}}\n'
    scope += 'return 0;\n}\nfn main(){let mut v63=7;{let mut v63=9;if v63!=9{return 1;}}reuse();return (result!=46)|(v63!=7);}\n'
    return {'TLOCAL.RIL':accepted, 'XLOCAL.RIL':rejected, 'TSCOPE.RIL':scope}
