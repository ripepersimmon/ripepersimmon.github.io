---
layout: default
title: 태그
permalink: /tags/
---

<h1>태그(악기)별 포스트</h1>
<ul>
{% assign all_tags = site.tags | sort %}
{% for tag in all_tags %}
  <li>
    <a href="/tags/{{ tag[0] | downcase | slugify }}/">
      {{ tag[0] }} ({{ tag[1].size }})
    </a>
  </li>
{% endfor %}
</ul>
