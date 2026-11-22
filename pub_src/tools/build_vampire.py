"""Arrange authored RILL text into continuing, optional adventure checkpoints."""
from pathlib import Path
import json,re

ROOT=Path(__file__).resolve().parents[1]
W=ROOT/'workbench/vampire';Q=ROOT/'qa/vampire'
AUTHORED=(ROOT/'tools/vampire.ril').read_text()
parts=re.split(r'(?=^fn \w+\()',AUTHORED,flags=re.M)
GLOBALS=parts[0].splitlines()[1:]
F={re.match(r'fn (\w+)',p)[1]:p.strip() for p in parts[1:]}

def omit(text,first,following):
    a=text.index(first);b=text.index(following,a)
    return text[:a]+text[b:]

def main(stage):
    if stage==1:
        return '''fn main(){
    say("Vampire Castle Adventure\\r\\n");
    say("You are in the Entrance Hall.\\r\\n");
    return 0;
}'''
    if stage==26:return F['main']
    body='''fn main(){
    say("Vampire Castle Adventure\\r\\n");
    startinput();
'''
    if stage>=4:body+='    newgame();describe();\n'
    else:body+='    say("You are in the Entrance Hall.\\r\\n");\n'
    body+='''    while playing{
        say("\\r\\n> ");
        let mut got=readline();
        if got==0{playing=0;}
'''
    if stage>=3:
        body+='''        if got==1{
            parse();
            if wordis(verb,"QUI"){say("Goodbye.\\r\\n");playing=0;}
            else{
                if words{
'''
        if stage>=12:body+='                    tick();if playing{act();}\n'
        else:body+='                    act();\n'
        body+='''                }
            }
        }
'''
    body+='''    }
    close(input);if status(){exit(1);}
    return 0;
}'''
    return body

def action(stage):
    if stage==26:return F['act']
    lines=['fn act(){','    if wordis(verb,"HEL"){help();return 0;}']
    if stage>=10:lines+=['    if wordis(verb,"INV"){inventory();return 0;}']
    if stage>=12:lines+=['    if wordis(verb,"WAI"){say("Time passes.\\r\\n");return 0;}']
    if stage>=18:
        lines+=['''    if wordis(verb,"SWI"){
        if location==11{lose("The ice-cold lake pulls you under.\\r\\n");}
        else{say("There is nowhere to swim here.\\r\\n");}
        return 0;
    }''']
    if stage>=4:
        lines+=['    if wordis(verb,"GO ")|wordis(verb,"CLI")|((words==1)&(direction()!=0)){walk();return 0;}']
    if stage>=11:
        lines+=['    if wordis(verb,"LOO")|wordis(verb,"REA"){inspect(nounid());return 0;}']
    elif stage>=4:lines+=['    if wordis(verb,"LOO"){describe();return 0;}']
    else:lines+=['    if wordis(verb,"LOO"){say("You are in the Entrance Hall.\\r\\n");return 0;}']
    if stage>=17:lines+=['    if dark(){say("It is too dark to do that.\\r\\n");return 0;}']
    if (stage>=6)&(stage<8):
        lines+=['''    if wordis(verb,"PUS"){
        let mut obj=0;if wordis(noun,"BOO"){obj=19;}
        push(obj);return 0;
    }''']
    if stage>=8:
        lines+=['    let mut obj=nounid();',
                '    if wordis(verb,"GET")|wordis(verb,"TAK"){take(obj);return 0;}',
                '    if wordis(verb,"DRO"){drop(obj);return 0;}']
    for start,line in [
        (16,'if wordis(verb,"HIT")|wordis(verb,"BRE"){hit(obj);return 0;}'),
        (13,'if wordis(verb,"TIE"){tie(obj);return 0;}'),
        (8,'if wordis(verb,"PUS"){push(obj);return 0;}'),
        (18,'if wordis(verb,"ROW"){rowboat();return 0;}'),
        (23,'if wordis(verb,"OIL"){oil(obj);return 0;}'),
        (24,'if wordis(verb,"OPE"){openobject(obj);return 0;}'),
        (25,'if wordis(verb,"KIL")|wordis(verb,"THR"){kill(obj);return 0;}')]:
        if stage>=start:
            if stage<8:raise AssertionError('Object lookup not installed')
            lines+=['    '+line]
    lines+=['    say("I don\'t know how to do that.\\r\\n");','    return 0;','}']
    return '\n'.join(lines)

def source(stage):
    first={
        1:['say'],2:['startinput','nextbyte','readline'],3:['parse','wordis','help','act'],
        4:['room','world','roomname','describe','dirname','direction','walk','newgame'],
        6:['push'],7:['item','itemname','items','lookitems','nounid'],8:['take','drop'],
        10:['carried','inventory'],11:['inspect'],12:['clock','tick','lose'],
        13:['ask','tie'],14:['water'],17:['dark'],16:['hit'],
        18:['rowboat'],21:['loosen'],23:['oil'],24:['openobject'],
        25:['kill'],26:['replay']}
    wanted={'main'}|{name for n,names in first.items() if n<=stage for name in names}
    f={name:F[name] for name in F if name in wanted}
    f['main']=main(stage)
    if stage>=3:
        f['act']=action(stage)
        if stage<26:
            commands='LOOK, HELP and QUIT.'
            if stage>=4:commands+=' GO NORTH or N; also S, E, W, U and D.'
            if stage>=8:commands+=' GET and DROP.'
            if stage>=10:commands+=' INVENTORY.'
            if stage>=11:commands+=' READ.'
            if stage>=6:commands+=' PUSH.'
            if stage>=12:commands+=' WAIT.'
            for n,word in [(16,'HIT'),(13,'TIE'),(18,'ROW and SWIM'),(23,'OIL'),(24,'OPEN'),(25,'KILL')]:
                if stage>=n:commands+=' '+word+'.'
            f['help']='fn help(){\n    say("Use the first and last words; only three letters count.\\r\\n");\n'
            for sentence in commands.split('. '):f['help']+='    say('+json.dumps(sentence+'\r\n')+');\n'
            f['help']+='    return 0;\n}'
    if stage>=4:
        if stage<6:
            rows=4 if stage==4 else 8
            f['world']='\n'.join(F['world'].splitlines()[:rows+1]+['    return 0;','}'])
            if stage==4:f['world']=f['world'].replace('"Armory",0,0,5,3','"Armory",0,0,0,3')
        if stage<7:f['describe']=F['describe'].replace('    lookitems();\n','')
        if stage<17:f['describe']=f['describe'].replace('    if dark(){say("It is dark. You cannot see.\\r\\n");return 0;}\n','')
        walk=F['walk'].split('    let mut obj=nounid();')[0]
        if stage>=13:walk+='    let mut obj=nounid();\n'
        for start,begin,end in [
            (15,'    if (obj==22)','    if (obj==21)'),
            (13,'    if (obj==21)','    if (obj==15)'),
            (18,'    if (obj==15)','    if (location==16)'),
            (20,'    if (location==16)','    say("You cannot go there.')]:
            if stage>=start:walk+=F['walk'][F['walk'].index(begin):F['walk'].index(end)]
        walk+=F['walk'][F['walk'].index('    say("You cannot go there.'):]
        f['walk']=walk
        resets=['location=1;playing=1;']
        for n,text in [(12,'elapsed=0;'),(12,'finished=0;'),(15,'fire_out=0;'),
                       (13,'rope_tied=0;'),(18,'shore=11;'),(19,'stakes=0;'),
                       (21,'nails_loose=0;'),(23,'door_open=0;'),(24,'coffin_open=0;')]:
            if stage>=n:resets.append(text)
        resets.append('world();')
        if stage>=7:resets.append('items();')
        f['newgame']='fn newgame(){\n    '+'\n    '.join(resets)+'\n    return 0;\n}'
        if stage==26:f['newgame']=F['newgame']
    if stage>=7:
        if stage<9:
            f['items']='''fn items(){
    let mut i=1;
    while i<=25{places[i]=99;i=i+1;}
    item(1,"Sledge Hammer",5);item(2,"Timepiece",1);
    item(3,"Coil of Rope",9);item(4,"Parchment Scroll",3);
    item(5,"Axe",4);item(6,"Oar",6);
    return 0;
}'''
        noun=F['nounid']
        if stage<13:noun=noun.replace('        if rope_tied{return 21;}return 3;','        return 3;')
        if stage<19:noun=omit(noun,'    if wordis(noun,"WOO")','    if wordis(noun,"BUC")')
        if stage<9:
            noun=omit(noun,'    if wordis(noun,"OAR")','    return 0;')
            noun=noun.replace('    return 0;','    if wordis(noun,"OAR"){return 6;}\n    if wordis(noun,"BOO"){return 19;}\n    return 0;')
        f['nounid']=noun
    if stage>=8:
        take=F['take']
        if stage<22:take=omit(take,'    if obj==7{','    places[obj]=0;')
        if stage<21:take=omit(take,'    if obj==13{','    places[obj]=0;')
        if stage<14:take=take.replace('    if obj==8{if water()==0{return 0;}}\n','')
        if stage<10:take=take.replace('    if carried()==7{say("You cannot carry any more.\\r\\n");return 0;}\n','')
        if stage<9:take=take.replace('    if (obj>=15)&(obj<=23){say("You cannot take that.\\r\\n");return 0;}\n','')
        f['take']=take
        if stage<15:f['drop']=omit(F['drop'],'    if (obj==8)','    places[obj]=location;')
    if stage>=11:
        if stage<17:f['inspect']=F['inspect'].replace('    if dark(){say("It is too dark to do that.\\r\\n");return 0;}\n','')
        if stage<12:f['inspect']=omit(f['inspect'],'    if obj==2{','    if obj==23{')
        if stage<22:f['inspect']=f['inspect'].replace('    if obj==23{places[7]=location;say("There is a key in the rat\'s mouth.\\r\\n");return 0;}\n','')
    if (stage>=16)&(stage<19):f['hit']=omit(F['hit'],'    if (obj==10)','    say("Nothing happens.')
    declarations={
        2:['input','ended','skip_lf','scripted','length','playing','command','octet'],
        3:['words','verb','noun'],4:['location','names','paths'],7:['things','places'],
        12:['elapsed','finished'],15:['fire_out'],13:['rope_tied'],18:['shore'],
        19:['stakes'],21:['nails_loose'],23:['door_open'],24:['coffin_open']}
    allowed={name for n,names in declarations.items() if n<=stage for name in names}
    globals_=[line for line in GLOBALS if line.strip() and re.match(r'(?:let mut|bytes) (\w+)',line)[1] in allowed]
    if stage==26:
        assert f==F,'The final checkpoint must retain the complete authored game'
    return '// Vampire Castle Adventure.\n'+'\n'.join(globals_)+'\n\n'+'\n\n'.join(f.values())+'\n'

def dos(path,text):path.write_bytes(text.replace('\r\n','\n').replace('\n','\r\n').encode('ascii'))

if __name__=='__main__':
    W.mkdir(parents=True,exist_ok=True);Q.mkdir(parents=True,exist_ok=True)
    for n in range(1,27):dos(W/f'V{n:02}.RIL',source(n))
    dos(W/'VAMPIRE.RIL',source(26))
    print('Arranged 26 continuing Vampire Castle Adventure sources')
