# Bootstrap Experiment v2

BOOTASM, ASM86, IR86, and the local Hugo site are implemented here, following the current `BOOTSTRAP_Rules_and_Plan.md` and the decisions for this experiment.

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
└── IR86
    ├── The IR workbench
    ├── 01–26: translator construction checkpoints
    ├── 27: complete translation pipeline and file copier
    ├── IR86 language and translator reference
    └── Three complete programs
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

The retained `qa/asm86/*-results.txt` records show all 29 construction checks, all 29 BASIC/native byte comparisons, 149 independent encoding/grammar/resource/I/O checks, and the three complete example tests passing. `validate_site.py` reconstructs the BASIC, ASM86, and IR86 checkpoints from their exact printed edits, validates all three archives (261 sources in total), and checks links, assets, anchors, editorial exclusions, and all 89 HTML pages.

`tools/verify_asm86_dos.py` uses local historical DOS media, mtools, and QEMU for a separate DOS 3.10 check. The BASIC-produced ASM86 assembles SELF; SELF assembles AGAIN; both output files match the initial executable byte for byte. DOS COMP reports matching files, CHECK reports PASS for successful builds, and a bad register-width source reports the expected diagnostic and FAIL. Results are in `qa/asm86/dos-results.txt`; local disk images and raw logs are excluded from Git and publication. This verifies native DOS execution, not the unresolved original BASIC file-I/O environment described below.

## IR86 production and verification

IR86 lives in `workbench/ir86` and `site/content/bootstrap/ir86`, beside the two assembler collections. Its final native image is 3,871 bytes and directly fits the completed ASM86. The language has 48 operations covering accumulator/stack computation, storage, pointers, control flow, procedures, and DOS. Its archive contains 116 source files, including identical published bootstrap sources, all 26 native construction checkpoints, accepted/rejected IR inputs, native-produced expected assembly, helpers, three console examples, and the complete file-copy program. No executable, external runtime, or historical interpreter is packaged.

`tools/ir86_core.asm` holds the authored translator routines. `tools/ir86_installments.json` holds the authored explanations, fixtures, and checkpoint specifications. `tools/build_ir86.py` arranges those routines and the existing published ASM86 helpers into source checkpoints; its template data is ASCII assembly text, not encoded instructions. Only the published native assemblers emit machine code. `tools/write_ir86_articles.py` lays out exact bottom-up source edits, native-produced target text, and measured counts after verification. The cover, workbench, pipeline article, and reference are maintained directly. Example IR sources live in the workbench; the example article is rendered from those tested sources.

For a fresh verification run, use the same Python 3.11/PC-BASIC and native-execution dependencies documented above. Native executables must be rebuilt from the source chain before use:

```sh
python3.11 pub_src/qa/asm86/bootstrap.py
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

The checkpoint test executes ASM86 to build every translator, executes each translator, and assembles its actual output with ASM86. Only complete generated programs are executed. Each acceptance/rejection test checks visible output and preservation of an older assembly file on rejection. The independent suite passes 183 semantics, grammar, capacity, memory, and DOS-I/O cases, including all comparison orders, word wrapping, expression boundaries, generated-name accounting, exact image capacity, source/text limits, delegated assembler errors, and short writes. The printed example rejection edits are tested too. Results are retained under `qa/ir86`.

`bootstrap_chain.py` separately executes the canonical BOOTASM.BAS to build ASM86, verifies that assembler's self-assembly, builds IR86 directly with it, and runs an IR86-generated target. `tools/verify_ir86_dos.py` runs the native ASM86 → IR86 → assembly → program sequence under the original local DOS 3.10 system in QEMU. The DOS-built translator, generated assembly, and executable programs match every byte of the bootstrap-tested versions. Console/procedure/pointer programs display the expected output. The file copier preserves text and all 256 byte values, and a missing input reports FAIL. The IR underflow rejection reports its exact diagnostic and leaves old assembly untouched. This native DOS evidence is separate from original BASIC interpreter compatibility.

Three new pencil cartoons were generated with the built-in Imagegen tool, inspected, and saved as `site/static/images/ir86-patterns.png`, `ir86-plates.png`, and `ir86-lock.png`. Their final prompts and original paths are in [qa/ir86/image-prompts.md](qa/ir86/image-prompts.md). The dressmaker, waiter, and canal keeper are distinct from the earlier collection's characters and settings.

Browser QA was unavailable: the computer-use inventory had no browser. No visual browser inspection is claimed.

The original-interpreter check is not yet passed. A historical COMPAQ MS-DOS 3.10 disk supplied COMPAQ BASIC 3.11 (verified from its startup screen), but in the generic QEMU/SeaBIOS workbench that interpreter reports error 52 even for independent, minimal OPEN tests. The cause is not established. The same problem occurs with and without output redirection and with the supplied loader or standalone interpreter; it is not attributed to BOOTASM without evidence. Do not describe the collection as verified on original BASIC or period hardware. Diagnostic scripts and results remain under `qa/` and `tools/` so this compatibility check can be continued with the intended interpreter/workbench.

The earlier collections' illustration prompts and paths are in `qa/image-prompts.md` and `qa/asm86/image-prompts.md`. Production provenance and modern tooling details belong here, outside the magazine prose.

Historical technical references inspected during production:

- Intel Corporation, *The 8086 Family User's Manual*, October 1979, processor instructions and encodings: https://bitsavers.org/components/intel/8086/9800722-03_The_8086_Family_Users_Manual_Oct79.pdf
- Microsoft Corporation, *GW-BASIC Interpreter User's Guide*, June 1986, command-line options, sequential/random files, and error codes. This particular printing targets DOS 3.2; it is a language and file-behavior cross-check, not a claim about the DOS 3.10 runtime: https://bitsavers.trailing-edge.com/pdf/microsoft/gw-basic/410130001-320-R01-0686_Microsoft_GW-BASIC_Interpreter_Users_Guide_1986.pdf
- Original COMPAQ DOS distribution contents: https://www.pcjs.org/software/pcx86/sys/dos/compaq/3.10/
- Hugo configuration: https://gohugo.io/configuration/all/

None of the historical interpreter or DOS copies under QA is included in the website or the reader source archive. No outside assembler, compiler, linker, or machine-code generator was used to produce a reader executable. The bytes tested as programs came from executing the published BASIC and native assemblers; assembly translated from IR input came from executing the published IR86 translator.
