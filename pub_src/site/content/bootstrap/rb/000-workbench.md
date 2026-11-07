+++
title = "The RILLBOOT workbench"
weight = 0
description = "Begin with the completed RILL0. Copy RILL0.IR to RB01.IR and continue editing its working compiler. Use IRKEEP and ASMAKEEP for every build. Each saved compiler accepts the earlier language while gaining one capability."
download = "RILLBOOT.ZIP"
download_group = "tools/rillboot"
reader_names = 1
aliases = ["/bootstrap/rb/033-the-systems-workbench/", "/bootstrap/rill/033-the-systems-workbench/"]
+++

Begin with the completed RILL0. Copy RILL0.IR to RB01.IR and continue editing its working compiler. Use IRKEEP and ASMAKEEP for every build. Each saved compiler accepts the earlier language while gaining one capability.

Keep VIEW.BAS and CHECK.BAT from the BOOTASM workbench. Work in an ordinary DOS hard-disk directory. Fixed names avoid adding a filename parser to each tool. Require a fresh OK and PASS before copying an output into the next stage.

```dos
COPY RB01.IR SOURCE.IR
CHECK IRKEEP
COPY RESULT.ASM SOURCE.ASM
CHECK ASMAKEEP
COPY RESULT.COM RB01.COM
```

An early stopping point may produce a fragment rather than a complete program. Inspect its length and bytes with VIEW.BAS; execute it only when the article gives a complete program. Recovery names protect an interrupted publication: inspect them before trying again.
