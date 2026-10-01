#!/usr/bin/env python3
"""Fetch publications from a Google Scholar profile into _data/scholar.json.

Google Scholar has no API, so this scrapes the public profile page. The
per-paper detail pages (full author list, publisher link) are only fetched
for papers not already in the data file, to keep the request count low.

Usage: python3 scripts/fetch_scholar.py [SCHOLAR_USER_ID]
The user id defaults to the `scholar` entry in _config.yml.
"""

import html
import json
import random
import re
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_FILE = ROOT / "_data" / "scholar.json"
BASE = "https://scholar.google.com"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
}


def fetch(url):
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=30) as resp:
        body = resp.read().decode("utf-8")
    if "gs_captcha" in body or "unusual traffic" in body:
        raise RuntimeError("Google Scholar returned a CAPTCHA page")
    return body


def text(fragment):
    return html.unescape(re.sub(r"<[^>]+>", "", fragment)).strip()


def user_id_from_config():
    config = (ROOT / "_config.yml").read_text()
    match = re.search(r"^scholar:.*user=([\w-]+)", config, re.M)
    if not match:
        sys.exit("No scholar user id given and none found in _config.yml")
    return match.group(1)


def parse_profile(page):
    pubs = []
    for row in re.findall(r'<tr class="gsc_a_tr">(.*?)</tr>', page, re.S):
        link = re.search(r'<a href="([^"]+)" class="gsc_a_at">(.*?)</a>', row, re.S)
        if not link:
            continue
        href = html.unescape(link.group(1))
        grays = re.findall(r'<div class="gs_gray">(.*?)</div>', row, re.S)
        venue = re.sub(r'<span class="gs_oph">.*?</span>', "", grays[1]) if len(grays) > 1 else ""
        cites = re.search(r'class="gsc_a_ac[^"]*">(\d*)</a>', row)
        year = re.search(r'class="gsc_a_h gsc_a_hc[^"]*">(\d*)</span>', row)
        pubs.append({
            "id": urllib.parse.parse_qs(urllib.parse.urlparse(href).query)["citation_for_view"][0],
            "title": text(link.group(2)),
            "authors": text(grays[0]) if grays else "",
            "venue": text(venue),
            "year": int(year.group(1)) if year and year.group(1) else None,
            "citations": int(cites.group(1)) if cites and cites.group(1) else 0,
            "scholar_url": BASE + href,
        })
    return pubs


def parse_detail(page):
    detail = {}
    link = re.search(r'class="gsc_oci_title_link" href="([^"]+)"', page)
    if link:
        detail["url"] = html.unescape(link.group(1))
    fields = dict(
        (text(k).lower(), text(v))
        for k, v in re.findall(
            r'<div class="gsc_oci_field">(.*?)</div><div class="gsc_oci_value"[^>]*>(.*?)</div>',
            page, re.S,
        )
    )
    if fields.get("authors"):
        detail["authors"] = fields["authors"]
    if fields.get("publication date"):
        detail["date"] = fields["publication date"]
    return detail


def main():
    user = sys.argv[1] if len(sys.argv) > 1 else user_id_from_config()
    known = {}
    if DATA_FILE.exists():
        known = {p["id"]: p for p in json.loads(DATA_FILE.read_text())}

    pubs, start = [], 0
    while True:
        page = fetch(f"{BASE}/citations?user={user}&hl=en&sortby=pubdate"
                     f"&cstart={start}&pagesize=100")
        batch = parse_profile(page)
        pubs += batch
        if len(batch) < 100:
            break
        start += 100
    if not pubs:
        sys.exit("No publications parsed; Scholar markup may have changed")

    for pub in pubs:
        old = known.get(pub["id"])
        if old and "detail_fetched" in old:
            for key in ("url", "authors", "date"):
                if key in old:
                    pub[key] = old[key]
            pub["detail_fetched"] = True
            continue
        time.sleep(random.uniform(2, 5))
        try:
            pub.update(parse_detail(fetch(pub["scholar_url"])))
            pub["detail_fetched"] = True
        except Exception as err:  # keep the profile-level data, retry next run
            print(f"warning: detail fetch failed for {pub['title']!r}: {err}", file=sys.stderr)
        pub.setdefault("url", pub["scholar_url"])

    DATA_FILE.parent.mkdir(exist_ok=True)
    DATA_FILE.write_text(json.dumps(pubs, indent=2, ensure_ascii=False) + "\n")
    print(f"Wrote {len(pubs)} publications to {DATA_FILE.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
