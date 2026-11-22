"""Build every adventure with the RILL-written trio and execute public commands."""
from pathlib import Path
import json,sys

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'tools'));sys.path.insert(0,str(ROOT/'qa/toolchain'))
from common import run,W as TOOLS
from machine import AssemblerMachine
from build_vampire import source,dos
from vampire_lessons import RECIPES,expand,cases
W=ROOT/'workbench/vampire';Q=ROOT/'qa/vampire'

def build(text):
    reports=[];sizes=[]
    for tool,kind,result in [('RILL','RIL','RESULT.IR'),('IR86','IR','RESULT.ASM'),('ASM86A','ASM','RESULT.COM')]:
        r=run((TOOLS/(tool+'.COM')).read_bytes(),text,kind)
        assert r.exitcode==0,(tool,r.output)
        assert not r.allocations and not r.handles,(tool,'builder resource leak')
        text=r.files[result];sizes.append(len(text));reports.append(r.output.decode('ascii'))
    return text,sizes,reports

def play(image,text='',console=False,files=None,command_line=None):
    f={'CON' if console else 'PLAY.TXT':text.encode('ascii')};f.update(files or {})
    return run(image,files=f,command_line=command_line if command_line is not None else ('' if console else 'PLAY.TXT'))

def clean(r):
    assert r.exitcode==0,(r.exitcode,r.output)
    assert not r.handles and not r.allocations,'adventure resource leak'
    return r.output.decode('ascii')

def main():
    logs=[];records=cases()
    exercise_only='--exercise-only' in sys.argv
    if exercise_only:records=json.loads((Q/'checkpoints.json').read_text())
    for name in RECIPES:dos(W/name,expand(name))
    for c in ([] if exercise_only else records):
        n=c['number'];dos(W/c['source'],source(n))
        image,sizes,reports=build((W/c['source']).read_bytes())
        (W/f'V{n:02}.COM').write_bytes(image)
        text=clean(play(image,expand(c['accept'])))
        for expected in c['expected']:assert expected in text,(n,expected,text)
        if c['alternate']:
            alternate=clean(play(image,expand(c['alternate'])))
            for expected in c['alternate_expected']:assert expected in alternate,(n,expected,alternate)
        else:alternate=''
        # A former public path remains usable after adding inventory dispatch.
        if n>=6:
            regression=clean(play(image,'E\nPUSH BOOKCASE\nD\n'))
            assert 'You are in the Hidden Corridor.' in regression,(n,'hidden route lost')
        c.update(ir_bytes=sizes[0],assembly_bytes=sizes[1],binary_bytes=sizes[2],
                 reports=reports,console=text,alternate_console=alternate)
        (Q/'checkpoints.json').write_text(json.dumps(records[:n],indent=2)+'\n')
        logs.append(f'PASS V{n:02}: project-only three-stage build ({len(image)} bytes); public commands and focused alternate; resources closed')
        print(logs[-1],flush=True)
    if exercise_only:image=(W/'VAMPIRE.COM').read_bytes()
    else:
        dos(W/'VAMPIRE.RIL',source(26));(W/'VAMPIRE.COM').write_bytes(image)
    # First/last words, exact input capacity, all accepted line endings and EOF.
    for line in ['lOoK THE SIGN','\tread\t the\t sign  ','REA SIGN']:
        assert 'The sign reads:' in clean(play(image,line+'\nQUIT\n'))
    for ending in ['\r\n','\r','\n']:
        assert 'Goodbye.' in clean(play(image,ending.join(['LOOK','QUIT',''])))
    assert 'Goodbye.' in clean(play(image,'QUIT'))
    for line in ['LOOK'+' '*76,'LOOK'+' '*77,'X'*81,'BAD\0BYTE']:
        t=clean(play(image,line+'\nQUIT\n'))
        assert ('Use at most 80 printable characters.' in t)==(len(line)>80 or '\0' in line)
        assert 'Goodbye.' in t
    assert 'Goodbye.' not in clean(play(image,'LOOK\x1aQUIT\n'))
    assert 'Goodbye.' in clean(play(image,'QUIT\r\n',console=True))
    logs.append('PASS console-selected path; first/last words; whitespace/case; 80/81-byte boundary; bad-byte draining; CR/LF/CR/LF; final line; Control-Z')
    # The 239th action still runs; the 240th terminates before dispatch.
    t=clean(play(image,'WAIT\n'*239+'LOOK\nN\n'))
    assert t.count('Time passes.')==239 and t.count('It is midnight.')==1
    assert t.count('You are in the Entrance Hall.')==1
    t=clean(play(image,'\n \t\n'+'GET TIME\nREAD TIME\nQUIT\n'))
    assert 'Time: 08:02 p.m.' in t
    logs.append('PASS command-driven clock: whitespace free; 239 actions accepted; midnight before action 240; QUIT free')
    # Regression for an accidental GET NORTH being treated as GO NORTH.
    t=clean(play(image,'GET NORTH\nLOOK\nQUIT\n'))
    assert 'I don\'t know that object.' in t and t.count('You are in the Entrance Hall.')==2
    # Replay after both a win and a changed world ending in death.
    for prefix in [expand('WIN.TXT'),'E\nPUSH BOOKCASE\nD\nGET ROPE\nU\nE\nE\nGO PARAPETS\n']:
        t=clean(play(image,prefix+'Y\nINVENTORY\nE\nD\nLOOK\nQUIT\n'))
        after=t.split('Play again (Y/N)? ',1)[1]
        assert 'You are in the Entrance Hall.' in after and '  Nothing.' in after
        assert 'You cannot go that way.' in after and 'You are in the Hidden Corridor.' not in after
    logs.append('PASS winning route, wrong-weapon death, parapet/fire/lake/midnight deaths; replay restores inventory and concealed map')
    # EOF during a reply cannot become a successful tool or weapon answer.
    for text in [expand('ROPE.TXT')+'TIE ROPE\n',expand('COFFIN.TXT')+'KILL DRACULA\n']:
        t=clean(play(image,text));assert 'Congratulations!' not in t and 'Play again' not in t
    # Bad file/argument reports do not masquerade as ordinary game outcomes.
    for args,expected in [('NOFILE.TXT','Cannot open commands.'),('ONE.TXT TWO.TXT','Use VAMPIRE or VAMPIRE COMMANDS.TXT.')]:
        r=play(image,command_line=args);assert r.exitcode==1 and expected.encode() in r.output
        assert not r.handles
    from unicorn.x86_const import UC_X86_REG_AH,UC_X86_REG_AX
    class ReadFailure(AssemblerMachine):
        def interrupt(self,c,n,unused):
            if n==0x21 and c.reg_read(UC_X86_REG_AH)==0x3f:
                c.reg_write(UC_X86_REG_AX,5);self.carry(True);return
            super().interrupt(c,n,unused)
    r=ReadFailure({'CON':b'LOOK\n'}).run(image)
    assert r.exitcode==1 and b'Cannot read commands.' in r.output and not r.handles
    logs.append('PASS EOF during follow-up; missing command file; argument count; injected read failure and owned-handle cleanup')
    (Q/'checkpoints.json').write_text(json.dumps(records,indent=2)+'\n')
    (Q/'test-results.txt').write_text('\n'.join(logs)+'\n')
    print('\n'.join(logs if exercise_only else logs[26:]),flush=True)

if __name__=='__main__':main()
