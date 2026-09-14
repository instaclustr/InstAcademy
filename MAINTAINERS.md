← [InstAcademy](README.md) · [Contributing](CONTRIBUTING.md)

# Maintainers and governance

This repository holds the hands-on labs for [InstAcademy](https://www.instaclustr.com/instacademy-courses/), the free course library from NetApp Instaclustr. The video lessons live in the library; the labs live here.


## Who maintains what

| Role | Who |
|---|---|
| Repository owner, course direction | Brian Graf — [`@TheBrianGraf`](https://github.com/TheBrianGraf) |
| Maintainers | Brian Graf — [`@TheBrianGraf`](https://github.com/TheBrianGraf), Ramya Ravi — [`@ramyaravi1`](https://github.com/ramyaravi1) |

Maintainers are jointly responsible for the project as a whole: reviewing pull requests, keeping the courses accurate against current engine versions, and triaging issues, regardless of which course or track a change touches.

## How decisions get made

- **Corrections** to a step that does not work, a stale screenshot, or an API that moved: any maintainer may review and merge.
- **Changes to course content** — steps, expected output, narration order — need review from a maintainer, because the labs are paired with recorded video lessons and the two must stay in step.
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
