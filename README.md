# The Bootstrap Experiment

An original, gradual course in building an 8086/8088 software workbench, starting with an assembler written in GW-BASIC.

The Hugo site lives in `pub_src/site`. Its published output goes to `public/` at the project root. BOOTASM contains eighteen construction installments, a workbench guide, a language reference, and complete example programs. ASM86 sits beside it with twenty-nine assembly construction checkpoints and a thirtieth installment proving self-assembly. IR86 is the fourth collection, with thirty-two translator checkpoints, a complete translation pipeline, a language reference, and examples. RILL is the fifth collection, with twenty-nine compiler construction checkpoints, a complete pipeline, a language reference, and four examples. Each collection has its own workbench guide and source downloads.

ASM86's first executable is built directly by the completed BOOTASM.BAS. Two native generations reproduce that executable byte for byte. ASM86 directly builds the 6,407-byte IR86 translator, whose assembly output is assembled by that same ASM86. IR programs use a processor-independent virtual machine and portable runtime services. An independent interpreter and the 8086 backend agree on unchanged sources; native DOS 3.10 checks cover the binding, byte streams, and a file copier. The first RILL compiler is written in IR86, emits IR86, and builds directly into a 5,173-byte executable. Its initial language includes mutable word variables, arithmetic, conditions, loops, and byte streams. It is not yet self-hosted.

**ASM86A is the third collection and a working rung in the bootstrap ladder: BOOTASM → ASM86 → ASM86A → IR86 → RILL.** Forty construction checkpoints build a 3342-byte ASMA0 seed directly with unchanged ASM86, then a 6422-byte streaming assembler with 8192 symbols, allocated workspace, broader 8086 addressing, data directives, and explicit long conditional expansions. Both milestones pass two self-assembly generations. The complete ladder builds the published IR86 and RILL byte for byte and runs compiler output under DOS 3.10. Their separate expansions remain future work. See [the implementation architecture](ASM86A_Design.md) and [ASM86A articles](pub_src/site/content/bootstrap/asm86a/_index.md).

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

Edit articles under `pub_src/site/content/`, commit, and push to the default branch to update the site. For generated construction articles, update the corresponding manuscript/source generator too; see `pub_src/README.md`. The publishing workflow builds the checked-in articles; it does not overwrite them by running the article generators. All four source collections are refreshed and checked before publication.

See GitHub's [custom Pages workflow guide](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages) and Hugo's [GitHub Pages deployment guide](https://gohugo.io/host-and-deploy/deploy-to-github-pages/) for the hosting requirements.

## Work locally

With Hugo installed, run this from the project root:

```sh
hugo --source pub_src/site --cleanDestinationDir
python3 -m http.server 8096 --directory public
```

Open `http://localhost:8096/bootstrap/`. The output can also be opened directly at `public/bootstrap/index.html`.

Development details, verification results, and the original-interpreter compatibility limit are recorded in [pub_src/README.md](pub_src/README.md).
