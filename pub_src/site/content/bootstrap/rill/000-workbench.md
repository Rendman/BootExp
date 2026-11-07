+++
title = "The RILL0 workbench"
weight = 0
description = "Begin with the completed ASM86 and native IR86 workbenches. Every compiler checkpoint is written in IR86. Translate SOURCE.IR with IRKEEP, copy accepted RESULT.ASM to SOURCE.ASM, then assemble with ASMAKEEP. The finished RILL0 reads SOURCE.RIL and publishes RESULT.IR."
download = "RILL0.ZIP"
download_group = "tools/rill0"
reader_names = 1
aliases = ["/bootstrap/rill/00-workbench/"]
+++

Begin with the completed ASM86 and native IR86 workbenches. Every compiler checkpoint is written in IR86. Translate SOURCE.IR with IRKEEP, copy accepted RESULT.ASM to SOURCE.ASM, then assemble with ASMAKEEP. The finished RILL0 reads SOURCE.RIL and publishes RESULT.IR.

Keep VIEW.BAS and CHECK.BAT from the BOOTASM workbench. Work in an ordinary DOS hard-disk directory. Fixed names avoid adding a filename parser to each tool. Require a fresh OK and PASS before copying an output into the next stage.

```dos
COPY R01.IR SOURCE.IR
CHECK IRKEEP
COPY RESULT.ASM SOURCE.ASM
CHECK ASMAKEEP
COPY RESULT.COM R01.COM
```

An early stopping point may produce a fragment rather than a complete program. Inspect its length and bytes with VIEW.BAS; execute it only when the article gives a complete program. Recovery names protect an interrupted publication: inspect them before trying again.
