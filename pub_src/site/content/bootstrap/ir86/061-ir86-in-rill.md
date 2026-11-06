+++
title = "IR86 in RILL"
weight = 61
description = "The same virtual-machine operations, with a RILL parser and a separate native binding."
download = "IR86.RIL"
download_group = "toolchain"
+++

The same virtual-machine operations, with a RILL parser and a separate native binding.

The complete IR86.RIL below uses the ordinary RILL language and portable services. Build it with R0 or the preserved compiler seed, then IWKEEP and ASMAKEEP. Require a fresh OK and PASS at each boundary before copying the next result. Preserve the resulting executable as I0.COM; VIEW.BAS must show **31472 bytes**.

The scanner and statement decoder implement the IR contract. The operation records contain argument classes, stack effects, and authored assembly templates. The header and runtime procedures are the 8086/DOS binding. They are not physical-register operations in the language. The input line and ordinary token stay bounded; RESULT.ASM streams through its owned temporary file.

## Complete source, by routine

Start a plain text IR86.RIL. Enter the declarations, then append each complete procedure in the displayed order. These are parts of one complete tool; a copied fragment is not a standalone program. All prerequisites are supplied by the completed RILL workbench.

### Declarations

```rill
// Processor-neutral IR parsing; native assembly belongs to its selected backend.
let mut input = 0;
let mut output = 0;
let mut own = 0;
let mut backup = 0;
let mut inpos = 0;
let mut inlen = 0;
let mut outlen = 0;
let mut total = 0;
let mut totalhi = 0;
let mut line = 0;
let mut linehi = 0;
let mut ended = 0;
let mut skipline = 0;
let mut pos = 0;
let mut length = 0;
let mut toklen = 0;
let mut depth = 0;
let mut params = 0;
let mut locals = 0;
let mut strid = 0;
let mut num = 0;
let mut entries = 0;
let mut have_main = 0;
bytes decimal[10];
bytes inbuf[4096];
bytes outbuf[4096];
bytes source[1024];
bytes token[64];
bytes name[32];
bytes ops[2048];
```

### main

```rill
fn main() {
    initops();
    if exists("IRTX.TMP") != 0 { fail(8); }
    if exists("IRRES.BAK") != 0 { fail(8); }
    input = open("SOURCE.IR"); if status() { fail(6); }
    output = create("IRTX.TMP"); if status() { fail(6); } own = 1;
    header();
    while readline() { pos = 0; statement(); }
    if depth { fail(4); }
    if have_main == 0 { fail(3); }
    close(input); if status() { fail(6); }
    runtime(); flush(); close(output); if status() { fail(6); }
    let mut present=exists("RESULT.ASM");
    if status() { fail(6); }
    if present {
        rename("RESULT.ASM","IRRES.BAK"); if status() { fail(6); } backup = 1;
    }
    rename("IRTX.TMP","RESULT.ASM"); if status() { fail(6); } own = 0;
    if backup { delete("IRRES.BAK"); if status() { fail(6); } }
    print("OK RESULT.ASM ");
    print32(totalhi,total);
    print(" text bytes\r\n"); return 0;
}
```

### op

```rill
fn op(n,kind,delta,t) {
    let mut p = ops+entries*8;
    store16(p,n); store16(p+2,kind); store16(p+4,delta); store16(p+6,t);
    entries = entries+1; if entries > 256 { fail(5); } return 0;
}
```

### readbyte

```rill
fn readbyte() {
    if ended { return 65535; }
    if inpos == inlen {
        inlen = read(input,inbuf,4096); if status() { fail(6); } inpos = 0;
        if inlen == 0 { ended = 1; return 65535; }
    }
    let mut c = inbuf[inpos]; inpos = inpos+1;
    if c == 26 { ended = 1; return 65535; } return c;
}
```

### readline

```rill
fn readline() {
    let mut c = 0; length = 0;
    while 1 {
        c = readbyte();
        if c == 65535 { if length == 0 { return 0; } return endline(); }
        if c == 10 { if skipline { skipline = 0; } else { return endline(); } }
        else {
            skipline = 0;
            if c == 13 { skipline = 1; return endline(); }
            if c < 32 { if c != 9 { fail(1); } }
            if c >= 127 { fail(1); }
            if length == 1023 { fail(5); }
            source[length] = c; length = length+1;
        }
    }
}
```

### endline

```rill
fn endline() {
    source[length] = 0; line = line+1;
    if line == 0 { linehi = linehi+1; if linehi == 0 { fail(5); } } return 1;
}
```

### scan

```rill
fn scan() {
    toklen = 0;
    while source[pos] == 32 | source[pos] == 9 { pos = pos+1; }
    let mut c = source[pos];
    if c == 59 { token[0] = 0; return 0; }
    while c != 0 {
        if c == 32 { c = 0; }
        else { if c == 9 { c = 0; } else { if c == 59 { c = 0; } } }
        if c != 0 {
            if toklen == 63 { fail(1); }
            if c >= 97 { if c <= 122 { c = c-32; } }
            token[toklen] = c; toklen = toklen+1; pos = pos+1; c = source[pos];
        }
    }
    token[toklen] = 0; return 0;
}
```

### same

```rill
fn same(a,b) {
    let mut i = 0;
    while load8(a+i) == load8(b+i) { if load8(a+i) == 0 { return 1; } i = i+1; }
    return 0;
}
```

### namearg

```rill
fn namearg() {
    scan(); if toklen == 0 { fail(3); } if toklen > 29 { fail(3); }
    let mut i = 0; let mut c = token[0];
    if letter(c) == 0 { fail(3); }
    while i < toklen { c = token[i]; if letter(c) == 0 { if c < 48 { fail(3); } if c > 57 { fail(3); } } name[i] = c; i = i+1; }
    name[i] = 0; return 0;
}
```

### letter

```rill
fn letter(c) { if c == 95 { return 1; } if c < 65 { return 0; } if c > 90 { return 0; } return 1; }
```

### numarg

```rill
fn numarg() {
    scan(); num = 0;
    let mut i = 0; let mut radix = 10; let mut end = toklen; let mut d = 0;
    if end == 0 { fail(2); }
    if token[0] < 48 { fail(2); } if token[0] > 57 { fail(2); }
    if token[end-1] == 72 { radix = 16; end = end-1; if end == 0 { fail(2); } }
    while i < end {
        d = token[i]; if d >= 65 { d = d-55; } else { d = d-48; }
        if d >= radix { fail(2); }
        if num > (65535-d)/radix { fail(2); }
        num = num*radix+d; i = i+1;
    }
    return num;
}
```

### finish

```rill
fn finish() { scan(); if toklen { fail(1); } return 0; }
```

### statement

```rill
fn statement() {
    scan(); if toklen == 0 { return 0; }
    let mut i = 0; let mut p = 0; let mut kind = 0; let mut delta = 0; let mut t = 0;
    let mut found = 0;
    while i < entries {
        p = ops+i*8;
        if same(load16(p),token) { found = 1; i = entries; } else { i = i+1; }
    }
    if found == 0 { fail(1); }
    kind = load16(p+2); delta = load16(p+4); t = load16(p+6);
    if kind == 6 { stringout(); return 0; }
    if kind == 1 { numarg(); }
    if kind == 2 { namearg(); }
    if kind == 3 { namearg(); numarg(); }
    if kind == 4 {
        if depth { fail(4); }
        namearg(); numarg(); if num > 16 { fail(1); } params = num;
        numarg(); if num > 64 { fail(1); } locals = num; num = num*2;
    }
    if kind == 5 {
        namearg(); numarg(); if num > depth { fail(4); }
        depth = depth-num; num = num*2;
    }
    finish();
    if kind == 2 { if same(t,"U_@:\r\n") { if depth { fail(4); } } }
    if kind == 4 | same(t,"U_@:\r\n") { if same(name,"MAIN") { have_main = 1; } }
    if same(t,"MOV AX,[BP-#]\r\n") | same(t,"MOV [BP-#],AX\r\n") | same(t,"LEA AX,[BP-#]\r\n") {
        if num >= locals { fail(1); } num = (num+1)*2;
    }
    if same(t,"MOV AX,[BP+#]\r\n") | same(t,"MOV [BP+#],AX\r\n") | same(t,"LEA AX,[BP+#]\r\n") {
        if num >= params { fail(1); } num = (params-num)*2+2;
    }
    if delta == 1 { if depth == 256 { fail(5); } depth = depth+1; }
    if delta == 2 { if depth == 0 { fail(4); } depth = depth-1; if kind==2 { if depth { fail(4); } } }
    if delta == 3 { if depth < 2 { fail(4); } depth = depth-2; }
    if delta == 4 { if depth { fail(4); } }
    expand(t); return 0;
}
```

### expand

```rill
fn expand(t) {
    let mut c = 0;
    while 1 {
        c = load8(t); t = t+1; if c == 0 { return 0; }
        if c == 64 { outstr(name); }
        else {
            if c == 35 { outnum(num); }
            else { if c == 63 { outnum(strid); } else { outchar(c); } }
        }
    }
}
```

### stringout

```rill
fn stringout() {
    strid = strid+1; if strid == 0 { fail(5); }
    expand("MOV AX,S_?\r\nJMP I_?\r\nS_?:\r\nDB ");
    while source[pos] == 32 | source[pos] == 9 { pos = pos+1; }
    if source[pos] != 34 { fail(1); } pos = pos+1;
    let mut c = 0;
    while source[pos] != 34 {
        c = source[pos]; pos = pos+1; if c == 0 { fail(1); }
        if c == 92 {
            c = source[pos]; pos = pos+1;
            if c == 110 { c = 10; }
            else { if c == 114 { c = 13; }
            else { if c == 116 { c = 9; }
            else { if c == 48 { c = 0; }
            else { if c != 92 { if c != 34 { fail(1); } } } } } }
        }
        outnum(c); outstr("\r\nDB ");
    }
    pos = pos+1; finish(); expand("0\r\nI_?:\r\n"); return 0;
}
```

### outchar

```rill
fn outchar(c) {
    outbuf[outlen] = c; outlen = outlen+1; total = total+1;
    if total == 0 { totalhi = totalhi+1; if totalhi == 0 { fail(5); } }
    if outlen == 4096 { flush(); } return 0;
}
```

### flush

```rill
fn flush() {
    if outlen { let mut n = write(output,outbuf,outlen); if status() { fail(6); } if n != outlen { fail(6); } outlen = 0; } return 0;
}
```

### outstr

```rill
fn outstr(s) { while load8(s) { outchar(load8(s)); s = s+1; } return 0; }
```

### outnum

```rill
fn outnum(n) {
    let mut place = 10000; let mut c = 0;
    while place { c = 48; while n >= place { n = n-place; c = c+1; } outchar(c); place = place/10; } return 0;
}
```

### print

```rill
fn print(s) { while load8(s) { putc(load8(s)); s = s+1; } return 0; }
```

### printnum

```rill
fn printnum(n) {
    let mut place = 10000; let mut c = 0;
    while place { c = 48; while n >= place { n = n-place; c = c+1; } putc(c); place = place/10; } return 0;
}
```

### fail

```rill
fn fail(code) {
    if input { close(input); } if output { close(output); }
    let mut recovery = 0;
    if backup { rename("IRRES.BAK","RESULT.ASM"); if status() { recovery = 1; } }
    if recovery == 0 { if own { delete("IRTX.TMP"); if status() { recovery=1; } } }
    print("IR ERROR "); print32(linehi,line); print(" CODE "); printnum(code); print("\r\n"); if recovery { print("Recovery: inspect IRTX.TMP and IRRES.BAK\r\n"); } exit(1); return 0;
}

// Divide a pair of words by ten without requiring a wider machine value.
```

### print32

```rill
fn print32(hi,lo) {
    let mut i = 0; let mut qhi = 0; let mut rem = 0;
    let mut qlo = 0; let mut bit = 0;
    while i < 10 {
        qhi = hi/10; rem = hi%10; qlo = 0; bit = 32768;
        while bit {
            rem = rem*2; if lo & bit { rem = rem+1; }
            qlo = qlo*2;
            if rem >= 10 { rem = rem-10; qlo = qlo+1; }
            bit = bit>>1;
        }
        decimal[i] = rem+48; hi = qhi; lo = qlo; i = i+1;
    }
    while i { i = i-1; putc(decimal[i]); } return 0;
}
```

### initops

```rill
fn initops() {
    op("NOP",0,0,"NOP\r\n");
    op("HALT",0,4,"MOV AX,4C00H\r\nINT 21H\r\n");
    op("EXIT",0,4,"MOV AH,4CH\r\nINT 21H\r\n");
    op("LABEL",2,0,"U_@:\r\n");
    op("LIT",1,0,"MOV AX,#\r\n");
    op("ADDR",2,0,"MOV AX,U_@\r\n");
    op("WORD",3,4,"U_@:\r\nDW #\r\n");
    op("BYTE",3,4,"U_@:\r\nDB #\r\n");
    op("BUFFER",3,4,"U_@:\r\nRESB #\r\n");
    op("LD",2,0,"MOV AX,[U_@]\r\n");
    op("ST",2,0,"MOV [U_@],AX\r\n");
    op("LDB",2,0,"MOV AL,[U_@]\r\nMOV AH,0\r\n");
    op("STB",2,0,"MOV [U_@],AL\r\n");
    op("FETCH",0,0,"MOV BX,AX\r\nMOV AX,[BX]\r\n");
    op("FETCHB",0,0,"MOV BX,AX\r\nMOV AL,[BX]\r\nMOV AH,0\r\n");
    op("NEG",0,0,"NEG AX\r\n");
    op("NOT",0,0,"NOT AX\r\n");
    op("PUSH",0,1,"PUSH AX\r\n");
    op("POP",0,2,"POP AX\r\n");
    op("PUT",0,2,"POP BX\r\nMOV [BX],AX\r\n");
    op("PUTB",0,2,"POP BX\r\nMOV [BX],AL\r\n");
    op("ADD",0,2,"POP BX\r\nADD AX,BX\r\n");
    op("AND",0,2,"POP BX\r\nAND AX,BX\r\n");
    op("OR",0,2,"POP BX\r\nOR AX,BX\r\n");
    op("XOR",0,2,"POP BX\r\nXOR AX,BX\r\n");
    op("SUB",0,2,"POP BX\r\nSUB BX,AX\r\nMOV AX,BX\r\n");
    op("MUL",0,2,"POP BX\r\nMUL BX\r\n");
    op("DIV",0,2,"MOV BX,AX\r\nPOP AX\r\nCMP BX,0\r\nJE NEAR R_STACKFAIL\r\nXOR DX,DX\r\nDIV BX\r\n");
    op("MOD",0,2,"MOV BX,AX\r\nPOP AX\r\nCMP BX,0\r\nJE NEAR R_STACKFAIL\r\nXOR DX,DX\r\nDIV BX\r\nMOV AX,DX\r\n");
    op("SHL",0,2,"MOV CX,AX\r\nAND CX,15\r\nPOP AX\r\nSHL AX,CL\r\n");
    op("SHR",0,2,"MOV CX,AX\r\nAND CX,15\r\nPOP AX\r\nSHR AX,CL\r\n");
    op("EQ",2,2,"POP BX\r\nCMP BX,AX\r\nJNE $+5\r\nJMP U_@\r\n");
    op("CEQ",0,2,"POP BX\r\nCMP BX,AX\r\nMOV AX,0\r\nJNE $+3\r\nINC AX\r\n");
    op("NE",2,2,"POP BX\r\nCMP BX,AX\r\nJE $+5\r\nJMP U_@\r\n");
    op("CNE",0,2,"POP BX\r\nCMP BX,AX\r\nMOV AX,0\r\nJE $+3\r\nINC AX\r\n");
    op("ULT",2,2,"POP BX\r\nCMP BX,AX\r\nJAE $+5\r\nJMP U_@\r\n");
    op("CULT",0,2,"POP BX\r\nCMP BX,AX\r\nMOV AX,0\r\nJAE $+3\r\nINC AX\r\n");
    op("ULE",2,2,"POP BX\r\nCMP BX,AX\r\nJA $+5\r\nJMP U_@\r\n");
    op("CULE",0,2,"POP BX\r\nCMP BX,AX\r\nMOV AX,0\r\nJA $+3\r\nINC AX\r\n");
    op("UGT",2,2,"POP BX\r\nCMP BX,AX\r\nJBE $+5\r\nJMP U_@\r\n");
    op("CUGT",0,2,"POP BX\r\nCMP BX,AX\r\nMOV AX,0\r\nJBE $+3\r\nINC AX\r\n");
    op("UGE",2,2,"POP BX\r\nCMP BX,AX\r\nJB $+5\r\nJMP U_@\r\n");
    op("CUGE",0,2,"POP BX\r\nCMP BX,AX\r\nMOV AX,0\r\nJB $+3\r\nINC AX\r\n");
    op("SLT",2,2,"POP BX\r\nCMP BX,AX\r\nJGE $+5\r\nJMP U_@\r\n");
    op("CSLT",0,2,"POP BX\r\nCMP BX,AX\r\nMOV AX,0\r\nJGE $+3\r\nINC AX\r\n");
    op("SLE",2,2,"POP BX\r\nCMP BX,AX\r\nJG $+5\r\nJMP U_@\r\n");
    op("CSLE",0,2,"POP BX\r\nCMP BX,AX\r\nMOV AX,0\r\nJG $+3\r\nINC AX\r\n");
    op("SGT",2,2,"POP BX\r\nCMP BX,AX\r\nJLE $+5\r\nJMP U_@\r\n");
    op("CSGT",0,2,"POP BX\r\nCMP BX,AX\r\nMOV AX,0\r\nJLE $+3\r\nINC AX\r\n");
    op("SGE",2,2,"POP BX\r\nCMP BX,AX\r\nJL $+5\r\nJMP U_@\r\n");
    op("CSGE",0,2,"POP BX\r\nCMP BX,AX\r\nMOV AX,0\r\nJL $+3\r\nINC AX\r\n");
    op("JZ",2,4,"CMP AX,0\r\nJNE $+5\r\nJMP U_@\r\n");
    op("JNZ",2,4,"CMP AX,0\r\nJE $+5\r\nJMP U_@\r\n");
    op("JMP",2,4,"JMP U_@\r\n");
    op("CALL",2,0,"CALL U_@\r\n");
    op("RET",0,4,"RET\r\n");
    op("PROC",4,0,"U_@:\r\nPUSH BP\r\nMOV BP,SP\r\nSUB SP,#\r\nCMP SP,0F000H\r\nJB NEAR R_STACKFAIL\r\n");
    op("RETURN",0,4,"MOV SP,BP\r\nPOP BP\r\nRET\r\n");
    op("INVOKE",5,0,"CALL U_@\r\nADD SP,#\r\n");
    op("LOCAL",1,0,"MOV AX,[BP-#]\r\n");
    op("SETLOCAL",1,0,"MOV [BP-#],AX\r\n");
    op("LADDR",1,0,"LEA AX,[BP-#]\r\n");
    op("PARAM",1,0,"MOV AX,[BP+#]\r\n");
    op("SETPARAM",1,0,"MOV [BP+#],AX\r\n");
    op("PADDR",1,0,"LEA AX,[BP+#]\r\n");
    op("LITS",6,0,"");
    op("PUTC",0,0,"CALL R_PUTC\r\n");
    op("GETC",0,0,"CALL R_GETC\r\n");
    op("OPEN",0,0,"CALL R_OPEN\r\n");
    op("CREATE",0,0,"CALL R_CREATE\r\n");
    op("CLOSE",0,0,"CALL R_CLOSE\r\n");
    op("STATUS",0,0,"MOV AX,[R_STATUS]\r\n");
    op("READ",0,3,"POP DX\r\nPOP BX\r\nCALL R_READ\r\n");
    op("WRITE",0,3,"POP DX\r\nPOP BX\r\nCALL R_WRITE\r\n");
    op("DELETE",0,0,"CALL R_DELETE\r\n");
    op("EXISTS",0,0,"CALL R_EXISTS\r\n");
    op("ALLOC",0,0,"CALL R_ALLOC\r\n");
    op("FREEBLOCK",0,0,"CALL R_FREEBLOCK\r\n");
    op("RENAME",0,2,"POP DX\r\nCALL R_RENAME\r\n");
    op("GET8",0,2,"POP BX\r\nMOV CX,1\r\nCALL R_GETMEM\r\n");
    op("GET16",0,2,"POP BX\r\nMOV CX,2\r\nCALL R_GETMEM\r\n");
    op("SET8",0,3,"POP DX\r\nPOP BX\r\nMOV CX,1\r\nCALL R_SETMEM\r\n");
    op("SET16",0,3,"POP DX\r\nPOP BX\r\nMOV CX,2\r\nCALL R_SETMEM\r\n");
    return 0;
}
```

### header

```rill
fn header() { outstr("CLD\r\nCMP SP,0FFFEH\r\nJNE NEAR R_STACKFAIL\r\nCALL U_MAIN\r\nMOV AH,4CH\r\nINT 21H\r\n"); return 0; }
```

### runtime

```rill
fn runtime() {
    outstr("R_OK:\r\nMOV DX,0\r\nMOV [R_STATUS],DX\r\nRET\r\nR_ERROR:\r\nMOV DX,1\r\nMOV [R_STATUS],DX\r\nRET\r\nR_FAIL:\r\nMOV AX,0\r\nJMP R_ERROR\r\n\r\nR_PUTC:\r\nMOV [R_BYTE],AL\r\nMOV BX,1\r\nMOV CX,1\r\nMOV DX,R_BYTE\r\nMOV AH,40H\r\nINT 21H\r\nJAE NEAR R_PUTCOUNT\r\nJMP R_FAIL\r\nR_PUTC");
    outstr("OUNT:\r\nCMP AX,1\r\nJE NEAR R_PUTGOOD\r\nJMP R_ERROR\r\nR_PUTGOOD:\r\nJMP R_OK\r\n\r\nR_GETC:\r\nMOV BX,0\r\nMOV CX,1\r\nMOV DX,R_BYTE\r\nMOV AH,3FH\r\nINT 21H\r\nJAE NEAR R_GETCOUNT\r\nMOV AX,65535\r\nJMP R_ERROR\r\nR_GETCOUNT:\r\nCMP AX,0\r\nJNE NEAR R_GETBYTE\r\nMOV AX,6553");
    outstr("5\r\nJMP R_OK\r\nR_GETBYTE:\r\nMOV AL,[R_BYTE]\r\nMOV AH,0\r\nJMP R_OK\r\n\r\nR_OPEN:\r\nMOV DX,3D00H\r\nJMP R_FILE\r\n\r\nR_CREATE:\r\nMOV DX,3C00H\r\nJMP R_FILE\r\n\r\nR_FILE:\r\nMOV [R_MODE],DX\r\nMOV [R_NAME],AX\r\nCALL R_FREE\r\nCMP BX,0\r\nJNE NEAR R_HAVESLOT\r\nJMP R_FAIL\r\nR");
    outstr("_HAVESLOT:\r\nMOV DX,[R_NAME]\r\nMOV CX,0\r\nMOV AX,[R_MODE]\r\nINT 21H\r\nJAE NEAR R_FILEGOOD\r\nJMP R_FAIL\r\nR_FILEGOOD:\r\nINC AX\r\nMOV DX,[R_MODE]\r\nCMP DX,3C00H\r\nJNE NEAR R_READSLOT\r\nADD AX,8000H\r\nR_READSLOT:\r\nMOV BX,[R_SLOT]\r\nMOV [BX],AX\r\nMOV AX,[R_NU");
    outstr("MBER]\r\nJMP R_OK\r\nR_FREE:\r\nMOV BX,R_HANDLES\r\nMOV CX,1\r\nR_NEXTSLOT:\r\nMOV AX,[BX]\r\nCMP AX,0\r\nJE NEAR R_SLOTFOUND\r\nADD BX,2\r\nINC CX\r\nCMP CX,9\r\nJB NEAR R_NEXTSLOT\r\nMOV BX,0\r\nRET\r\nR_SLOTFOUND:\r\nMOV [R_SLOT],BX\r\nMOV [R_NUMBER],CX\r\nRET\r\n\r\nR_FIND:\r\n");
    outstr("CMP BX,1\r\nJB NEAR R_BADHANDLE\r\nCMP BX,8\r\nJA NEAR R_BADHANDLE\r\nDEC BX\r\nADD BX,BX\r\nADD BX,R_HANDLES\r\nMOV [R_SLOT],BX\r\nMOV BX,[BX]\r\nCMP BX,0\r\nJE NEAR R_BADHANDLE\r\nMOV AX,1\r\nCMP BX,8000H\r\nJB NEAR R_HANDLEKIND\r\nAND BX,7FFFH\r\nMOV AX,2\r\nR_HANDLEKI");
    outstr("ND:\r\nDEC BX\r\nRET\r\nR_BADHANDLE:\r\nMOV AX,0\r\nRET\r\n\r\nR_READ:\r\nMOV [R_COUNT],AX\r\nMOV [R_BUFFER],DX\r\nCALL R_FIND\r\nCMP AX,1\r\nJE NEAR R_READVALID\r\nJMP R_FAIL\r\nR_READVALID:\r\nMOV CX,[R_COUNT]\r\nCMP CX,0\r\nJNE NEAR R_READMORE\r\nMOV AX,0\r\nJMP R_OK\r\nR_READ");
    outstr("MORE:\r\nMOV DX,[R_BUFFER]\r\nMOV AH,3FH\r\nINT 21H\r\nJAE NEAR R_READGOOD\r\nJMP R_FAIL\r\nR_READGOOD:\r\nJMP R_OK\r\n\r\nR_WRITE:\r\nMOV [R_COUNT],AX\r\nMOV [R_BUFFER],DX\r\nCALL R_FIND\r\nCMP AX,2\r\nJE NEAR R_WRITEVALID\r\nJMP R_FAIL\r\nR_WRITEVALID:\r\nMOV CX,[R_COUNT]");
    outstr("\r\nCMP CX,0\r\nJNE NEAR R_WRITEMORE\r\nMOV AX,0\r\nJMP R_OK\r\nR_WRITEMORE:\r\nMOV DX,[R_BUFFER]\r\nMOV AH,40H\r\nINT 21H\r\nJAE NEAR R_WRITECOUNT\r\nJMP R_FAIL\r\nR_WRITECOUNT:\r\nMOV DX,[R_COUNT]\r\nCMP AX,DX\r\nJE NEAR R_WRITEGOOD\r\nJMP R_ERROR\r\nR_WRITEGOOD:\r\nJMP R");
    outstr("_OK\r\n\r\nR_CLOSE:\r\nMOV BX,AX\r\nCALL R_FIND\r\nCMP AX,0\r\nJNE NEAR R_CLOSEVALID\r\nJMP R_FAIL\r\nR_CLOSEVALID:\r\nMOV AH,3EH\r\nINT 21H\r\nJAE NEAR R_CLOSEGOOD\r\nJMP R_FAIL\r\nR_CLOSEGOOD:\r\nMOV BX,[R_SLOT]\r\nMOV AX,0\r\nMOV [BX],AX\r\nJMP R_OK\r\n\r\nR_STATUS:\r\nDW 0\r\n\r");
    outstr("\nR_BYTE:\r\nDB 0\r\n\r\nR_MODE:\r\nDW 0\r\nR_NAME:\r\nDW 0\r\nR_SLOT:\r\nDW 0\r\nR_NUMBER:\r\nDW 0\r\nR_HANDLES:\r\nDW 0,0,0,0,0,0,0,0\r\n\r\nR_COUNT:\r\nDW 0\r\nR_BUFFER:\r\nDW 0\r\n\r\n; Authored portable-services binding. No physical values escape this layer.\r\nR_DELETE:\r\nMOV");
    outstr(" DX,AX\r\nMOV AH,41H\r\nINT 21H\r\nJC NEAR R_DFAIL\r\nMOV AX,0\r\nJMP R_OK\r\nR_DFAIL:\r\nJMP R_FAIL\r\nR_RENAME:\r\nMOV DI,AX\r\nMOV AX,DS\r\nMOV ES,AX\r\nMOV AH,56H\r\nINT 21H\r\nJC NEAR R_DFAIL\r\nMOV AX,0\r\nJMP R_OK\r\nR_EXISTS:\r\nMOV DX,AX\r\nMOV AX,3D00H\r\nINT 21H\r\nJC NE");
    outstr("AR R_NOFILE\r\nMOV BX,AX\r\nMOV AH,3EH\r\nINT 21H\r\nJC NEAR R_DFAIL\r\nMOV AX,1\r\nJMP R_OK\r\nR_NOFILE:\r\nCMP AX,2\r\nJNE NEAR R_EFAIL\r\nMOV AX,0\r\nJMP R_OK\r\nR_EFAIL:\r\nMOV AX,65535\r\nJMP R_ERROR\r\nR_ALLOC:\r\nCMP AX,0\r\nJE NEAR R_DFAIL\r\nMOV [R_WANT],AX\r\nMOV AX,C");
    outstr("S\r\nMOV ES,AX\r\nMOV BX,1000H\r\nMOV AH,4AH\r\nINT 21H\r\nJC NEAR R_DFAIL\r\nMOV SI,R_BLOCKS\r\nMOV DI,1\r\nR_ALLOCSLOT:\r\nCMP WORD [SI],0\r\nJE NEAR R_ALLOCFOUND\r\nADD SI,4\r\nINC DI\r\nCMP DI,17\r\nJB NEAR R_ALLOCSLOT\r\nJMP R_FAIL\r\nR_ALLOCFOUND:\r\nMOV BX,[R_WANT]\r\n");
    outstr("MOV CL,4\r\nSHR BX,CL\r\nMOV AX,[R_WANT]\r\nAND AX,15\r\nCMP AX,0\r\nJE NEAR R_ALLOCROUND\r\nINC BX\r\nR_ALLOCROUND:\r\nMOV AH,48H\r\nINT 21H\r\nJC NEAR R_ALLOCBAD\r\nMOV [SI],AX\r\nMOV AX,[R_WANT]\r\nMOV [SI+2],AX\r\nMOV AX,DI\r\nJMP R_OK\r\nR_ALLOCBAD:\r\nMOV AX,CS\r\nMOV E");
    outstr("S,AX\r\nJMP R_FAIL\r\nR_BLOCKPTR:\r\nCMP BX,1\r\nJB NEAR R_BLOCKBAD\r\nCMP BX,16\r\nJA NEAR R_BLOCKBAD\r\nDEC BX\r\nSHL BX,1\r\nSHL BX,1\r\nADD BX,R_BLOCKS\r\nMOV SI,BX\r\nMOV BX,[SI]\r\nCMP BX,0\r\nJE NEAR R_BLOCKBAD\r\nMOV ES,BX\r\nMOV BX,[SI+2]\r\nCMP AX,BX\r\nJAE NEAR R_B");
    outstr("LOCKBAD\r\nSUB BX,AX\r\nCMP BX,CX\r\nJB NEAR R_BLOCKBAD\r\nMOV BX,AX\r\nMOV AX,1\r\nRET\r\nR_BLOCKBAD:\r\nMOV AX,CS\r\nMOV ES,AX\r\nMOV AX,0\r\nRET\r\nR_GETMEM:\r\nPUSH CX\r\nCALL R_BLOCKPTR\r\nPOP CX\r\nCMP AX,0\r\nJE NEAR R_DFAIL\r\nMOV AL,ES:[BX]\r\nMOV AH,0\r\nCMP CX,1\r\nJE NE");
    outstr("AR R_MEMDONE\r\nMOV AX,ES:[BX]\r\nR_MEMDONE:\r\nMOV DX,CS\r\nMOV ES,DX\r\nJMP R_OK\r\nR_SETMEM:\r\nMOV [R_MEMVALUE],AX\r\nMOV AX,DX\r\nCALL R_BLOCKPTR\r\nCMP AX,0\r\nJE NEAR R_DFAIL\r\nMOV AX,[R_MEMVALUE]\r\nCMP CX,1\r\nJNE NEAR R_SETWORD\r\nMOV ES:[BX],AL\r\nJMP R_MEMDON");
    outstr("E\r\nR_SETWORD:\r\nMOV ES:[BX],AX\r\nJMP R_MEMDONE\r\nR_FREEBLOCK:\r\nMOV BX,AX\r\nCMP BX,1\r\nJB NEAR R_DFAIL\r\nCMP BX,16\r\nJA NEAR R_DFAIL\r\nDEC BX\r\nSHL BX,1\r\nSHL BX,1\r\nADD BX,R_BLOCKS\r\nMOV SI,BX\r\nMOV AX,[SI]\r\nCMP AX,0\r\nJE NEAR R_DFAIL\r\nMOV ES,AX\r\nMOV AH,");
    outstr("49H\r\nINT 21H\r\nJC NEAR R_FREEBAD\r\nMOV WORD [SI],0\r\nMOV AX,CS\r\nMOV ES,AX\r\nMOV AX,0\r\nJMP R_OK\r\nR_FREEBAD:\r\nMOV AX,CS\r\nMOV ES,AX\r\nJMP R_FAIL\r\nR_STACKFAIL:\r\nMOV AX,4C02H\r\nINT 21H\r\nR_WANT:\r\nDW 0\r\nR_MEMVALUE:\r\nDW 0\r\nR_BLOCKS:\r\nRESW 32\r\n");
    return 0;
}
```

## Complete build

```dos
COPY IR86.RIL SOURCE.RIL
CHECK R0
COPY RESULT.IR SOURCE.IR
CHECK IWKEEP
COPY RESULT.ASM SOURCE.ASM
CHECK ASMAKEEP
COPY RESULT.COM I0.COM
```

Require each OK and PASS **before** the next copy. The complete source link is the same file assembled from the routine blocks above.

Test the fixed-file translator with this complete IR program:

```ir
PROC MAIN 0 0
LIT 65
PUTC
LIT 0
RETURN
```

Save it as TEST.IR. COPY TEST.IR SOURCE.IR and run CHECK I0. Require OK and PASS, copy RESULT.ASM to SOURCE.ASM, and run CHECK ASMAKEEP. Save the accepted RESULT.COM as TRY.COM; CHECK TRY displays A and reports PASS.

For rejection, replace its LIT 65 with LIT 65536. CHECK I0 must report `IR ERROR 0000000002 CODE 00002` and FAIL, preserving the accepted RESULT.ASM. An unexpected PASS fails this check.
