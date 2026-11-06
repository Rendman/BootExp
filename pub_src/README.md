# Bootstrap Experiment v2

BOOTASM, ASM86, ASM86A, IR86, RILL, and the local Hugo site are implemented here, following the current `BOOTSTRAP_Rules_and_Plan.md` and the decisions for this experiment.

GitHub Pages publication is configured in `../.github/workflows/pages.yml`. It builds and checks the site, then deploys the root `public/` directory after pushes to the repository's default branch. See the project-root [README](../README.md) for the one-time repository and Pages setup.

The published hierarchy is:

```text
The Bootstrap Experiment
├── BOOTASM
│   ├── The workbench
│   ├── 01–18: construction installments
│   ├── BOOTASM reference
│   └── Three complete programs
├── ASM86
│   ├── The assembly workbench
│   ├── 01–29: construction checkpoints
│   ├── 30: two generations of self-assembly
│   ├── ASM86 reference
│   └── Three complete programs
├── ASM86A
│   ├── The streaming assembler workbench
│   ├── 01–40: construction checkpoints, including both self-build handoffs
│   ├── 41: the complete bootstrap ladder
│   ├── ASM86A language and memory reference
│   └── Four complete assembly programs
├── IR86
│   ├── 23 streaming native translator checkpoints
│   ├── Streaming IR contract and complete RILL-written translator
│   ├── The IR workbench
│   ├── 01–32: translator construction checkpoints
│   ├── 33: complete translation pipeline and file copier
│   ├── IR86 language and translator reference
│   └── Four complete console/stream programs
└── RILL
    ├── 47 IR-written systems compiler checkpoints
    ├── 43 RILL-written compiler checkpoints
    ├── Complete language, examples, tools, and two closed-loop rebuilds
    ├── The RILL workbench
    ├── 01–29: IR-written compiler construction checkpoints
    ├── 30: complete RILL-to-executable pipeline
    ├── RILL language and compiler reference
    └── Four complete RILL programs
```

`site/` is the Hugo source. `../public/` (at the project root) is the generated static website. `workbench/bootasm/` contains the ASCII/CRLF period sources. `site/static/downloads/bootasm/BOOTASM.ZIP` is the 59-file reader source collection, without prebuilt executables or an interpreter.

From the project root, build with an installed Hugo:

```sh
hugo --source pub_src/site --cleanDestinationDir
```

The retained local Hugo binary is version 0.169.0. On Linux, this workspace's mount does not permit direct execution, so its small memory-backed launcher also works:

```sh
python3 pub_src/tools/hugo.py --source pub_src/site --cleanDestinationDir
```

Preview the output with:

```sh
python3 -m http.server 8096 --directory public
```

Open `http://localhost:8096/bootstrap/`. Relative resource URLs and explicit index-file navigation are enabled so the output can also be opened directly from a copied static directory. From the project root, start with `public/bootstrap/index.html`.

`tools/build_bootasm.py` maintains the authored BASIC patches, complete checkpoint copies, matching fixtures, and seventeen construction articles. The articles print exact source changes and the old surrounding lines. Run `tools/package_sources.py` after changing source or the printed examples, then rebuild Hugo. The other content pages are maintained directly as Markdown.

Production checks use Python 3.11 with PC-BASIC 2.0.7 in `tools/python-pcbasic207`, plus Unicorn 2.1.4 and Beautiful Soup 4.15.0 in `tools/python`. These execute and inspect the published tools; they do not replace a reader assembler:

```sh
python3.11 pub_src/qa/test_bootasm.py
python3 pub_src/qa/validate_site.py
```

The first runs the actual published BASIC source in a GW-BASIC-compatible interpreter and compares output to independently specified machine bytes. It runs only fixtures identified as complete executable programs in the CPU execution checks. The second reconstructs every checkpoint from its printed changes and checks the site, links, assets, archive, line endings, filenames, and editorial exclusions.

BOOTASM's results are in `qa/test-results.txt`: 64 BASIC/encoding/runtime/boundary test groups pass. Seven complete BASIC-produced programs were also run under the original COMPAQ DOS 3.10 system in QEMU, using the published CHECK.BAT. Their displayed text and PASS/FAIL reports match, including the deliberately nonzero FAIL program; see `qa/dos-program-results.txt`. This validates those executable outputs and the batch helper independently of BASIC interpreter compatibility.

## ASM86 production and verification

ASM86 lives in `workbench/asm86` and `site/content/bootstrap/asm86`, as a sibling collection. Its archive contains 86 source files, including BOOTASM.BAS, all 29 assembly checkpoints, accepted/rejected fixtures, the unchanged viewer/checker, and three examples. It contains no executable or interpreter. The native assembler is 2,622 bytes. The completed BOOTASM directly builds every ASM86 checkpoint within its published capacity. Both collections supply the identical BOOTASM.BAS source.

`tools/asm86_template.asm` holds the authored native routines. `tools/build_asm86.py` arranges the authored source fragments into checkpoints and the explanation manifest. It prepares source text, not machine code. `tools/write_asm86_articles.py` prints exact edits and context after checkpoint verification has recorded the real image sizes. The workbench, self-assembly article, reference, and examples are maintained directly. `tools/package_sources.py` refreshes all source collections without changing an archive whose contents already match. The publishing workflow packages and builds checked-in material; it does not reconstruct the assembler or rewrite articles.

BASIC verification uses Python 3.11 and PC-BASIC 2.0.7, installed locally under `tools/python-pcbasic207`. Install `pcbasic==2.0.7` into that directory with a Python 3.11 pip if reproducing these checks. Unicorn and Beautiful Soup remain in `tools/python`.

From the project root, using a Python 3.11 executable for the first command:

```sh
python3.11 pub_src/qa/asm86/bootstrap.py
python3 pub_src/qa/asm86/test_asm86.py
python3.11 pub_src/qa/asm86/basic_checkpoints.py
python3 pub_src/qa/asm86/test_limits.py
python3 pub_src/tools/write_asm86_articles.py
python3 pub_src/tools/package_sources.py
python3 pub_src/qa/asm86/test_examples.py
python3 pub_src/tools/hugo.py --source pub_src/site --cleanDestinationDir
python3 pub_src/qa/validate_site.py
```

Where Python 3.11 is managed by uv, `uv run --python 3.11 --no-project python` can replace `python3.11`. To regenerate source checkpoints first, run `tools/build_asm86.py` before this sequence. Regeneration clears measured image sizes; run the verification before rendering articles. The bootstrap command executes the published BOOTASM.BAS, making the first native ASM86.COM. The native checks then build/run every checkpoint and prove two identical self-assembly generations. The BASIC checkpoint check independently executes BOOTASM for every checkpoint and requires exact agreement with those native-built files. No outside assembler, compiler, linker, or machine-code generator supplies executable bytes.

The retained `qa/asm86/*-results.txt` records show all 29 construction checks, all 29 BASIC/native byte comparisons, 149 independent encoding/grammar/resource/I/O checks, and the three complete example tests passing. `validate_site.py` reconstructs the BASIC, ASM86, ASM86A, IR86, and RILL checkpoints from their exact printed edits, validates all six source bundles (811 sources in total), and checks links, assets, anchors, editorial exclusions, and all 303 HTML pages.

`tools/verify_asm86_dos.py` uses local historical DOS media, mtools, and QEMU for a separate DOS 3.10 check. The BASIC-produced ASM86 assembles SELF; SELF assembles AGAIN; both output files match the initial executable byte for byte. DOS COMP reports matching files, CHECK reports PASS for successful builds, and a bad register-width source reports the expected diagnostic and FAIL. Results are in `qa/asm86/dos-results.txt`; local disk images and raw logs are excluded from Git and publication. This verifies native DOS execution, not the unresolved original BASIC file-I/O environment described below.

## ASM86A production and verification

ASM86A is the third sibling collection and the inserted rung between ASM86 and IR86. Its forty construction checkpoints, ladder exercise, reference, and four complete programs have exact source downloads. The source-only archive contains 127 ASCII/CRLF/8.3 files, including unchanged BOOTASM.BAS, ASM86.ASM, VIEW.BAS, and CHECK.BAT. The original prompted assembler remains ASMKEEP.COM; the tested fixed-file successor is ASMAKEEP.COM.

The unchanged 2622-byte ASM86 directly builds the 3342-byte ASMA0 seed within its published source/symbol/output limits. The seed builds the 6422-byte ASM86A. Both reproduce their preceding-builder executable in two self-assembly generations. ASM86A streams 4 KiB blocks, stores 8192 symbols with 31-character names in eight DOS-allocated 40 KiB pages and an 8 KiB bucket block, and uses checked 32-bit source counters. Its main segment plus allocated blocks requires 392 KiB before DOS/environment/control overhead. The target remains one COM image, at most 61184 bytes; this limit is independent of source extent and assembler workspace.

The authored assembly is in `tools/asm86a_seed.asm`, `asm86a_memory.asm`, `asm86a_counts.asm`, and `asm86a_language.asm`. `build_asm86a.py` and `build_asm86a_series.py` arrange source text and explicit assembly branch bridges; they never encode instructions. `asm86a_installments.json` supplies explanations and fixtures. The article writer prints exact bottom-up edits with unchanged context and native-measured counts. All executable bytes come from the published BASIC and native project assemblers. New accepted source features are implemented using only the seed vocabulary.

Run from the project root after building the preceding native tools:

```sh
python3.11 pub_src/qa/asm86/bootstrap.py
python3 pub_src/tools/build_asm86a.py
python3 pub_src/qa/asm86a/test_checkpoints.py
python3 pub_src/qa/asm86a/test_asm86a.py
python3 pub_src/qa/asm86a/test_failures.py
python3 pub_src/qa/asm86a/test_programs.py
python3.11 pub_src/qa/asm86a/test_basic_fixtures.py
python3.11 pub_src/qa/asm86a/bootstrap_chain.py
python3 pub_src/tools/verify_asm86a_dos.py
python3 pub_src/tools/write_asm86a_articles.py
python3 pub_src/qa/asm86a/test_reader_exercises.py
python3 pub_src/tools/package_sources.py
python3 pub_src/tools/hugo.py --source pub_src/site --cleanDestinationDir
python3 pub_src/qa/validate_site.py
```

The BASIC checks use the same compatible interpreter/dependencies as the existing collection. Sequential BASIC text output includes its normal final Control-Z. LONGSRC.BAS and SYMS.BAS generate source text only, never executable bytes. Their actual output and the exact article capacity exercises are checked independently of the small stopping fixtures.

All forty native checkpoints pass build, exact acceptance, rejection, old-output preservation, and allocation cleanup. The independent suite passes 114 encoding/language/capacity checks, including 8192 symbols, overflow, full-spelling hash collisions, every symbol page, lines beyond 65535, source-block boundaries, and exact 61184-byte output. Nineteen failure and consistency tests cover partial allocation, memory shortage, open/read/write/short-write/close/rename/restore/delete/free failures, short successful reads, and changed pass-two definitions. The allocated-memory model poisons new RAM to detect reliance on implicit zero initialization. Four complete assembly programs and their exact rejection edits pass.

The full ladder executes canonical BOOTASM.BAS, recreates ASM86, builds ASMA0 and ASM86A, rebuilds published IR86 and RILL byte for byte, and runs a RILL program through IR and assembly to output HI. A separate DOS 3.10/QEMU run builds both assembler milestones and their self-generations, IR86, RILL, and the four complete programs with matching bytes and expected status/output. It also checks a source beyond 65535 lines, all 8192 definitions, exact maximum output, overflow preservation, and a native parent reserving memory so the child must report insufficient memory without replacing its result. Results remain in `qa/asm86a/*-results.txt`; private images and binaries are ignored. These checks do not resolve the original historical BASIC limitation documented below, and do not claim period-hardware execution.

The article validator reconstructs all forty checkpoints from the actual printed source blocks, verifies canonical aliases, fixtures, examples, BASIC text exercises, downloads, and archive contents. Publication refreshes archives and builds checked-in manuscripts; it does not run an outside compiler. The initial IR86 and RILL milestones retain their independent limits. The streaming and systems constructions below remove their complete-output buffers and build the full RILL toolchain.

Three original pencil cartoons were generated with the built-in Imagegen tool and inspected before copying into the site: a newspaper press, theater cloakroom, and stage bridge. Prompts and original file locations are in [qa/asm86a/image-prompts.md](qa/asm86a/image-prompts.md). The browser inventory was empty; HTML structure, links, anchors, assets, and source listings were checked locally without claiming a visual browser inspection.

## IR86 production and verification

IR86 lives in `workbench/ir86` and `site/content/bootstrap/ir86`. Its 6,407-byte native translator fits the completed ASM86 directly. The language defines virtual A, fixed sixteen-bit values, a value stack, declared storage, and processor-independent control flow. Its portable service API exposes byte streams, opaque handles, and ordinary STATUS values. There are no register-transfer, interrupt, or carry-flag operations in the language.

The 8086/DOS backend and runtime binding implement that contract. `tools/ir86_runtime.asm` holds the authored runtime fragments; `ir86_runtime_text.py` selects them. `qa/ir86/measure_runtime.py` uses the actual published ASM86 to measure their code/data sizes. The complete binding is 448 bytes and 42 definitions. Those resources are included in target accounting. No host assembler or instruction encoder supplies bytes.

`tools/ir86_core.asm` and `tools/ir86_installments.json` hold translator routines and authored manuscript/test specifications. `tools/build_ir86.py` prepares source checkpoints and backend text constants. `tools/write_ir86_articles.py` prints exact edits and actual native-produced results. `qa/ir86/language.json` records the portable operation forms; `backend-8086.json` keeps machine-byte and assembly-pattern details separate. The reference distinguishes the language from the target profile and includes the full binding source. The archive contains 143 ASCII/CRLF/8.3 sources, with identical bootstrap sources, all 32 checkpoints, fixtures, expected assembly, runtime source, four portable console/stream examples, and a file copier. No executable or historical interpreter is packaged.

The processor-independent reference interpreter in `qa/ir86/portable_machine.py` models A, byte storage, an expression stack, calls, streams, and file services without processor registers, flags, or DOS. Tests move its data to 4000H and 8000H and allocate handle tokens starting at 101 and 301, deliberately unlike the native layout. Identical source must produce matching output, status, and files. The interpreter never emits assembly or machine code and is not part of the reader bootstrap.

From the project root, use the dependencies above:

```sh
python3.11 pub_src/qa/asm86/bootstrap.py
python3 pub_src/qa/ir86/measure_runtime.py
python3 pub_src/tools/build_ir86.py
python3 pub_src/qa/ir86/test_checkpoints.py
python3.11 pub_src/qa/ir86/bootstrap_chain.py
python3 pub_src/qa/ir86/test_limits.py
python3 pub_src/qa/ir86/test_programs.py
python3 pub_src/tools/write_ir86_articles.py
python3 pub_src/tools/package_sources.py
python3 pub_src/tools/hugo.py --source pub_src/site --cleanDestinationDir
python3 pub_src/qa/validate_site.py
```

All 32 native checkpoints pass their acceptance/rejection and output-preservation checks. Valid complete-language fixtures also agree with the portable model. The independent suite passes 205 portable-contract and binding checks: word arithmetic and comparisons, pointer-based storage, stack boundaries, source/target resources, rejection of physical-register escapes, opaque handles, access modes, persistent status, EOF, zero counts, partial writes, and normalized errors. Each complete example runs unchanged in both models, including empty and binary stream/file cases. The printed example rejection edits are checked too.

`bootstrap_chain.py` executes canonical BOOTASM.BAS, verifies ASM86 self-assembly, builds the translator directly, and runs its generated output. `tools/verify_ir86_dos.py` separately rebuilds the translator and programs under local DOS 3.10 in QEMU. It compares the DOS-built code with the bootstrap-built code, checks all example displays/statuses, copies every byte value through the stream/file binding, checks missing-input failure, and checks preservation of rejected assembly output. These are native DOS checks, separate from the original BASIC interpreter limitation below. Results are retained in `qa/ir86/*-results.txt`.

Three new pencil cartoons were generated with the built-in Imagegen tool, inspected, and saved as `site/static/images/ir86-patterns.png`, `ir86-plates.png`, and `ir86-lock.png`. Their final prompts and original paths are in [qa/ir86/image-prompts.md](qa/ir86/image-prompts.md). The dressmaker, waiter, and canal keeper are distinct from the earlier collection's characters and settings.

Browser QA was unavailable: the computer-use inventory had no browser. No visual browser inspection is claimed.

## RILL production and verification

RILL is the fifth sibling collection. Its first compiler is written in portable IR86 and emits IR86. The unchanged published IR86 and ASM86 directly build the 5,173-byte native compiler. It uses 255 definitions and 24,676 bytes of assembly text, within existing limits. The language supports one main function, mutable word variables, + and -, unary minus, parentheses, if/else, while, putc, getc, status, and exit. The implementation is not self-hosted; its exact subset, limits, and reasons are in the language reference.

`tools/rill_parts.ir` is the authored complete IR implementation. `build_rill.py` only arranges those IR records and selected source variants into checkpoints; it does not parse RILL or encode instructions. Constant text is represented as authored IR literal data. `rill_installments.json` holds explanations and fixtures. `write_rill_articles.py` lays out exact edits and counts measured by the real translator and assembler. The source-only archive contains 160 files: canonical bootstrap sources, unchanged helpers, all checkpoints, diagnostic/accepted/rejected fixtures, native-produced IR/assembly, and four examples.

The compiler reads SOURCE.RIL and buffers accepted output before creating RESULT.IR. Its scanner compares exact keyword groups and its parser saves recursive state explicitly. All executable bytes come from the published tools. The semantic interpreter executes the same complete IR compiler with different address and handle representations; it never emits an artifact for the bootstrap chain.

From the project root, after the earlier tools are built:

```sh
python3 pub_src/tools/build_rill.py
python3 pub_src/qa/rill/test_checkpoints.py
python3 pub_src/qa/rill/test_rill.py
python3 pub_src/qa/rill/test_programs.py
python3.11 pub_src/qa/rill/bootstrap_chain.py
python3 pub_src/tools/verify_rill_dos.py
python3 pub_src/tools/write_rill_articles.py
python3 pub_src/tools/package_sources.py
python3 pub_src/tools/hugo.py --source pub_src/site --cleanDestinationDir
python3 pub_src/qa/validate_site.py
```

The bootstrap command executes canonical BASIC to recreate ASM86, verifies self-assembly, builds IR86, builds RILL from IR source, and compiles HELLO.RIL through IR and assembly to a COM displaying HI. All 29 checkpoint acceptance/rejection checks pass. The independent suite passes 119 language, portability, resource, rejection, and binding checks. Compiler sources run unchanged in the IR interpreter with data bases 4000H and 8000H and handle bases 101 and 301. All four full examples and their exact printed rejection edits pass. Empty, text, and binary echo cases preserve byte values.

The DOS 3.10 check rebuilds RILL using the bootstrap-produced IR86 and ASM86 under QEMU. Generated compiler assembly and machine bytes match; all four RILL programs compile, translate, assemble, and run with the expected outputs and PASS. Overflow and missing-input checks produce exact diagnostics and FAIL, older IR survives source rejection, and the compiled echo program preserves all 256 byte values. These tests do not resolve the original BASIC-interpreter limitation below. Results remain under `qa/rill/*-results.txt`; local disk images and raw DOS output are ignored.

The 29 printed edits reconstruct every exact compiler checkpoint. The site contains 303 HTML pages and 811 archived source files across the five collections and complete toolchain bundle. `validate_site.py` checks reconstruction, links, anchors, source downloads, archive contents, ASCII/CRLF/8.3 rules, and editorial exclusions. Publication refreshes source archives and builds checked-in articles; it does not run a host compiler or regenerate manuscripts.

Three selected pencil illustrations were made with the built-in Imagegen tool, inspected, and copied to `site/static/images/rill-tails.png`, `rill-drawers.png`, and `rill-paths.png`. The dog-show judge, cabinetmaker with apprentice, and gardeners use different characters and situations. Final prompts and original locations are in [qa/rill/image-prompts.md](qa/rill/image-prompts.md). No browser visual inspection is claimed; generated HTML structure, assets, and links are checked locally.

The original-interpreter check is not yet passed. A historical COMPAQ MS-DOS 3.10 disk supplied COMPAQ BASIC 3.11 (verified from its startup screen), but in the generic QEMU/SeaBIOS workbench that interpreter reports error 52 even for independent, minimal OPEN tests. The cause is not established. The same problem occurs with and without output redirection and with the supplied loader or standalone interpreter; it is not attributed to BOOTASM without evidence. Do not describe the collection as verified on original BASIC or period hardware. Diagnostic scripts and results remain under `qa/` and `tools/` so this compatibility check can be continued with the intended interpreter/workbench.

The earlier collections' illustration prompts and paths are in `qa/image-prompts.md` and `qa/asm86/image-prompts.md`. Production provenance and modern tooling details belong here, outside the magazine prose.

Historical technical references inspected during production:

- Intel Corporation, *The 8086 Family User's Manual*, October 1979, processor instructions and encodings: https://bitsavers.org/components/intel/8086/9800722-03_The_8086_Family_Users_Manual_Oct79.pdf
- Microsoft Corporation, *GW-BASIC Interpreter User's Guide*, June 1986, command-line options, sequential/random files, and error codes. This particular printing targets DOS 3.2; it is a language and file-behavior cross-check, not a claim about the DOS 3.10 runtime: https://bitsavers.trailing-edge.com/pdf/microsoft/gw-basic/410130001-320-R01-0686_Microsoft_GW-BASIC_Interpreter_Users_Guide_1986.pdf
- Original COMPAQ DOS distribution contents: https://www.pcjs.org/software/pcx86/sys/dos/compaq/3.10/
- Hugo configuration: https://gohugo.io/configuration/all/

None of the historical interpreter or DOS copies under QA is included in the website or the reader source archive. No outside assembler, compiler, linker, or machine-code generator was used to produce a reader executable. The bytes tested as programs came from executing the published BASIC and native assemblers; assembly translated from IR input came from executing the published IR86 translator.


## The self-hosting RILL toolchain

The current tools are authored RILL sources under `workbench/toolchain`: `RILL.RIL`, `IR86.RIL`, and `ASM86A.RIL`. Their measured executable sizes are 26625, 31472, and 32404 bytes. All three are first built through the native seed chain, then rebuilt twice using only the RILL-written compiler, translator, and assembler. Every corresponding executable matches byte for byte. `TOOLCHN.ZIP` contains 236 source files, including all 113 continuation checkpoints, exact fixtures/rejections, source notebooks, eight complete language programs, canonical bootstrap sources, unchanged helpers, and the reader's `TMAKE.BAT`.

The native bridge `workbench/ir86/IRWIDE.ASM` is 11577 executable bytes. `workbench/rill/RILLBOOT.IR` is an authored processor-independent compiler seed and builds to 21818 bytes. Neither is supplied as a prebuilt binary. The canonical old `IR86.ASM` and `RILL.IR` remain the earlier, separately named bootstrap milestones; their references and source counts describe those milestones. The main collection source icons now link to the complete RILL implementations.

`tools/ir86_wide.asm` and `ir86_wide_runtime.asm` contain authored native translator/binding routines. `build_ir86_wide.py` arranges inherited reader/publication helpers and authored backend text templates. `build_ir86_extensions.py` selects progressive operation and binding groups into IW01–IW23. `tools/rill_bootstrap.ir` contains the complete authored IR compiler; `build_rill_seed_series.py` selects routines and explicitly rejecting recursive placeholders into RB01–RB47. `tools/rill_self.ril` is the compiler in RILL; `build_rill_self_series.py` supplies RC01–RC43. Source ordering stays stable so a handoff does not require retyping the helper library.

`tools/ir86_port.ril` and `asm86a_port.ril` contain the two other authored RILL implementations. `prepare_toolchain_sources.py` arranges those routine blocks and authored operation/backend string tables. It does not parse RILL/IR or encode executable instructions. The full port source notebooks reproduce those exact sources by procedure. `write_toolchain_articles.py` prints exact bottom-up edits and native-measured reports; `write_toolchain_guides.py` prints complete port notebooks, self-build comparisons, and the reader batch.

RILL has 24-character folded names, 512 global/procedure records, sixteen parameters, sixteen simultaneously live local words, lexical scope restoration, word expressions, procedure recursion, strings, byte storage, and opaque file/block services. The compiler and translator stream 4096-byte blocks and publish closed temporary files through checked rename/recovery sequences. Ordinary pointers and indexing are deliberately unchecked; checked allocated-block access is a distinct API. These bounds suffice for the actual three tools without an ownership or memory-safety claim. The assembler retains its 8192-symbol and EF00H image contract.

From the project root, after the existing dependency setup:

```sh
python3 pub_src/tools/build_ir86_wide.py
python3 pub_src/qa/toolchain/common.py
python3 pub_src/tools/prepare_toolchain_sources.py
python3 pub_src/qa/toolchain/build_compiler.py
python3 pub_src/qa/toolchain/self_compiler.py
python3 pub_src/qa/toolchain/build_ports.py
python3 pub_src/qa/toolchain/rebuild.py
python3 pub_src/tools/build_ir86_extensions.py
python3 pub_src/qa/toolchain/test_ir_extensions.py
python3 pub_src/tools/build_rill_seed_series.py
python3 pub_src/qa/toolchain/test_rill_seed_series.py
python3 pub_src/tools/build_rill_self_series.py
python3 pub_src/qa/toolchain/test_rill_self_series.py
python3 pub_src/qa/toolchain/test_tools.py
python3 pub_src/qa/toolchain/test_language.py
python3 pub_src/qa/toolchain/test_boundaries.py
python3 pub_src/qa/toolchain/test_failures.py
python3 pub_src/qa/toolchain/test_examples.py
python3.11 pub_src/qa/toolchain/bootstrap_chain.py
python3 pub_src/tools/write_toolchain_articles.py
python3 pub_src/tools/write_toolchain_guides.py
python3 pub_src/tools/package_sources.py
python3 pub_src/tools/verify_toolchain_dos.py
python3 pub_src/tools/hugo.py --source pub_src/site --cleanDestinationDir
python3 pub_src/qa/validate_site.py
```

All 23 native IR, 47 IR-written compiler, and 43 RILL-written compiler stopping tests pass. The independent assembler checks cover 70 encodings, rejections, earlier native-source compatibility, executable examples, exact output limits, all 8192 definitions, and source beyond 65535 lines. Forty-three failure checks cover short positive reads, short writes, open/create/read/write/close/rename/delete, allocation/release, recovery names, and correct preservation/ownership. Language/boundary checks cover word arithmetic, argument order, saved expressions across calls, recursive frames, scopes, addresses, checked blocks, malformed strings, exact symbol/local/parameter/name limits, and decimal source diagnostics beyond 65535 lines. Comment skipping is iterative, so many comment lines do not consume one call frame each.

The independent `qa/toolchain/portable.py` executes the same unchanged IR compiler at data bases 2000H and 4000H with file and block handle values deliberately unlike the native binding. Its self-compilation output matches the native compiler exactly. Complete programs also agree on status, console output, and files; counted copying preserves empty input and all byte values. The model never generates bootstrap source or executable code.

`bootstrap_chain.py` executes canonical BOOTASM.BAS and recreates ASM86, ASMA0, ASM86A, IRWIDE, the IR-written compiler seed, all three RILL tools, and both closed-loop generations. The DOS check separately executes the exact published TMAKE.BAT under DOS 3.10 on a private 16 MiB FAT16 hard-disk workbench. All nine RILL-tool executables match the bootstrap-built images, and generation two compiles, translates, assembles, and executes HI. Private DOS disks, generated binaries, and intermediate build output are ignored. This does not resolve the historical BASIC 3.11 OPEN limitation documented above and is not a period-hardware claim.

The site and archive checks reconstruct all 113 continuation checkpoints from their actual printed blocks, verify canonical handoffs, exact source notebooks, example/rejection text, generated counts, source-only archives, ASCII/CRLF/8.3 rules, and all local links/assets/anchors. Existing collection illustrations are reused where their subject applies; no new collection or illustration-generation workflow is introduced.
