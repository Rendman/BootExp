"""Publish the optional adventure, with edits anchored at unique RILL routines."""
from pathlib import Path
from difflib import SequenceMatcher
import json,re
from publication_names import write_page
from vampire_lessons import LESSONS,RECIPES,expand

ROOT=Path(__file__).resolve().parents[1]
W=ROOT/'workbench/vampire';Q=ROOT/'qa/vampire';C=ROOT/'site/content/bootstrap/vampire'
CASES=json.loads((Q/'checkpoints.json').read_text())
assert len(CASES)==26,'Execute all construction checkpoints before publishing'

def fence(kind,text):return '```'+kind+'\n'+text.replace('\r\n','\n').rstrip('\n')+'\n```\n\n'
def front(title,weight,description,download,cover=False):
    meta=dict(title=title,weight=weight,description=description,download=download,
              download_group='tools/vampire',reader_names=1)
    if cover:meta.update(cover=True,optional=True,tool_id='VAMPIRE',collection_key='vampire')
    return '+++\n'+''.join(k+' = '+json.dumps(v)+'\n' for k,v in meta.items())+'+++\n\n'
def picture(name,alt,caption,depth=3):
    return f'![{alt}]('+('../'*depth)+f'images/{name}.svg)\n\n*{caption}*\n\n'
def lines(text):return [line for line in text.splitlines() if line.strip()]
def functions(text):
    return {re.match(r'fn (\w+)',part)[1]:lines(part) for part in re.split(r'(?=^fn \w+\()',text,flags=re.M)[1:]}

def edits(before,after):
    """Use complete unique declarations and function headers, never line coordinates."""
    old=lines(before);new=lines(after);changes=[];out=''
    def apply(change):
        nonlocal old,out
        number=len(changes)+1;kind=change['kind']
        out+=f'### Change {number}\n\n'
        if kind=='insert':
            anchor=change['anchor'];assert old.count(anchor)==1
            out+='Find this unique existing declaration or routine header; leave it in place:\n\n'+fence('rill',anchor)
            out+='Insert the following source immediately before it:\n\n'+fence('rill','\n'.join(change['new']))
            index=old.index(anchor);old[index:index]=change['new']
        elif kind=='append':
            out+='Append these complete routines after the final routine in your source:\n\n'+fence('rill','\n'.join(change['new']))
            old+=change['new']
        else:
            a=change['old'];b=change['new']
            count=sum(old[i:i+len(a)]==a for i in range(len(old)))
            assert count==1,(change['routine'],'ambiguous edit')
            out+='Find the unique routine header `'+change['routine']+'`. Within that routine, replace this existing block, including its shown context:\n\n'+fence('rill','\n'.join(a))
            out+='With this complete block:\n\n'+fence('rill','\n'.join(b))
            index=next(i for i in range(len(old)) if old[i:i+len(a)]==a)
            old[index:index+len(a)]=b
        changes.append(change)
    # New declarations are inserted before the next declaration already present.
    declarations=[line for line in new if line.startswith(('let mut ','bytes '))]
    previous_declarations=[line for line in old if line.startswith(('let mut ','bytes '))]
    additions=[op for op in SequenceMatcher(None,previous_declarations,declarations,autojunk=False).get_opcodes() if op[0]!='equal']
    for tag,a,b,c,d in reversed(additions):
        assert tag=='insert','Declarations are introduced without replacing unrelated state'
        at=new.index(declarations[d-1])
        anchor=next(line for line in new[at+1:] if line in old)
        apply(dict(kind='insert',anchor=anchor,new=declarations[c:d]))
    oldf=functions(before);newf=functions(after)
    for name,body in oldf.items():
        desired=newf[name]
        if body==desired:continue
        diffs=[op for op in SequenceMatcher(None,body,desired,autojunk=False).get_opcodes() if op[0]!='equal']
        a,b=diffs[0][1],diffs[-1][2];c,d=diffs[0][3],diffs[-1][4]
        left=min(a,2);right=min(len(body)-b,2)
        while True:
            prior=body[a-left:b+right]
            count=sum(old[i:i+len(prior)]==prior for i in range(len(old)))
            if count==1:break
            if left<a:left+=1
            elif right<len(body)-b:right+=1
            else:raise AssertionError((name,'no unique source context'))
        replacement=desired[c-left:d+right]
        apply(dict(kind='replace',routine=body[0],old=prior,new=replacement))
    # Reverse order makes an inserted following routine available as a locator.
    order=list(newf)
    for index in range(len(order)-1,-1,-1):
        name=order[index]
        if name in oldf:continue
        if index+1<len(order):apply(dict(kind='insert',anchor=newf[order[index+1]][0],new=newf[name]))
        else:apply(dict(kind='append',new=newf[name]))
    assert old==new,'Printed edits must reconstruct the next complete checkpoint'
    return out,changes

FRAGMENTS={}
def fixture(name):
    r=RECIPES[name]
    if name=='X12.TXT':
        listing='10 OPEN "O", #1, "X12.TXT"\n20 FOR I=1 TO 240\n30 PRINT #1, "WAIT"\n40 NEXT I\n50 CLOSE: END\n'
        FRAGMENTS['WAIT.BAS']=listing
        return ('Create WAIT.BAS to make the long deadline input without repeatedly typing WAIT:\n\n'+fence('basic',listing)+
                fence('dos','GWBASIC WAIT.BAS')+'This writes 240 WAIT records to X12.TXT.\n\n')
    if r['base']:
        if r['text']:
            fragment=next((key for key,value in FRAGMENTS.items() if key.endswith('.TXT') and value==r['text']),None)
            if fragment:
                opening=f'Reuse the saved {fragment} command tail.\n\n'
            else:
                fragment='F'+str(list(RECIPES).index(name)+1).zfill(3)+'.TXT'
                FRAGMENTS[fragment]=r['text']
                opening=f'Create {fragment} with these additional commands:\n\n'+fence('text',r['text'])
            return (opening+
                    f'Join the saved {r["base"]} walk and this tail as {name}:\n\n'+
                    fence('dos',f'COPY /B {r["base"]}+{fragment} {name}'))
        return fence('dos',f'COPY {r["base"]} {name}')
    if not r['text']:return ''
    return f'Create {name} as plain text:\n\n'+fence('text',r['text'])

C.mkdir(parents=True,exist_ok=True)
t=front('Vampire Castle Adventure',100,'An optional text adventure built with our completed RILL workbench.','VAMPIRE.RIL',True)
t+='The compiler finally builds programs of its own, and I want to use it for an evening in a different sort of workshop. A BASIC adventure listing offers a castle, a sleeping vampire and a collection of objects that are never quite where I need them. Vampire Castle Adventure is an optional RILL application after [Rebuilding Our Tools in RILL](../toolchain/index.html); it is outside the required bootstrap ladder.\n\n'
t+='Twenty-six working stopping points grow the title into the complete adventure. Each uses the established compiler, translator and assembler. The world, command reader and puzzles are built in small pieces; saved journeys avoid entering the same long route for each check. LINK86 and EDIT86 are not prerequisites.\n\n'
t+='The BASIC listing supplies the map, objects and puzzle sequence. The RILL program uses plain DOS text, bounded input, visible object checks and an independent reset for each game. It contains no BASIC interpreter and loads no external game data.\n\n'
t+='Begin with [the adventure workbench](00-workbench/index.html). The [source disk](../../downloads/tools/vampire/VAMPIRE.ZIP) contains every RILL stopping point, command fixture and the complete game, without prebuilt executables. [Playing the adventure](27-playing/index.html) keeps the solution separate from the construction; [the program reference](28-reference/index.html) records the rules and limits.\n\n'
t+=picture('vampire-gate','A young programmer holding a disk asks a castle gatekeeper to admit a small compiler.','The tools have brought us to a different sort of gate.',2)
write_page(C/'_index.md',t)

t=front('The adventure workbench',0,'Preserve the completed RILL trio and build each game before trying its commands.','VAMPIRE.ZIP')
t+='This optional series begins after the three RILL-written tools and their matching rebuilds. Preserve the compiler as R0.COM, translator as I0.COM and assembler as A0.COM. Use the DOS 3.10 work directory and a plain ASCII editor. Copy the established CHECK.BAT here. No linker, screen service extension or outside development tool is needed.\n\n'
t+='## A build worth keeping\n\nCreate VMAKE.BAT:\n\n'
batch='''ECHO OFF
IF "%1"=="" GOTO USAGE
R0 %1.RIL RESULT.IR
IF ERRORLEVEL 1 GOTO FAILED
I0 RESULT.IR RESULT.ASM
IF ERRORLEVEL 1 GOTO FAILED
A0 RESULT.ASM RESULT.COM
IF ERRORLEVEL 1 GOTO FAILED
COPY RESULT.COM %1.COM >NUL
IF ERRORLEVEL 1 GOTO FAILED
ECHO BUILD PASS
GOTO END
:USAGE
ECHO Use VMAKE V01
GOTO END
:FAILED
ECHO BUILD FAIL - DO NOT RUN AN OLDER GAME
:END
'''
FRAGMENTS['VMAKE.BAT']=batch
t+=fence('dos',batch)
t+='Enter `VMAKE V01` to build V01.RIL through all three tools and preserve V01.COM. Each tool must print a fresh OK report; require BUILD PASS before running the preserved program. A failed build can leave an older .COM with the same name. BUILD FAIL does not authorize running it. Keep all three result names distinct from the checkpoint name. The batch invokes executable tools directly and works without nested batch calls.\n\n'
t+='## Keyboard and saved commands\n\nEnter `V26` for keyboard play. It opens DOS CON as a readable device and uses ordinary line input; press Return to submit a command. The game writes its replies through putc. The first input-reading checkpoint returns at end of input; Control-Z followed by Return ends console text. From the command-parser checkpoint onward, QUIT also returns to DOS.\n\n'
t+=fence('dos','CHECK V26 WIN.TXT')
t+='The optional filename comes from argc()/arg(1), backed by the saved PSP command tail. It must be an unquoted 8.3 name in the current directory. A command file is read-only and is echoed as it runs. CR/LF, bare CR and LF are accepted. End of file stops play; it does not save a position. A terminal game result can ask for Y/N; include the answer in a script if you want a replay.\n\n'
t+='## Retain the journeys\n\nEnter each named command file when it first appears and keep it. COPY /B joins a saved prefix and a short tail; it does not run the game. Command files contain ordinary text without a Control-Z terminator. Keep the final newline before appending a tail. The fixtures in the source disk already have the exact DOS line endings.\n\n'
t+='Every construction article builds its own Vnn.COM, runs a focused accepted walk and checks a relevant alternate. The printed expected lines are the significant parts of the ordinary game transcript, in addition to prompts, room descriptions and echoed commands. CHECK reports PASS for ordinary play, including death and victory; those outcomes are game rules. File, argument or service failures return nonzero and must report FAIL.\n\n'
t+='## Preserve the finished adventure\n\n'+fence('dos','COPY V26.RIL VAMPIRE.RIL\nCOPY V26.COM VAMPIRE.COM\nVAMPIRE')
t+='The game remains optional. No bootstrap article depends on its executable, source or extra files. Its source disk is self-contained apart from the already constructed RILL trio and DOS/BASIC workbench.\n'
write_page(C/'00-workbench.md',t)

patches=[];previous=''
for c,lesson in zip(CASES,LESSONS):
    n=c['number'];title,why,opening,explanation,trouble=lesson
    slug=re.sub(r'[^a-z0-9]+','-',title.lower()).strip('-');page=f'{n:02}-{slug}.md'
    current=(W/c['source']).read_text()
    t=front(f'{n:02} · {title}',n,why,c['source'])+opening+'\n\n## What changes\n\n'+explanation+'\n\n'
    t+='## Enter the source\n\n'
    if n==1:
        t+='Create V01.RIL as plain ASCII:\n\n'+fence('rill',current)
        changes=[dict(kind='initial',new=lines(current))]
    else:
        t+=f'Copy V{n-1:02}.RIL to V{n:02}.RIL. Apply the following edits in order. All locators are existing declarations or unique routine headers; no editor line numbers are needed. Keep the source outside each stated edit.\n\n'
        patch,changes=edits(previous,current);t+=patch
    t+='## Build and try it\n\n'+fence('dos',f'VMAKE V{n:02}')
    t+='Require these fresh tool reports, followed by BUILD PASS:\n\n'+fence('text',''.join(c['reports'])+'BUILD PASS\n')
    t+=f'The preserved V{n:02}.COM is {c["binary_bytes"]:,} bytes. Its natural display and behavior are the checks below.\n\n'
    added=[name for name,r in RECIPES.items() if r['stage']==n]
    for name in added:
        if n==1:continue
        t+=fixture(name)
    t+=fence('dos',f'CHECK V{n:02}'+('' if n==1 else f' T{n:02}.TXT'))
    t+='Require these significant game lines, followed by CHECK\'s PASS:\n\n'+fence('text','\n'.join(c['expected'])+'\nPASS')
    if c['alternate']:
        t+='## Check the other case\n\n'+fence('dos',f'CHECK V{n:02} {c["alternate"]}')
        t+='Require these significant lines and PASS:\n\n'+fence('text','\n'.join(c['alternate_expected'])+'\nPASS')
        if n>=12:t+='A player death or an unsuccessful action is an ordinary game outcome, so CHECK still reports PASS. Judge the stated message and the resulting world as well as the process status.\n\n'
    t+='## If it differs\n\n'+trouble+'\n'
    if n==10:t+='\n'+picture('vampire-rat','A rat guards an oversized key while a visitor offers a wedge of cheese beside a crowded coat rack.','Not every obstacle calls for a larger tool.')
    if n==25:t+='\n'+picture('vampire-clock','A vampire in a nightcap watches a clock while a programmer carries a little wooden stake.','One command before midnight.')
    write_page(C/page,t)
    patches.append(dict(number=n,page=page,source=c['source'],changes=changes))
    previous=current

t=front('Playing the adventure',27,'Keyboard commands, hints and a separately marked winning walk.','VAMPIRE.RIL')
t+='Compile the complete VAMPIRE.RIL with the same three tools, or preserve the accepted V26.COM under that name. Enter VAMPIRE for keyboard play, or VAMPIRE followed by a saved command filename. This is a text adventure: no color display, cursor-addressing driver or sound hardware is required.\n\n'
t+='## Commands\n\nUse the first word for an action and the last for its object; only the first three letters of each count. LOOK describes the room; READ THE SIGN examines the sign. N, S, E, W, U and D move through ordinary exits. GET/T AKE, DROP and INVENTORY manage possessions. HIT, OPEN, TIE, PUSH, ROW and OIL act on the surroundings. CLIMB shares GO; BREAK shares HIT; THRUST shares KILL. HELP lists the commands, WAIT spends a minute and QUIT returns to DOS. When asked With what?, In what? or To what?, answer with the object, such as HAMMER or BUCKET.\n\n'.replace('GET/T AKE','GET/TAKE')
t+='The adventure begins at 8:00 p.m. Every nonempty, well-formed command except QUIT spends one minute, including LOOK, HELP and an unknown action. A follow-up answer belongs to its original action. Midnight ends play before the 240th action can run. There is room for seven carried objects. A visible fixed object cannot be taken; an object in another room cannot be inspected by guessing its name.\n\n'
t+='## Hints\n\nRead the entrance sign and the parchment. Try moving furniture. An opening may require a tool even after it is safe to enter. A rope needs an anchor; water needs a vessel. Keep the crate intact until it has served as a step. A small guardian may prefer food to a fight. The timepiece is useful but need not occupy a carrying place throughout the walk.\n\n'
t+='## Solution — stop here to explore unaided\n\nWIN.TXT is a complete winning walk assembled from the saved journeys in the construction. It leaves the oar briefly on the Torture Chamber floor to demonstrate that the rat still guards a reachable key, then retrieves it before crossing the lake. The crate supports the climb before becoming stakes. Nails, tapestry and axe are dropped when their jobs are complete.\n\n'
t+=fence('dos','CHECK VAMPIRE WIN.TXT')
victory=CASES[-1]['console'];clock=re.findall(r'Time: [^\r\n]+',victory)[-1]
t+='Require the following ending; EOF after the replay question returns to DOS:\n\n'+fence('text','Congratulations! You have killed Dracula.\n'+clock+'\nPlay again (Y/N)?\nPASS')
t+='The actual commands in the complete walk are:\n\n'+fence('text',expand('WIN.TXT'))
t+='The game does not write a saved position. To replay a journey, run its command file again. A new game resets every object, exit and puzzle flag.\n'
write_page(C/'27-playing.md',t)

t=front('The adventure reference',28,'Input, world storage, puzzle rules, memory bounds and return status.','VAMPIRE.RIL')
t+='VAMPIRE is a native DOS .COM program written in RILL. Its map, text and logic are compiled into the executable. The compiler, translator and assembler are build tools; they are not loaded to play the game. The program uses only the completed language and its ordinary portable services.\n\n'
t+='## Input and results\n\n| Item | Contract |\n|---|---|\n| No arguments | Read lines from DOS CON |\n| One argument | Read an unquoted current-directory 8.3 command file supplied through the portable PSP-backed argument services |\n| Command | At most 80 printable ASCII characters; tabs become spaces |\n| Parser | Uppercase three-character prefixes of first and last words; middle words ignored |\n| Line endings | CR/LF, CR, LF, final unterminated line; Control-Z ends text |\n| Overlong or invalid record | Drain to its end, print the input diagnostic, spend no turn |\n| EOF or QUIT | Return normally; no position is written |\n| Exit zero | Ordinary play, including victory and death |\n| Exit one | Argument, file or checked service failure |\n\n'
t+='The input handle is closed on normal return and on a detected read failure. Output errors terminate with failure. No output file or recovery file is created. Keyboard echo comes from DOS; command files are echoed by the game. Follow-up answers use the same input stream and have no separate clock tick.\n\n'
t+='## World representation\n\nThere are nineteen rooms numbered 1–19 and twenty-five objects numbered 1–25. Six exit bytes per room represent North, South, East, West, Up and Down. Zero means no exit. Object locations are zero for carried, 1–19 for a room, and 99 for absent or consumed. Names are ordinary pointers stored with load16/store16; these tables are private program data, not a new language feature. Room zero and object zero are reserved.\n\n'
t+='Mutable flags record extinguished fire, tied rope, stakes, loose nails, open door and open coffin. The boat shore is eleven or sixteen. A replay calls both world and items, restoring all names and map rows as well as flags and locations. Input stream state is preserved across replay.\n\n'
t+='## Memory and omissions\n\n'
t+=f'The accepted complete image is **{CASES[-1]["binary_bytes"]:,} bytes**, including generated code, literals, tables and shared runtime. The declared byte arrays total 328 bytes, and the game allocates no auxiliary blocks. It retains only the current command, not a whole command file. All code and ordinary data fit the existing 61,184-byte image profile; the upper 4 KiB remains the native stack reservation. RILL still reserves its standard sixty-four local words per procedure call.\n\n'
t+='There is no screen buffer, graphics renderer, sound, random movement, disk paging, saved-game format or external resource file. The torch is already lit, carrying capacity counts objects rather than weight, and oil quantities are not tracked. These choices keep the application small enough to type and understand. The BASIC terminal escape effects and external menu handoff are replaced by plain DOS text and return to DOS. Ordinary visibility checks apply consistently, and leaving the boat returns to its current shore.\n\n'
t+='The engine keeps processor registers, DOS function numbers and PSP offsets out of its RILL source. DOS-specific CON naming is confined to selecting its default input device. The same world and action routines do not depend on that name.\n'
write_page(C/'28-reference.md',t)

for name,text in FRAGMENTS.items():(W/name).write_bytes(text.replace('\n','\r\n').encode('ascii'))
(Q/'article-patches.json').write_text(json.dumps(patches,indent=2)+'\n')
(Q/'extra-files.json').write_text(json.dumps(list(FRAGMENTS),indent=2)+'\n')
print('Published optional adventure: cover, workbench, 26 constructions, play guide and reference')
