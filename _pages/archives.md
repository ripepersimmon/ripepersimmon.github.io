---
layout: default
title: 아카이브
permalink: /archives/
---

<h1>전체 포스트 아카이브</h1>
<ul>
{% for post in site.posts %}
  <li>
    <a href="{{ post.url | relative_url }}">{{ post.title }}</a>
    <span>({{ post.date | date: '%Y-%m-%d' }})</span>
  </li>
{% endfor %}
</ul>
