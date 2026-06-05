---
layout: page
title: Archive
permalink: /archive/
eyebrow: Chronological index
summary: "All public notes, listed from newest to oldest."
---

{% assign candidate_posts = site.posts | where_exp: "post", "post.hidden != true" %}
{% assign visible_count = 0 %}
{% for post in candidate_posts %}
{% if post.status == "published" or post.status == "corrected" %}
{% assign visible_count = visible_count | plus: 1 %}
<article class="archive-item">
  <p class="post-meta">{{ post.date | date: "%Y-%m-%d" }} · {{ post.topic | default: 'other' | escape }} · {{ post.source_visibility | default: 'public-only' | escape }}</p>
  <h2><a href="{{ post.url | relative_url }}">{{ post.title | escape }}</a></h2>
  <p>{{ post.summary | escape }}</p>
</article>
{% endif %}
{% endfor %}
{% if visible_count == 0 %}
<p>No public notes yet.</p>
{% endif %}
