# The Bootstrap Experiment

An original, gradual course in building an 8086/8088 software workbench, starting with an assembler written in GW-BASIC.

The Hugo source lives in `pub_src/site`; generated pages go to root `public/`. The collections follow **BOOTASM → ASM0 → ASM1 → ASM86 → IR86 → RILL0 → RILLBOOT → RILL**:

| Tool | Article series |
|---|---|
| BOOTASM | Our First Assembler |
| ASM0 | An Assembler That Builds Itself |
| ASM1 | Building a Streaming Assembler |
| ASM86 | Extending the 8086 Assembler |
| IR86 | Building an Intermediate Language |
| RILL0 | Our First Compiler |
| RILLBOOT | A Compiler for Writing Tools |
| RILL | A Compiler Written in Its Own Language |

Each collection has its own workbench, reference, complete examples, and source archive. Reader downloads use these tool names. Existing article URLs and saved checkpoint filenames remain stable. Internal production paths retain their established names; [pub_src/README.md](pub_src/README.md) explains the mapping.

The complete chain builds a RILL-written compiler (26,625 bytes), IR86 translator (31,472 bytes), and ASM86 assembler (32,404 bytes), then reproduces all three through two closed-loop generations. The RILLBOOT seed is written in IR86. The native ASM86 is built through ASM1 and ASM0 from the BASIC foundation.

IR86 and RILL stream bounded input/output blocks. The language supplies general identifiers, word expressions, recursive procedures with parameters and local state, lexical scopes, byte buffers, literal strings, and portable file/allocated-block services. IR remains processor-independent; the 8086/DOS binding keeps native conventions private. Output remains DOS `.COM`, with an explicit 61,184-byte profile. The RILL-written assembler retains 8,192 symbols in allocated pages.

The existing collections contain the initial bootstrap milestones and their separately named builders. The continuation adds 23 native IR checkpoints, 47 IR-written compiler checkpoints, and 43 RILL-written compiler checkpoints, followed by complete tool sources and closed-loop rebuild instructions. Read [the systems workbench](pub_src/site/content/bootstrap/rb/033-the-systems-workbench.md), [the language reference](pub_src/site/content/bootstrap/rb/132-the-rill-systems-language.md), or [the complete toolchain exercise](pub_src/site/content/bootstrap/rc/135-the-complete-toolchain.md). [TOOLCHAIN_Design.md](TOOLCHAIN_Design.md) records the architecture and verification.

## Publish with GitHub Pages

The included `.github/workflows/pages.yml` builds and deploys the site automatically after each push to the repository's default branch (`master` in Rendman/BootExp). It also supports a manual run from the repository's Actions tab. It installs Hugo 0.169.0, refreshes the source downloads, builds into `public/`, checks the pages and listings, and publishes that directory. The workflow reads the default branch from GitHub rather than assuming it is named `main`.

One-time setup:

1. Create an empty GitHub repository and note its default branch name. The workflow supports `main`, `master`, or another default branch name. A public repository supports Pages on GitHub Free; private-repository availability depends on your plan.
2. Push this project, including the hidden `.github/` directory, to the repository. Keep the repository structure as it is; the generated `public/` directory is ignored and is rebuilt by the workflow.
3. In the repository, open **Settings → Pages → Build and deployment** and set **Source** to **GitHub Actions**. Do not add another generated Hugo workflow; this project already has one.
4. Open **Actions → Publish Bootstrap Experiment → Run workflow**, choosing the repository's default branch. Later pushes to that branch trigger publication automatically. Runs on other branches deliberately skip both jobs.

For a new, empty repository, these commands push the project from this folder. Replace the example remote URL with the URL GitHub gives you:

```sh
git init -b main
git add .
git commit -m "Add Bootstrap Experiment and Pages publishing"
git remote add origin https://github.com/YOUR-USERNAME/YOUR-REPOSITORY.git
git push -u origin main
```

These example commands create a new `main` branch. For an existing repository, use its existing default branch; Rendman/BootExp uses `master`.

The deployment reports the live address in the `github-pages` environment. The build keeps the site's portable relative URLs, which work both under a project path such as `https://USERNAME.github.io/REPOSITORY/` and at an account site's root. Keep the existing `baseURL = '/'` and `relativeURLs = true` settings together; adding a repository prefix to this portable build would duplicate it in the generated links. No username, repository name, or personal access token needs to be embedded in the workflow.

Edit articles under `pub_src/site/content/`, commit, and push to the default branch to update the site. For generated construction articles, update the corresponding manuscript/source generator too; see `pub_src/README.md`. The publishing workflow builds the checked-in articles; it does not overwrite them by running the article generators. All source bundles are refreshed and checked before publication.

See GitHub's [custom Pages workflow guide](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages) and Hugo's [GitHub Pages deployment guide](https://gohugo.io/host-and-deploy/deploy-to-github-pages/) for the hosting requirements.

## Work locally

With Hugo installed, run this from the project root:

```sh
hugo --source pub_src/site --cleanDestinationDir
python3 -m http.server 8096 --directory public
```

Open `http://localhost:8096/bootstrap/`. The output can also be opened directly at `public/bootstrap/index.html`.

Development details, verification results, and the original-interpreter compatibility limit are recorded in [pub_src/README.md](pub_src/README.md).
