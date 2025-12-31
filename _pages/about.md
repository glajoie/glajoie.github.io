---
layout: about
title: >
  {%- if site.active_lang == "fr" -%}
    à propos
  {%- else -%}
    about
  {%- endif -%}
permalink: /
redirect_from:
  - /home/
subtitle: >
  {%- if site.active_lang == "fr" -%}
    Professeur agrégé à <a href='https://www.umontreal.ca/'>l'Université de Montréal</a> ⋅ Membre académique principal de <a href='https://mila.quebec/fr'>Mila – Institut québécois d'intelligence artificielle</a>
  {%- else -%}
    Associate Professor at <a href='https://www.umontreal.ca/en/'>Université de Montréal</a> ⋅ Core Member of <a href='https://mila.quebec/en'>Mila – Quebec AI Institute</a>
  {%- endif -%}

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

{% if site.active_lang == "fr" %}

  <p id="about-bio">Je suis mathématicien appliqué et m'intéresse aux interactions et aux points communs entre les calculs neuronaux biologiques et artificiels. Mon groupe de recherche travaille à l'intersection de l'IA et des neurosciences, ou Neuro-IA, en développant des outils pour mieux comprendre les réseaux neuronaux ainsi que des algorithmes pour les interfaces cerveau-machine à des fins scientifiques et cliniques. Mon travail est motivé par la remarquable capacité des réseaux neuronaux (biologiques et artificiels) à apprendre et à soutenir des calculs complexes et émergents. J'utilise des outils issus des systèmes dynamiques, de la théorie de l'information, des statistiques et de l'apprentissage automatique pour aborder une gamme de problèmes, en collaboration avec des neuroscientifiques expérimentaux et des chercheurs en intelligence artificielle.</p>
  <p id="about-bio-alt" class="d-none">Guillaume Lajoie est professeur agrégé au Département de mathématiques et de statistique de l'Université de Montréal et membre académique principal de Mila - Institut québécois d'intelligence artificielle. Il détient une Chaire de recherche en intelligence artificielle du Canada CIFAR et une Chaire de recherche du Canada en calcul neural et interface. Sa recherche se situe à l'intersection de l'IA et des neurosciences, où il développe des outils pour mieux comprendre les mécanismes d'intelligence communs aux systèmes biologiques et artificiels. Les contributions du groupe de recherche vont des avancées dans les paradigmes d'apprentissage multi-échelle pour les grands systèmes artificiels, aux applications en neurotechnologie. Le Dr Lajoie participe activement aux efforts de développement responsable de l'IA, cherchant à identifier des lignes directrices et des meilleures pratiques pour l'utilisation de l'IA dans la recherche et au-delà.</p>
{% else %}
  <p id="about-bio">I am an applied mathematician interested in the interactions and commonalities of biological and artificial neural computations. My research group works at the intersection of AI and Neuroscience, or Neuro-AI, developing tools to better understand neural networks as well as algorithms for brain-machine interfaces for scientific and clinical use. My work is motivated by the remarkable ability of neural networks (biological and artificial) to learn and support complex, emergent computations. I use tools from dynamical systems, information theory, statistics, and machine learning to address a range of problems, in collaboration with experimental neuroscientists and machine intelligence researchers.</p>
  <p id="about-bio-alt" class="d-none">Guillaume Lajoie is an Associate Professor in the Department of Mathematics and Statistics at Université de Montréal and a Core Academic Member of Mila – Quebec Artificial Intelligence Institute. He holds a Canada CIFAR AI Research Chair, and a Canada Research Chair in Neural Computation and Interfacing. His research is positioned at the intersection of AI and Neuroscience where he develops tools to better understand mechanisms of intelligence common to both biological and artificial systems. His research group's contributions range from advances in multi-scale learning paradigms for large artificial systems, to applications in neurotechnology. Dr. Lajoie is actively involved in responsible AI development efforts, seeking to identify guidelines and best practices for use of AI in research and beyond.</p>
{% endif %}

{% include bio_toggle.liquid easter-eggs=page.easter-eggs %}

<!-- Social -->

{% if page.social %}

  <div class="social">
    <div class="contact-icons">{% include social.liquid %}</div>
  </div>
{% endif %}

## affiliations

{% if site.active_lang == "fr" %}

- Professeur agrégé, [Mathématiques et statistique](https://dms.umontreal.ca/fr/), [Université de Montréal](https://www.umontreal.ca)
- Membre académique principal, [Mila – Institut québécois d'intelligence artificielle](https://mila.quebec/fr)
- Chercheur invité, [Google Paradigms of Intelligence Team](https://github.com/paradigms-of-intelligence)
- [Chaire en intelligence artificielle Canada-CIFAR](https://cifar.ca/fr/biographie/guillaume-lajoie/)
- [Chaire de recherche du Canada en calcul et interfaçage neuronaux](https://www.chairs-chaires.gc.ca/media-medias/lists-listes/2022/january-janvier-fra.aspx)
- Affiliations aux centres de recherche : [UNIQUE](https://fr.unique.quebec/accueil), [CIRCA](https://circa.openum.ca), [CRM](https://www.crmath.ca)
- Accréditations départementales (UdeM) : [Informatique et recherche opérationnelle](https://diro.umontreal.ca/accueil/), [Neurosciences](https://neurosciences.umontreal.ca)

{% else %}

- Associate Professor, [Mathematics and Statistics](https://dms.umontreal.ca/en/), [Université de Montréal](https://www.umontreal.ca/en)
- Core Member, [Mila – Quebec AI Institute](https://mila.quebec/en)
- Visiting Researcher, [Google Paradigms of Intelligence Team](https://github.com/paradigms-of-intelligence)
- [Canada CIFAR AI Chair](https://cifar.ca/bios/guillaume-lajoie/)
- [Canada Research Chair in Neural Computation and Interfacing](https://www.chairs-chaires.gc.ca/media-medias/lists-listes/2022/january-janvier-eng.aspx)
- Research Center Affiliations: [UNIQUE](https://www.unique.quebec/home), [CIRCA](https://circa.openum.ca/en), [CRM](https://www.crmath.ca/en/)
- Departmental Accreditations (UdeM): [Computer Science and Operations Research](https://diro.umontreal.ca/english/home/), [Neuroscience](https://neurosciences.umontreal.ca)

{% endif %}
