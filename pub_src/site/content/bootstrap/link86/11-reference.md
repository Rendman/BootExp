+++
title = "The object and linker reference"
weight = 11
description = "The complete text format, layout arithmetic, limits and publication contract."
download = "LINK86.RIL"
download_group = "tools/link86"
reader_names = 1
+++

LINK86 reads MAIN.OBJ and UTIL.OBJ in that order and writes one DOS .COM image. The format is our own ASCII object text. It contains authored bytes and relocation records; it is not compatible with commercial OBJ files.

## Records

| Record | Meaning |
|---|---|
| OBJ1 | Required first nonblank, noncomment record |
| B hh ... | Emit one through sixteen hexadecimal byte pairs |
| P name hhhh | Export a module-relative offset, exactly four hexadecimal digits |
| R name | Emit target minus the address after this two-byte operand, modulo 65536 |
| A name | Emit the target's absolute loaded word address |
| END | Required final record; only blank lines/comments may follow |

Fields are separated by spaces or tabs. A semicolon ends the meaningful part of a physical record. Names and record spellings are folded to uppercase; hexadecimal digits accept either case. Each B item has exactly two digits. Numeric fields have no H suffix, signs or expressions. P's offset is independent of the record's position and may be written before its bytes. R and A each occupy two bytes at their own record position; there is no separate patch-offset field or addend.

Names begin with a letter or underscore and continue with letters, digits or underscores, at most 31 characters. Public names are unique across both modules. References may precede definitions and may name a public in the same module. An unexported location is not a linker symbol. The format has no private-name records, implicit imports, alignment, sections, short/far relocations, library search or entry-selection directive.

## Layout and passes

MAIN begins at loaded offset 0100H. UTIL begins immediately after MAIN's emitted bytes. Public offsets are relative to their owning module, never loaded addresses. They must be between zero and that module's length, inclusive; an end label is a position, not an extra allocated byte. Programs remain responsible for live storage and valid executable entry bytes.

Pass one validates records, counts the layout and stores public definitions. Pass two reopens both inputs, verifies public values, owners and occurrences, verifies module lengths, and resolves references into streamed output. Keep the inputs unchanged. Same-sized edits to byte records or references are not all detected; this is not a general file identity check.

Words are emitted low byte first. A near relative word is ordinary sixteen-bit displacement arithmetic in this one code segment. There is no check that a symbol denotes executable instructions rather than data. The two complete acceptance programs supply their own DOS exit/output instructions; LINK86 adds no runtime or executable header.

## Limits

| Resource | Bound |
|---|---|
| Input modules | Two fixed files: MAIN.OBJ, then UTIL.OBJ |
| Emitted image | 61184 bytes, loaded at 0100H through EFFFH |
| Public definitions | 256, stored in a checked 10240-byte allocated block |
| Name spelling | 31 characters, compared in full |
| Physical record | 120 characters, including comments and whitespace |
| Physical records | At most 65535 per input per pass |
| B record | One through sixteen byte pairs |
| File buffers | 1024 bytes each; no complete object or image buffer |

The upper 4 KiB remains the generated program's stack reservation. A zero-byte output is valid for inspection only. Allocated symbol storage does not enlarge the target code segment. The linker itself is built by the established RILL toolchain, whose normal DOS entry and stack guard apply.

Object text accepts CR/LF, bare CR or LF and a final unterminated record. Control-Z ends input text. Other control bytes except tab and high bytes are rejected. B records can materialize every byte value, including zero, FF and 1A.

## Files, reports and failures

Existing LINK.TMP or LINK.BAK blocks a publishing run. Create the temporary file only after a successful layout pass. Flush and close it, release allocated symbol storage, then rename the previous RESULT.COM to LINK.BAK, rename LINK.TMP to RESULT.COM, and delete the backup. A failed second rename attempts restoration. Failed restoration or backup deletion can leave recovery files; inspect them before another run. DOS rename is not atomic replacement. Source rejection preserves the accepted result and removes only this run's owned temporary output.

A completed link prints `OK RESULT.COM nnnnn bytes` and returns zero. Failures print `LINK ERROR uuuuu lllll CODE ccccc` and return one. Input numbers one and two identify MAIN and UTIL; zero identifies global setup/publication. The line is the current physical record, or zero before reading. At a record-count overflow, the counter retains 65535. L01/L02 use return status only; L05 deliberately reports and leaves LINK.TMP for inspection.

| Code | Meaning |
|---|---|
| 1 | Malformed header/record, source byte or missing END |
| 2 | Invalid byte/word hexadecimal spelling |
| 3 | Invalid, duplicate or undefined public name |
| 4 | Public offset outside its module |
| 5 | Record, name, symbol, byte-record or image capacity |
| 6 | File, allocation, transfer or publication failure |
| 7 | Definitions or module layout differ between passes |
| 8 | Reserved temporary/backup name already exists |

Require the fresh success report and PASS before copying or executing output. A failure report never authorizes use of an older RESULT.COM.
