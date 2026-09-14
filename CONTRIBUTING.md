← [InstAcademy](README.md) · [Report a problem](https://github.com/instaclustr/instacademy/issues/new/choose)

# Contributing

Thanks for helping improve InstAcademy. The most valuable contribution is usually the simplest one: you ran a step, it did not do what the page said, and you told us exactly what happened.

## Reporting a step that fails

[Open an issue](https://github.com/instaclustr/instacademy/issues/new/choose) with these six things. The first four are what make a report actionable:

1. **Which course**, for example "OpenSearch · Optimizing Vector Storage & Search".
2. **Chapter and step number**, for example "Chapter 4, Step 8".
3. **The request you sent**, copied from Dev Tools or Bruno.
4. **The response you got**, in full, including the error body.
5. **Your engine version** (for OpenSearch, `GET /` returns it) and whether the cluster is Instaclustr-managed or self-hosted.
6. **What the page said to expect.**

A step that fails for you may well be a step that fails for everyone on a newer version, so this is genuinely useful. If you already know the fix, say so in the issue and open a pull request.

## Proposing a change

Fork, branch, and open a pull request against `main`. Small, focused changes merge fastest: one fix per pull request, with the course, chapter, and step in the title.

## House rules

These keep the courses trustworthy. Anything that breaks one of them will be sent back, so it's worth reading before you write.

**Every Expected block is a real response.** The output shown in a step must be what the cluster actually returned when someone ran that exact request, not an idealized or hand-written example. If you change a request, re-run it and paste the new response. If a number in the prose (a score, a document count, a memory figure) came from a run, and your change moves it, update the prose too.

**The chapter README is the source of truth.** Bulk payloads are inlined in the README so a learner can copy any block and run it as printed. The `.ndjson` file beside each bulk request in the course's `bruno/<chapter-slug>/` is the machine-readable mirror the Bruno collection sends, and it must stay byte-identical to the README block. Change one, regenerate the other.

**Bruno stays in sync with the README.** If you add, remove, or edit a request in a chapter:

- Add, remove, or edit the matching `.bru` file in `bruno/<chapter-slug>/`.
- The `seq:` value inside the file must equal the number in its filename.
- File numbers must ascend in the order the steps appear in the README.
- Update the **Fast mode** line at the end of the step so it names the right files.
- Run the course's validation script; it checks all of the above.

**Paths use lowercase kebab-case.** Course and chapter folders carry a zero-padded ordinal prefix and no spaces, like `opensearch/01-vector-storage-and-search/chapters/03-hybrid-search/`. Folder names are slugs; the human title lives in the page's H1. Screenshots and diagrams go in the course's `assets/<chapter-slug>/`, never beside a README.

**Table cells follow the sentence rule.** A cell that is a complete sentence gets a full stop; a cell that is a label, a fragment, or a list does not. Keep it consistent down a column: if one description cell in a table ends with a full stop, they all should.

**Plain spoken English.** This text is narrated in a video, so write the way an instructor talks: short sentences, one idea each, no metaphors that need a pause to land. Say what the learner does and what happens.

**Every step earns its place.** A step must produce a visible, explainable result. If a request only returns `"acknowledged": true` and nothing later depends on it, it probably belongs in the prose of another step rather than as a step of its own.

**Document version-specific behavior.** If something works on one engine version and not another, say so inline, with the version, and note how you verified it. Each course's changelog has a Known limitations section for the ones that affect the whole course.

## Before you open the pull request

Run the validation script for the course you touched, from that course's folder:

```bash
cd opensearch/01-vector-storage-and-search
scripts/validate.sh
```

This checks that every Bruno file is referenced by its README, that no README names a file that doesn't exist, that `seq` values match filenames, that request ordering matches step ordering, and that every bulk payload resolves and matches its README block. It runs in a couple of seconds and needs only Python 3.

You can also run the repo-wide link check the same way CI does:

```bash
python3 .github/scripts/check_links.py
```

It resolves every relative link **and every `#anchor`** against the headings they point at. Anchors matter: GitHub builds a heading's anchor from its text, so renaming a heading, or adding a leading emoji that shifts the slug, silently breaks every link aimed at it. Headings that are linked to in-page are kept free of leading emoji for exactly this reason.

Both checks run automatically on every pull request ([`.github/workflows/ci.yml`](.github/workflows/ci.yml)), and the course validator runs for every course found in the repo, so adding a course needs no CI change.

If your change touches the steps themselves, also add an entry to that course's `CHANGELOG.md` under a new **Unreleased** heading, describing the change from a learner's point of view.

## Testing against a real cluster

Each course names the cluster it was validated on in its `CLUSTER-SETUP.md`. For the OpenSearch vector course, that is a NetApp Instaclustr managed cluster with the AI Search Plugin and three m.80 data nodes. A local Docker instance works for most steps, with two exceptions worth knowing: the managed cluster blocks outbound calls to some LLM APIs, and cluster settings differ. If you validate on something else, say which in your pull request.

**Never commit credentials.** Bruno environments ship placeholders, and they must stay that way. Redact cluster hostnames, usernames, passwords, and API keys from anything you paste into an issue or a pull request; see [`SECURITY.md`](SECURITY.md).

## Course index

| Course | Contributing notes |
|---|---|
| [OpenSearch · Optimizing Vector Storage & Search](opensearch/01-vector-storage-and-search/README.md) | [Changelog](opensearch/01-vector-storage-and-search/CHANGELOG.md) · [Cluster setup](opensearch/01-vector-storage-and-search/CLUSTER-SETUP.md) · [How to run labs](opensearch/01-vector-storage-and-search/HANDS-ON-GUIDE.md) |
