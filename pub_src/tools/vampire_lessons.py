"""Manuscript notes and reusable, authored adventure command files."""
LESSONS=[
('A castle beyond the compiler',
 'Print the adventure title and our first room using the completed RILL toolchain.',
 'I have spent so many evenings making programs that make other programs that I want to try something different. A castle, a locked coffin and a few troublesome objects will do. This is an optional excursion from the completed RILL workbench: an adventure adapted from the BASIC listing, with its nineteen rooms and midnight deadline.',
 'say walks a zero-terminated string one byte at a time. Its parameter is a byte address, not a BASIC string variable. putc writes each character; failed output terminates with status one. CR followed by LF starts a DOS display line. main supplies only the title and the Entrance Hall. Both strings remain part of the game.',
 'A missing backslash changes the displayed line ending. Keep the quotes and both escape sequences.'),
('Listening at the gate',
 'Read bounded command lines from the console or a PSP-selected command file.',
 'An adventure needs the player to answer back. The same file operations that read source text can open the DOS console device, CON. A command file gives us a way to repeat a walk through the castle without typing the walk again.',
 'startinput selects CON with no arguments, or arg(1) with exactly one. input is an owned readable handle. nextbyte returns a byte or the distinct word 65535 for end of input; it checks status before using the transfer count. readline retains at most eighty characters plus its terminating zero. It drains an overlong or nonprintable line before returning two, so its tail cannot become another command. A complete line returns one; end of input returns zero. CR/LF, bare CR and LF are accepted, as is a final line without a newline. Control-Z ends text input. Scripted commands are echoed; the DOS console supplies keyboard echo.',
 'An accidental zero in the input is rejected, not treated as a string terminator. Check length before storing the next byte.'),
('Three letters are enough',
 'Separate the first and last words, fold case, and recognize LOOK, HELP and QUIT.',
 'The BASIC adventure makes a useful bargain: the player can write a phrase, but only the first three letters of its first and last words matter. READ THE SIGN can therefore mean the same thing as READ SIGN.',
 'parse clears two four-byte buffers, retaining three uppercase letters or spaces and a terminating zero. words counts whole words, even when their spellings are longer. Middle words are deliberately ignored. wordis compares exactly three bytes, so its literal arguments are padded to three characters. main ignores whitespace-only input and recognizes QUIT before dispatching an action. act gives unknown actions a message; they never become a movement by accident. HELP describes the vocabulary currently accepted by the program.',
 'If a short direction or keyword fails, check its padding. The three-character token for LOOK is LOO, not the complete spelling.'),
('Four rooms and six directions',
 'Represent room names and exits as tables, then walk through the first four rooms.',
 'A room number is easier to move around than a whole description. I sketch four boxes on paper before entering their connections. The sketch catches a wrong east or west more quickly than staring at a long string of numbers.',
 'names holds word-sized pointers: room n uses bytes n*2 and n*2+1. paths holds six bytes per room, ordered North, South, East, West, Up, Down. Zero means no exit; actual rooms begin at one. room writes one complete row, and roomname reads its pointer. describe prints the current room and its nonzero exits. direction accepts full direction prefixes and one-letter commands. walk changes location only when the selected exit is nonzero. All table indices remain within the declared twenty room records.',
 'Check the six argument positions against the heading on your paper map. A room pointer is a word, so use store16 and load16.'),
('The upper castle',
 'Extend the map to the tower, chapel and fireplace rooms.',
 'The rooms above ground fit in the same table. No movement routine needs to know how many descriptions I have entered.',
 'world adds the remaining upper rooms and opens the Armory eastward to the Tower. The Lower Tower leads south to the Chapel; the Chapel stair returns up to the Armory. The Fireplace leads south into the Study. A stored exit is directional: entering a connection does not create its reverse. Some rooms have no ordinary incoming exit because their entrances are objects or concealed openings. Do not fill those empty cells merely to make the map look symmetrical.',
 'The tower should be east of the Armory, and its west exit should return there. Check the room number as well as the displayed name.'),
('A door behind the bookcase',
 'Add the underground map and reveal a hidden exit by pushing the library bookcase.',
 'A map need not show every way out at first. The Library has a bookcase, and moving it changes a connection rather than changing the rules for movement.',
 'world supplies the remaining eleven room rows. push recognizes the bookcase only in the Library and writes room nine into its Down exit. At this stopping point act obtains the bookcase number directly from the noun prefix; push already receives an object number. describe then shows Down, and walk uses the altered row without a special case. Repeating PUSH BOOKCASE writes the same destination and is harmless. The hidden corridor, laboratory and storeroom can now be explored, including the storeroom stair back to the Study.',
 'If Down appears in the wrong room, check the row calculation: the Library starts at 3*6, and Down adds five.'),
('Putting things in rooms',
 'List named objects separately from the room map.',
 'The first objects are ordinary possessions: a timepiece, scroll, rope, axe, hammer and oar. Their names stay fixed while their locations will change. I keep these facts in separate tables.',
 'things stores word pointers to object names; places stores one byte per object. A positive room number places an object there. Zero means carried, and 99 means absent from play. item writes the name and location together. Unintroduced object slots are explicitly set to 99, so they cannot appear in an inventory by accident. lookitems walks the object numbers in a stable order and prints those in the current room. nounid gives command prefixes the corresponding object number; zero means unrecognized.',
 'Do not confuse object numbers with room numbers. Both begin at one, but they index different tables.'),
('Picking up and putting down',
 'Move objects between a room and the player without copying their descriptions.',
 'GET and DROP are small changes to places. The name table does not move. That separation makes taking the scroll no more complicated than taking the timepiece.',
 'take checks that a noun was recognized, that the object is not already carried, and that it is actually in this room. Only then does it write zero into places. drop requires zero and writes the current room number. Both messages name the object through itemname. GET and TAKE use the same routine. Calls receive an object number before doing any work, keeping parsing separate from game rules. The bookcase command now obtains its number through nounid as well.',
 'If GET seems to work from another room, check the location comparison before the assignment. Never index places with an unrecognized zero noun.'),
('Furnishing the castle',
 'Enter all twenty-five objects and distinguish possessions from scenery.',
 'A boat, sign and fireplace are visible objects, but they do not belong in a pocket. Filling the tables makes the castle feel like a place rather than a corridor between compiler tests.',
 'items initializes every object name and location, including the absent key. nounid adds aliases such as HAM for Sledge Hammer and DOO for Rusty Door. Objects fifteen through twenty-three are fixed scenery; take refuses them. This contiguous range is a property of our table, not a rule built into RILL. Other objects remain movable unless a particular puzzle adds a condition. The unused zero slot is never visited. Names use pointers to terminated literal strings, with no private string allocator.',
 'The fire and brick fireplace have separate entries. FIRE and BRICK commands refer to the brick structure; the fire entry supplies its visible description.'),
('Seven things in a pocket',
 'Display the inventory and enforce a seven-object carrying limit.',
 'I could keep a separate count and adjust it after every action. Counting the zero locations is simpler, and it cannot drift out of step when a puzzle consumes an object.',
 'carried counts entries whose location is zero. inventory displays exactly those entries and prints Nothing when there are none. take checks the carrying limit after rejecting unknown, absent, fixed or already-carried objects. A rejected eighth possession changes no location. Dropping one frees a place immediately. The bound is deliberately a game rule: these tables themselves occupy very little memory. The inventory display is part of the adventure, not a temporary testing routine.',
 'A failed eighth GET must leave the object in its room. Make the check before writing zero.'),
('Reading the warnings',
 'Examine reachable objects, including the sign and parchment scroll.',
 'The entrance sign is a warning; the scroll is a hint. LOOK and READ can share the same inspection rules while ordinary LOOK still describes the room.',
 'inspect receives nounid and treats an empty noun as a room description. It rejects an unknown or unreachable object before examining its particular number. The sign can be read where it hangs. The scroll must be carried, so finding it and reading it are separate actions. All other accessible objects receive the ordinary nothing-special response. This ordering prevents a special description from disclosing an object from anywhere in the castle.',
 'READ THE SCROLL uses the last word. If the command is recognized but asks you to pick it up, inspect places[4], not the parser.'),
('Four hours until midnight',
 'Advance one minute per command, read the timepiece and end the game at midnight.',
 'A countdown makes a familiar room feel different. The clock advances when I decide what to do, not while I sit thinking at the keyboard.',
 'elapsed starts at zero, meaning 8:00 p.m. tick runs before each nonempty action except QUIT. At 240 it calls lose before the requested action can run. Blank lines and rejected input records cost nothing; an unknown but well-formed command costs a minute. clock prints two decimal digits each for hours and minutes. Reading the carried timepiece includes the minute spent on READ itself. finished records a terminal result while playing controls the command loop. No hardware timer or processor-specific operation is needed.',
 'If the display is a minute behind, check whether tick runs before act. Both input prompts belonging to one action must not receive separate ticks.'),
('A rope over the parapets',
 'Ask for a second object and tie the carried rope to the tower parapets.',
 'TIE ROPE is not quite a complete instruction. The question To what? lets the player finish it without turning the command parser into a grammar for every possible sentence.',
 'ask uses the same bounded reader and parser, returning whether a usable answer exists. The object number passed to tie is already in its private parameter, so parsing the answer cannot lose the original object. Tying requires the rope in inventory and the Tower as the current room. It removes the loose rope, sets rope_tied, and changes the parapets description. ROPE then names that fixed anchor for movement. Going over the parapets without the rope is fatal. The answer to the question costs no additional minute.',
 'Keep the tower-specific PARAPETS alias ahead of PARCHMENT. Both begin with PAR; the room supplies the distinction.'),
('A bucket of holywater',
 'Require a carried bucket when collecting holywater in the chapel.',
 'A location table tells us where the water is, but not whether we can carry it. The bucket is the extra condition for this particular GET.',
 'take calls water only after the ordinary visibility and capacity checks. water asks In what? and accepts the BUCKET prefix only when the bucket is carried. A failed answer leaves the holywater in the Chapel. The bucket and water retain separate object entries; taking the water occupies another carrying place. This simple representation avoids inventing a general container system for a single puzzle. The supply transcript gathers a bucket before visiting the Tower and carries an oar and hammer for its walk.',
 'The container answer is parsed into verb, since it is the first word of a new reply. Checking noun would inspect an empty last-word field.'),
('Putting out the fire',
 'Consume holywater in the study and make the fireplace safe to enter.',
 'Some actions change more than an object location. Dropping the water in the Study removes it from play, changes what the room contains and makes another entrance usable.',
 'drop handles the water-in-study case before the ordinary drop. It sets fire_out and replaces the fire description with Smoldering Ashes. The bucket stays carried. walk accepts GO FIRE only in the Study; the flag decides between entering the Fireplace room and a fatal burn. Water dropped elsewhere uses the ordinary floor location and can be collected again subject to its bucket rule. A flag expresses a persistent world fact that cannot be inferred from where the water happens to be.',
 'Do not merely set the water location to the Study: that would leave the object available for another use after it had extinguished the fire.'),
('Breaking through the bricks',
 'Use the carried hammer to open a passage from inside the fireplace.',
 'The entrance is safe now, but its back wall is still solid. HIT FIRE asks which tool is being used and changes the map only when the hammer is available.',
 'hit first checks that the target is reachable, with an explicit exception for the fireplace structure viewed from inside it. Its original object entry remains in the Study. ask obtains the tool prefix; HAMMER and SLEDGE name the carried hammer. Success writes room ten into the Fireplace north exit and updates both room and object descriptions. The normal direction code then reaches the Secret Passage. An unsuitable or absent tool produces Nothing happens and changes no exit.',
 'If the inner wall is reported absent, check the fireplace exception before the ordinary visibility rejection.'),
('A torch in the dark',
 'Hide room contents in unlit underground areas and make the carried torch reveal them.',
 'Knowing a room number is not the same as being able to see its contents. The torch gives the description routine a reason to leave some information out.',
 'dark is true in rooms ten through twelve and eighteen unless the torch is carried. describe still identifies the room but withholds objects and exits. inspect and object-changing actions also respect darkness. Movement, inventory and HELP remain available, allowing the player to retrace a known route. The torch found in the fireplace is already burning; this game has no separate lighting or fuel system. Dropping it removes the carried-light condition immediately.',
 'Test both sides of the condition in the same room. Merely seeing a torch on the floor does not mean places[12] is zero.'),
('Across the underground lake',
 'Enter the boat, row with the oar and keep track of its current shore.',
 'The Boat is a room while I am aboard and an object while I stand beside it. Its shore must agree with both representations.',
 'GO BOAT requires the boat object at the current location. rowboat requires room twelve and the carried oar. shore alternates between eleven and sixteen because their sum is twenty-seven. The action moves both player and boat to that shore, and updates the Boat south exit to the same destination. Thus leaving the boat without rowing returns to the correct bank. SWIM in the lake chamber is fatal; swimming elsewhere does not end the game. All travel still uses ordinary word values and table bytes.',
 'After crossing, test GO BOAT followed by SOUTH. A stale exit would return the player to the wrong bank.'),
('Making wooden stakes',
 'Chop the crate with the axe and preserve its identity while changing its use.',
 'The crate can become a weapon, but breaking it is a decision. Its object number stays ten, so the inventory and location rules need no new entry.',
 'hit adds the crate-and-axe case after the fireplace case. The axe must be carried and the crate reachable. stakes records the change, and the name pointer becomes Wooden Stakes. nounid now recognizes WOO and STA only after that change. The ordinary crate prefix still identifies the same object. Chopping twice cannot produce another set. GEAR.TXT is a copy of the established supply walk with a crate, axe and oil added; its object count remains within seven.',
 'Check both the flag and the name pointer. Renaming the crate alone must not make its other uses depend on the spelling of a message.'),
('Reaching the overhang',
 'Stand on an intact crate placed in the gallery to reach the overhang.',
 'A useful object need not be carried. The crate works as a step only when it is on the Gallery floor, and wooden stakes no longer make a suitable platform.',
 'walk recognizes OVERHANG in the Gallery after checking ordinary directions and the boat. It requires places[10] to be sixteen and stakes to be zero before moving to room fifteen. The Overhang down exit returns to the Gallery through the regular map. Neither entering nor leaving moves the crate. An unsuccessful climb changes no location. This is why the crate conversion is represented separately from its object number.',
 'A crate in inventory does not satisfy the floor-location test. Drop it before climbing, and compare against room sixteen rather than zero.'),
('Nails behind a tapestry',
 'Loosen the nails with the hammer and uncover an exit by taking the tapestry.',
 'The tapestry conceals a doorway, but pulling at it from the floor is not enough. Getting above it and removing the nails makes the two sides of the room agree.',
 'take gives Nails and Tapestry separate conditions. loosen requires the carried hammer, sets nails_loose and then allows the nails to enter inventory. Taking the tapestry requires that flag and writes the Gallery north exit to room seventeen. Capacity is checked before either change, so a full inventory cannot silently loosen nails or reveal a doorway. Dropping the nails does not attach them again. The shared gallery transcript leaves spare inventory space rather than treating the carrying limit as an exception.',
 'If the tapestry moves while still nailed, check that its conditional return precedes the ordinary places[obj]=0 assignment.'),
('The rat and the key',
 'Discover the hidden key and distract its guardian with cheese.',
 'A LOOK can change what is known. The key starts absent; examining the rat brings it into the room, where GET can find it.',
 'inspect reveals the key only when the rat itself is reachable. take refuses it while the rat is present unless the cheese is on that room floor. With cheese supplied, the rat and cheese leave play and the key becomes carried. The ordinary visibility and capacity checks still happen first. Already-carried objects retain their usual response. The longer KEY.TXT walk collects cheese before entering the passage, then reuses the established gallery actions to reach the Antechamber with the key.',
 'The cheese must be dropped, not merely carried. Inspecting a rat elsewhere must not reveal the key in the player\'s current room.'),
('Oil on the rusty hinges',
 'Open the antechamber door with the carried flask of oil.',
 'The door has a place and a name like other scenery, but its passage is another table entry. The oil changes all three facts consistently.',
 'oil requires the door noun, the Antechamber and the carried flask. It sets door_open, changes the visible name and installs the north exit to the Tomb. It does not consume the flask; this game does not measure remaining quantities of oil. Repeating the action is harmless. Wrong locations and missing oil leave the map untouched. The KEY.TXT route provides the carried oil without requiring a special command-line setup or a hidden test mode.',
 'Use paths[17*6] for North. Changing the door description without changing that byte would leave an apparently open but impassable door.'),
('The locked coffin',
 'Use the carried key to open the coffin and reveal Dracula.',
 'An open door is not an open coffin. The final room has its own condition, and opening it should not work from the other end of the castle.',
 'openobject first requires the target in the current room. A rusty door reports its open or rusted condition. The coffin requires the carried key before setting coffin_open and replacing its description with Dracula in the Coffin. A key merely dropped beside the coffin is insufficient. COFFIN and DRACULA refer to the same fixed object number; its changing description never alters that identity. The existing darkness gate requires the torch here too.',
 'Check that key location is zero, not eighteen. Keep the reachability check ahead of the object-specific cases.'),
('Before he wakes',
 'Finish the adventure with carried wooden stakes, or suffer the result of a wrong weapon.',
 'The last action uses the same small pieces as the first: a recognized noun, a private parameter, an answer to a question and a few persistent facts about the world.',
 'kill requires the Tomb and an open coffin before asking With what? A stake prefix succeeds only when the crate has actually become stakes and object ten is carried. Victory prints its natural message and time, sets finished to two, and stops command processing. An unsuitable answer wakes Dracula and calls lose. EOF while answering stops input without pretending a weapon was supplied. The winning transcript exercises the complete map and puzzle chain with the same public commands as keyboard play.',
 'Seeing Wooden Stakes in an earlier inventory is not enough if they were dropped. Check their current location at the point of the attack.'),
('Another visit to the castle',
 'Offer a replay after victory or death and reset the entire mutable world.',
 'I finally have a program worth handing to someone who has never read an assembler listing. Before doing that, I try playing twice. A bookcase that stays open between games is a surprisingly easy mistake to leave behind.',
 'main adds an outer replay loop around the existing command loop. newgame restores every flag, counter, room row, object name and object location. replay accepts Y or YES after a terminal result; an ordinary QUIT does not ask again. The command input remains open, allowing a script to include both games. Its input position, end marker and CR/LF state belong to the input stream and must not be reset with the castle. EOF never starts another game. Preserve V26.RIL as VAMPIRE.RIL and its accepted executable as VAMPIRE.COM.',
 'Test a second game after changing a passage or object, not just after quitting at the entrance. A reset must rebuild names and exits as well as numeric flags.'),
]

RECIPES={}
def recipe(name,stage,text='',base=None):
    RECIPES[name]=dict(stage=stage,text=text.strip('\n')+'\n' if text else '',base=base)
    return name
def expand(name):
    r=RECIPES[name]
    return (expand(r['base']) if r['base'] else '')+r['text']

recipe('ROPE.TXT',13,'E\nPUSH BOOKCASE\nD\nGET ROPE\nU\nE\nE')
recipe('CHAPEL.TXT',13,'TIE ROPE\nPARAPETS\nGO ROPE\nS','ROPE.TXT')
recipe('SUPPLY.TXT',14,'''E
PUSH BOOKCASE
D
GET ROPE
N
N
GET BUCKET
U
E
E
E
E
GET HAMMER
TIE ROPE
PARAPETS
GO ROPE
GET OAR
S
GET WATER
BUCKET
U
W
W
W''')
recipe('DARK.TXT',16,'DROP WATER\nDROP BUCKET\nGO FIRE\nHIT FIRE\nHAMMER\nN','SUPPLY.TXT')
recipe('LIGHT.TXT',17,'S\nGET TORCH\nN','DARK.TXT')
recipe('LAKE.TXT',18,'N','LIGHT.TXT')
recipe('GEAR.TXT',19,'''E
PUSH BOOKCASE
D
GET ROPE
N
GET OIL
N
GET BUCKET
GET CRATE
U
E
E
E
GET AXE
E
GET HAMMER
TIE ROPE
PARAPETS
GO ROPE
GET OAR
S
GET WATER
BUCKET
U
W
W
W''')
recipe('EQUIP.TXT',20,'DROP WATER\nDROP BUCKET\nGO FIRE\nGET TORCH\nHIT FIRE\nHAMMER\nN\nN\nGO BOAT\nROW','GEAR.TXT')
GALLERY='DROP CRATE\nGO OVERHANG\nGET NAILS\nDROP NAILS\nD\nGET TAPESTRY\nDROP TAPESTRY\nGET CRATE\nHIT CRATE\nAXE\nDROP AXE\nN'
recipe('GATE.TXT',21,GALLERY,'EQUIP.TXT')
recipe('KEYBASE.TXT',22,'DROP WATER\nDROP BUCKET\nGET CHEESE\nGO FIRE\nGET TORCH\nHIT FIRE\nHAMMER\nN\nW\nLOOK RAT\nDROP OAR\nGET KEY\nGET OAR\nDROP CHEESE\nGET KEY\nE\nN\nGO BOAT\nROW','GEAR.TXT')
recipe('KEY.TXT',22,GALLERY,'KEYBASE.TXT')
recipe('TOMB.TXT',23,'OIL DOOR\nN','KEY.TXT')
recipe('COFFIN.TXT',24,'OPEN COFFIN','TOMB.TXT')
recipe('WIN.TXT',25,'KILL DRACULA\nSTAKES','COFFIN.TXT')

# A public command script and a focused alternate input per checkpoint.
TESTS=[
('',None,['Vampire Castle Adventure','You are in the Entrance Hall.'],None,None,[]),
('hello\nsecond entry',None,['hello','second entry','End of commands.'],'X'*81+'\nlook',None,['Use at most 80 printable characters.','look']),
('  lOoK   around\nhelp\ndance\nquit',None,['Use the first and last words','I don\'t know how to do that.','Goodbye.'],'\t\nLOO longer words\nquit',None,['You are in the Entrance Hall.','Goodbye.']),
('E\nW\nN\nGET NORTH',None,['You are in the Library.','You cannot go that way.','I don\'t know how to do that.'],'GO UP',None,['You cannot go that way.']),
('E\nE\nE\nW',None,['You are in the Tower.','You are in the Armory.'],'E\nE\nE\nE',None,['You cannot go that way.']),
('E\nPUSH BOOKCASE\nD\nN\nN\nU',None,['A doorway opens behind the bookcase.','You are in the Hidden Corridor.','You are in the Storeroom.','You are in the Study.'],'PUSH BOOKCASE\nD',None,['Nothing happens.','You cannot go that way.']),
('LOOK\nE\nLOOK',None,['  Timepiece','  Parchment Scroll'],'W\nLOOK',None,['You are in the Study.','  Nothing interesting.']),
('GET TIME\nGET TIME\nDROP TIME\nGET SCROLL',None,['Taken: Timepiece.','You already have it.','Dropped: Timepiece.','You cannot see it here.'],'GET DRAGON\nDROP AXE',None,['I don\'t know that object.','You do not have it.']),
('LOOK\nW\nLOOK',None,['  Sign','  Fire in the Fireplace','  Cheddar Cheese'],'GET SIGN\nE\nGET BOOKCASE',None,['You cannot take that.']),
('GET TIME\nW\nGET WINE\nGET CHEESE\nE\nE\nGET SCROLL\nPUSH BOOKCASE\nD\nGET ROPE\nN\nGET OIL\nN\nGET BUCKET\nGET CRATE\nDROP BUCKET\nGET CRATE\nINVENTORY',None,['You cannot carry any more.','Dropped: Bucket.','Taken: Crate.','You are carrying:'],'INVENTORY',None,['  Nothing.']),
('READ THE SIGN\nE\nREAD SCROLL\nGET SCROLL\nREAD THE SCROLL',None,['Dracula wakes at midnight.','Pick up the scroll to read it.','Not all exits are obvious.'],'READ AXE',None,['You cannot see it here.']),
('GET TIME\nREAD TIME\nWAIT\nREAD TIME',None,['Time: 08:02 p.m.','Time: 08:04 p.m.'],'WAIT\n'*240,None,['It is midnight. Dracula wakes and finds you.']),
('', 'CHAPEL.TXT',['The rope is tied to the parapets.','You climb down the rope.','You are in the Chapel.'],'E\nE\nE\nGO PARAPETS',None,['You fall from the parapets.']),
('INVENTORY','SUPPLY.TXT',['Taken: Holywater.','  Holywater'],'GET WATER\nBUCKET','CHAPEL.TXT',['You need to carry the bucket.']),
('DROP WATER\nGO FIRE','SUPPLY.TXT',['The holywater puts out the fire.','You are in the Brick Fireplace.'],'W\nGO FIRE',None,['The fire burns you to death.']),
('', 'DARK.TXT',['The bricks break away. A passage leads north.','You are in the Secret Passage.'],'DROP WATER\nGO FIRE\nHIT FIRE\nAXE\nN','SUPPLY.TXT',['Nothing happens.','You cannot go that way.']),
('', 'LIGHT.TXT',['It is dark. You cannot see.','Taken: Torch.','You are in the Secret Passage.'],'DROP TORCH\nLOOK\nGET TORCH','LIGHT.TXT',['It is too dark to do that.']),
('GO BOAT\nROW\nGO BOAT\nS\nGO BOAT\nROW','LAKE.TXT',['You are in the Gallery.','You row across the lake.','You are in the Underground Lake Chamber.'],'SWIM','LAKE.TXT',['The ice-cold lake pulls you under.']),
('HIT CRATE\nAXE\nINVENTORY','GEAR.TXT',['The crate splits into wooden stakes.','  Wooden Stakes'],'HIT CRATE\nHAMMER','GEAR.TXT',['Nothing happens.']),
('GO OVERHANG\nDROP CRATE\nGO OVERHANG\nD','EQUIP.TXT',['The overhang is too high.','You are in the Overhang.','You are in the Gallery.'],'DROP CRATE\nHIT CRATE\nAXE\nGO OVERHANG','EQUIP.TXT',['The overhang is too high.']),
('', 'GATE.TXT',['The tapestry comes loose.','A hole opens behind the tapestry.','You are in the Antechamber.'],'DROP CRATE\nDROP HAMMER\nGO OVERHANG\nGET NAILS\nD\nGET TAPESTRY','EQUIP.TXT',['You need the hammer.','It is nailed to the overhang.']),
('', 'KEY.TXT',["There is a key in the rat's mouth.",'The rat guards the key.','The rat runs off with the cheese.','Taken: Key.'],'LOOK RAT',None,['You cannot see it here.']),
('', 'TOMB.TXT',['The rusty door squeaks open.',"You are in the Dracula's Tomb."],'DROP OIL\nOIL DOOR\nN','GATE.TXT',['You cannot oil that here.','You cannot go that way.']),
('', 'COFFIN.TXT',['The lid opens. Dracula lies inside.'],'DROP KEY\nOPEN COFFIN','TOMB.TXT',['The coffin is locked.']),
('', 'WIN.TXT',['Congratulations! You have killed Dracula.'],'KILL DRACULA\nAXE','COFFIN.TXT',['Dracula wakes. You have failed.']),
('Y\nLOOK\nQUIT','WIN.TXT',['Play again (Y/N)?','Goodbye.'],'N','WIN.TXT',['Play again (Y/N)?']),
]

for n,(text,base,expected,bad,badbase,badexpected) in enumerate(TESTS,1):
    recipe(f'T{n:02}.TXT',n,text,base)
    if bad is not None:recipe(f'X{n:02}.TXT',n,bad,badbase)

def cases():
    return [dict(number=n,source=f'V{n:02}.RIL',title=lesson[0],why=lesson[1],
                 accept=f'T{n:02}.TXT',expected=TESTS[n-1][2],
                 alternate=f'X{n:02}.TXT' if TESTS[n-1][3] is not None else None,
                 alternate_expected=TESTS[n-1][5]) for n,lesson in enumerate(LESSONS,1)]
