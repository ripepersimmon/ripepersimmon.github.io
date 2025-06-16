---
layout: default
title: "카테고리별 태그별 악보 모아보기"
permalink: /category-tags/
---

<h1>카테고리별 태그(악기)별 포스트 모아보기</h1>
<ul>
{% for category in site.categories %}
  <li>
    <h2>{{ category[0] }}</h2>
    <ul>
    {% assign tags = "" | split: "" %}
    {% for post in category[1] %}
      {% for tag in post.tags %}
        {% unless tags contains tag %}
          {% assign tags = tags | push: tag %}
        {% endunless %}
      {% endfor %}
    {% endfor %}
    {% assign tags = tags | sort %}
    {% for tag in tags %}
      <li>
        <a href="/category/{{ category[0] | downcase | slugify }}/tag/{{ tag | downcase | slugify }}/">
          {{ tag }} 악보 모아보기
        </a>
      </li>
    {% endfor %}
    </ul>
  </li>
{% endfor %}
</ul>
