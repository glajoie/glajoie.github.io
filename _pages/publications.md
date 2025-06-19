---
layout: page
permalink: /publications/
title: "{{ site.data.text.publications[site.active_lang].title }}"
description: "{{ site.data.text.publications[site.active_lang].description }}"
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
