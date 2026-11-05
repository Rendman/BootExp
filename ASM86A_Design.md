# ASM86A: the capacity-building bootstrap step

Status: implemented and verified. The ASM86A collection has forty native construction checkpoints, a complete ladder exercise, a language/memory reference, and four complete programs. The published IR86 and RILL implementations retain their independent language and buffer limits.

## Position in the chain

```text
GW-BASIC -> BOOTASM -> ASM86 -> ASM86A -> expanded IR86 -> expanded RILL
```

ASM86A is a native 8086/8088 assembler, distributed as a DOS `.COM` program. Its first implementation is written in assembly accepted by ASM86. It removes the small assembler's output-buffer and symbol-storage ceilings before those ceilings shape the next languages.

There are two internal construction milestones, both in the ASM86A collection:

1. **ASMA0**, a streaming seed built directly by the unchanged ASM86.
2. **ASM86A**, the larger assembler built by ASMA0, then verified by self-assembly.

This distinction is necessary. ASM86 can build at most 8192 executable bytes with 256 symbols. An assembler built within those bounds can nevertheless stream a much larger executable to disk. Its own workspace and the program it assembles are separate things.

The unchanged ASM86 directly builds the 3342-byte ASMA0. ASMA0 builds the 6422-byte ASM86A. Both reproduce their initial executable in two self-assembly generations. Native DOS 3.10 checks also rebuild the tools, IR86, RILL, and complete example programs. The results are retained in `pub_src/qa/asm86a/`.

## Fixed files

| File | Role |
|---|---|
| `SOURCE.ASM` | Read-only source, reopened for each pass |
| `RESULT.COM` | Last successfully published executable |
| `ASMA.TMP` | Streamed output for the current assembly |
| `RESULT.BAK` | Previous executable during the final rename sequence |

Neither assembler prompts for a filename or reads command-line arguments. `COPY ASMA0.ASM SOURCE.ASM` selects an input. Fixed names are also the default for the expanded IR86 and RILL tools: `SOURCE.IR -> RESULT.ASM` and `SOURCE.RIL -> RESULT.IR`.

Retain the existing ASM86 filename prompt only for the initial seed build. No rewrite of a preceding tool is required.

## Streaming, two passes, and publication

The assembler retains one physical line, one input block, and one output block. It never retains the complete source or complete emitted image.

**Pass one:** read SOURCE.ASM sequentially; validate statement forms; collect definitions; count instruction/data sizes. Forward operand references may be unresolved, but anything affecting statement length must already be known. No output bytes are written.

**Pass two:** close and reopen SOURCE.ASM; reset every reader field and the location counter; resolve references; check short-branch ranges and definition consistency; stream bytes into ASMA.TMP through the output block. Every definition must agree with its first-pass kind/value, and the final image length must agree. No instruction shortening or branch relaxation changes statement lengths between passes.

The source must remain unchanged throughout both passes. Address/length checks detect some changes, not every possible same-size edit. Two passes do not require keyboard/pipe input: the input is a reopenable disk file, read incrementally.

Readers accept short successful reads and refill again; only zero bytes read means file EOF. Writers flush only a nonempty buffer, check carry and the actual write count, and treat a short write as failure. They never use a zero-length DOS write as a buffer flush. The final partial block and close must succeed before publication.

Publication rules:

1. Refuse to start if ASMA.TMP or RESULT.BAK already exists. Explain the reserved filename; do not erase an earlier recovery file automatically.
2. Create ASMA.TMP for this run after pass one succeeds. Track ownership and open-handle state separately.
3. On source/read/encoding failure, close and remove only this run's temporary output. An older RESULT.COM remains untouched. Report cleanup failures too.
4. After successful pass two, flush and close both files. If RESULT.COM exists, rename it to RESULT.BAK; rename ASMA.TMP to RESULT.COM; then remove RESULT.BAK.
5. If the second rename fails, try to restore the backup. If restoration fails, retain the recovery files and report their names. Do not report OK. If backup removal fails after publication, retain it and report failure rather than silently treating cleanup as complete.

DOS rename is not an atomic replace operation. The backup sequence preserves recovery options but is not a guarantee against power loss. Every stage in the chain still requires a fresh OK and immediate CHECK.BAT result before using an executable.

## Capacity contract

| Resource | ASMA0 seed | Complete ASM86A |
|---|---|---|
| Built by | Unchanged ASM86 | ASMA0, then itself |
| Initial source restrictions | ASM86's 256 symbols, 4000 lines, 120 characters, 16-character names; image at most 8192 bytes | Source stays within ASMA0's language and bounds |
| Input/output blocks | 1024 bytes each | 4096 bytes each |
| Symbol capacity | 2048 | 8192 |
| Symbol spelling | 16 characters | 31 characters |
| Physical input line | 120 characters | 1023 characters, plus terminator |
| Token buffer | 16 characters plus terminator | 63 characters plus terminator |
| Source extent | Checked 16-bit line count, at most 65535 lines per pass | Checked 32-bit byte and physical-line counts; no small whole-file buffer limit |
| Emitted `.COM` image | At most 61,184 bytes | At most 61,184 bytes |
| Location counter | 0100H through F000H, without wrap | Same |
| Expression nesting | Existing simple value syntax | At most 16 nested expression levels |

61,184 is EF00H: offsets 0100H–EFFFH contain the maximum image, and F000H–FFFFH remain reserved for a generated program's stack. F000H is a valid one-past-image end label. An additional emitted byte is rejected. This is a chosen safe `.COM` profile, not an 8 KB implementation buffer.

Assembler workspace is not part of the target image. A small source may emit a large zero-filled region; a very large source may emit very little. Source extent and output extent are checked independently. RESW multiplication and all output-size additions are checked before narrowing to a word.

An empty source may produce a zero-byte file for inspection. It is not an executable test. Files beyond the `.COM` profile and larger executable formats remain outside this step.

## ASMA0 memory layout

The seed executes entirely in its original 64 KB DOS segment. It needs no allocated symbol pages.

| Offsets | Use |
|---|---|
| 0000H–00FFH | PSP |
| 0100H–3FFFH | Resident code, constants, and scalar state; initial ASM86-built image still at most 8192 bytes |
| 4000H–4078H | 120-character line and zero |
| 4080H–4090H | Token and zero |
| 4100H–41FFH | Saved operand/name state and work space |
| 4200H–45FFH | 1024-byte input block |
| 4600H–49FFH | 1024-byte output block |
| 4A00H–4FFFH | Reserved work space; no image growth into it |
| 5000H–EFFFH | 2048 twenty-byte symbol records, exactly 40,960 bytes |
| F000H–FFFFH | Native stack reservation |

Unused gaps remain reserved. Validate a full segment before using the high workspace. The seed's resident-image ceiling is 16,128 bytes; its first build is subject to ASM86's smaller 8192-byte ceiling. Neither ceiling limits the image being assembled to disk.

The seed retains ASM86's accepted forms and adds only what the larger assembler implementation needs immediately: MOV between ordinary word and segment registers, excluding CS as a destination, and ES overrides on the existing MOV memory forms. Its implementation uses only ASM86-accepted instructions. Encoding a new instruction is distinct from executing that instruction in the assembler itself.

The first complete ASM86A source uses this seed vocabulary, names no longer than sixteen characters, and lines no longer than 120 characters. Larger source-language features are implemented by that source; they are not prerequisites for assembling it.

## Complete ASM86A memory layout

The executable keeps CS, DS, and SS in its original segment and uses near calls. ES selects separately allocated DOS work blocks. This permits more workspace without `.EXE` files, far-call program structure, or hardware beyond the 8086/8088.

| Main-segment offsets | Use |
|---|---|
| 0000H–00FFH | PSP |
| 0100H–BFFFH | Resident code and static data: at most 48,896 bytes |
| C000H–C7FFH | Reserved workspace; allocation descriptors, scalar state, and operand descriptors are in the loaded image |
| C800H–CBFFH | 1023-character line and zero |
| CC00H–CC3FH | Token and zero |
| CC40H–CFFFH | Saved names, bounded parser work space |
| D000H–DFFFH | 4096-byte input block |
| E000H–EFFFH | 4096-byte output block |
| F000H–FFFFH | 4096-byte stack reservation |

Startup verifies the owned allocation covers the full main segment, establishes its stack there before shrinking memory, and retains that segment with DOS Set Block, function 4AH. It allocates eight symbol pages with function 48H, plus one bucket block. It stores every returned segment and handles partial-allocation failure. It releases owned blocks with function 49H on ordinary cleanup; process termination is the final DOS cleanup boundary.

Initialize allocation descriptors, counters, reader/writer state, and every bucket head explicitly. Newly allocated RAM and workspace outside the loaded image are not assumed to contain zeroes. Initialize every inserted record, including its name padding and links; unused record slots need not be read or cleared.

| Separate allocation | Amount |
|---|---|
| Eight symbol pages | 1024 records × 40 bytes per page = 40,960 bytes = A00H paragraphs each |
| Hash buckets | 4096 word heads = 8192 bytes = 200H paragraphs |
| Total symbols | 327,680 bytes = 320 KiB |
| Main segment + pages + buckets | 401,408 bytes = 392 KiB, excluding allocation-control overhead and environment storage |

This fits the reference machine's 640 KB conventional-memory design with room for DOS, but allocation success must be tested in the actual environment. Report insufficient memory before opening output; do not write beyond a reduced allocation. The initial full profile requires all eight pages, so its published capacity does not silently vary with free RAM. ASMA0 remains the low-memory bootstrap tool.

Allocation and normal symbol-definition/value operations restore ES to the main data segment. Internal SYMPTR deliberately returns ES:BX selecting a record; RECORDWRITE temporarily leaves ES selecting the bucket block. Their callers restore ES before ordinary string or publication work, including cleanup paths. In particular, DOS rename receives the destination in the main segment through ES:DI, and memory-management calls receive their required block segment. Ordinary string helpers can therefore continue to use ES=DS. DOS file buffers and ordinary state stay in DS. Save an offset and its page selector together inside page helpers; an offset alone is not a pointer into an arbitrary symbol page. Registers and pages are private assembler implementation details, not additions to IR language semantics.

## Symbol representation and lookup

Each forty-byte record contains:

| Bytes | Field |
|---|---|
| 0–31 | Uppercase name, at most 31 bytes, then zero and padding |
| 32–33 | Sixteen-bit value |
| 34–35 | Next symbol ID in its bucket, zero for none |
| 36–37 | Definition/pass-state flags |
| 38–39 | Symbol kind: loaded label or absolute EQU constant |

IDs are 1–8192; zero is the empty marker. Subtract one, divide by 1024 for the page index, and multiply the remaining index by forty for the offset. The last record ends within its own A000H-byte allocation; records never cross a segment boundary.

A simple sixteen-bit name hash selects one of 4096 buckets. Every candidate is compared against the complete stored spelling. Collisions never establish identity. Separate chaining uses record IDs and does not require an extra link allocation. All defined symbols are retained between passes; unresolved references do not consume placeholder records on pass one.

Pass two rejects undefined symbols, duplicate definitions, changed definition values/kinds, and inconsistent final length. No symbol eviction, disk swapping, host-generated symbol map, or outside assembler supplies missing definitions. Diagnostics report the current full source line; records do not truncate a saved line number to sixteen bits.

## Language additions for the expanded tools

Retain ASM86 forms and fixed instruction encodings so the published project sources remain accepted with identical bytes. Document the newly reserved segment-register names; do not claim every conceivable old source using those names as labels remains compatible. Add capabilities in separately tested groups:

- **Data and constants:** DB quoted byte strings with case preserved and doubled quotes for a literal quote; existing numeric DB/DW lists; zero-materializing RESB/RESW; earlier-resolved EQU constants; `$`; unary plus/minus and parenthesized addition/subtraction. Counts and constants affecting layout must resolve in pass one. Forward/cyclic EQU definitions are not supported.
- **Segment access:** the seed's segment-register moves and ES override, followed by explicit segment overrides on supported memory operands. MOV to CS is rejected.
- **Addressing and frames:** the legal 8086 BX/BP/SI/DI effective-address combinations, direct addresses, and displacements; LEA; near indirect CALL/JMP; RET with a word operand. A written displacement uses a fixed word encoding; the special bare [BP] form uses its required zero displacement. No pass-dependent displacement shortening.
- **Word/byte operations:** ADC/SBB, TEST, NEG/NOT, unsigned MUL/DIV, signed one-operand IMUL/IDIV, and 8086 shifts/rotates by one or CL. Register/immediate forms come first, then memory forms with explicit width where no register supplies it.
- **Byte movement:** LODSW/STOSW, MOVSB/MOVSW, and REP on explicitly supported string forms. No arbitrary prefix combinations are accepted.
- **Conditional transfers:** existing short branches and clear aliases such as JZ/JNZ, plus explicit `Jcc NEAR label`. The NEAR form is an opposite short branch over a three-byte near JMP: five bytes, no extra symbol-table entry. It is an assembler expansion, not a later-CPU near-conditional opcode. Ordinary Jcc remains short and range-checked.

No PUSH immediate, two-/three-operand IMUL, immediate shift count other than one, or other later-CPU encoding is silently admitted. Additional CPU forms are not accepted merely because an emulator can run them.

The reader preserves raw text case. The scanner folds names and mnemonics only outside quoted strings; semicolons within strings are data. Strings are read directly from the bounded physical line rather than forced through the ordinary token buffer. ASCII, CR/LF, bare CR/LF, a final unterminated text line, and source Control-Z have explicit tests.

Layout values are evaluated as words with checked context-specific narrowing. In particular, unary -1 forms FFFFH for a word; a byte context still requires 0–255. Includes, macros, conditional assembly, object records, relocations, multiple code segments, and a linker are outside the initial ASM86A collection.

## Gradual construction order

The published construction splits these capability groups into forty checkpoints, with separate seed and full self-assembly handoffs.

1. Fixed source name and an owned temporary-file copy diagnostic; inspect file length and bytes rather than executing copied data.
2. Block input, with EOF, short reads, and boundary-crossing line endings.
3. Block output, final partial flush, short writes, and close failures.
4. Fixed result publication and recovery handling.
5. Two-pass driver using the accepted ASM86 grammar; streamed emission replaces the complete image buffer.
6. Larger in-segment symbol table; demonstrate definitions beyond 256 and output beyond 8192 bytes.
7. Seed segment-MOV and ES-memory encodings, accepted without using them in the seed implementation.
8. ASMA0 direct build and two matching self-assembly generations. This is the first mandatory bootstrap gate.
9. A small allocated-memory diagnostic, built by ASMA0, followed by page-boundary symbol storage and cleanup.
10. Exact-spelling bucket lookup, 8192-symbol capacity, long names, longer lines, and checked word-pair source counters.
11. Quoted data and constants, followed by addressing, arithmetic, and string-operation families in small additions.
12. Explicit long conditional expansion, full compatibility checks, two matching ASM86A self-assemblies, and the complete chain.

Preserve working executables before each handoff. No new source instruction may be used until its builder accepts it. If a seed source exceeds ASM86's limits, move nonessential feature additions past the seed's self-build; do not change ASM86's published capacity or use an outside encoder.

## Acceptance gates

- Execute canonical BOOTASM.BAS to build ASM86; use that ASM86 to build ASMA0 directly. Verify both seed self-assembly generations match its initial executable.
- Build the complete ASM86A from ASMA0. Two ASM86A self-assembly generations must match the seed-produced executable, with deterministic encodings.
- Reassemble the existing ASM86, IR86, and RILL-generated assembly and require identical bytes. New forms are opt-in; compatibility is a measured result.
- Prove source streaming beyond 64 KB, beyond 65535 lines, and across every block/line/token boundary. The seed has its separately stated line bound.
- Prove exactly 8192 distinct definitions, lookup of the final record on every page, deliberate bucket collisions, and rejection of definition 8193. Verify long names differing only at the final character.
- Prove exactly EF00H emitted bytes and rejection of one extra byte, PC arithmetic without wrap, large reserves, and final partial/empty output.
- Prove boundary short branches and exact five-byte NEAR expansions without synthetic symbols or non-8086 opcodes.
- Inject memory, open, read, write, close, rename, restore, and cleanup failures. Preserve prior output/recovery files as specified and never print a false OK.
- Execute representative assembler outputs and the assembler itself under DOS 3.10, with allocation sentinels and explicit shortage tests. Keep complete-program tests separate from encoding-only data fixtures.
- Reconstruct every checkpoint from its printed edits; package ASCII/CRLF/8.3 sources, never prebuilt executables. Modern verification may execute and inspect these tools but must not encode a bootstrap artifact.

## Handoff to IR86 and RILL

Assembler capacity alone does not remove the later tools' independent limits. ASM86A passes the construction gates. The separate expansion work for IR86 and RILL is:

1. Have IR86 read SOURCE.IR incrementally and stream RESULT.ASM through its own temporary file. Remove its 32 KB whole-output buffer and its inherited 8192-byte/256-definition target assumptions. Keep genuine target image and symbol limits explicit.
2. Use ASM86A's NEAR conditional forms so the backend does not consume a public symbol for every comparison skip. Expand backend addressing/runtime support without exposing processor registers or DOS conventions in the IR contract.
3. Define the IR procedure/frame, indexed storage, and allocation interfaces needed by a larger RILL before selecting the RILL grammar. Keep portable word/pointer/handle semantics separate from native storage representation.
4. Replace RILL's 1024-byte result buffer, twenty-six single-letter-variable table, and restrictive parser-state organization with streaming emission, general identifiers, real scopes/symbol tables, procedures, parameters, local storage, and indexed data. Do not merely increase one buffer and call the language expanded.

The initial `.COM` execution profile still has a real near-code/image limit. Extra allocated workspace makes larger compilers practical; it does not turn a `.COM` file into an unlimited or multisegment executable. Linker and executable-format work remains a separate milestone.

## Production reference

Memory allocation, block resizing, handle I/O, and rename behavior are checked against Microsoft, *MS-DOS 3.10 Programmer's Reference Manual*, November 1984, memory-management overview and functions 3CH–41H, 48H–4AH, and 56H. The [archived original manual](https://ftpmirror.your.org/pub/misc/bitsavers/pdf/microsoft/msdos_3.10/8411-310-02_MSDOS_3.10_Programmers_Reference_Manual_1984.pdf) is a production reference; reader-facing articles should cite its printed title and sections rather than a web address.
