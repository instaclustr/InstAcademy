# Publishing the lab guide (GitHub Pages)

**InstAcademy → OpenSearch → Optimizing OpenSearch Vector Storage and Search for Faster AI Applications**

The formatted lab site is built with [MkDocs Material](https://squidfunk.github.io/mkdocs-material/) and deployed from the [InstAcademy](https://github.com/instaclustr/InstAcademy) repository via GitHub Actions.

## Live site

After the first successful deploy:

**https://instaclustr.github.io/InstAcademy/**

## One-time GitHub setup

1. Open [InstAcademy on GitHub](https://github.com/instaclustr/InstAcademy) → **Settings** → **Pages**
2. Under **Build and deployment**, set **Source** to **GitHub Actions**
3. Push to `main` (or run the **Deploy MkDocs to GitHub Pages** workflow manually)

The workflow file is [`.github/workflows/docs.yml`](../../../../.github/workflows/docs.yml) at the InstAcademy repo root.

## Local preview

From **this course folder**:

```bash
pip install -r requirements-docs.txt
python tools/sync-mkdocs-content.py
mkdocs serve
```

Open [http://127.0.0.1:8000/InstAcademy/](http://127.0.0.1:8000/InstAcademy/) when the dev server starts.

## How content is synced

Lesson READMEs stay the source of truth under `src/Chapter …`. Before each build, [`tools/sync-mkdocs-content.py`](../tools/sync-mkdocs-content.py) copies them into `site-docs/` (gitignored) and rewrites internal links for the site.

Edit lesson READMEs as usual, then re-run sync + serve to preview.

```bash
python tools/sync-mkdocs-content.py && mkdocs serve
```

## Files

| File | Purpose |
|------|---------|
| `mkdocs.yml` | Site config, navigation, Material theme |
| `requirements-docs.txt` | MkDocs dependencies |
| `docs/stylesheets/extra.css` | Lab step styling |
| `tools/sync-mkdocs-content.py` | Copy + link rewrite |
| `site-docs/` | Generated content (gitignored) |
| `site/` | Built HTML output (gitignored) |

## Up a level

- [Course README](../README.md)
- [OpenSearch courses](../../)
- [InstAcademy home](../../../)
