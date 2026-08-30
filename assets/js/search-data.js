// get the ninja-keys element
const ninja = document.querySelector('ninja-keys');

// add the home and posts menu items
ninja.data = [{
    id: "nav-about",
    title: "about",
    section: "Navigation",
    handler: () => {
      window.location.href = "/";
    },
  },{id: "nav-group",
          title: "group",
          description: "members of the {{ site.group_alt_name }} at {{ site.institute_name }}",
          section: "Navigation",
          handler: () => {
            window.location.href = "/group/";
          },
        },{id: "nav-publications",
          title: "publications",
          description: "publications by categories in reversed chronological order",
          section: "Navigation",
          handler: () => {
            window.location.href = "/publications/";
          },
        },{id: "nav-teaching",
          title: "teaching",
          description: "courses taught at {{ site.university_name }} and links to materials",
          section: "Navigation",
          handler: () => {
            window.location.href = "/teaching/";
          },
        },{id: "nav-fun",
          title: "fun",
          description: "pictures from group retreats and mountaineering adventures",
          section: "Navigation",
          handler: () => {
            window.location.href = "/fun/";
          },
        },{id: "news-as-we-welcome-spring-the-group-s-website-has-finally-been-updated-seedling-cherry-blossom",
          title: 'As we welcome spring, the group’s website has finally been updated! :seedling: :cherry_blossom:...'.replace(/:([a-zA-Z0-9_+-]+):/g, ""),
          description: "",
          section: "News",},{id: "news-avec-l-arrivée-du-printemps-le-site-web-du-groupe-a-enfin-été-mis-à-jour-seedling-cherry-blossom",
          title: 'Avec l’arrivée du printemps, le site web du groupe a enfin été mis...'.replace(/:([a-zA-Z0-9_+-]+):/g, ""),
          description: "",
          section: "News",},{id: "news-congratulations-to-françois-paugam-for-successfully-defending-his-phd-thesis-mortar-board",
          title: 'Congratulations to François Paugam for successfully defending his PhD thesis! :mortar_board:'.replace(/:([a-zA-Z0-9_+-]+):/g, ""),
          description: "",
          section: "News",},{id: "news-félicitations-à-françois-paugam-pour-la-soutenance-réussie-de-sa-thèse-de-doctorat-mortar-board",
          title: 'Félicitations à François Paugam pour la soutenance réussie de sa thèse de doctorat...'.replace(/:([a-zA-Z0-9_+-]+):/g, ""),
          description: "",
          section: "News",},{id: "news-roman-starts-as-a-research-scientist-at-google-in-the-paradigms-of-intelligence-team-he-ll-still-join-us-for-friday-drinks-though-beers",
          title: 'Roman starts as a Research Scientist at Google, in the Paradigms of Intelligence...'.replace(/:([a-zA-Z0-9_+-]+):/g, ""),
          description: "",
          section: "News",},{id: "news-roman-commence-comme-chercheur-scientifique-chez-google-dans-l-équipe-paradigms-of-intelligence-il-nous-rejoindra-quand-même-pour-les-bières-du-vendredi-beers",
          title: 'Roman commence comme chercheur scientifique chez Google, dans l’équipe Paradigms of Intelligence. Il...'.replace(/:([a-zA-Z0-9_+-]+):/g, ""),
          description: "",
          section: "News",},{id: "news-olivier-starts-as-a-research-scientist-at-meta-reality-labs-nyc-we-ll-miss-having-him-here-city-sunset",
          title: 'Olivier starts as a Research Scientist at Meta Reality Labs, NYC. We’ll miss...'.replace(/:([a-zA-Z0-9_+-]+):/g, ""),
          description: "",
          section: "News",},{id: "news-olivier-commence-comme-chercheur-scientifique-chez-meta-reality-labs-nyc-il-nous-manquera-city-sunset",
          title: 'Olivier commence comme chercheur scientifique chez Meta Reality Labs, NYC. Il nous manquera...'.replace(/:([a-zA-Z0-9_+-]+):/g, ""),
          description: "",
          section: "News",},{id: "news-congratulations-to-amine-natik-for-successfully-defending-his-phd-thesis-mortar-board",
          title: 'Congratulations to Amine Natik for successfully defending his PhD thesis! :mortar_board:'.replace(/:([a-zA-Z0-9_+-]+):/g, ""),
          description: "",
          section: "News",},{id: "news-félicitations-à-amine-natik-pour-la-soutenance-réussie-de-sa-thèse-de-doctorat-mortar-board",
          title: 'Félicitations à Amine Natik pour la soutenance réussie de sa thèse de doctorat...'.replace(/:([a-zA-Z0-9_+-]+):/g, ""),
          description: "",
          section: "News",},{id: "news-congratulations-to-ezekiel-williams-on-defending-his-phd-thesis-mortar-board",
          title: 'Congratulations to Ezekiel Williams on defending his PhD thesis! :mortar_board:'.replace(/:([a-zA-Z0-9_+-]+):/g, ""),
          description: "",
          section: "News",},{id: "news-félicitations-à-zeke-williams-pour-l-obtention-de-son-doctorat-mortar-board",
          title: 'Félicitations à Zeke Williams pour l’obtention de son doctorat ! :mortar_board:'.replace(/:([a-zA-Z0-9_+-]+):/g, ""),
          description: "",
          section: "News",},{id: "news-colin-starts-as-an-assistant-professor-at-the-university-of-oregon-we-wish-him-all-the-best-in-this-next-chapter-and-raise-a-blanche-de-charlevoix-in-his-honour-beers",
          title: 'Colin starts as an Assistant Professor at the University of Oregon! We wish...'.replace(/:([a-zA-Z0-9_+-]+):/g, ""),
          description: "",
          section: "News",},{id: "news-colin-devient-professeur-adjoint-à-l-université-de-l-oregon-nous-lui-souhaitons-le-meilleur-pour-ce-nouveau-chapitre-et-levons-une-blanche-de-charlevoix-à-sa-santé-beers",
          title: 'Colin devient professeur adjoint à l’Université de l’Oregon ! Nous lui souhaitons le...'.replace(/:([a-zA-Z0-9_+-]+):/g, ""),
          description: "",
          section: "News",},{
        id: 'social-email',
        title: 'email',
        section: 'Socials',
        handler: () => {
          window.open("mailto:%67.%6C%61%6A%6F%69%65@%75%6D%6F%6E%74%72%65%61%6C.%63%61", "_blank");
        },
      },{
        id: 'social-scholar',
        title: 'Google Scholar',
        section: 'Socials',
        handler: () => {
          window.open("https://scholar.google.com/citations?user=ifu_7_0AAAAJ", "_blank");
        },
      },{
        id: 'social-x',
        title: 'X',
        section: 'Socials',
        handler: () => {
          window.open("https://twitter.com/g_lajoie_", "_blank");
        },
      },{
        id: 'social-bluesky',
        title: 'Bluesky',
        section: 'Socials',
        handler: () => {
          window.open("https://bsky.app/profile/glajoie.bsky.social", "_blank");
        },
      },{
        id: 'social-orcid',
        title: 'ORCID',
        section: 'Socials',
        handler: () => {
          window.open("https://orcid.org/0000-0003-2730-7291", "_blank");
        },
      },{
        id: 'social-cv',
        title: 'Curriculum Vitae',
        section: 'Socials',
        handler: () => {
          window.open("https://drive.google.com/file/d/1Q4mVLYZignHPm0I1RggS7h7oFttNgpgL/view", "_blank");
        },
      },{id: "profile-matteo-alleman",
      title: "Matteo Alleman",
      description: "Postdocs",
      section: "Group",
      handler: () => {
        window.location.href = "/group#matteo-alleman";
      },
    },{id: "profile-ryan-vogt",
      title: "Ryan Vogt",
      description: "Postdocs",
      section: "Group",
      handler: () => {
        window.location.href = "/group#ryan-vogt";
      },
    },{id: "profile-tom-george",
      title: "Tom George",
      description: "Postdocs",
      section: "Group",
      handler: () => {
        window.location.href = "/group#tom-george";
      },
    },{id: "profile-abdel-mfougouon-njupoun",
      title: "Abdel Mfougouon Njupoun",
      description: "PhD students",
      section: "Group",
      handler: () => {
        window.location.href = "/group#abdel-mfougouon-njupoun";
      },
    },{id: "profile-avery-hee-woon-ryoo",
      title: "Avery Hee-Woon Ryoo",
      description: "PhD students",
      section: "Group",
      handler: () => {
        window.location.href = "/group#avery-hee-woon-ryoo";
      },
    },{id: "profile-chen-jiang",
      title: "Chen Jiang",
      description: "PhD students",
      section: "Group",
      handler: () => {
        window.location.href = "/group#chen-jiang";
      },
    },{id: "profile-eric-elmoznino",
      title: "Eric Elmoznino",
      description: "PhD students",
      section: "Group",
      handler: () => {
        window.location.href = "/group#eric-elmoznino";
      },
    },{id: "profile-juan-david-guerra",
      title: "Juan David Guerra",
      description: "PhD students",
      section: "Group",
      handler: () => {
        window.location.href = "/group#juan-david-guerra";
      },
    },{id: "profile-léo-choinière",
      title: "Léo Choinière",
      description: "PhD students",
      section: "Group",
      handler: () => {
        window.location.href = "/group#l%C3%A9o-choini%C3%A8re";
      },
    },{id: "profile-léo-gagnon",
      title: "Léo Gagnon",
      description: "PhD students",
      section: "Group",
      handler: () => {
        window.location.href = "/group#l%C3%A9o-gagnon";
      },
    },{id: "profile-nanda-h-krishna",
      title: "Nanda H Krishna",
      description: "PhD students",
      section: "Group",
      handler: () => {
        window.location.href = "/group#nanda-h-krishna";
      },
    },{id: "profile-pingsheng-li",
      title: "Pingsheng Li",
      description: "PhD students",
      section: "Group",
      handler: () => {
        window.location.href = "/group#pingsheng-li";
      },
    },{id: "profile-pravish-sainath",
      title: "Pravish Sainath",
      description: "PhD students",
      section: "Group",
      handler: () => {
        window.location.href = "/group#pravish-sainath";
      },
    },{id: "profile-sangnie-bhardwaj",
      title: "Sangnie Bhardwaj",
      description: "PhD students",
      section: "Group",
      handler: () => {
        window.location.href = "/group#sangnie-bhardwaj";
      },
    },{id: "profile-sarthak-mittal",
      title: "Sarthak Mittal",
      description: "PhD students",
      section: "Group",
      handler: () => {
        window.location.href = "/group#sarthak-mittal";
      },
    },{id: "profile-thomas-jiralerspong",
      title: "Thomas Jiralerspong",
      description: "PhD students",
      section: "Group",
      handler: () => {
        window.location.href = "/group#thomas-jiralerspong";
      },
    },{id: "profile-ximeng-mao",
      title: "Ximeng Mao",
      description: "PhD students",
      section: "Group",
      handler: () => {
        window.location.href = "/group#ximeng-mao";
      },
    },{id: "profile-julia-price",
      title: "Julia Price",
      description: "MSc students",
      section: "Group",
      handler: () => {
        window.location.href = "/group#julia-price";
      },
    },{id: "profile-mauricio-rivera",
      title: "Mauricio Rivera",
      description: "MSc students",
      section: "Group",
      handler: () => {
        window.location.href = "/group#mauricio-rivera";
      },
    },{id: "profile-tejas-kasetty",
      title: "Tejas Kasetty",
      description: "MSc students",
      section: "Group",
      handler: () => {
        window.location.href = "/group#tejas-kasetty";
      },
    },{id: "profile-mathys-loiselle",
      title: "Mathys Loiselle",
      description: "Undergrads",
      section: "Group",
      handler: () => {
        window.location.href = "/group#mathys-loiselle";
      },
    },{
      id: 'light-theme',
      title: 'Change theme to light',
      description: 'Change the theme of the site to Light',
      section: 'Theme',
      handler: () => {
        setThemeSetting("light");
      },
    },
    {
      id: 'dark-theme',
      title: 'Change theme to dark',
      description: 'Change the theme of the site to Dark',
      section: 'Theme',
      handler: () => {
        setThemeSetting("dark");
      },
    },
    {
      id: 'system-theme',
      title: 'Use system default theme',
      description: 'Change the theme of the site to System Default',
      section: 'Theme',
      handler: () => {
        setThemeSetting("system");
      },
    },];
