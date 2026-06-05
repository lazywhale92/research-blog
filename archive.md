---
layout: page
title: Archive
permalink: /archive/
eyebrow: Chronological index
summary: "All public notes, listed from newest to oldest."
---

{% assign visible_posts = site.posts | where_exp: "post", "post.hidden != true" %}
{% for post in visible_posts %}
<article class="archive-item">
  <p class="post-meta">{{ post.date | date: "%Y-%m-%d" }} · {{ post.topic | default: 'other' }} · {{ post.source_visibility | default: 'public-only' }}</p>
  <h2><a href="{{ post.url | relative_url }}">{{ post.title }}</a></h2>
  <p>{{ post.summary }}</p>
</article>
{% else %}
<p>No public notes yet.</p>
{% endfor %}
