+++
title = "Counted file transfer"
weight = 56
description = "File handles carry access modes and remain opaque. Read returns actual progress, with zero for EOF. Check status and the exact write count before reusing the buffer. File data preserves every byte, including Control-Z."
download = "ECOPY.RIL"
download_group = "tools/rillboot"
aliases = ["/bootstrap/rill/088-counted-file-transfer/"]
reader_names = 1
+++

File handles carry access modes and remain opaque. Read returns actual progress, with zero for EOF. Check status and the exact write count before reusing the buffer. File data preserves every byte, including Control-Z.

Save ECOPY.RIL:

```rill
bytes block[256];
fn main() {
    let mut input=open("IN.TXT");
    if status() { return 1; }
    let mut output=create("OUT.TXT");
    if status() { close(input); return 1; }
    let mut n=read(input,block,256);
    while n {
        if status() { close(input); close(output); return 1; }
        let mut written=write(output,block,n);
        if status() | (written!=n) { close(input); close(output); return 1; }
        n=read(input,block,256);
    }
    if status() { close(input); close(output); return 1; }
    close(input); if status() { close(output); return 1; }
    close(output); if status() { return 1; }
    return 0;
}
```

```dos
COPY ECOPY.RIL SOURCE.RIL
CHECK RILLBOOT
COPY RESULT.IR SOURCE.IR
CHECK IWKEEP
COPY RESULT.ASM SOURCE.ASM
CHECK ASMAKEEP
```

Require `OK RESULT.IR 0000001476`, translator `OK RESULT.ASM 0000007577 text bytes`, and assembler `OK RESULT.COM 01765 bytes`, each with PASS **before** the following copy. VIEW.BAS must show result length 1765 and these first thirty-two bytes:

```text
FC 81 FC FE FF 74 03 E9 92 06 E8 BA 02 B4 4C CD 21 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
```

Copy RESULT.COM to ECOPY.COM. Create IN.TXT with `ECHO A short copy.>IN.TXT`. CHECK ECOPY reports PASS. COMP IN.TXT OUT.TXT must report no differences; answer N to its compare-more-files question. Empty and binary input are valid too. A missing IN.TXT must report FAIL before creating OUT.TXT. Here `\r\n` means carriage return and line feed.

For a separate source rejection, create BAD.RIL:

```rill
fn main(){return read(1,2);}
```

```dos
COPY BAD.RIL SOURCE.RIL
CHECK RILLBOOT
```

Require:

```text
ERROR 0000000001 CODE 00004
FAIL
```

The older RESULT.IR must remain unchanged. An unexpected PASS fails the rejection check. Restore the accepted source before another build.
