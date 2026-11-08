+++
title = "29 \u00b7 An assembler makes its own copy"
weight = 29
description = "Build two generations and compare every byte against the BASIC-produced starting tool."
download = "ASM0.ASM"
download_group = "tools/asm0"
reader_names = 1
url = "/bootstrap/asm86/30-self-assembly/"
+++

We have a native assembler whose source uses the language accepted by BOOTASM. Let it assemble that complete source, then repeat the job with its newly built copy.

There is no source addition here. ASM0.ASM is the saved AS28.ASM. Preserve that exact source for both native generations.

## Keep the BASIC-built copy

```dos
COPY AS28.ASM ASM0.ASM
COPY ASM0.ASM SOURCE.ASM
GWBASIC BOOTASM.BAS
```

Require `OK RESULT.COM 2431 bytes`, allowing BASIC's numeric spaces. Return to DOS with SYSTEM, then preserve the accepted executable:

```dos
COPY RESULT.COM ASMKEEP.COM
CHECK ASMKEEP
```

SOURCE.ASM still contains the exact assembler source. Require `OK 02431 bytes` and PASS before preserving the first native copy:

```dos
COPY RESULT.COM SELF.COM
ECHO N>NO.TXT
COMP ASMKEEP.COM SELF.COM <NO.TXT
```

COMP must report no differences. NO.TXT answers N if the DOS utility asks whether to compare more files. The native tool reads SOURCE.ASM and writes RESULT.COM without console input. Keep ASMKEEP.COM separately named so the output cannot overwrite the running builder.

## Let the copy do the same job

```dos
CHECK SELF
```

Require `OK 02431 bytes` and PASS, then preserve and compare the second generation:

```dos
COPY RESULT.COM AGAIN.COM
COMP SELF.COM AGAIN.COM <NO.TXT
```

Both generated files must be exactly 2,431 bytes and match every byte of the BASIC-built executable. A failed assembly is not a new generation, even if an older RESULT.COM remains on disk.

## Check a failure through the native copy

Save BAD.ASM:

```asm
MOV AX,AL
```

```dos
COPY BAD.ASM SOURCE.ASM
CHECK SELF
```

Require `ERROR 00001 CODE 1` and FAIL. Byte and word registers cannot be mixed. The accepted RESULT.COM must remain unchanged. An unexpected PASS fails the check; restore ASM0.ASM as SOURCE.ASM before another self-build.

If a comparison differs, check that the same exact source was assembled by BASIC and both native generations. Then compare the instruction and register tables, label storage, and pass resets. Do not copy a mismatching executable over the known working tool.

Keep ASMKEEP.COM, BOOTKEEP.BAS, BOOTASM.BAS and the sources together so the means to recover the tool remain available.
