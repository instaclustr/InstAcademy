← [InstAcademy](README.md) · [Contributing](CONTRIBUTING.md)

# Maintainers and governance

This repository holds the hands-on labs for [InstAcademy](https://www.instaclustr.com/instacademy-courses/), the free course library from NetApp Instaclustr. The video lessons live in the library; the labs live here.

> [!NOTE]
> **The names and handles below are placeholders.** Fill them in before this repository goes public.

## Who maintains what

| Area | Maintainer | GitHub |
|---|---|---|
| Repository owner, course direction | Brian Graf | `@TBD` |
| OpenSearch track | TBD | `@TBD` |
| Course content review, technical accuracy | TBD | `@TBD` |

Maintainers are responsible for reviewing pull requests in their area, keeping the courses accurate against current engine versions, and triaging issues.

## How decisions get made

- **Corrections** to a step that does not work, a stale screenshot, or an API that moved: any maintainer may review and merge.
- **Changes to course content** — steps, expected output, narration order — need review from the maintainer of that track, because the labs are paired with recorded video lessons and the two must stay in step.
- **New courses or tracks** are decided by the repository owner, in step with the InstAcademy course roadmap.

## Response expectations

These are goals, not guarantees.

| | |
|---|---|
| Issue triage | Within five working days |
| Pull request first response | Within ten working days |
| Security reports | See [`SECURITY.md`](SECURITY.md) |
| Badge requests | Reviewed in batches; see [`README.md`](README.md#-what-you-get-when-you-finish) |

## Adding a course

Courses follow the layout and house rules in [`CONTRIBUTING.md`](CONTRIBUTING.md). A new course needs a `README.md`, a `CLUSTER-SETUP.md`, numbered chapters under `chapters/`, and its own `scripts/validate.sh` so CI picks it up automatically.

## Code of conduct

This repository follows the NetApp code of conduct. **TODO: link the official policy here before going public.**
