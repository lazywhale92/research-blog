---
layout: default
title: Home
summary: "A compact public channel for paper-like applied research notes."
---

<section class="hero">
  <p class="eyebrow">Public research channel</p>
  <h1>Small research notes with paper-like structure.</h1>
  <p class="hero-copy">This site publishes public-safe technical notes that foreground problem framing, method, evidence, limitations, and reproducibility. Private drafts and raw work logs stay private until rewritten for release.</p>
  <div class="hero-actions">
    <a class="button" href="{{ '/archive/' | relative_url }}">Read notes</a>
    <a class="button secondary" href="{{ '/docs/publishing-pipeline/' | relative_url }}">Publication pipeline</a>
  </div>
</section>

<section class="lane-grid" aria-label="Research lanes">
  <article>
    <h2>Continual learning</h2>
    <p>Taxonomy drift, updating classifiers, and keeping category systems useful over time.</p>
  </article>
  <article>
    <h2>LLM evaluation</h2>
    <p>Practical tests for agent behavior, work quality, and reproducible judgment loops.</p>
  </article>
  <article>
    <h2>Agent systems</h2>
    <p>Research automation loops from topic search to experiment logs and public summaries.</p>
  </article>
</section>

<section class="post-list">
  <div class="section-heading">
    <p class="eyebrow">Latest</p>
    <h2>Research notes</h2>
  </div>
  {% assign candidate_posts = site.posts | where_exp: "post", "post.hidden != true" %}
  {% assign visible_count = 0 %}
  {% for post in candidate_posts %}
    {% if visible_count < 6 %}
      {% if post.status == "published" or post.status == "corrected" %}
        {% assign visible_count = visible_count | plus: 1 %}
        <article class="post-row">
          <div>
            <p class="post-meta">{{ post.date | date: "%Y-%m-%d" }} · {{ post.topic | default: 'other' | escape }} · {{ post.status | default: 'draft' | escape }}</p>
            <h3><a href="{{ post.url | relative_url }}">{{ post.title | escape }}</a></h3>
            <p>{{ post.summary | escape }}</p>
          </div>
          <a class="read-link" href="{{ post.url | relative_url }}">Read →</a>
        </article>
      {% endif %}
    {% endif %}
  {% endfor %}
  {% if visible_count == 0 %}
    <p>No public notes yet.</p>
  {% endif %}
</section>
