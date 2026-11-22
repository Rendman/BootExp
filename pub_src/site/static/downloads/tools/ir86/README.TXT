BOOTSTRAP EXPERIMENT - IR86

Read the matching workbench and construction articles in order.
Use your own DOS 3.10 and period BASIC interpreter.
VIEW.BAS inspects lengths and bytes. CHECK.BAT checks program status.
Require each fresh OK and PASS before copying a result to the next tool.
Sources are ASCII with DOS line endings and 8.3 filenames.
No executable, interpreter, or outside compiler is included.

The completed ASM86 builds every native checkpoint.
Bring ASM86.ASM and the tested ASMAKEEP.COM from that workbench.
ASMAKEEP.COM is the 6433-byte assembler, not the earlier ASMKEEP.COM.
CHECK ASMAKEEP ASM86.ASM ASTEST.COM must report OK and PASS.
C:\DOS\FC.EXE /B ASMAKEEP.COM ASTEST.COM must show no differences.
Keep ASM86.ASM unchanged; copy it to IR01.ASM before editing.
CHECK ASMAKEEP IR01.ASM RESULT.COM builds the 2534-byte reader.
Require OK and PASS, then COPY RESULT.COM IR01.COM.
IR01.ASM through IR23.ASM form one continuing translator.
IR86.ASM is identical to IR23.ASM.
Supply each translator its source and result names on the command line.
No arguments select SOURCE.IR and RESULT.ASM.
After the final checks, preserve the source and accepted executable:
COPY IR23.ASM IR86.ASM
COPY IR23.COM IR86.COM
COPY IR86.COM IRKEEP.COM
COPY IRKEEP.COM IWKEEP.COM
Keep these matching working copies for the compiler workbenches.

Early helper output can be an incomplete fragment; inspect its bytes.
Execute only programs identified as complete in their article.
Source rejection preserves accepted output. A failed publication may
leave temporary or backup files; inspect those before a new run.

COMMAND-LINE FILENAMES
From ASM1 onward, supply input and output filenames on the command
line: CHECK tool INPUT.EXT OUTPUT.EXT. No arguments select the
default work names. Use unquoted 8.3 filenames in the current directory;
paths and switches are not accepted. Input, output, temporary and backup
names must be distinct. LINK86 takes two object names then the result;
EDIT86 takes one document name and saves that same document.
