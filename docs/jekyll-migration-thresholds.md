---
layout: page
title: Jekyll migration thresholds
permalink: /docs/jekyll-migration-thresholds/
eyebrow: Stack guardrail
summary: "When to keep Jekyll simple and when to migrate to a custom static build."
---

Jekyll is the MVP default because it is Markdown-first, GitHub Pages-compatible, and sufficient for paper-like notes.

## Migrate before publishing a post if required

Move to a custom GitHub Actions static build, such as Astro, Hugo, or a static Next export, if a required post cannot honestly satisfy the template or verification criteria without:

- Unsupported Jekyll plugins or custom build steps for citations, bibliography, diagrams, notebooks, or assets.
- Interactive figures, executable demos, notebook-derived pages, or rich components that are central to the research claim.
- A typed/validated content schema that Jekyll cannot approximate without fragile workarounds.
- Build behavior that Pages-native Jekyll cannot reproduce locally and in deployment.

## Do not migrate merely for

- Decorative animations or portfolio polish.
- Advanced search before enough posts exist.
- CMS-like editing convenience.
- Visual refinements that do not affect argument clarity or publication safety.

## Schedule migration after the current release if

Two consecutive posts spend more effort on Jekyll/layout workarounds than on research writing and review.

## Migration invariant

Post frontmatter and Markdown section schema must remain portable so old posts can move without rewriting their research content.
