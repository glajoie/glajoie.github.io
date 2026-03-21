---
layout: page
permalink: /fr/group/
title: groupe
description: membres du groupe de recherche en calcul neuronal à {{ site.institute_name }}
lang: fr
lang_pair: /group/
---

{% assign profiles = site.data.profiles | group_by: 'category' %}
{% for group in profiles %}
{% include profiles.liquid profiles=group is_first=forloop.first %}
{% endfor %}
