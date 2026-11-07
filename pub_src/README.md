# Bootstrap Experiment source and verification

Reader hierarchy: BOOTASM -> ASM0 -> ASM1 -> ASM86 -> IR86 -> RILL0 -> RILLBOOT -> RILL, followed by the toolchain in RILL. Site source is site/, generated HTML is ../public/, period source is workbench/, manuscript arrangement is tools/, and verification is qa/. Internal asm86/asma0/asm86a and rill/rb/rc paths retain the established production keys; tools/publication_names.py maps reader names and downloads.

Every bootstrap executable comes from published BASIC or project assemblers/translators/compilers. Source arrangement scripts select authored text and backend templates; they never parse a bootstrap language or encode machine instructions. Archives contain ASCII/CRLF/8.3 source, fixtures and inspection helpers, without executables or historical interpreters.


| Internal source directory | Reader tool | Complete reader source |
|---|---|---|
| `workbench/bootasm` | BOOTASM | `BOOTASM.BAS` |
| `workbench/asm86` | ASM0 | `ASM0.ASM` (internal `ASM86.ASM`) |
| `workbench/asma0`, `workbench/asm86a` | ASM1 seed | `ASM1.ASM` (internal `ASMA0.ASM`, A12) |
| `workbench/asm86a` | Native ASM86 | `ASM86.ASM` (internal `ASM86A.ASM`, A40) |
| `workbench/ir86` | Native IR86 | `IR86.ASM`, identical to `IRWIDE.ASM` and IR23 |
| `workbench/rill` | RILL0 | `RILL0.IR` (internal `RILL.IR`, R39) |
| `workbench/toolchain`, `workbench/rb` | RILLBOOT | `RILLBOOT.IR`, identical to RB12 |
| `workbench/toolchain`, `workbench/rc` | RILL compiler | `RILL.RIL`, identical to RC43 |
| `workbench/toolchain` | RILL-written tools | `IR86.RIL`, `ASM86.RIL` (internal `ASM86A.RIL`) |

Canonical reader downloads live under `site/static/downloads/tools/<tool>/`. Legacy download directories retain their internal names. The RILL0 archive is `RILL0.ZIP`; the final compiler archive is `RILL.ZIP`. Generation-zero `workbench/toolchain/RILL0.IR` is generated IR for the full RILL compiler, distinct from the initial compiler's authored `workbench/rill/RILL.IR`.

## Continuing source constructions

- build_bootasm.py and build_asm86.py arrange the BASIC foundation and ASM0. ASM0 has only the vocabulary needed to build ASM1; ASM1 adds XOR for ASM86.
- build_asm86a_series.py arranges twelve ASM1 and twenty-four ASM86 checkpoints. The omitted unary, signed arithmetic, rotate, repeat/string and branch-alias rows are not needed by successor sources. Keep the broader addressing, explicit long conditional expansion, data expressions, bounds and recovery that the runtime needs.
- build_ir86.py arranges one native construction, IR01..IR23. The working text translator grows into the frame/string/workspace translator. IR86.ASM and IRWIDE.ASM are identical; IW source names remain internal aliases, not a second article sequence.
- compiler_profiles.py selects shared authored routines from rill_bootstrap.ir. build_compiler_ladder.py arranges R01..R39 and then RB01..RB12. RILL0 and RILLBOOT retain the same scanner, symbol layout, emitter and parser. Every RB stage is a complete extension of the previous compiler. The seed omits syntax and wrappers absent from the RILL compiler construction.
- build_rill_self_series.py arranges RC01..RC43 from rill_self.ril. prepare_toolchain_sources.py arranges the authored RILL compiler/translator/assembler sources and backend text tables. RILLBOOT builds RILL; that compiler builds the two ports. The RILL construction introduces the 23680-byte table at RC12, eighty parameter/local records at RC18, sixty-four live slots at RC39, and sixty-four-slot procedure frames at RC42. RC43 is the completed compiler. Its first self-build establishes its own frame convention before byte comparisons begin. rill_local_capacity.py supplies storage acceptance fixtures, printed with the complete-compiler lesson. Two closed-loop generations reproduce each tool exactly.

Source generation clears measured facts. Run the relevant native checks before article generation. write_ladder_articles.py publishes the continuing IR/RILL0/RILLBOOT series, write_toolchain_articles.py publishes RC, write_rc_programs.py publishes final compiler examples/reference, and write_toolchain_guides.py publishes self-builds, exact port notebooks and rebuild instructions. Earlier article URLs redirect to the current working part. package_sources.py refreshes all nine archives; it does not generate executables or rewrite articles.

series_overviews.py supplies each collection cover's "What we're adding" section: the additions and their purpose, plus explicit removal notes. publication_names.write_page retains that section when a cover is regenerated. Run `python3 pub_src/tools/publication_names.py` from the repository root to refresh these summaries after editing them.

## Verification commands

Run from the repository root. PC-BASIC requires Python 3.11; the locally installed interpreter is in tools/python-pcbasic207. CPU execution and static inspection use the retained dependencies under tools/python. With uv, prefix BASIC commands with `uv run --offline --python 3.11 --no-project`.

```sh
python3.11 pub_src/qa/test_bootasm.py
python3.11 pub_src/qa/asm86/bootstrap.py
python3 pub_src/qa/asm86/test_asm86.py
python3 pub_src/qa/asm86a/test_checkpoints.py
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
python3 pub_src/tools/package_sources.py
python3 pub_src/tools/hugo.py --source pub_src/site --cleanDestinationDir
python3 pub_src/qa/validate_site.py
```

The scope audit lists successor-source witnesses for every retained mnemonic and checks the actual published seed grammar and source-continuation boundaries. Execution checks cover retained compiler subsets, correct file/block operations, exact target encodings, resource boundaries, failure cleanup, native/portable agreement and generation equality. Publication checks reconstruct printed edits, compare source-only archives and port notebooks, and inspect every local site link and alias. qa/toolchain/bootstrap_chain.py recreates the required ladder from the BASIC source. tools/verify_toolchain_dos.py independently runs the published TMAKE under the retained DOS 3.10 image.

## Historical interpreter status

The original-interpreter check is not yet passed. A historical COMPAQ MS-DOS 3.10 disk supplied COMPAQ BASIC 3.11 (verified from its startup screen), but in the generic QEMU/SeaBIOS workbench that interpreter reports error 52 even for independent, minimal OPEN tests. The cause is not established. The same problem occurs with and without output redirection and with the supplied loader or standalone interpreter; it is not attributed to BOOTASM without evidence. Do not describe the collection as verified on original BASIC or period hardware. Diagnostic scripts and results remain under `qa/` and `tools/` so this compatibility check can be continued with the intended interpreter/workbench.

The historical DOS/interpreter files and private test images under qa/ are never packaged. Modern verification tools do not supply any reader executable. The publication workflow packages the checked-in source and articles, builds root public/, and verifies their consistency.
