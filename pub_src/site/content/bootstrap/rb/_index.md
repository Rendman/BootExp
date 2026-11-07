+++
title = "A Compiler for Writing Tools"
weight = 7
description = "Begin with the completed RILL0. Copy RILL0.IR to RB01.IR and continue editing its working compiler. Use IRKEEP and ASMAKEEP for every build. Each saved compiler accepts the earlier language while gaining one capability."
download = "RILLBOOT.IR"
download_group = "tools/rillboot"
reader_names = 1
cover = true
tool_id = "RILLBOOT"
collection_key = "rb"
+++

Continue the completed RILL0 source. Add word arithmetic, masks, strings, global storage, procedures, and the file and workspace services needed to compile the RILL compiler. Every continuation remains a working compiler for its preceding subset. The seed deliberately omits XOR, left shift, unary minus, bitwise complement, explicit address-of, and unused intrinsic wrappers; RILL adds the operations needed by the later tool sources.

Read the workbench first. The [source collection](../../downloads/tools/rillboot/RILLBOOT.ZIP) contains plain source and test files.
