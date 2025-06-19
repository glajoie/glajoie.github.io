---
layout: page
permalink: /publications/
title: publications
description: >
  {%- if site.active_lang == "fr" -%}
    liste de publications en ordre chronologique inversé
  {%- else -%}
    list of publications in reversed chronological order
  {%- endif -%}
nav: true
nav_order: 2
---

<!-- _pages/publications.md -->

<!-- Bibsearch Feature -->

{% include bib_search.liquid %}

<div class="publications">

{% bibliography %}

</div>

<hr>

<p>
{% if site.active_lang == "fr" %}
Pour les publications plus anciennes, visitez <a href="https://scholar.google.com/citations?user={{ site.data.socials.scholar_userid }}">Google Scholar</a>.
{% else %}
For older publications, visit <a href="https://scholar.google.com/citations?user={{ site.data.socials.scholar_userid }}">Google Scholar</a>.
{% endif %}
</p>
