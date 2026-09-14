← [InstAcademy](README.md) · [Contributing](CONTRIBUTING.md)

# Maintainers and governance

This repository holds the hands-on labs for [InstAcademy](https://www.instaclustr.com/instacademy-courses/), the free course library from NetApp Instaclustr. The video lessons live in the library; the labs live here.

> [!NOTE]
> **This is a one-person project for now.** Brian Graf owns every area below. The table is split by area so it's ready to hand off pieces as other maintainers join.

## Who maintains what

| Area | Maintainer | GitHub |
|---|---|---|
| Repository owner, course direction | Brian Graf | [`@TheBrianGraf`](https://github.com/TheBrianGraf) |
| OpenSearch track | Brian Graf | [`@TheBrianGraf`](https://github.com/TheBrianGraf) |
| Course content review, technical accuracy | Brian Graf | [`@TheBrianGraf`](https://github.com/TheBrianGraf) |

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

This repository follows the [Instaclustr Code of Conduct](https://github.com/instaclustr/.github/blob/main/CODE_OF_CONDUCT.md) (Contributor Covenant), which applies org-wide across NetApp Instaclustr's open-source repositories.
