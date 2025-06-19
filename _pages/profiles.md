---
layout: page
permalink: /group/
redirect_from:
  - /people/
title: >
  {%- if site.active_lang == "fr" -%}
    groupe
  {%- else -%}
    group
  {%- endif -%}
description: >
  {%- if site.active_lang == "fr" -%}
    membres du groupe de recherche en calculs neuronaux au Mila
  {%- else -%}
    members of the Neural Computations Research Group at Mila
  {%- endif -%}
nav: true
nav_order: 1
---

{% assign profiles = site.data.profiles | group_by: 'category' %}
{% for group in profiles %}
{% include profiles.liquid profiles=group is_first=forloop.first %}
{% endfor %}
