"""Reader-facing additions and removals at the front of each collection."""
import re

OVERVIEWS = {
 'link86': (
  [
   '**Two object modules:** Place MAIN.OBJ before UTIL.OBJ so independently described pieces can form one DOS .COM image.',
   '**Public names:** Collect complete exported spellings and module-relative offsets so one module can refer to a definition in the other.',
   '**Relative and absolute words:** Resolve near calls and loaded addresses while streaming so the output needs no backward patching.',
   '**Checked publication:** Validate both passes and publish a closed temporary file so rejected objects do not replace an accepted executable.',
  ],
  'None. The RILL compiler, IR86 translator and ASM86 assembler keep their existing languages and outputs; the object fixtures are entered as plain text.'),
 'bootasm': (
  [
   '**Named instructions and data:** Translate a small assembly vocabulary into bytes so programs can be entered and understood without calculating every opcode by hand.',
   '**Labels and two passes:** Resolve named addresses, including forward references, so inserting code does not require renumbering every branch destination.',
   '**Fixed work files and a BASIC implementation:** Read SOURCE.ASM and write RESULT.COM directly. Use the interpreter already on the workbench to create the first assembler without an outside assembler or compiler.',
   '**DOS program files and byte inspection:** Write runnable .COM files and inspect their contents so every small addition has a concrete result to check.',
  ],
  'None; this collection establishes the first assembler.'),
 'asm86': (
  [
   '**An assembler written in assembly:** BOOTASM builds a native .COM program that runs directly under DOS and can assemble its own source.',
   '**More source and output room:** Raise the bounds to 4,000 source lines and 8,192 emitted bytes so the native tool can handle larger construction sources.',
   '**OR instructions:** Extend the small arithmetic encoder with the operation used by the streaming assembler source.',
   '**DOS status and repeatable self-assembly:** Return success or failure to CHECK.BAT and compare two self-builds so accepted output and reproducible tool construction can be checked separately.',
  ],
  'No accepted BOOTASM instruction forms are removed. BOOTASM remains the builder of the first native executable.'),
 'asma0': (
  [
   '**Streamed input and output:** Work through 1 KiB blocks so source and executable size are independent of the resident file buffers.',
   '**Larger assembly capacity:** Retain 2,048 symbols and emit as many as 61,184 bytes so the seed can build a substantially larger assembler.',
   '**XOR and segment access:** Add segment-register MOV and ES overrides on the existing MOV memory forms so the assembler can work with separately allocated storage.',
   '**Checked publication:** Write a temporary file and use backup/recovery names so rejected source does not replace an accepted RESULT.COM.',
  ],
  'The complete-image output buffer; streaming removes the resident output-size bottleneck. The fixed SOURCE.ASM/RESULT.COM names are retained from ASM0. ES, CS, SS and DS also become reserved names so labels cannot be confused with the new segment-register operands.'),
 'asm86a': (
  [
   '**Allocated symbol storage:** Keep 8,192 definitions with names up to 31 characters, using complete-spelling lookup so larger translator and compiler sources fit.',
   '**Larger streamed text records:** Use 4 KiB file blocks, 1,023-character lines and checked 32-bit source counts so long sources can be processed with bounded resident buffers.',
   '**8086 addressing and frame operations:** Add legal base/index combinations, displacements, segment overrides and LEA so generated code can address parameters, locals and tables.',
   '**Data directives and expressions:** Add quoted DB text, EQU, RESB/RESW and address arithmetic so strings, constants and storage can be expressed without long numeric byte lists.',
   '**Arithmetic and distant conditions:** Add unsigned multiply/divide, logical shifts and explicit Jcc NEAR expansions so the backend can express word operations and reach distant labels with fixed instruction sizes.',
  ],
  'No ASM1 instruction forms are removed. The output remains a single DOS .COM image with the same 61,184-byte bound.'),
 'ir86': (
  [
   '**A processor-independent instruction language:** Define word values, a virtual accumulator and an expression stack so compilers can describe computations without naming physical registers.',
   '**Declared storage and byte addresses:** Supply words, byte buffers, strings and indirect access so generated programs can keep and manipulate their own data.',
   '**Procedure frames:** Name parameters and local slots, with up to sixteen parameters and sixty-four locals, so nested and recursive calls keep their state separate.',
   '**Portable service handles:** Provide counted file transfers, persistent status and checked allocated blocks so programs can process files and larger workspaces without exposing DOS descriptors or segments.',
   '**A separate 8086/DOS binding:** Emit assembly through bounded streams so the native implementation can build the compiler while keeping processor details outside the IR operations.',
  ],
  'No earlier IR operation forms are removed. PROC and RETURN add explicit call frames while LABEL remains available for branch destinations and the early flat programs.'),
 'rill': (
  [
   '**Structured source translated into IR:** Add a scanner and parser so expressions, assignments and control statements can be written directly instead of spelling out each IR operation.',
   '**Local names and lexical scopes:** Provide up to sixteen live local words, with slots reused at closing braces, so blocks can keep temporary state without permanent global scratch cells.',
   '**Expressions and branches:** Compile addition, subtraction, unsigned comparisons, if/else and while so the first language can express useful decisions and repeated work.',
   '**A continuing compiler implementation:** Establish the symbol records, bounded streams, parser and publication routines that RILLBOOT extends, keeping this first compiler a required working foundation.',
  ],
  'None. IR86 remains the compiler output language, and the first RILL language stays small enough to construct gradually.'),
 'rb': (
  [
   '**Word arithmetic and masks:** Add multiplication, unsigned division/remainder, bitwise AND/OR, right shift and logical negation so compiler calculations and character tests can be expressed.',
   '**Strings and global storage:** Add quoted text, mutable global words, byte buffers and byte access so the compiler can retain tokens, tables and output templates.',
   '**Named procedures and recursion:** Add parameters and separate call frames, with sixteen parameters and sixteen live locals, so the compiler can be divided into reusable and recursive routines.',
   '**File and workspace services:** Add counted transfers, file publication and checked allocated blocks so the compiler can process long source files and maintain its symbol table.',
   '**A compiler for its successor source:** Extend the accepted RILL0 implementation only far enough to compile the RILL-written compiler and its construction checkpoints.',
  ],
  'No accepted RILL0 language features are removed; every continuation retains the preceding compiler subset.'),
 'rc': (
  [
   '**The compiler written in RILL:** Express the scanner, tables, emitter and parser in the language accepted by RILLBOOT so the compiler implementation can be maintained with its own language.',
   '**Additional word and pointer operations:** Add XOR, left shift, unary minus, complement, address-of and ordinary word loads/stores so the translator and assembler implementations can express their data and encoding operations.',
   '**More local storage:** Build sixty-four live local slots and eighty active parameter/local name records into the storage and procedure lessons, keeping sixteen parameters, so larger functions fit the existing IR frame contract.',
   '**Matching compiler generations:** Establish the compiler using its own frame convention, then compare two further self-builds so the completed source reproduces its executable.',
  ],
  'No accepted RILLBOOT language features are removed. The native stack guard still bounds active calls even though each emitted procedure reserves a larger local frame.'),
 'toolchain': (
  [
   '**IR86 written in RILL:** Implement the established IR parser and native binding in RILL so the translator can be rebuilt by the RILL compiler.',
   '**ASM86 written in RILL:** Implement streamed assembly, symbol pages and instruction encoding in RILL so the assembler can join the same rebuild process.',
   '**An explicit bootstrap handoff:** Use the preserved native builders to establish the first RILL implementations so each replacement has a known source and builder.',
   '**Two complete rebuild generations:** Let the RILL-written compiler, translator and assembler rebuild all three tools and compare corresponding executables so the complete toolchain is reproducible.',
  ],
  "The rebuild generations' dependence on the native translator and assembler. The preserved native tools still establish the initial RILL builds; the accepted languages, encodings and image bounds remain the same."),
}

TITLE = "## What we're adding"
FOLLOWING = '## The construction'

def with_overview(group, text):
    """Keep one additions section immediately after the opening paragraph."""
    additions, removals = OVERVIEWS[group]
    section = TITLE+'\n\n'+'\n'.join('- '+item for item in additions)+'\n\n**Removing:** '+removals
    if TITLE in text:
        return re.sub(re.escape(TITLE)+r'\n.*?(?=\n\n'+re.escape(FOLLOWING)+r'\n)', lambda _: section, text, count=1, flags=re.S)
    header, body = text.rsplit('+++', 1)
    opening, separator, rest = body.strip().partition('\n\n')
    assert separator, group
    return header+'+++\n\n'+opening+'\n\n'+section+'\n\n'+FOLLOWING+'\n\n'+rest+'\n'
