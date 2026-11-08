# Bootstrap Experiment source and verification

Reader hierarchy: BOOTASM -> ASM0 -> ASM1 -> ASM86 -> IR86 -> RILL0 -> RILLBOOT -> RILL, followed by the toolchain in RILL, LINK86 and EDIT86. Site source is site/, generated HTML is ../public/, period source is workbench/, manuscript arrangement is tools/, and verification is qa/. Collection directories use current tool names throughout. tools/project_paths.py translates retained construction metadata keys to those directories; tools/publication_names.py maintains source naming and published routes.

Every bootstrap executable comes from published BASIC or project assemblers/translators/compilers. Source arrangement scripts select authored text and backend templates; they never parse a bootstrap language or encode machine instructions. Archives contain ASCII/CRLF/8.3 source, fixtures and inspection helpers, without executables or historical interpreters.

## Directory layout

| Directory | Contents |
|---|---|
| `site/content/bootstrap/<tool>/` | Article manuscripts, using current tool names |
| `site/layouts/`, `site/static/css/`, `site/static/images/` | Hugo templates, styles and illustrations |
| `site/static/downloads/tools/<reader-name>/` | Current reader-facing source files and archives |
| `site/downloads/<tool>/` | Archive staging sources mounted at supported earlier download URLs |
| `workbench/<tool>/` | Period source listings, fixtures and build products |
| `tools/` | Authored implementation text, manuscript arrangement and packaging tools |
| `qa/` | Verification commands, manifests and recorded results |
| `../public/` | Generated HTML at the repository root |

Tool directories are bootasm, asm0, asm1, asm86, ir86, rill0, rillboot, rill, toolchain, link86 and edit86. The manuscript, workbench, archive staging and reader-download trees use these names. QA uses the same names where a collection has its own checks; shared compiler checks live in qa/compilers and qa/toolchain. Construction checkpoint filenames such as AS28.ASM, A12.ASM, RB12.IR and RC43.RIL remain stable.

Hugo mounts site/downloads/<tool> at the earlier download addresses; explicit article URLs preserve existing article links after the manuscript directories move. Canonical reader downloads remain in site/static/downloads/tools/<tool>. The retained metadata keys describe those earlier constructions and URLs; project_paths.py translates them only when locating files.

BOOTASM construction checks live directly under `qa/`; original-interpreter verification uses `qa/bootasm`; the compiler collections share `qa/compilers` and `qa/toolchain`. Other collection checks use their own subdirectories. Local dependencies under `tools/python*`, DOS test directories, generated executables and interpreter caches are ignored development material. They are not source archive members or website input.

Packaging removes obsolete generated seed stages from the RILLBOOT/toolchain workbenches and toolchain archive staging while preserving the current shared assembly listings. `qa/validate_directories.py` checks the directory sets, source aliases, shared inputs and root publication destination. The website validation runs it too. The established `qa/toolchain/validate_publication.py` and `qa/compilers/validate_publication.py` commands delegate to the current continuing-ladder checks.


| Source directory | Tool | Complete reader source |
|---|---|---|
| `workbench/bootasm` | BOOTASM | `BOOTASM.BAS` |
| `workbench/asm0` | ASM0 | `ASM0.ASM` (internal `ASM86.ASM`) |
| `workbench/asm1`, `workbench/asm86` | ASM1 seed | `ASM1.ASM` (internal `ASMA0.ASM`, A12) |
| `workbench/asm86` | Native ASM86 | `ASM86.ASM` (internal `ASM86A.ASM`, A40) |
| `workbench/ir86` | Native IR86 | `IR86.ASM`, identical to `IRWIDE.ASM` and IR23 |
| `workbench/rill0` | RILL0 | `RILL0.IR` (internal `RILL.IR`, R39) |
| `workbench/toolchain`, `workbench/rillboot` | RILLBOOT | `RILLBOOT.IR`, identical to RB12 |
| `workbench/toolchain`, `workbench/rill` | RILL compiler | `RILL.RIL`, identical to RC43 |
| `workbench/toolchain` | RILL-written tools | `IR86.RIL`, `ASM86.RIL` (internal `ASM86A.RIL`) |
| `workbench/link86` | LINK86 | `LINK86.RIL`, identical to L10 |
| `workbench/edit86` | EDIT86 and service editions | `EDIT86.RIL`, `RILLED.RIL`, `IRED.RIL`, `EDITRT.ASM` |

Canonical reader downloads live under `site/static/downloads/tools/<tool>/`. Archive staging folders use current tool names; Hugo preserves their earlier published download routes. The RILL0 archive is `RILL0.ZIP`; the final compiler archive is `RILL.ZIP`. Generation-zero `workbench/toolchain/RILL0.IR` is generated IR for the full RILL compiler, distinct from the initial compiler's authored `workbench/rill0/RILL.IR`.

## Continuing source constructions

- build_bootasm.py and build_asm86.py arrange the BASIC foundation and ASM0. ASM0 has only the vocabulary needed to build ASM1; ASM1 adds XOR for ASM86.
- build_asm86a_series.py arranges twelve ASM1 and twenty-four ASM86 checkpoints. The omitted unary, signed arithmetic, rotate, repeat/string and branch-alias rows are not needed by successor sources. Keep the broader addressing, explicit long conditional expansion, data expressions, bounds and recovery that the runtime needs.
- build_ir86.py arranges one native construction, IR01..IR23. The working text translator grows into the frame/string/workspace translator. IR86.ASM and IRWIDE.ASM are identical; IW source names remain internal aliases, not a second article sequence.
- compiler_profiles.py selects shared authored routines from rill_bootstrap.ir. build_compiler_ladder.py arranges R01..R39 and then RB01..RB12. RILL0 and RILLBOOT retain the same scanner, symbol layout, emitter and parser. Every RB stage is a complete extension of the previous compiler. The seed omits syntax and wrappers absent from the RILL compiler construction.
- build_rill_self_series.py arranges RC01..RC43 from rill_self.ril. prepare_toolchain_sources.py arranges the authored RILL compiler/translator/assembler sources and backend text tables. RILLBOOT builds RILL; that compiler builds the two ports. The RILL construction introduces the 23680-byte table at RC12, eighty parameter/local records at RC18, sixty-four live slots at RC39, and sixty-four-slot procedure frames at RC42. RC43 is the completed compiler. Its first self-build establishes its own frame convention before byte comparisons begin. rill_local_capacity.py supplies storage acceptance fixtures, printed with the complete-compiler lesson. Two closed-loop generations reproduce each tool exactly.

Source generation clears measured facts. Run the relevant native checks before article generation. write_ladder_articles.py publishes the continuing IR/RILL0/RILLBOOT series, write_toolchain_articles.py publishes RC, write_rc_programs.py publishes final compiler examples/reference, and write_toolchain_guides.py publishes self-builds, exact port notebooks and rebuild instructions. Earlier article URLs redirect to the current working part. package_sources.py refreshes all eleven archives; it does not generate executables or rewrite articles.

series_overviews.py supplies each collection cover's "What we're adding" section: the additions and their purpose, plus explicit removal notes. publication_names.write_page retains that section when a cover is regenerated. Run `python3 pub_src/tools/publication_names.py` from the repository root to refresh these summaries after editing them.

LINK86 follows the completed RILL trio. tools/link86.ril is the authored implementation; build_link86.py selects ten continuing checkpoints and small hand-entered object fixtures. Run qa/link86/test_link86.py with the RILL-written tools built, then tools/write_link86_articles.py. The last source is L10.RIL, also LINK86.RIL. tools/package_link86.py packages only ASCII/CRLF source; qa/link86/validate_publication.py reconstructs every printed edit and checks its objects and archives. This stage does not change ASM86 output or the compiler language.

EDIT86 follows LINK86. tools/edit86.ril and edit86_runtime.asm are authored source; prepare_edit86_platform.py applies small source edits to copies of the final compiler/translator. IRED reads the explicitly authored EDITRT.ASM when emitting a program's runtime. build_edit86.py arranges twenty service/editor checkpoints; edit86_format.py only lays out source text. All executable bytes come from executing the RILL-written trio. The preserved baseline sources and tools remain unchanged. The extended pair is bootstrapped with the old trio and checked through three normalized service generations; the editor is built with that pair and the existing RILL-written assembler.

Regenerate in this order: prepare_edit86_platform.py, build_edit86.py, qa/edit86/services.py, qa/edit86/test_checkpoints.py, qa/edit86/test_editor.py, tools/write_edit86_articles.py, package_sources.py. Run qa/edit86/test_storage.py after packaging for actual-source round trips, large columns, undo capacity and service-boundary checks. The publication check reconstructs the printed compiler, translator, binding and editor edits. qa/edit86/test_editor.py covers byte-preserving saves, all navigation/edit operations, large/page-boundary files, exact capacity, recovery, injected DOS failures and memory cleanup. tools/verify_edit86_dos.py separately exercises the actual editor on DOS 3.10 with an 84,000-byte document and BIOS keyboard/video. Its generated test disks and executable images are ignored and never packaged. The final EDIT86 image is 22,073 bytes; its requested program blocks total 336 KiB plus DOS/environment overhead. No disk paging is implemented.

## Verification commands

Run from the repository root. PC-BASIC requires Python 3.11; the locally installed interpreter is in tools/python-pcbasic207. CPU execution and static inspection use the retained dependencies under tools/python. With uv, prefix BASIC commands with `uv run --offline --python 3.11 --no-project`.

```sh
python3.11 pub_src/qa/test_bootasm.py
python3.11 pub_src/qa/asm0/bootstrap.py
python3 pub_src/qa/asm0/test_asm86.py
python3 pub_src/qa/asm86/test_checkpoints.py
python3 pub_src/qa/toolchain/common.py
python3 pub_src/qa/toolchain/test_ir_extensions.py
python3 pub_src/qa/toolchain/test_compiler_ladder.py
python3 pub_src/qa/toolchain/self_compiler.py
python3 pub_src/qa/toolchain/test_local_capacity.py
python3 pub_src/qa/toolchain/build_ports.py
python3 pub_src/qa/toolchain/rebuild.py
python3 pub_src/qa/toolchain/test_rill_self_series.py
python3 pub_src/qa/toolchain/test_language.py
python3 pub_src/qa/toolchain/test_boundaries.py
python3 pub_src/qa/toolchain/test_failures.py
python3.11 pub_src/qa/toolchain/bootstrap_chain.py
python3 pub_src/qa/review_bootstrap_scope.py --strict
python3 pub_src/qa/validate_directories.py
python3 pub_src/tools/verify_gwbasic32_dos.py --interpreter /path/to/GWBASIC.EXE
python3 pub_src/qa/link86/test_link86.py
python3 pub_src/qa/edit86/services.py
python3 pub_src/qa/edit86/test_checkpoints.py
python3 pub_src/qa/edit86/test_editor.py
python3 pub_src/qa/edit86/test_storage.py
python3 pub_src/tools/verify_edit86_dos.py
python3 pub_src/tools/package_sources.py
python3 pub_src/tools/hugo.py --source pub_src/site --cleanDestinationDir
python3 pub_src/qa/validate_site.py
```

The scope audit lists successor-source witnesses for every retained mnemonic and checks the actual published seed grammar and source-continuation boundaries. Execution checks cover retained compiler subsets, correct file/block operations, exact target encodings, resource boundaries, failure cleanup, native/portable agreement and generation equality. Publication checks reconstruct printed edits, compare source-only archives and port notebooks, and inspect every local site link and alias. qa/toolchain/bootstrap_chain.py recreates the required ladder from the BASIC source. tools/verify_toolchain_dos.py independently runs the published TMAKE under the retained DOS 3.10 image.

## Original-interpreter verification

The original GW-BASIC 3.20 executable passes BOOTASM compatibility checks under emulated DOS 3.10. Its startup banner was captured from the BIOS text screen and identifies GW-BASIC 3.20, with 60,332 bytes free. The unchanged published sources pass all seventeen BASIC assembler checkpoints, twenty-six additional boundary/rejection cases, the BYTE.BAS and VIEW.BAS exercises, output truncation and the three complete example programs. The same interpreter builds all twenty-eight ASM0 construction stages with byte-identical results; the resulting 2,431-byte ASM0 then reproduces itself twice. The executable comes from the local DOS 3.20 distribution disk and is never packaged. This verifies the actual interpreter in emulation, not original hardware.

Run tools/verify_gwbasic32_dos.py with --interpreter pointing to the original GW-BASIC 3.20 executable. The local DOS 3.20 disk is also recognized when present. The runner uses private DOS/media copies under qa/bootasm/gwbasic32, preserves the supplied disks, and records its version, interpreter identity and checks in qa/bootasm/gwbasic32-results.json. The private executable and generated disks are ignored. Test files use a DOS subdirectory to avoid the 360 KiB floppy root-entry bound; zero-byte results are preserved with REN.

COMPAQ BASIC 3.11 remains unverified. A historical COMPAQ MS-DOS 3.10 disk supplied COMPAQ BASIC 3.11 (verified from its startup screen), but in the generic QEMU/SeaBIOS workbench that interpreter reports error 52 even for independent, minimal OPEN tests. The cause is not established. The same problem occurs with and without output redirection and with the supplied loader or standalone interpreter; it is not attributed to BOOTASM without evidence. Do not describe the collection as verified on original BASIC or period hardware. Diagnostic scripts and results remain under `qa/` and `tools/` so this compatibility check can be continued with the intended interpreter/workbench.

The historical DOS/interpreter files and private test images under qa/ are never packaged. Modern verification tools do not supply any reader executable. The publication workflow packages the checked-in source and articles, builds root public/, and verifies their consistency.
