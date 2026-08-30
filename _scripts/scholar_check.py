#!/usr/bin/env python3
"""
Scholar Check: Cross-reference Guillaume Lajoie's publications against the
local papers.bib file.

Usage:
    python3 _scripts/scholar_check.py [--min-year 2019] [--no-cache]
    python3 _scripts/scholar_check.py --source scholar [--fetch-bibs]

This script:
1. Fetches publications from OpenAlex (default) or Google Scholar (--source scholar)
2. Parses the local _bibliography/papers.bib file
3. Cross-references to find:
   - Papers missing from the bib
   - Potential duplicates (arXiv e-prints of published papers)
   - Year/venue mismatches
4. Optionally fetches BibTeX for missing papers (--fetch-bibs, Scholar only)
"""

import argparse
import json
import re
import time
import urllib.request
import urllib.parse
from difflib import SequenceMatcher
from pathlib import Path

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
OPENALEX_AUTHOR_ID = "A5043037494"  # Guillaume Lajoie
SCHOLAR_ID = "ifu_7_0AAAAJ"  # Guillaume Lajoie (Google Scholar)
BIB_PATH = Path(__file__).resolve().parent.parent / "_bibliography" / "papers.bib"
CACHE_DIR = Path(__file__).resolve().parent
MIN_YEAR_DEFAULT = 2019
CACHE_MAX_AGE_HOURS = 24

# OpenAlex work types to skip (peer reviews, datasets, etc.)
OPENALEX_SKIP_TYPES = {"peer-review", "dataset", "editorial", "erratum", "letter"}

# Titles to always skip (theses, popular science, corrections, etc.)
# Use normalize_title() output for matching
SKIP_TITLES = {
    "generative models theory and applications",  # thesis
    "que notre cerveau soit constitue de neurones nest pas un accident",  # popsci (Scholar)
    "que notre cerveau soit constitué de neurones nest pas un accident",  # popsci (OpenAlex)
    "author correction gradient-based learning drives robust representations",
    "large language models what could they do for neurology",  # talk
}

# Known title variants: external title (normalized) -> bib key
# For papers where preprint and published versions have very different titles
KNOWN_VARIANTS = {
    # Google Scholar variants
    "goal-driven optimization of single-neuron properties in artificial networks reveals regularization role of neural diversity and adaptation": "geadah2024neural",
    "deliberation gated by opportunity cost adapts to context with urgency": "puelmatouzel2022performance-gated",
    "neural manifolds and gradient-based adaptation in neural-interface tasks": "payeur2026comparing",
    "a complexity-based theory of compositionality": "elmoznino2025towards",
    "rapidly inferring personalized neurostimulation parameters with meta-learning a case study of individualized fiber recruitment in vagus nerve stimulation": "mao2024personalized",
    "on the inadequacy of cka as a measure of similarity in deep learning": "davari2023reliability",
    "inductive biases for relational tasks": "kerg2022neural",
    "deceiving the cka similarity measure in deep learning": "davari2023reliability",
    "gradient-based learning drives robust representations in recurrent neural networks by balancing compression and expansion vol 4 pg 564 2022": "farrell2022gradient-based",
    "temporal phate a multi-view manifold learning method for brain state trajectories": "busch2023multi-view",
    "online bayesian optimization of nerve stimulation": "wernisch2024online",
    "conn2res a toolbox for connectome-based reservoir computing": "suárez2024connectome-based",
    "explicit knowledge factorization meets in-context learning what do we gain": "mittal2025does",
    "what is a good model for brain encoding in a videogame task": "paugam2025training",
    "exploring exchangeable dataset amortization for bayesian posterior inference": "mittal2025amortized",
    "accelerated learning of a noninvasive human brain-computer interface via manifold geometry": "busch2026human",
    # OpenAlex variants (different normalization from HTML entities, etc.)
    "neural networks with optimized single-neuron adaptation uncover biologically plausible regularization": "geadah2024neural",
    "on neural architecture inductive biases for relational tasks": "kerg2022neural",
    "reliability of cka as a similarity measure in deep learning": "davari2023reliability",
    "multi-view manifold learning of human brain state trajectories": "busch2023multi-view",
    "neural manifolds and learning regimes in neural-interface tasks": "payeur2026comparing",
    "tt conn2res tt  a toolbox for connectome-based reservoir computing": "suárez2024connectome-based",
    # Preprints with different titles from published version
    "recurrent neural networks learn robust representations by dynamically balancing compression and expansion": "farrell2022gradient-based",
    "predictive learning extracts latent space representations from sensory observations": "recanatesi2021predictive",
    "dynamic compression and expansion in a classifying recurrent network": "recanatesi2019dimensionality",
    "learning to evoke complex motor outputs with spatiotemporal neurostimulation using a hierarchical and adaptive optimization algorithm": "bonizzato2020hierarchical",
    "individual auto-regressive models for long-term prediction of bold fmri signal": "paugam2024benchmark",
    "optimizing neuroprosthetic therapies via autonomous learning agents": "bonizzato2023autonomous",
    "implicit regularization in deep learning a view from function space": "baratin2021implicit",
    "lead least-action dynamics for min-max optimization": "askarihemmat2023lead",
    "lead min-max optimization from a physical perspective": "askarihemmat2023lead",
    "modelling working memory using deep recurrent reinforcement learning": "sainath2019modelling",
}

# Bib keys for papers that don't exist yet in the bib - these are intentionally
# excluded older preprints. Add here so they don't appear as "missing".
_INTENTIONAL_EXCLUSIONS = {
    # Old bioRxiv preprint superseded by bonizzato2020hierarchical (published version)
    "learning to evoke complex motor outputs with spatiotemporal neurostimulation using a hierarchical and adaptive optimization algorithm",
}


def normalize_title(title: str) -> str:
    """Normalize a title for comparison: lowercase, strip punctuation/latex/html."""
    title = title.lower()
    # Remove HTML tags
    title = re.sub(r"<[^>]+>", " ", title)
    # Remove LaTeX commands
    title = re.sub(r"\\[a-zA-Z]+\{([^}]*)\}", r"\1", title)
    title = re.sub(r"[\{\}\\]", "", title)
    # Remove punctuation except hyphens
    title = re.sub(r"[^\w\s-]", "", title)
    # Collapse whitespace
    title = re.sub(r"\s+", " ", title).strip()
    return title


def title_similarity(a: str, b: str) -> float:
    """Fuzzy match two titles."""
    return SequenceMatcher(None, normalize_title(a), normalize_title(b)).ratio()


def load_cache(
    cache_path: Path,
    source: str,
    identifier: str,
    requested_min_year: int | None = None,
) -> list[dict] | None:
    """Load a fresh, correctly scoped cache created by this script."""
    if not cache_path.exists():
        return None

    age_hours = (time.time() - cache_path.stat().st_mtime) / 3600
    if age_hours >= CACHE_MAX_AGE_HOURS:
        return None

    try:
        payload = json.loads(cache_path.read_text())
    except (OSError, json.JSONDecodeError):
        return None

    # Flat-list caches were produced by the old script and carry no author or
    # year scope, so using them can silently return the wrong profile/results.
    if not isinstance(payload, dict):
        return None
    if payload.get("source") != source or payload.get("identifier") != identifier:
        return None
    if requested_min_year is not None:
        cached_min_year = payload.get("min_year")
        if not isinstance(cached_min_year, int) or cached_min_year > requested_min_year:
            return None

    publications = payload.get("publications")
    if not isinstance(publications, list):
        return None
    print(f"  Using cached {source} data ({age_hours:.1f}h old)")
    return publications


def save_cache(
    cache_path: Path,
    publications: list[dict],
    source: str,
    identifier: str,
    min_year: int | None = None,
) -> None:
    """Write cache data together with the scope needed to validate it."""
    payload = {
        "source": source,
        "identifier": identifier,
        "fetched_at": int(time.time()),
        "publications": publications,
    }
    if min_year is not None:
        payload["min_year"] = min_year
    cache_path.write_text(json.dumps(payload, indent=2) + "\n")


# ---------------------------------------------------------------------------
# Parse local bib file
# ---------------------------------------------------------------------------
def parse_bib(bib_path: Path) -> list[dict]:
    """Parse a .bib file into a list of entries with key, title, year, type."""
    content = bib_path.read_text()
    entries = []
    for m in re.finditer(
        r"@(\w+)\{([^,]+),\s*\n(.*?)(?=\n@|\Z)", content, re.DOTALL
    ):
        entry_type = m.group(1).lower()
        key = m.group(2).strip()
        body = m.group(3)

        title_m = re.search(r"title\s*=\s*\{(.+?)\}(?:\s*,|\s*\n)", body)
        year_m = re.search(r"year\s*=\s*(\{?\d{4}\}?)", body)
        abbr_m = re.search(r"abbr\s*=\s*\{(.+?)\}", body)

        title = title_m.group(1) if title_m else ""
        year = int(re.sub(r"[{}]", "", year_m.group(1))) if year_m else 0
        abbr = abbr_m.group(1) if abbr_m else ""

        entries.append(
            {
                "key": key,
                "type": entry_type,
                "title": title,
                "title_norm": normalize_title(title),
                "year": year,
                "abbr": abbr,
            }
        )
    return entries


# ---------------------------------------------------------------------------
# Fetch from OpenAlex
# ---------------------------------------------------------------------------
def fetch_openalex_pubs(
    author_id: str, min_year: int, use_cache: bool = True
) -> list[dict]:
    """Fetch publications from OpenAlex API. Caches results."""
    cache_path = CACHE_DIR / ".openalex_cache.json"

    if use_cache:
        cached = load_cache(cache_path, "OpenAlex", author_id, min_year)
        if cached is not None:
            return cached

    print("  Fetching publications from OpenAlex...")
    all_works = []
    page = 1
    per_page = 100

    while True:
        params = urllib.parse.urlencode(
            {
                "filter": f"author.id:{author_id},from_publication_date:{min_year}-01-01",
                "sort": "publication_date:desc",
                "per_page": per_page,
                "page": page,
                "select": "title,publication_year,primary_location,type,cited_by_count,doi,ids",
            }
        )
        url = f"https://api.openalex.org/works?{params}"
        req = urllib.request.Request(
            url, headers={"User-Agent": "LajoieGroupWebsite/1.0 (scholarly check)"}
        )
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode())

        results = data.get("results", [])
        all_works.extend(results)
        total = data["meta"]["count"]
        print(f"  Page {page}: {len(all_works)}/{total} works...")

        if len(all_works) >= total or not results:
            break
        page += 1
        time.sleep(0.5)  # polite rate limiting

    # Convert to common format
    pubs = []
    for w in all_works:
        wtype = w.get("type", "")
        if wtype in OPENALEX_SKIP_TYPES:
            continue

        title = w.get("title", "") or ""
        year = w.get("publication_year", 0) or 0
        loc = w.get("primary_location") or {}
        source = (loc.get("source") or {}).get("display_name", "")
        doi = w.get("doi", "") or ""

        pubs.append(
            {
                "title": title,
                "title_norm": normalize_title(title),
                "year": year,
                "venue": source,
                "num_citations": w.get("cited_by_count", 0),
                "doi": doi,
                "type": wtype,
                "source": "openalex",
            }
        )

    print(f"  Fetched {len(pubs)} publications from OpenAlex")
    save_cache(cache_path, pubs, "OpenAlex", author_id, min_year)
    return pubs


# ---------------------------------------------------------------------------
# Fetch from Google Scholar via scholarly (fallback)
# ---------------------------------------------------------------------------
def fetch_scholar_pubs(scholar_id: str, use_cache: bool = True) -> list[dict]:
    """Fetch publications from Google Scholar. Caches results to avoid rate limits."""
    cache_path = CACHE_DIR / ".scholar_cache.json"

    if use_cache:
        cached = load_cache(cache_path, "Google Scholar", scholar_id)
        if cached is not None:
            return cached

    try:
        from scholarly import scholarly
    except ImportError as exc:
        raise SystemExit(
            "Google Scholar support requires the optional 'scholarly' package. "
            "Install it with: python3 -m pip install scholarly"
        ) from exc

    print("  Fetching author profile from Google Scholar...")
    for attempt in range(3):
        try:
            time.sleep(5 * (attempt + 1))
            author = scholarly.search_author_id(scholar_id)
            time.sleep(5)
            author = scholarly.fill(author, sections=["publications"])
            break
        except Exception as e:
            print(f"  Attempt {attempt + 1} failed: {e}")
            if attempt == 2:
                raise

    pubs = []
    total = len(author["publications"])
    for i, pub in enumerate(author["publications"]):
        bib = pub.get("bib", {})
        title = bib.get("title", "")
        year = int(bib.get("pub_year", 0) or 0)
        venue = bib.get("citation", "")
        num_citations = pub.get("num_citations", 0)

        pubs.append(
            {
                "title": title,
                "title_norm": normalize_title(title),
                "year": year,
                "venue": venue,
                "num_citations": num_citations,
                "author_pub_id": pub.get("author_pub_id", ""),
                "source": "scholar",
            }
        )
        if (i + 1) % 20 == 0:
            print(f"  Processed {i + 1}/{total} publications...")

    print(f"  Fetched {len(pubs)} publications from Scholar")
    save_cache(cache_path, pubs, "Google Scholar", scholar_id)
    return pubs


def fetch_bibtex_for_pub(pub: dict) -> str | None:
    """Fetch a BibTeX string for a single Scholar publication."""
    try:
        from scholarly import scholarly
    except ImportError:
        return "% Install the optional 'scholarly' package to fetch BibTeX"

    try:
        result = next(scholarly.search_pubs(pub["title"]))
        return scholarly.bibtex(result)
    except Exception as e:
        return f"% Error fetching bibtex: {e}"


# ---------------------------------------------------------------------------
# Cross-reference logic
# ---------------------------------------------------------------------------
def find_best_match(
    pub: dict, bib_entries: list[dict]
) -> tuple[dict | None, float]:
    """Find the best matching bib entry for a publication."""
    best_match = None
    best_score = 0.0
    for entry in bib_entries:
        score = title_similarity(pub["title"], entry["title"])
        if score > best_score:
            best_score = score
            best_match = entry
    return best_match, best_score


def is_preprint_venue(venue: str) -> bool:
    """Check if a venue string suggests a preprint."""
    venue_lower = venue.lower()
    return any(
        p in venue_lower
        for p in ["arxiv", "biorxiv", "psyarxiv", "preprint", "ssrn"]
    )


def is_nonpublication_venue(venue: str) -> bool:
    """Check for repositories that OpenAlex may expose as a work's venue."""
    venue_lower = venue.lower()
    return is_preprint_venue(venue) or any(
        marker in venue_lower
        for marker in [
            "repository",
            "research data",
            "zenodo",
            "figshare",
            "hal open science",
            "osf",
        ]
    )


def classify_pub(
    pub: dict, bib_entries: list[dict], threshold: float = 0.82
) -> dict:
    """Classify a publication relative to the bib file."""
    best_match, score = find_best_match(pub, bib_entries)

    result = {
        "title": pub["title"],
        "year": pub["year"],
        "venue": pub.get("venue", ""),
        "citations": pub.get("num_citations", 0),
        "doi": pub.get("doi", ""),
        "match_score": score,
        "bib_key": best_match["key"] if best_match and score >= threshold else None,
        "bib_title": best_match["title"] if best_match and score >= threshold else None,
        "bib_year": best_match["year"] if best_match and score >= threshold else None,
        "bib_abbr": best_match["abbr"] if best_match and score >= threshold else None,
        "status": "unknown",
    }

    # Skip known exclusions
    if pub["title_norm"] in SKIP_TITLES or pub["title_norm"] in _INTENTIONAL_EXCLUSIONS:
        result["status"] = "skip"
        return result

    # Check known variants map
    if pub["title_norm"] in KNOWN_VARIANTS:
        target_key = KNOWN_VARIANTS[pub["title_norm"]]
        target = next((e for e in bib_entries if e["key"] == target_key), None)
        if target:
            result["bib_key"] = target["key"]
            result["bib_title"] = target["title"]
            result["bib_year"] = target["year"]
            result["bib_abbr"] = target["abbr"]
            external_preprint = is_nonpublication_venue(pub.get("venue", ""))
            bib_preprint = is_preprint_venue(target.get("abbr", ""))
            if external_preprint and not bib_preprint:
                result["status"] = "published_version_present"
            elif not external_preprint and bib_preprint:
                result["status"] = "published_update_candidate"
            else:
                result["status"] = "known_variant"
            return result

    if score >= threshold:
        external_preprint = is_nonpublication_venue(pub.get("venue", ""))
        bib_preprint = is_preprint_venue(best_match.get("abbr", ""))
        if external_preprint and not bib_preprint:
            result["status"] = "published_version_present"
        elif not external_preprint and bib_preprint:
            result["status"] = "published_update_candidate"
        elif pub["year"] != best_match["year"] and not (
            external_preprint and bib_preprint
        ):
            result["status"] = "matched_year_mismatch"
        else:
            result["status"] = "matched"
    elif score >= 0.65:
        result["bib_key"] = best_match["key"]
        result["bib_title"] = best_match["title"]
        result["status"] = "possible_variant"
    else:
        result["status"] = "missing"

    return result


# ---------------------------------------------------------------------------
# Report
# ---------------------------------------------------------------------------
def print_report(results: list[dict], source: str, fetch_bibs: bool = False):
    missing = [r for r in results if r["status"] == "missing"]
    variants = [r for r in results if r["status"] == "possible_variant"]
    year_mismatches = [r for r in results if r["status"] == "matched_year_mismatch"]
    published_present = [
        r for r in results if r["status"] == "published_version_present"
    ]
    update_candidates = [
        r for r in results if r["status"] == "published_update_candidate"
    ]
    known_variants = [r for r in results if r["status"] == "known_variant"]
    matched = [r for r in results if r["status"] == "matched"]
    skipped = [r for r in results if r["status"] == "skip"]

    source_label = "OpenAlex" if source == "openalex" else "Google Scholar"
    print("\n" + "=" * 70)
    print(f"{source_label} vs BIB CROSS-REFERENCE REPORT")
    print("=" * 70)

    print(f"\n  Total pubs checked:         {len(results)}")
    print(f"  Matched:                    {len(matched)}")
    print(f"  Year mismatches:            {len(year_mismatches)}")
    print(f"  Known variants:             {len(known_variants)}")
    print(f"  Possible variants:          {len(variants)}")
    print(f"  Published version present:  {len(published_present)}")
    print(f"  Published updates to check: {len(update_candidates)}")
    print(f"  Missing from bib:           {len(missing)}")
    print(f"  Skipped (thesis/popsci):    {len(skipped)}")

    if missing:
        print("\n" + "-" * 70)
        print("MISSING FROM BIB FILE")
        print("-" * 70)
        for r in sorted(missing, key=lambda x: -x["year"]):
            cite_str = f" [{r['citations']} cites]" if r["citations"] else ""
            print(f"\n  [{r['year']}] {r['title']}")
            print(f"         Venue: {r['venue']}{cite_str}")
            if r.get("doi"):
                print(f"         DOI: {r['doi']}")
            if fetch_bibs and source == "scholar":
                print("         Fetching BibTeX...")
                bib = fetch_bibtex_for_pub(r)
                if bib:
                    print("         " + bib.replace("\n", "\n         "))
                time.sleep(2)

    if variants:
        print("\n" + "-" * 70)
        print("POSSIBLE VARIANTS (different title, might be related)")
        print("-" * 70)
        for r in sorted(variants, key=lambda x: -x["year"]):
            print(f"\n  [{r['year']}] {r['title']}")
            print(f"         Venue: {r['venue']}")
            if r.get("doi"):
                print(f"         DOI: {r['doi']}")
            print(
                f"         ~~ Possible match: {r['bib_key']} "
                f"(score: {r['match_score']:.2f})"
            )
            print(f"            Bib title: {r['bib_title']}")

    if year_mismatches:
        print("\n" + "-" * 70)
        print("YEAR MISMATCHES (matched but years differ)")
        print("-" * 70)
        for r in sorted(year_mismatches, key=lambda x: -x["year"]):
            print(f"\n  [{r['year']}] {r['title']}")
            print(
                f"         Bib: {r['bib_key']} (year={r['bib_year']}, "
                f"abbr={r['bib_abbr']})"
            )

    if update_candidates:
        print("\n" + "-" * 70)
        print("PUBLISHED UPDATES TO CHECK (external venue, preprint in bib)")
        print("-" * 70)
        for r in sorted(update_candidates, key=lambda x: -x["year"]):
            print(f"\n  [{r['year']}] {r['title']}")
            print(f"         Venue: {r['venue']}")
            print(
                f"         Bib preprint: {r['bib_key']} "
                f"(score: {r['match_score']:.2f})"
            )

    print("\n" + "=" * 70)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(
        description="Cross-reference publications vs bib file"
    )
    parser.add_argument(
        "--source",
        choices=["openalex", "scholar"],
        default="openalex",
        help="Data source (default: openalex)",
    )
    parser.add_argument(
        "--fetch-bibs",
        action="store_true",
        help="Fetch BibTeX for missing papers (Scholar only)",
    )
    parser.add_argument(
        "--min-year",
        type=int,
        default=MIN_YEAR_DEFAULT,
        help=f"Minimum publication year (default: {MIN_YEAR_DEFAULT})",
    )
    parser.add_argument(
        "--no-cache",
        action="store_true",
        help="Ignore cached data",
    )
    args = parser.parse_args()

    print(f"Bib file: {BIB_PATH}")
    print(f"Source: {args.source}")
    print(f"Min year: {args.min_year}")

    # Parse local bib
    print("\nParsing local bib file...")
    bib_entries = parse_bib(BIB_PATH)
    print(f"  Found {len(bib_entries)} entries")

    # Fetch publication data
    print(f"\nFetching from {args.source}...")
    if args.source == "openalex":
        pubs = fetch_openalex_pubs(
            OPENALEX_AUTHOR_ID, args.min_year, use_cache=not args.no_cache
        )
    else:
        pubs = fetch_scholar_pubs(SCHOLAR_ID, use_cache=not args.no_cache)

    # Filter by year
    pubs = [p for p in pubs if p["year"] >= args.min_year]
    print(f"  {len(pubs)} publications after year filter (>= {args.min_year})")

    # Deduplicate by normalized title, preferring a venue publication over its
    # preprint when an index returns both records.
    pubs_by_title = {}
    for pub in pubs:
        norm = pub["title_norm"]
        if not norm:
            continue
        existing = pubs_by_title.get(norm)
        if existing is None or (
            is_nonpublication_venue(existing.get("venue", ""))
            and not is_nonpublication_venue(pub.get("venue", ""))
        ):
            pubs_by_title[norm] = pub
    unique_pubs = list(pubs_by_title.values())
    print(f"  {len(unique_pubs)} unique titles after dedup")

    # Cross-reference
    print("\nCross-referencing...")
    results = []
    for pub in unique_pubs:
        result = classify_pub(pub, bib_entries)
        results.append(result)

    print_report(results, source=args.source, fetch_bibs=args.fetch_bibs)


if __name__ == "__main__":
    main()
