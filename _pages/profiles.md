---
layout: page
permalink: /group/
redirect_from:
  - /people/
title: "{{ site.data.text.group[site.active_lang].title }}"
description: "{{ site.data.text.group[site.active_lang].description }}"
nav: true
nav_order: 1
---

{% assign profiles = site.data.profiles | group_by: 'category' %}
{% for group in profiles %}
{% include profiles.liquid profiles=group is_first=forloop.first %}
{% endfor %}
