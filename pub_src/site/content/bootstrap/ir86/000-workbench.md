+++
title = "The IR86 workbench"
weight = 0
description = "ASM86 builds every saved source in this collection. The translator always reads SOURCE.IR and writes RESULT.ASM. Preserve the completed translator as IRKEEP.COM; make the identical IWKEEP.COM copy used by later workbenches."
download = "IR86.ZIP"
download_group = "tools/ir86"
reader_names = 1
aliases = ["/bootstrap/ir86/00-workbench/"]
+++

ASM86 builds every saved source in this collection. The translator always reads SOURCE.IR and writes RESULT.ASM. Preserve the completed translator as IRKEEP.COM; make the identical IWKEEP.COM copy used by later workbenches.

Keep VIEW.BAS and CHECK.BAT from the BOOTASM workbench. Work in an ordinary DOS hard-disk directory. Fixed names avoid adding a filename parser to each tool. Require a fresh OK and PASS before copying an output into the next stage.

```dos
COPY IR01.ASM SOURCE.ASM
CHECK ASMAKEEP
COPY RESULT.COM IR01.COM
```

An early stopping point may produce a fragment rather than a complete program. Inspect its length and bytes with VIEW.BAS; execute it only when the article gives a complete program. Recovery names protect an interrupted publication: inspect them before trying again.
