---
layout: page
title: Publishing pipeline
permalink: /docs/publishing-pipeline/
eyebrow: Operating model
summary: "How a research idea becomes a public-safe paper-like note."
---

The blog is the public endpoint of a private-to-public research workflow. It is not the place where private drafts, raw logs, or unreleased experiment traces are stored.

## State machine

| State | Public artifact | Exit gate |
|---|---|---|
| Idea | None by default | Question is narrow enough for a bounded experiment or literature note |
| Private draft | None by default | Draft has a paper-note outline and all private/public source boundaries are known |
| Experiment note | Optional public artifact candidates | Results, failures, and unreleased parts are explicitly separated |
| Public-safe rewrite | Post draft in this repo only after sanitation | Public-content checklist passes before branch, PR, or commit publication |
| Public repo PR/commit | Markdown post, assets, public-safety artifact | Build, link, originality, evidence, and safety checks pass |
| Publish | GitHub Pages URL | Public URL returns 200 and the note appears in home/archive |
| Correction/archive | Dated correction note or changelog | Correction is transparent and public-safe |

## Minimum real-post quality gate

A real post should not publish until it has:

- A clear problem statement and explicit research question.
- Method, result, discussion, limitations, and references sections.
- Public reproducibility artifacts, or a clear statement of what is not released.
- Public-content contract checklist completed.
- Human accountability owner approval for publication.
- A not-workslop review: the note must not merely look research-shaped; it must show evidence, limits, and decision relevance.

## Automation connection

The long-term automation loop should connect to this blog as a final, reviewed publication channel:

1. Topic explorer proposes bounded questions.
2. Experiment runner or literature workflow gathers public-safe evidence candidates.
3. Result summarizer creates a private technical note.
4. Public-safe rewriter removes private context and rewrites claims against public sources.
5. Human owner performs final release accountability review.
6. This repo receives the sanitized Markdown post, review artifact, and public assets.

## Publication command shape

For a real post, prefer:

1. Create `draft/<post-slug>` branch.
2. Add `_posts/YYYY-MM-DD-<post-slug>.md` using `templates/paper-note-template.md`.
3. Add `_reviews/<post-slug>.public-safety.md`.
4. Run local build and link/content checks.
5. Open PR using `.github/pull_request_template.md`.
6. Merge only after human public-safety approval.

Synthetic placeholder posts may be committed directly during scaffold if they are public-only and pass the same safety checklist.
