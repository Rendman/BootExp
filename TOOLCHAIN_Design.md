# RILL toolchain construction

Status: implemented and verified.

The endpoint is RILL implementations of ASM86, IR86, and RILL, each rebuilt for two matching generations from the published BASIC/native ladder. No host compiler, assembler, or source-language translator supplies a bootstrap artifact.

IR86 keeps its word accumulator, byte-addressed storage, opaque services, and separate 8086/DOS backend. Extend its streamed native translator with procedures, indexed frame slots, argument calls, word multiply/divide/remainder/shifts, value comparisons, literal strings, and opaque allocated memory blocks. Source and output are streamed; closed temporary files are published through recoverable renames. The target remains a single COM image with the explicit EF00H image bound.

RILL gains general identifiers, global words and byte buffers, lexical local variables, parameters and recursive procedures, return values, full word expressions, strings, indexed byte storage, and portable file/memory services. Ordinary memory pointers and allocated-block handles are different interfaces. No physical register, segment, interrupt number, or DOS handle is exposed in the language.

The expanded compiler is initially implemented in IR86. Its RILL implementation must then compile itself without special syntax, embedded executable images, or a host-generated translation. The assembler and translator ports use the same general RILL features. Published construction must introduce every prerequisite before use and include exact edits, visible stopping checks, negative cases, and preserved sources at the handoffs.

## Measured result

| RILL implementation | COM bytes |
|---|---:|
| ASM86 | 32404 |
| IR86 | 31472 |
| RILL | 26625 |

The unchanged native assembler builds the 11577-byte IRWIDE bridge. Its output and native ASM86 build the 21818-byte IR-written compiler seed. The seed builds the three authored RILL tools, and two closed-loop generations reproduce every corresponding executable exactly. `pub_src/qa/toolchain/bootstrap_chain.py` also recreates the chain from canonical BOOTASM.BAS.

The DOS 3.10 test executes the published TMAKE.BAT on a private FAT16 hard-disk workbench, builds the seed and all nine tool executables, compares each with the bootstrap-built image, and compiles/executes HI through generation two. Native kernel checks are distinct from original period-hardware or historical BASIC-interpreter verification.

The compiler executes its own unchanged IR implementation in a processor-independent model with relocated data and different file/block handles. Native and model outputs agree on its self-compilation, complete language examples, and service effects. The model never emits assembly or executable bytes. Source layout scripts arrange authored IR/RILL/assembly and backend string tables; only the project tools translate bootstrap languages and encode instructions.

Construction remains gradual: 23 native IR, 47 IR-compiler, and 43 RILL-compiler saved sources, each with a measured stopping test. The continuation includes exact printed edits, complete tool source notebooks, eight short language programs, references, the self-build comparison, and the complete three-tool rebuild loop. Real limits are documented in the systems-language and streaming IR references.

## Compiler article collections

The first small RILL compiler keeps its own collection. RILLBOOT contains the 47 IR-written systems-compiler checkpoints and hands off RILLBOOT.IR/RILLBOOT.COM. RILL contains the 43 RILL-written compiler checkpoints, compiler self-builds, assembler port notebook, and complete three-tool rebuild loop. Both have independent workbenches, matching language references, complete programs, and source-only archives. Source filenames and earlier article links remain valid. Shared source production and native verification remain in tools and qa/toolchain; the combined TOOLCHN.ZIP remains the complete continuation archive.

Reader naming and validation: the native assemblers are ASM0, ASM1, and ASM86; the compiler stages are RILL0, RILLBOOT, and RILL. Existing production directory names and ASxx/Axx/Rxx/RBxx/RCxx checkpoint filenames remain stable. Canonical reader source archives are published under pub_src/site/static/downloads/tools. The naming map and descriptive article titles are maintained by pub_src/tools/publication_names.py.

Prefer inspecting the actual emitted file, with its exact length and bytes, when an addition has no retained display behavior. Do not add a formatting routine merely to display internal test state. A pure runtime helper may compare its result and return a status through the existing CHECK.BAT. Keep rejection tests relevant to the new behavior; do not repeat predecessor overflow and missing-file tests in every lesson. Retain natural compiler reports, meaningful program output, and final self-build comparisons.
