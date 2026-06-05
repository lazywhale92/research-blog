---
layout: page
title: Public-content contract
permalink: /docs/public-content-contract/
eyebrow: Safety boundary
summary: "Rules for keeping the public blog repository safe, reproducible, and reviewable."
---

## Allowed public sources

- Public papers, official docs, public datasets, public repositories, public model cards, and public blog posts.
- User-authored research notes that have been generalized and sanitized.
- Synthetic/sample data created only for demonstration.
- Public-safe summaries of private direction, without names, screenshots, direct quotes, internal paths, or confidential details.

## Forbidden content classes

Do not commit, push, reference, screenshot, or quote:

- Private conversations or personally identifying details not already public.
- Company-confidential data, unreleased metrics, customer/user data, vendor secrets, credentials, or internal URLs.
- Private model outputs or experiment traces that reveal non-public systems or context.
- Work-log paths, private draft IDs, raw-source paths, or provenance trackers from the private workspace.
- Material whose release requires employer, legal, or other accountability approval that has not been obtained.

## Required post frontmatter

```yaml
---
title: "..."
date: YYYY-MM-DD
layout: paper-note
status: draft | published | corrected
topic: continual-learning | llm-eval | agent-systems | data-quality | other
tags: []
summary: "1-2 sentence public-safe summary"
public_safety: reviewed
source_visibility: public-only | private-sanitized
repo_artifacts: []
---
```

## Review checklist

Before a post enters public history:

- [ ] All sources are public or explicitly sanitized.
- [ ] No private conversation, private draft, work-log path, internal URL, credential, personal data, or confidential detail is exposed.
- [ ] Claims that depend on private context are generalized or removed.
- [ ] Reproducibility claims point to public code/data or clearly say "not released".
- [ ] Method/result/limitations are concrete enough to avoid research-looking workslop.
- [ ] A human owner is accountable for final publication of real posts.

## If unsafe content is pushed

Treat it as a privacy/security incident: pause publication, remove or rotate exposed material where applicable, rewrite public history if still feasible, and document the correction in a public-safe way.
