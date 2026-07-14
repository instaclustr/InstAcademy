← [Course index](README.md) · [How to run labs](HANDS-ON-GUIDE.md) · [Changelog](CHANGELOG.md)

# Contributing

Thanks for helping improve this course. The most valuable contribution is usually the simplest one: you ran a step, it did not do what the page said, and you told us exactly what happened.

## Reporting a step that fails

Open an issue with these five things. The first three are what make a report actionable:

1. **Chapter and step number**, for example "Chapter 4, Step 8".
2. **The request you sent**, copied from Dev Tools or Bruno.
3. **The response you got**, in full, including the error body.
4. **Your OpenSearch version** (`GET /` returns it) and whether the cluster is Instaclustr-managed or self-hosted.
5. **What the page said to expect.**

A step that fails for you may well be a step that fails for everyone on a newer OpenSearch version, so this is genuinely useful. If you already know the fix, say so in the issue and open a pull request.

## Proposing a change

Fork, branch, and open a pull request against `main`. Small, focused changes merge fastest: one fix per pull request, with the chapter and step in the title.

## House rules

These keep the course trustworthy. Anything that breaks one of them will be sent back, so it's worth reading before you write.

**Every Expected block is a real response.** The output shown in a step must be what the cluster actually returned when someone ran that exact request, not an idealized or hand-written example. If you change a request, re-run it and paste the new response. If a number in the prose (a score, a document count, a memory figure) came from a run, and your change moves it, update the prose too.

**The chapter README is the source of truth.** Bulk payloads are inlined in the README so a student can copy any block and run it as printed. The NDJSON files in `rest/bulk/` are the machine-readable mirror the Bruno collection sends, and they must stay byte-identical to the README block. Change one, regenerate the other.

**Bruno stays in sync with the README.** If you add, remove, or edit a request in a chapter:

- Add, remove, or edit the matching `.bru` file in `bruno/Chapter N/`.
- The `seq:` value inside the file must equal the number in its filename.
- File numbers must ascend in the order the steps appear in the README.
- Update the **Fast mode** line at the end of the step so it names the right files.
- Run the validation script below; it checks all of the above.

**Plain spoken English.** This text is narrated in a video, so write the way an instructor talks: short sentences, one idea each, no metaphors that need a pause to land. Say what the student does and what happens.

**Every step earns its place.** A step must produce a visible, explainable result. If a request only returns `"acknowledged": true` and nothing later depends on it, it probably belongs in the prose of another step rather than as a step of its own.

**Document version-specific behavior.** If something works on one OpenSearch version and not another, say so inline, with the version, and note how you verified it. The [changelog](CHANGELOG.md) has a Known limitations section for the ones that affect the whole course.

## Before you open the pull request

```bash
scripts/validate.sh
```

This checks that every Bruno file is referenced by its README, that no README names a file that doesn't exist, that `seq` values match filenames, that request ordering matches step ordering, and that every bulk payload resolves and matches its README block. It runs in a couple of seconds and needs only Python 3.

If your change touches the steps themselves, also add an entry to [`CHANGELOG.md`](CHANGELOG.md) under a new **Unreleased** heading, describing the change from a learner's point of view.

## Testing against a real cluster

The course is validated on the cluster described in [`CLUSTER-SETUP.md`](CLUSTER-SETUP.md): NetApp Instaclustr managed, AI Search Plugin, three m.80 data nodes. A local Docker OpenSearch works for most steps, with two exceptions worth knowing: the managed cluster blocks outbound calls to some LLM APIs, and cluster settings differ. If you validate on something else, say which in your pull request.

**Never commit credentials.** The Bruno environment ships placeholders, and it must stay that way. Redact cluster hostnames, usernames, passwords, and API keys from anything you paste into an issue or a pull request; see [`SECURITY.md`](SECURITY.md).
