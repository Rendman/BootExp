+++
title = "The editor workbench"
weight = 0
description = "Preserve the established trio and give the editor its own work directory."
download = "EDIT86.ZIP"
download_group = "tools/edit86"
reader_names = 1
+++

Begin after Rebuilding Our Tools in RILL and its matching generations. Keep the compiler R0.COM, translator I0.COM and assembler A0.COM unchanged. Make an editor work directory on the hard disk, with these builders, CHECK.BAT, VIEW.BAS and a plain ASCII editor. Use the DOS 3.10 workbench and an 80-column text display.

## Command-line filenames

```dos
CHECK EDIT86 INPUT.RIL
```

DOS supplies the names in the PSP command tail. The native entry binding copies them into owned zero-terminated storage before file services. The language-level interface supplies argument counts and ordinary string pointers through portable services. CHECK.BAT forwards the arguments and reports status immediately. No arguments select EDIT.TXT. Use unquoted 8.3 disk names in the current directory: letters, digits, underscore and hyphen, with an optional extension. Paths, switches, excess arguments and overlong names are rejected. Keep selected files distinct from each other and from EDIT.TMP and EDIT.BAK. Those temporary/backup names remain reserved.

The selected document is opened and saved under the same name. Keep a separately named accepted source while editing; the status row shows the selected name.

## The service builders

Copy the exact RILL.RIL and IR86.RIL from the toolchain collection. The first two articles extend those sources as RILLED.RIL and IRED.RIL. Build each with R0, I0 and A0, preserving the new executables as RILLED.COM and IRED.COM. They accept the established language plus the editor operations. The earlier builders remain available.

IRED appends an explicitly authored EDITRT.ASM target binding after the established runtime. Pass that binding as the third IRED filename: CHECK IRED INPUT.IR OUTPUT.ASM EDITRT.ASM. With two arguments the binding defaults to EDITRT.ASM; no arguments also select the established source/result defaults. The optional binding name must differ from source, result and recovery names. S02.ASM is empty; S03.ASM through S07.ASM are complete saved stages of the binding. Copy the stated stage to EDITRT.ASM before translating its probe. The complete editor uses S07.ASM, also supplied as EDITRT.ASM. This is source read by our translator and assembler, not a prebuilt machine-code library.

## One build pattern

```dos
CHECK RILLED E08.RIL RESULT.IR
CHECK IRED RESULT.IR RESULT.ASM EDITRT.ASM
CHECK A0 RESULT.ASM RESULT.COM
COPY RESULT.COM E08.COM
```

Require every fresh OK report and PASS before the following COPY. Preserve each accepted executable under its checkpoint name. RILLED emits RESULT.IR for IRED; IRED emits ordinary assembly input for A0. The resulting native instructions come from A0. E20.RIL and EDIT86.RIL are the same completed editor source.

## Select a document

```dos
CHECK E15 T15.TXT
```

Give the document name after the editor name: CHECK EDIT86 INPUT.RIL. filename() obtains it through argc()/arg(n); no argument selects EDIT.TXT. Exactly one unquoted 8.3 name is accepted, without paths or switches. EDIT.TMP and EDIT.BAK remain reserved save/recovery names. The same selected name is opened, shown on the status row and saved. Keep a separately named accepted source until the edited source has passed its own build and tests.

Do not run two editor instances in the same work directory or change these files while an instance is active. Inspect a pre-existing EDIT.TMP or EDIT.BAK before removing it. A recovery file may be the only copy of a failed save.

## Inspect results

Use CHECK immediately so a silent return is visibly PASS or FAIL. Use VIEW.BAS for the reported length and hexadecimal bytes. COMP compares a round trip against its preserved original:

```dos
ECHO N>NO.TXT
COMP T15.TXT T15.TXT <NO.TXT
```

NO.TXT answers N to COMP's request for another comparison. The screen services need the physical text screen and keyboard; redirecting ordinary DOS output does not supply key events or capture the screen. F10 leaves a screen probe or editor. After editing is introduced, Escape cancels the unsaved-changes question.

## Memory before entry

The finished editor retains a 64 KiB main DOS block, obtains eight 32 KiB text blocks and one 16 KiB undo block. That is 336 KiB plus the DOS environment, memory-control records and resident system software. Use the reference 640 KiB machine; total installed RAM alone does not guarantee enough free DOS memory. Every allocation is checked. A failed startup frees the blocks it obtained and returns FAIL without saving the document.
