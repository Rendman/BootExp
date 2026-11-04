+++
title = "30 · An assembler makes its own copy"
weight = 30
description = "Build two generations and compare every byte against the BASIC-produced starting tool."
download = "ASM86.ASM"
+++

We have a native assembler whose source uses the same instruction forms it accepts. That fact makes a stronger test possible than assembling a handful of small examples: let it assemble the complete source, then repeat the job with the newly built program.

There is no source addition in this installment. `ASM86.ASM` is exactly the saved `AS29.ASM`. The spelling, record order, fixed instruction lengths, and 0100H origin must produce the same bytes regardless of which implementation reads them.

## Keep the BASIC-built copy

At DOS:

```dos
COPY AS29.ASM ASM86.ASM
GWBASIC BAWIDE.BAS
```

Enter `ASM86`. Require `OK ASM86.COM 2622 bytes`, allowing BASIC's extra numeric spaces. Return with `SYSTEM`, then preserve the result:

```dos
COPY ASM86.COM ASMKEEP.COM
COPY ASM86.ASM SELF.ASM
CHECK ASMKEEP
```

At `Source name:` enter `SELF`. Require:

```text
Source name: SELF
OK 02622 bytes
PASS
```

SELF.COM came from running the assembler built by BASIC. The original is still safe as ASMKEEP.COM.

## Compare the complete files

Use DOS's COMP utility from the DOS disk or command path:

```dos
COMP ASMKEEP.COM SELF.COM
```

Require `Files compare ok` with no differing-byte reports. In the DOS 3.10 utility, `Eof mark not found` may also appear for these binary files: they are not text files ending in Ctrl-Z. The comparison must still report that the files compare. Answer `N` to `Compare more files (Y/N)?`. Wording and capital letters may vary with the DOS distribution. Equal lengths alone are not enough; COMP must compare the contents.

Now let the copy do the work:

```dos
COPY ASM86.ASM AGAIN.ASM
CHECK SELF
```

Enter `AGAIN`. Require `OK 02622 bytes` and PASS. Compare the second generation:

```dos
COMP SELF.COM AGAIN.COM
```

Again require the matching-files report, no differing bytes, and answer N. Both generated files must be exactly 2,622 bytes. A failed assembly is not a new generation, even if an older file with the requested name remains on disk.

## Check a failure through the native copy

Save this as BAD.ASM:

```asm
MOV AX,AL
```

Run `CHECK SELF`, enter `BAD`, and require `ERROR 00001 CODE 1` followed by FAIL. Byte and word registers cannot be mixed. An unexpected PASS is a failed test; do not run BAD.COM.

If a comparison differs, first check that SELF.ASM and AGAIN.ASM were plain copies of the exact source assembled by BASIC. Then compare the instruction and register tables, label storage, and pass resets. Do not copy a mismatching executable over the known working tool.

The result establishes agreement between the BASIC assembler and two native generations on this complete source. It does not establish support for instructions absent from the reference or prove that every possible input is correct. Keep ASMKEEP.COM, BOOTKEEP.BAS, BAWIDE.BAS, and the sources together; a useful bootstrap retains the means to recover its tools.
