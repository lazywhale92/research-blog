---
layout: page
title: Reference and design synthesis
permalink: /docs/reference-synthesis/
eyebrow: Design brief
summary: "Public-safe reference synthesis, information architecture, and originality guardrails."
---

This note defines the public-safe design direction for the research blog. It is a synthesis of public research-blog patterns and private direction notes. It intentionally avoids copying any single site.

## Design thesis

The blog should feel like a compact research desk: chronological enough to publish frequently, structured enough to support paper-like notes, and plain enough that readers focus on claims, methods, evidence, and limitations.

## Reference matrix

| Source | Useful pattern to adopt | What this blog will not copy |
|---|---|---|
| muted-color / Mini Research | Paper-like post anatomy, table-of-contents support, figures/tables/captions, concise applied-research framing | Exact hero/card composition, typography scale, spacing rhythm, icon language, or post hierarchy |
| Lilian Weng | Long-form technical notes, visible date/author/reading context, archive-first discoverability | Full personal-blog breadth or broad topic sprawl before enough posts exist |
| Andrej Karpathy | Simple chronological index, high-signal one-line summaries, low-friction publishing | A generic personal homepage or personality-led portfolio front page |
| Distill | Figure/table/caption culture, explicit article types, reproducibility mindset | Heavy interactive-article infrastructure for the MVP |
| Colah | Concept maps, distinction between polished posts and rough notes, research taste through taxonomy | Dense visual taxonomy before the content corpus justifies it |

## Sanitized direction from private notes

Private direction notes were reviewed and generalized into public editorial rules:

- Prefer bounded, publishable technical reports over slow monolithic papers.
- Treat problem definition, experiment operation, result interpretation, and limitations as the core research artifact.
- Keep each research unit small enough to finish and understand in a short cycle.
- Use automation as a ladder: it may accelerate search, experiment support, and rewriting, but the human owner must still understand the plan, results, and public-release risk.
- A public post should never leak private chats, company context, internal paths, unreleased metrics, or confidential experiment traces.

## Information architecture

The MVP exposes these public-safe page and content types:

1. **Home** — mission, latest notes, research lanes, and navigation.
2. **About** — publication stance, author context, and safety boundary.
3. **Archive** — chronological list of posts with summaries and topics.
4. **Paper note** — structured research article layout for polished or placeholder notes.
5. **Experiment log summary** — public-safe summary pattern for future experiment writeups; raw logs stay private unless intentionally released.
6. **Pipeline doc** — topic → experiment → public-safe publication workflow.
7. **Reference/design synthesis** — this document, plus the originality checklist below.

## Originality checklist

Before launch and before major redesigns, verify:

- [ ] Home composition is mission/index-led, not a clone of the muted-color hero/card stack.
- [ ] Typography, spacing, borders, and color palette are independently chosen.
- [ ] Reference ideas are described as patterns, not copied visual implementations.
- [ ] Sample content is synthetic or public-only.
- [ ] No private note, chat, company, work-log, or internal source path appears in public pages.

## Adopted visual direction

- Narrow readable measure for prose; slightly wider surfaces for tables and figures.
- Soft warm background with ink-like text and muted accent colors.
- Clear metadata chips for topic, status, source visibility, and public-safety state.
- Paper-note sections with stable heading order and in-page navigation.
- Minimal decorative motion; no app-like interaction for the MVP.
