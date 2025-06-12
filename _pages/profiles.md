---
layout: page
permalink: /group/
redirect_from:
  - /people/
title: group
description: members of the {{ site.group_alt_name }} at {{ site.institute_name }}
nav: true
nav_order: 1
---

{% assign profiles = site.data.profiles | group_by: 'category' %}
{% for group in profiles %}
{% include profiles.liquid profiles=group is_first=forloop.first %}
{% endfor %}
