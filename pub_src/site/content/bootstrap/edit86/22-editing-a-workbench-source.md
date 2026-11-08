+++
title = "Editing a workbench source"
weight = 22
description = "Use the editor on the actual source formats and preserve an accepted source."
download = "EDIT86.RIL"
download_group = "tools/edit86"
reader_names = 1
+++

Use EDIT86 in a separate hard-disk directory. Keep EDIT86.COM, its source, the service builders and their binding together. Select a source with COPY:

```dos
COPY IR86.RIL HOLD.RIL
COPY IR86.RIL EDIT.TXT
CHECK EDIT86
```

Try F3 to find a routine name, F5 for another occurrence, and F6/F7 for document ends. On this first pass, make no changes; press F2 then F10. Require Saved on screen and CHECK PASS. Compare the complete file:

```dos
COMP EDIT.TXT HOLD.RIL <NO.TXT
```

Require no difference, then inspect its length with VIEW.BAS. Repeat with a .BAS, .ASM and .IR source selected under the same EDIT.TXT name. This checks source round trips rather than adding a new display program. A source larger than 65535 bytes is still one document. The total occupied bytes must not exceed 262144, and a full document needs a deletion before growth.

For an actual edit, keep HOLD.RIL, change the working document, save with F2 and leave with F10. Copy it back only after the Saved report:

```dos
COPY EDIT.TXT IR86.RIL
```

Build and test that changed source with the existing toolchain before replacing an accepted tool executable. Keep the old source and executable until that check passes. EDIT86 edits bytes; it does not validate RILL syntax or assemble source for you.

To test rejection without risking a source, preserve EDIT.TXT, create a small EDIT.TMP containing HOLD, and run CHECK EDIT86. Require FAIL with the recovery-file diagnostic. Inspect both files to confirm they were preserved. Remove only the deliberate exercise file after that check.
