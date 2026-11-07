+++
title = "More Local Storage"
weight = 46
description = "Give each function sixty-four local slots while keeping sixteen parameters."
download = "RC44.RIL"
download_group = "tools/rill"
reader_names = 1
+++

Begin after the first compiler self-build comparisons. Keep the matching RC43 compiler copies and RC43.RIL separately. R0 is still the tested sixteen-local compiler from that exercise. Copy RC43.RIL to RC44.RIL and make the four edits below, from the bottom upward. Everything else stays in place.

The final compiler accepts sixty-four simultaneously live local words and sixteen parameters per function. IR86 already accepts that frame. RILL0, RILLBOOT, and RC43 retain their sixteen-local bounds.

## The record and frame bounds

A name record occupies forty bytes. The 512 global/procedure records occupy bytes 0 through 20479. Eighty parameter/local records occupy bytes 20480 through 23679: sixteen parameter names plus sixty-four live local names. Allocate 23680 bytes and check that allocation before using the table. Record initialization and lexical restoration keep their earlier jobs.

PROC now reserves sixty-four local words for every compiled function, even a function using fewer. That is 128 bytes of local storage per active call, plus its parameters, return state and expression temporaries. The native stack guard still applies; this change does not promise a fixed recursion depth. Parameters retain their separate sixteen-word bound.

## Enter the source

### Edit 1

Unchanged source immediately before the edit:

```rill
    lex(); if !isword("MUT") { fail(2); } lex(); if tok != 1 { fail(2); }
    let mut old = find(20480,localcount);
    if old != 65535 { if reclevel == level { fail(4); } }
```

Remove this source at old physical positions 331–331 in RC43.RIL:

```rill
    if nextlocal >= 16 { fail(5); }
```

Replace it with:

```rill
    if nextlocal >= 64 { fail(5); }
```

The following old source remains in place:

```rill
    let mut slot = nextlocal;
    recval = slot; reclevel = level; let mut p = newlocal(8); nextlocal = nextlocal+1;
```

### Edit 2

Unchanged source immediately before the edit:

```rill
    }
    if oldargs != 65535 { if oldargs != argc { fail(4); } }
    set16(table,p+34,argc);
```

Remove this source at old physical positions 316–316 in RC43.RIL:

```rill
    outstr("PROC F_"); outname(p); outchar(32); outnum(argc); outstr(" 16\r\n");
```

Replace it with:

```rill
    outstr("PROC F_"); outname(p); outchar(32); outnum(argc); outstr(" 64\r\n");
```

The following old source remains in place:

```rill
    lex(); block(); outstr("LIT 0\r\nRETURN\r\n"); return 0;
}
```

### Edit 3

Unchanged source immediately before the edit:

```rill
    return record(p);
}
fn newlocal(kind) {
```

Remove this source at old physical positions 230–230 in RC43.RIL:

```rill
    if localcount >= 32 { fail(5); }
```

Replace it with:

```rill
    if localcount >= 80 { fail(5); }
```

The following old source remains in place:

```rill
    rectype = kind;
    let mut p = 20480+localcount*40; localcount = localcount+1;
```

### Edit 4

Unchanged source immediately before the edit:

```rill
    output = create("RILL.TMP");
    if status() != 0 { fail(1); }
    own = 1;
```

Remove this source at old physical positions 42–42 in RC43.RIL:

```rill
    table = alloc(22000);
```

Replace it with:

```rill
    table = alloc(23680);
```

The following old source remains in place:

```rill
    if status() != 0 { fail(5); }
    next(); lex();
```

## Build with the tested compiler

```dos
COPY RC44.RIL SOURCE.RIL
CHECK R0
COPY RESULT.IR SOURCE.IR
CHECK IWKEEP
COPY RESULT.ASM SOURCE.ASM
CHECK ASMAKEEP
COPY RESULT.COM RC44.COM
```

Require compiler `OK RESULT.IR 0000049992`, translator `OK RESULT.ASM 0000103091 text bytes`, assembler `OK RESULT.COM 26617 bytes`, and each PASS before the following copy. VIEW.BAS must show RC44.COM length 26617.

The preceding compiler built RC44.COM with sixteen-slot frames for its own functions. RC44 nevertheless emits sixty-four-slot frames. Let it compile its own source before establishing the new comparison baseline:

```dos
COPY RC44.RIL SOURCE.RIL
CHECK RC44
COPY RESULT.IR SOURCE.IR
CHECK IWKEEP
COPY RESULT.ASM SOURCE.ASM
CHECK ASMAKEEP
COPY RESULT.COM R0.COM
COPY RC44.RIL RILL.RIL
```

Require compiler `OK RESULT.IR 0000049992`, translator `OK RESULT.ASM 0000103091 text bytes`, assembler `OK RESULT.COM 26617 bytes`, and each PASS before copying. R0 is now the final compiler, with sixty-four-slot frames both in its own implementation and in its generated programs. Its length is 26617 bytes.

Compile RILL.RIL with this R0 through IWKEEP and ASMAKEEP, saving the accepted executable as R1.COM. Repeat with R1, saving R2.COM. Require each fresh OK and PASS. Then compare:

```dos
ECHO N>NO.TXT
COMP R0.COM R1.COM <NO.TXT
COMP R0.COM R2.COM <NO.TXT
```

Both comparisons must report no differences. These are the compiler copies carried into the toolchain collection.

## Fill the local and parameter regions

Create TLOCAL.RIL:

```rill
fn check(a0,a1,a2,a3,a4,a5,a6,a7,a8,a9,a10,a11,a12,a13,a14,a15){
let mut v0=0;let mut v1=1;let mut v2=2;let mut v3=3;let mut v4=4;let mut v5=5;let mut v6=6;let mut v7=7;
let mut v8=8;let mut v9=9;let mut v10=10;let mut v11=11;let mut v12=12;let mut v13=13;let mut v14=14;let mut v15=15;
let mut v16=16;let mut v17=17;let mut v18=18;let mut v19=19;let mut v20=20;let mut v21=21;let mut v22=22;let mut v23=23;
let mut v24=24;let mut v25=25;let mut v26=26;let mut v27=27;let mut v28=28;let mut v29=29;let mut v30=30;let mut v31=31;
let mut v32=32;let mut v33=33;let mut v34=34;let mut v35=35;let mut v36=36;let mut v37=37;let mut v38=38;let mut v39=39;
let mut v40=40;let mut v41=41;let mut v42=42;let mut v43=43;let mut v44=44;let mut v45=45;let mut v46=46;let mut v47=47;
let mut v48=48;let mut v49=49;let mut v50=50;let mut v51=51;let mut v52=52;let mut v53=53;let mut v54=54;let mut v55=55;
let mut v56=56;let mut v57=57;let mut v58=58;let mut v59=59;let mut v60=60;let mut v61=61;let mut v62=62;let mut v63=63;
if (v0!=0) | (v1!=1) | (v2!=2) | (v3!=3) | (v4!=4) | (v5!=5) | (v6!=6) | (v7!=7) {return 1;}
if (v8!=8) | (v9!=9) | (v10!=10) | (v11!=11) | (v12!=12) | (v13!=13) | (v14!=14) | (v15!=15) {return 1;}
if (v16!=16) | (v17!=17) | (v18!=18) | (v19!=19) | (v20!=20) | (v21!=21) | (v22!=22) | (v23!=23) {return 1;}
if (v24!=24) | (v25!=25) | (v26!=26) | (v27!=27) | (v28!=28) | (v29!=29) | (v30!=30) | (v31!=31) {return 1;}
if (v32!=32) | (v33!=33) | (v34!=34) | (v35!=35) | (v36!=36) | (v37!=37) | (v38!=38) | (v39!=39) {return 1;}
if (v40!=40) | (v41!=41) | (v42!=42) | (v43!=43) | (v44!=44) | (v45!=45) | (v46!=46) | (v47!=47) {return 1;}
if (v48!=48) | (v49!=49) | (v50!=50) | (v51!=51) | (v52!=52) | (v53!=53) | (v54!=54) | (v55!=55) {return 1;}
if (v56!=56) | (v57!=57) | (v58!=58) | (v59!=59) | (v60!=60) | (v61!=61) | (v62!=62) | (v63!=63) {return 1;}
return (a0!=0)|(a15!=15);
}
fn main(){return check(0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15);}
```

```dos
COPY TLOCAL.RIL SOURCE.RIL
CHECK R0
COPY RESULT.IR SOURCE.IR
CHECK IWKEEP
COPY RESULT.ASM SOURCE.ASM
CHECK ASMAKEEP
COPY RESULT.COM TRY.COM
CHECK TRY
```

Require compiler `OK RESULT.IR 0000005625`, translator `OK RESULT.ASM 0000015732 text bytes`, and assembler `OK RESULT.COM 03098 bytes`, with PASS before each following copy. TRY must return zero and report PASS; it needs no display routine. VIEW.BAS must show 3098 bytes and these first thirty-two bytes:

```text
FC 81 FC FE FF 74 03 E9 C7 0B E8 1F 08 B4 4C CD 21 55 8B EC 81 EC 80 00 81 FC 00 F0 73 03 E9 B0
```

## Reject one more live local

Copy TLOCAL.RIL to XLOCAL.RIL. Just before `return (a0!=0)|(a15!=15);`, insert:

```rill
let mut extra=0;
```

```dos
COPY XLOCAL.RIL SOURCE.RIL
CHECK R0
```

Require `ERROR 0000000018 CODE 00005` and FAIL. The accepted RESULT.IR must remain unchanged; keep a copy for comparison before this check.

## Reuse slots at a closing brace

Create TSCOPE.RIL using the following skeleton. At each comment, copy the eight declaration lines for v0 through v63 from TLOCAL.RIL; the comments are placement markers. There are two sibling scopes, each filling all sixty-four slots.

```rill
let mut result=0;
fn reuse(){
{
// Copy the eight declaration lines here.
v63=17;result=result+v63;
}
{
// Copy the same eight declaration lines here.
v63=29;result=result+v63;
}
return 0;
}
fn main(){
let mut v63=7;
{let mut v63=9;if v63!=9{return 1;}}
reuse();
return (result!=46)|(v63!=7);
}
```

The complete disk source has the declarations in place. It checks both slot reuse between sibling scopes and restoration of an outer binding after a shadowing block.

```dos
COPY TSCOPE.RIL SOURCE.RIL
CHECK R0
COPY RESULT.IR SOURCE.IR
CHECK IWKEEP
COPY RESULT.ASM SOURCE.ASM
CHECK ASMAKEEP
COPY RESULT.COM TRY.COM
CHECK TRY
```

Require compiler `OK RESULT.IR 0000004080`, translator `OK RESULT.ASM 0000010171 text bytes`, and assembler `OK RESULT.COM 02133 bytes`, with PASS before each following copy. TRY must return zero and report PASS; it needs no display routine. VIEW.BAS must show 2133 bytes and these first thirty-two bytes:

```text
FC 81 FC FE FF 74 03 E9 02 08 E8 5A 04 B4 4C CD 21 00 00 55 8B EC 81 EC 80 00 81 FC 00 F0 73 03
```

Keep the sixteen-parameter limit. A procedure with seventeen parameters is still rejected with capacity code five. The following toolchain construction uses this completed RILL.RIL and the matching R0/R1/R2 copies.
