+++
title = "Linking Our First Modules"
weight = 10
description = "A RILL-written linker for two small text object modules."
download = "LINK86.RIL"
download_group = "tools/link86"
reader_names = 1
cover = true
tool_id = "LINK86"
collection_key = "link86"
+++

The RILL-written toolchain can now build another tool. LINK86 places two object modules in one DOS .COM image, resolves their public names and emits relative calls and absolute addresses. Its source is compiled with the completed RILL compiler, IR86 translator and ASM86 assembler.

## What we're adding

- **Two object modules:** Place MAIN.OBJ before UTIL.OBJ so independently described pieces can form one DOS .COM image.
- **Public names:** Collect complete exported spellings and module-relative offsets so one module can refer to a definition in the other.
- **Relative and absolute words:** Resolve near calls and loaded addresses while streaming so the output needs no backward patching.
- **Checked publication:** Validate both passes and publish a closed temporary file so rejected objects do not replace an accepted executable.

**Removing:** None. The RILL compiler, IR86 translator and ASM86 assembler keep their existing languages and outputs; the object fixtures are entered as plain text.

## The construction

Ten working stopping points build the reader, record decoder, streamed writer, publication checks, module layout, public table and relocations. The last two fixtures are complete programs: one calls a function in the other module, and one displays text exported by the other module. The object files are entered as plain ASCII; this collection does not change ASM86 or require another assembler.

Read the workbench first and keep every accepted checkpoint separately named. The [disk source collection](../../downloads/tools/link86/LINK86.ZIP) contains the RILL sources, exact text-object fixtures, viewer and checker. It supplies no prebuilt executable. The [object reference](11-reference/index.html) gives the complete small format and its limits.
