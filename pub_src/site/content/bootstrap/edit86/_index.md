+++
title = "Building Our Screen Editor"
weight = 11
description = "A RILL-written screen editor with a paged document, recoverable saves and bounded undo."
download = "EDIT86.RIL"
download_group = "tools/edit86"
reader_names = 1
cover = true
tool_id = "EDIT86"
collection_key = "edit86"
+++

We can build our tools with RILL. EDIT86 gives that workbench a screen editor of its own: a window on a plain source file, an insertion position, navigation, search and a way to reverse a mistaken edit. It follows the RILL-written toolchain and LINK86 on the bootstrap ladder.

## What we're adding

- **A screen editor written in RILL:** Edit the plain source files used by the workbench, with navigation, insertion, deletion, literal search and bounded undo.
- **A 256 KiB document buffer:** Keep text and its insertion gap in eight allocated pages so source files larger than one segment remain editable.
- **Portable screen and key services:** Extend preserved copies of RILL and IR86 with cell positions, counted screen writes and key events, keeping native details in the target binding.
- **Checked bulk transfers:** Move text between allocated pages and the file buffer without a procedure call for every byte.
- **Recoverable saves:** Publish EDIT.TXT through temporary and backup names so failed saves preserve the accepted file or leave explicit recovery files.

**Removing:** None. Preserve the established RILL-written trio. The editor uses extended compiler/translator copies; earlier bootstrap sources, object linking and the single-segment executable format remain available.

## The construction

The executable remains a DOS .COM program. Its text lives in eight separately allocated pages rather than in the code segment. The complete 256 KiB buffer holds both the file and its free insertion gap. Moving around changes memory; disk writes happen only when Save is requested. A bounded undo ring uses one more block.

The construction begins with preserved copies of the compiler and translator. We add counted screen writes, key events and checked bulk transfers, then grow one editor source through file loading, safe saving, a movable gap, line boundaries, a window, navigation and editing. Native screen and segment details remain in the target binding.

Begin with the workbench. The [source collection](../../downloads/tools/edit86/EDIT86.ZIP) contains every stopping point, the service extensions, plain text fixtures and the established inspection helpers. No executable is supplied. The complete source is EDIT86.RIL; the reference gives its memory budget and working limits.
