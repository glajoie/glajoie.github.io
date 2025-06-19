---
layout: page
permalink: /fun/
title: fun
description: >
  {%- if site.active_lang == 'fr' -%}
    photos des retraites de groupe et des aventures d'alpinisme
  {%- else -%}
    pictures from group retreats and mountaineering adventures
  {%- endif -%}
nav: true
nav_order: 4
---

<div class="container">
  <div class="row justify-content-sm-center">
    <div class="col-sm">
      {% include figure.liquid path="assets/img/fun/group1.jpg" title="Group Meeting" class="img-fluid rounded z-depth-1" %}
    </div>
  </div>
  <div class="row justify-content-sm-center">
    <div class="col-sm pr-sm-0">
      {% include figure.liquid path="assets/img/fun/mountaineering1.jpg" title="Mountaineering" class="img-fluid rounded z-depth-1" %}
      {% include figure.liquid path="assets/img/fun/mountaineering2.jpg" title="Mountaineering" class="img-fluid rounded z-depth-1" %}
    </div>
    <div class="col-sm">
      {% include figure.liquid path="assets/img/fun/mountaineering3.jpg" title="Mountaineering" class="img-fluid rounded z-depth-1" %}
      {% include figure.liquid path="assets/img/fun/mountaineering4.jpg" title="Mountaineering" class="img-fluid rounded z-depth-1" %}
      {% include figure.liquid path="assets/img/fun/mountaineering5.jpg" title="Mountaineering" class="img-fluid rounded z-depth-1" %}
    </div>
  </div>
</div>
