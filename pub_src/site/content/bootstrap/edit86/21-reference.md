+++
title = "The editor and service reference"
weight = 21
description = "Keys, logical positions, memory, native binding and save recovery."
download = "EDIT86.RIL"
download_group = "tools/edit86"
reader_names = 1
+++

EDIT86 edits one fixed document, EDIT.TXT. An absent file starts an empty document; a failed inspection or read is an error. Saving an empty document creates a genuine zero-byte file. No byte is treated as a text EOF marker: 1A, NUL and high bytes round-trip unchanged.

## Keys

| Key | Action |
|---|---|
| Printable ASCII, Tab | Insert the character or a literal tab |
| Enter | Insert CR/LF together |
| Backspace, Delete | Remove text on the left or right; CR/LF stays paired |
| Arrows | Move the insertion position; up/down retain a preferred visual column |
| Home, End | Beginning/end of the physical line |
| Page Up, Page Down | Move twenty-four physical lines |
| F6, F7 | Document start/end |
| F2 or Control-S | Save EDIT.TXT |
| F3 | Enter a literal, case-sensitive search; Enter accepts, Escape cancels |
| F5 | Find the next occurrence, starting one byte later; no wrap |
| F4 or Control-Z | Undo one retained edit |
| F10 or Control-Q | Quit; S saves, Q discards, Escape cancels when dirty |

Tabs use eight-column stops. Other control and high bytes display as dots but retain their exact values. Long lines scroll horizontally; they do not wrap into extra screen rows. CR/LF, lone CR, lone LF and a final unterminated line are accepted. Newly entered line endings are CR/LF. There is no line-length or line-count table bound. Very long lines and distant searches require scans and can be slow on an 8088.

## Document representation

Positions are unsigned pairs of words, low word first. Capacity is (0000H,0004H), or 262144 bytes. Logical text has length bytes. Physical text occupies [0,gap) and [gapend,capacity); the interval [gap,gapend) is free. Thus gapend minus gap equals space, and length plus space equals capacity. gap is also the insertion position. Logical positions below gap map directly; positions at or after it add space. End positions may equal capacity, but byte access is restricted to positions below length.

The physical page number is high-word times two plus bit fifteen of the low word. The page offset is the low word AND 32767. Eight opaque block handles identify the pages. A handle is never a segment or a near pointer. A checked bulk move clips at both source and destination page ends; the helper handles overlap within each chunk.

A full 256 KiB file is accepted, but it has no free insertion room. Delete before inserting. Enter requires two free bytes and is refused as a whole if only one remains. Refused edits create no undo record. The editor keeps the complete document in RAM; navigation neither pages text to disk nor silently saves it.

## Memory budget

| Storage | Amount | Reason |
|---|---|---|
| Main DOS block | 64 KiB | PSP, near code/static data, ordinary buffers and stack |
| Document | 8 times 32 KiB | 256 KiB shared by occupied text and gap |
| Undo | 16 KiB | 2048 records of eight bytes |
| Requested program blocks | 336 KiB | Main block plus nine auxiliary blocks |
| Additional conventional memory | Depends on DOS environment | Environment, DOS control records, resident software and fragmentation |

The main image remains below the 61184-byte profile bound; the upper 4 KiB remains its guarded stack. Auxiliary memory enlarges data capacity, not near-code reach. The existing sixteen-slot allocator has seven unused slots. No full line index, second document copy or disk cache is allocated. A startup failure frees acquired blocks and returns nonzero. Installed RAM is not the same as available DOS memory.

Undo stores kind and count bytes, low/high logical position words and two deleted bytes. It retains the newest 2048 successful insert/delete actions, including paired line endings. New edits overwrite the oldest retained record. There is no redo. Saving does not clear the ring. Undo conservatively marks dirty even when it happens to restore saved text.

## Screen and key services

These are extensions in RILLED and IRED, not changes required by the preceding bootstrap tools. Every service sets persistent status: zero on success, nonzero on failure. STATUS itself leaves that state unchanged; save it before another service replaces it.

| RILL call | Meaning |
|---|---|
| vbegin(), vend() | Enter/leave a screen session; preserve cursor settings, clear the working screen |
| vpos(cell) | Position the cursor at cell 0 through 1999 |
| vwrite(pointer,count) | Write literal consecutive cells with the normal attribute; never scroll |
| key() | Wait for a character/event word; zero denotes an unrecognized extended key |
| blockload(block,offset,pointer,count) | Near buffer to checked allocated block |
| blockread(block,offset,pointer,count) | Checked allocated block to near buffer |
| blockmove(source,sourceOffset,dest,destOffset,count) | Checked overlap-safe transfer between blocks |

Near pointers must name valid program storage for the complete count. Wrapping a near address is rejected. Both allocated extents are validated before a move. An offset must be strictly below the allocation size, including on a zero-count transfer; counts must fit the remaining extent. Copies set no terminator. Main-segment state is restored on success and failure.

VWRITE checks its screen extent; it advances the internal cell position but leaves hardware cursor placement to VPOS. It writes literal byte values; the editor supplies tab expansion and control substitution. Screen calls and KEY require a successful VBEGIN. The 8086 binding accepts BIOS text modes 3 and 7 with eighty columns and twenty-five rows. It uses the active page, a fixed normal attribute, BIOS cursor/key services and private text-video addresses. It does not switch modes, preserve old screen contents, resize the screen or implement terminal escape sequences.

| Event | Value |
|---|---|
| Left, Right, Up, Down | 256, 257, 258, 259 |
| Home, End, Page Up, Page Down | 260, 261, 262, 263 |
| Delete, Save, Quit, Undo | 264, 265, 266, 267 |
| Find, Next, Document start, Document end | 268, 269, 270, 271 |

The IR names are VBEGIN, VEND, VPOS, VWRITE, KEY, BLOAD, BREAD and BMOVE. Multi-argument operations take their final argument in A and consume the earlier arguments from the expression stack in source order. VWRITE consumes one saved word; BLOAD/BREAD consume three; BMOVE consumes four. Their result is zero except KEY's event. STATUS gives the service outcome. No physical registers, native handles or video addresses appear in this IR interface.

## Saving and recovery

Existing EDIT.TMP or EDIT.BAK blocks entry and saving. Saving needs enough free disk space for a complete temporary document alongside the accepted file. Use the hard-disk workbench for large sources. After the complete text is written to EDIT.TMP and that handle is closed, an existing EDIT.TXT is renamed EDIT.BAK, the temporary is renamed EDIT.TXT and the backup is deleted. A failed publication attempts restoration. DOS renaming is not atomic replacement, and this is not a power-loss guarantee.

Ordinary failed saves leave the accepted document intact and keep dirty set. Failed restoration retains EDIT.TMP and EDIT.BAK for inspection, possibly with no EDIT.TXT. Failed backup removal retains the new EDIT.TXT and old EDIT.BAK. Cleanup protects retained recovery material, prints a warning and returns FAIL. Do not retry blindly or delete either copy before inspecting it. Copy a selected recovery file to a separately named safe file first.

The normal return is zero. Startup, fatal service or cleanup failure returns one; screen/file diagnostics identify the failing operation. A rejected edit or failed recoverable save leaves the editor running with a status-line explanation. CHECK reports the final DOS status, while the on-screen Saved message confirms an accepted save. A clean quit does not prove a prior failed save succeeded: a deliberate discard also returns zero.

There are no filename prompts, command-line options, multiple documents, selection, clipboard, replace, redo, syntax coloring, automatic writes or disk-backed document pages. The fixed names and bounded records keep this first editor within the existing language and memory profile.
