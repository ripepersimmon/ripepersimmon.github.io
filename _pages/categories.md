---
layout: default
title: 카테고리
permalink: /categories/
---

<h1>카테고리별 포스트</h1>
<ul>
{% for category in site.categories %}
  <li>
    <a href="/category/{{ category[0] | downcase | slugify }}/">
      {{ category[0] }} ({{ category[1].size }})
    </a>
  </li>
{% endfor %}
</ul>
