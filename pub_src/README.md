# Bootstrap Experiment v2

BOOTASM's first collection and the local Hugo site are implemented here. The only project reference used was the current `BOOTSTRAP_Rules_and_Plan.md` and the decisions in this conversation.

GitHub Pages publication is configured in `../.github/workflows/pages.yml`. It builds and checks the site, then deploys the root `public/` directory after pushes to the repository's default branch. See the project-root [README](../README.md) for the one-time repository and Pages setup.

The published hierarchy is:

```text
The Bootstrap Experiment
├── BOOTASM
│   ├── The workbench
│   ├── 01–18: construction installments
│   ├── BOOTASM reference
│   └── Three complete programs
└── ASM86 (reserved introduction; implementation not started)
```

`site/` is the Hugo source. `../public/` (at the project root) is the generated static website. `workbench/bootasm/` contains the ASCII/CRLF period sources. `site/static/downloads/bootasm/BOOTASM.ZIP` is the 59-file reader source collection, without prebuilt executables or an interpreter. The final assembler has 213 BASIC lines. Its largest construction patch has 45 required BASIC lines; the initial byte exercise and viewer together have 39.

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

For production checks, the local Python dependencies are retained in `tools/python` (PC-BASIC 2.0.8, Unicorn 2.1.4, Beautiful Soup 4.15.0). They are verification tools, not a way to build any reader executable outside BASIC:

```sh
python3 pub_src/qa/test_bootasm.py
python3 pub_src/qa/validate_site.py
```

The first runs the actual published BASIC source in a GW-BASIC-compatible interpreter and compares output to independently specified machine bytes. It runs only fixtures identified as complete executable programs in the CPU execution checks. The second reconstructs every checkpoint from its printed changes and checks the site, links, assets, archive, line endings, filenames, and editorial exclusions.

The final results are in `qa/test-results.txt` and `qa/site-results.txt`: 64 BASIC/encoding/runtime/boundary test groups pass, and all 25 HTML pages and 59 packaged sources pass the structural checks. Seven complete BASIC-produced programs were also run under the original COMPAQ DOS 3.10 system in QEMU, using the published CHECK.BAT. Their displayed text and PASS/FAIL reports match, including the deliberately nonzero FAIL program; see `qa/dos-program-results.txt`. This validates those executable outputs and the batch helper independently of BASIC interpreter compatibility.

Browser QA was unavailable: the computer-use inventory had no browser, and starting the in-app browser returned “Browser is not available: iab.” No visual browser inspection is claimed.

The original-interpreter check is not yet passed. A historical COMPAQ MS-DOS 3.10 disk supplied COMPAQ BASIC 3.11 (verified from its startup screen), but in the generic QEMU/SeaBIOS workbench that interpreter reports error 52 even for independent, minimal OPEN tests. The cause is not established. The same problem occurs with and without output redirection and with the supplied loader or standalone interpreter; it is not attributed to BOOTASM without evidence. Do not describe the collection as verified on original BASIC or period hardware. Diagnostic scripts and results remain under `qa/` and `tools/` so this compatibility check can be continued with the intended interpreter/workbench.

Three original pencil cartoons were generated with the built-in Imagegen tool and copied into `site/static/images/`. Their retained prompts and paths are in `qa/image-prompts.md`. Production provenance and modern tooling details belong here, outside the magazine prose.

Historical technical references inspected during production:

- Intel Corporation, *The 8086 Family User's Manual*, October 1979, processor instructions and encodings: https://bitsavers.org/components/intel/8086/9800722-03_The_8086_Family_Users_Manual_Oct79.pdf
- Microsoft Corporation, *GW-BASIC Interpreter User's Guide*, June 1986, command-line options, sequential/random files, and error codes. This particular printing targets DOS 3.2; it is a language and file-behavior cross-check, not a claim about the DOS 3.10 runtime: https://bitsavers.trailing-edge.com/pdf/microsoft/gw-basic/410130001-320-R01-0686_Microsoft_GW-BASIC_Interpreter_Users_Guide_1986.pdf
- Original COMPAQ DOS distribution contents: https://www.pcjs.org/software/pcx86/sys/dos/compaq/3.10/
- Hugo configuration: https://gohugo.io/configuration/all/

None of the historical interpreter or DOS copies under QA is included in the website or the reader source archive. No outside assembler, compiler, linker, or machine-code generator was used to produce a reader executable. The bytes tested as programs came from executing the published BASIC listings.
