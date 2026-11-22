"""The narrative thread for the native IR86 construction articles."""

COVER = (
    "The assembler can now build the larger programs on our workbench. I want to write a compiler next, "
    "and I need to choose what that compiler will produce. I shall give it a small language for values, "
    "storage, and calls, then build a translator that turns those operations into the assembly we can already assemble.\n\n"
    "We begin with the assembler's working file routines. A reader becomes a scanner, the scanner feeds an "
    "operation table, and that table starts producing assembly text. Each later addition gives the future "
    "compiler something concrete to use: saved operands, named storage, procedure frames, strings, and file services. "
    "By the last checkpoint, we shall have the translator needed to build RILL0. ASM86 assembles every stage.\n\n"
    "The language defines word values, a virtual accumulator, an expression stack, byte addresses, and opaque "
    "service handles. The 8086 instructions appear in the backend templates and DOS binding; they are not part "
    "of the IR program interface. Keeping that boundary explicit gives a later implementation a precise set of rules to preserve."
)

WORKBENCH = (
    "I have a working assembler and a way to inspect its output. For the next tool I want another visible "
    "stopping point between the source I enter and the bytes DOS executes: an assembly file I can read. "
    "IR86 will write that file, and the preserved ASM86 will turn it into a program.\n\n"
    "## Carry the tested assembler forward\n\n"
    "Bring ASM86.ASM and ASMAKEEP.COM from the completed ASM86 workbench into the directory used for this collection. "
    "ASM86.ASM is the accepted A40 source; ASMAKEEP.COM is the 6,433-byte assembler preserved after its two self-build comparisons. "
    "Keep that source untouched. ASMKEEP.COM names the earlier ASM0 and is not the builder used here.\n\n"
    "Before editing a copy, check the source and executable together:\n\n"
    "```dos\nCHECK ASMAKEEP ASM86.ASM ASTEST.COM\nC:\\DOS\\FC.EXE /B ASMAKEEP.COM ASTEST.COM\n```\n\n"
    "Require OK ASTEST.COM 06433 bytes and PASS before the comparison. FC must report no differences. "
    "This checks the same preserved assembler and source that begin the construction.\n\n"
    "## Building the translator\n\n"
    "The first four checkpoints prepare the reader, scanner, writer, and operation records separately. "
    "The fifth joins them into a small translator. From there we keep extending the same source until it can "
    "support the compiler. I shall save each accepted translator with its source so there is a working place to return to.\n\n"
)

READER = (
    "The copied source changes jobs. START keeps the full-segment stack check and calls CMDFILES and OPENFILE, "
    "then READLINE until EOF. SHOWBYTE displays each character from the completed line; TEXT supplies the line ending. "
    "CLOSEFILE finishes the input before the zero-status DOS exit. The first driver creates no output file.\n\n"
    "Remove the assembly statement dispatcher, instruction encoders, symbol records, hash table and symbol-page allocation. "
    "They describe an assembler's work, which this reader no longer performs. The source retains the scanner, lookup, numeric, "
    "file and report helpers; the driver above uses only its reader and display path.\n\n"
    "The reader's buffers have explicit new addresses. Keep their pointer constants together with the corresponding capacity checks:\n\n"
    "| Offsets | Use |\n|---|---|\n"
    "| C800H–CBFFH | Up to 1023 physical line characters and a zero |\n"
    "| CC00H–CC3FH | Up to 63 token characters and a zero |\n"
    "| D000H–DFFFH | 4096-byte input block |\n"
    "| E000H–EFFFH | Reserved 4096-byte output block |\n"
    "| F000H–FFFFH | Stack reservation |\n\n"
    "NEXTBYTE hands back a buffered byte or EOF. READLINE retains raw character case, normalizes line endings, "
    "and checks the physical line length and two-word source counters. The input is reopened by DOS for each new program run; "
    "there is no complete source image or allocated symbol workspace in this diagnostic.\n\n"
)

OPENINGS = {
    1: "The assembler already knows how to read a long source a block at a time. I want to carry that working reader into the translator. For this first stopping point, I shall strip away the assembly parser and ask the inherited file machinery to show me a short input line. There is no IR translation yet.",
    2: "I can read the input. Now I need to separate an operation name from its operand without losing my place. I shall try a lowercase `lit 7` and have the scanner show the two tokens it found. Later, quoted text will need its original spelling, so folding a token must leave the raw line available.",
    3: "The scanner can tell me what it read, but the finished translator must leave an assembly file on disk. I shall exercise the output path with a simple copy before asking it to generate instructions. The temporary-file and recovery rules inherited from the assembler will protect the last accepted result here too.",
    4: "The assembler used a table to recognize instructions. I want the translator to use the same idea, with a record that says what kind of operand each IR operation needs. I shall begin with `LIT` and inspect its argument class. Once that lookup works, an operation can select both its checks and its output pattern.",
    5: "The separate pieces are ready to work together. I want to enter a tiny IR program, read the assembly it produces, and assemble that text with the tool we already trust. `LABEL`, `LIT`, and `EXIT` are enough for a complete first program: find MAIN, produce a value, and return a DOS status.",
    6: "A program needs somewhere to keep values after an instruction finishes. I shall add named words and byte buffers, with declarations before the executable body. The first storage test only needs to prove that the declarations reach the assembly file and occupy the expected space; using their contents comes next.",
    7: "The declarations now reserve real bytes in the generated program. I want an IR operation to obtain the address of those bytes and another to read a word through it. Our test will fetch the value 65 from X and return it as the program's status. That gives the pointer path an observable result before we add display output.",
    8: "One accumulator can hold the current value, but a calculation often needs to keep an earlier value while finding the next one. I shall add a checked expression stack. The test saves seven, loads another seven, and subtracts them. This is the arrangement a compiler can later use for the two sides of an expression.",
    9: "Arithmetic can produce a value; now a program needs to decide where to go with it. I shall compare two saved values and branch on the result. The IR source will name only its intended destination. The backend will supply the native jump sequence needed to reach that destination.",
    10: "I can follow a pointer to read a word. I also need to change the word it names. I shall save a destination address on the expression stack, load the new value, and let PUT consume the saved address. Reading X afterward will show whether the store reached the right bytes.",
    11: "So far I have used the program's exit status to see what its calculations did. I want the generated program to put a character on the screen. PUTC will be our first small service binding: the IR supplies a byte value, and the runtime performs the output and remembers whether it succeeded.",
    12: "A word load was enough for the first storage test. Text and input buffers need one byte at a time. I shall add FETCHB and use it to read the first byte of a declared word, then pass that byte to PUTC. This also gives us a concrete check of the language's low-byte-first storage rule.",
    13: "A compiler must read a source file whose name can change from one run to the next. I shall let an IR program obtain a startup filename and ask OPEN for a readable handle. The program will keep an ordinary string pointer and an opaque handle; the entry binding and runtime will manage the DOS details.",
    14: "Opening an existing file gives us input. I also need a way to start an output file. CREATE will use the same handle table, with a writable slot for the new file. I shall first check that creation succeeds; writing the contents can then be tested separately.",
    15: "The file can be opened and the buffer can be declared. Now I want bytes to move between them. READ will take a handle, a buffer address, and a count, then return how many bytes actually arrived. I shall begin by requesting one byte from a known file so the returned progress is easy to check.",
    16: "The input side can transfer a counted block. I want the output side to make the same promise about actual progress. WRITE will receive a handle, a pointer, and a byte count. The first test asks it to write one byte; a later compiler can use that same operation to flush a whole output buffer.",
    17: "The generated program can now open, create, read, and write files. It also needs to finish its ownership of a handle explicitly. I shall add CLOSE and retire a slot only when the underlying close succeeds. That leaves a useful distinction between a handle that is finished and a failed operation that still needs attention.",
    18: "A compiler will need routines that call other routines while keeping their own temporary values. Shared scratch words will soon become difficult to manage. I shall add procedure declarations, parameters, and local slots, with a separate frame for each active call. The test will keep one expression operand while calling a procedure with its own parameter and local.",
    19: "The procedure machinery can carry values between calls. I want the word operations those routines will need for counts, masks, and character tests to have precise results too. This checkpoint completes the arithmetic and comparison set, including unsigned division and relations that produce exactly zero or one.",
    20: "A filename or diagnostic is awkward to spell as a row of numeric bytes. I shall let IR source contain quoted text and return a pointer to its terminated bytes. The generated code must branch around that inline storage as it runs. Our first literal will be small enough to follow from its spelling to the displayed character.",
    21: "Writing an output file is only part of finishing a compiler run. I want the compiler to be able to check a name, remove an obsolete file, and rename a completed temporary file into place. These services will give the later compiler the same tools for protecting accepted output that our native workbench already uses.",
    22: "The compiler's source and symbol records will need workspace beyond the bytes reserved in its main image. I shall add allocation and release through opaque block handles. The first test requests a 40 KiB block and frees it again. Accessing its contents will be a separate step, with bounds carried by the allocation.",
    23: "An allocated block is useful only when the program can reach its contents. I shall add byte and word access through a block handle and a byte offset, checking the complete extent before touching storage. The final test puts a word in the last two bytes of a 40 KiB block and reads it back. That is the workspace interface our compiler can now build on.",
}

AFTER_CHECKS = {
    1: "The displayed `ABC` gives me a working reader to keep. The source counters and file errors are already attached to it; the next step can concentrate on recognizing pieces of the line.",
    2: "`[LIT][7]` shows that the scanner found a complete operation spelling and a separate operand. I can now build the output side while keeping this small scanner test as an accepted stopping point.",
    3: "The five bytes in RESULT.ASM prove that a stream can pass through the writer and become a published file. It is still copied data. The next two steps will give that writer generated assembly to carry.",
    4: "The reported class one tells me that LIT was found as a complete name and that its record requests a numeric operand. I now have a place to describe the translation rules without adding another chain of name comparisons.",
    5: "The first complete path is in place: IR source became assembly text, and ASM86 turned that text into a program that returned zero. I save this translator before adding storage. Later operations will extend the same path.",
    6: "The generated image now includes the declared words and the 300-byte buffer. Its successful exit checks that the entry sequence reaches MAIN past those declarations. Next I want to read one of the values we have placed there.",
    7: "The test deliberately returns 65, so CHECK reports FAIL for this particular program. That status is the value we fetched, exactly as intended. It gives us evidence that ADDR and FETCH agree about where X lives and how its word is represented.",
    8: "The zero result checks that SUB combined the saved word with the current value. The expression stack is empty again at EXIT, ready for the control-flow checks we shall add next.",
    9: "The test reaches GOOD and returns zero after comparing the two sevens. Its IR contains only the program's own labels. I can leave the native branch arrangement to the backend when writing later compiler output.",
    10: "Returning 65 after loading X checks the whole store path: the saved pointer, the word write, and the later named load. CHECK's FAIL is expected for this fixture because 65 is its deliberate exit status.",
    11: "The displayed `A` comes from the program we generated. I no longer have to use a nonzero exit value just to observe a byte. The same output service will let the compiler print its own diagnostics.",
    12: "The `A` now came through FETCHB before reaching the console. A compiler can use that operation to inspect source characters without exposing a native byte register in its IR implementation.",
    13: "Passing the name A on the command line now leads to a successful open through ARG and OPEN. The test returns the service status. Later code can save the returned handle and then inspect STATUS to check whether it is usable.",
    14: "The successful CREATE gives us a writable handle and a real output file. I shall keep this small check while adding the counted transfers; a failure to create a file and a failure to move its bytes should remain distinguishable.",
    15: "The fixture checks that READ returned one byte of progress. A full reader will also inspect STATUS and keep consuming any short positive read before requesting more. The buffer's capacity and the file's length can now be separate concerns.",
    16: "The fixture accepts only a returned count of one. For a larger flush I shall need both the full requested count and a successful STATUS before treating the bytes as written. That is the condition the compiler's output routine can use.",
    17: "OPEN followed by CLOSE now returns a successful status. Together with the counted transfers, this gives an IR-written file routine an explicit beginning, progress, and finish for each handle it owns.",
    18: "The test keeps seven while TWICE doubles nine, then checks the combined result against twenty-five. That exercises the caller's saved operand, the callee's parameter and local, and the returned value in one short program. The compiler can now divide its parser into routines with their own state.",
    19: "The fixture divides 65535 by 255 and checks for 257. It returns zero when the comparison agrees. The compiler's calculations can now rely on the language's unsigned word rules while the backend handles their native implementation.",
    20: "The displayed `H` is the first byte fetched from the literal `Hi`. The literal keeps its case and supplies a terminated string pointer. I can use the same form for readable filenames and messages in the compiler source.",
    21: "The fixture confirms that EXISTS recognizes the file A. Together with DELETE and RENAME, the completed service set lets the compiler describe its own temporary-file and backup sequence and check each result before moving on.",
    22: "The allocation and release both succeeded. I save the handle rather than a segment address, so the next operations can validate it against the runtime's owned block table before accessing any bytes.",
    23: "The word round trip at offset 40958 reaches exactly the end of the 40960-byte allocation, and the test releases the block afterward. We now have storage, calls, text, files, and checked workspace for an IR-written compiler. In RILL0 I shall use this language to build that compiler's reader, symbol records, emitter, and parser.",
}
