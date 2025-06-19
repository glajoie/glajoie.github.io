---
layout: about
title: "{{ site.data.text.about[site.active_lang].title }}"
permalink: /
redirect_from:
  - /home/
subtitle: "{{ site.data.text.about[site.active_lang].subtitle }}"

profile:
  align: right
  image: profile_pic.jpg
  image_circular: false

easter-eggs: true

selected_papers: false
social: true

announcements:
  enabled: true
  scrollable: true
  limit: 5

latest_posts:
  enabled: false
  scrollable: true
  limit: 3
---

<p id="about-bio">{{ site.data.text.about[site.active_lang].bio }}</p>

<p id="about-bio-alt" class="d-none">{{ site.data.text.about[site.active_lang].bio-formal }}</p>

{% include bio_toggle.liquid easter-eggs=page.easter-eggs %}

<!-- Social -->

{% if page.social %}

  <div class="social">
    <div class="contact-icons">{% include social.liquid %}</div>
  </div>
{% endif %}

## affiliations

<ul>
  {% for affiliation in site.data.text.about[site.active_lang].affiliations %}
    <li>{{ affiliation }}</li>
  {% endfor %}
</ul>
