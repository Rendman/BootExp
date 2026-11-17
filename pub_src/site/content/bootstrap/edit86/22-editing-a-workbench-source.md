+++
title = "Editing a workbench source"
weight = 22
description = "Use the editor on the actual source formats and preserve an accepted source."
download = "EDIT86.RIL"
download_group = "tools/edit86"
reader_names = 1
+++

Use EDIT86 in a separate hard-disk directory. Keep EDIT86.COM, its source, the service builders and their binding together. Preserve an accepted copy, then pass the source filename directly:

```dos
COPY IR86.RIL HOLD.RIL
CHECK EDIT86 IR86.RIL
```

Try F3 to find a routine name, F5 for another occurrence, and F6/F7 for document ends. On this first pass, make no changes; press F2 then F10. Require Saved on screen and CHECK PASS. Compare the complete file:

```dos
C:\DOS\FC.EXE /B IR86.RIL HOLD.RIL
```

Require no difference, then inspect its length with VIEW.BAS. Repeat by passing a .BAS, .ASM and .IR source filename directly to EDIT86. This checks source round trips rather than adding a new display program. A source larger than 65535 bytes is still one document. The total occupied bytes must not exceed 262144, and a full document needs a deletion before growth.

For an actual edit, keep HOLD.RIL, change the working document, save with F2 and leave with F10. The save replaces the selected source only after the temporary file is closed. After the Saved report, inspect and rebuild that same named source.

Build and test that changed source with the existing toolchain before replacing an accepted tool executable. Keep the old source and executable until that check passes. EDIT86 edits bytes; it does not validate RILL syntax or assemble source for you.

To test rejection without risking a source, preserve the source, create a small EDIT.TMP containing HOLD, and run CHECK EDIT86 IR86.RIL. Require FAIL with the recovery-file diagnostic. Inspect both files to confirm they were preserved. Remove only the deliberate exercise file after that check.
