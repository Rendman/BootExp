+++
title = "The assembly workbench"
weight = 0
description = "Use the completed BASIC assembler and prepare a single-segment workspace."
download = "ASM86.ZIP"
+++

Begin with the completed BOOTASM collection: `BOOTASM.BAS`, `VIEW.BAS`, and `CHECK.BAT`. Keep the same DOS 3.10 directory and the period GW-BASIC supplied with your distribution. The instructions call the interpreter `GWBASIC`; use its actual name on your disk. DOS and BASIC version numbers are independent; note the interpreter's startup banner before beginning.

BOOTASM's assembly language is the language used to write every checkpoint here. There is no other assembler, linker, or supplied executable in the construction. A `.COM` file starts at offset 0100H without an executable header.

## Preserve the foundation

At DOS, make an untouched copy:

```dos
COPY BOOTASM.BAS BOOTKEEP.BAS
```

The completed BOOTASM supplies the instruction forms and storage needed to build every ASM86 checkpoint. Its symbol table holds 256 labels, and its output image can contain 4,096 bytes. Use the normal roughly 60 KB BASIC workspace for the program, symbols, and output array.

Build the first ASM86 executable by running `GWBASIC BOOTASM.BAS` and entering an assembly source base name. Require its printed `OK` and byte count. `SYSTEM` returns from BASIC to DOS. BASIC's printed error report is the build result; CHECK.BAT is for a complete assembled `.COM` program, not for judging the interpreter.

## Keep the steps separate

Enter `AS01.ASM` from the first installment. Each subsequent installment starts with a copy of the preceding source under the next name. Preserve both source and executable after a successful test. Every checkpoint can still be assembled with BOOTASM; the native program replaces it only after the self-assembly test.

Sources are plain ASCII with DOS CR/LF line endings and short filenames. `COPY CON T07.ASM` begins a small test file; Ctrl-Z and Enter finish input. The Ctrl-Z keystroke is not a token to type into an instruction. `TYPE T07.ASM` displays the saved text. An editor may be more convenient for the growing assembler; it must save ordinary text without formatting codes.

Choose ordinary disk base names of one through eight letters, digits, or underscores. Supply no path or extension at a source prompt. DOS device names such as CON, NUL, PRN, AUX, COM1, and LPT1 are excluded from this workbench even with an extension: the small name checker leaves their special meaning to DOS.

## The native memory arrangement

The native program requires a complete 64 KB segment, with the normal entry stack at FFFEH. It checks SP before using its buffers and reports code 7 if that requirement is not met. Code and static data occupy the low part of the segment; fixed buffers are kept clear of them:

| Offsets | Use |
|---|---|
| 0000H–00FFH | DOS program segment prefix; leave it alone |
| 0100H–20FFH | Reserved image area, maximum 8,192 bytes |
| 2200H–2278H | Physical source line, 120 characters and a zero |
| 2300H–2310H | Token, 16 characters and a zero |
| 2400H–240BH | DOS console input buffer |
| 3000H–43FFH | 256 symbol records of 20 bytes |
| 6000H–7FFFH | Output buffer, 8,192 bytes |
| Near FFFEH | Stack, growing toward lower offsets |

The program does not relocate these buffers or request a second segment. Keep DS, ES, and SS at the DOS entry segment. Its calls are shallow and nonrecursive; reserve the upper 4 KB for the stack and do not place data there. The completed image is under 3 KB, so BOOTASM's 4 KB output bound is sufficient to build it. ASM86's **own** 8 KB output bound is a different limit.

## Visible checks

Use the BOOTASM workbench's unchanged CHECK.BAT and VIEW.BAS. Run `CHECK AS01` to execute a complete checkpoint and immediately print PASS or FAIL from its DOS return status. The checker accepts a base name without arguments. A missing program reports `Missing program`. DOS may echo its first ECHO OFF command.

To inspect a file, run `GWBASIC VIEW.BAS`, enter the complete filename including `.COM`, and compare both length and hexadecimal bytes. Use `SYSTEM` afterward. A zero-byte output is a valid inspection result but is never a runnable program.

All AS01 through AS29 checkpoint programs are executable tools or diagnostics. Their **output fixtures** often are just data or encoding exercises. Run an output fixture only when its installment explicitly calls it a complete executable. Use a new test name and require a fresh OK before trusting an output file: source errors leave an older `.COM` untouched, while a disk error during writing can leave a partial file.
