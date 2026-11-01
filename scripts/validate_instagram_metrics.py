#!/usr/bin/env python3
"""Check public-counter accuracy and portfolio preservation before publishing."""
import argparse
from collections import Counter
import json
from pathlib import Path
import re
from update_instagram_metrics import ROOT, aggregate, build, extract_cases, valid_count
from render_instagram_metrics import render


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--baseline", type=Path)
    parser.add_argument("--snapshot", type=Path)
    args = parser.parse_args()
    source = (ROOT / "index.html").read_text()
    from render_campaigns import remove as remove_campaigns
    legacy_source = remove_campaigns(source)
    data = json.loads((ROOT / "INSTAGRAM_METRICS.json").read_text())
    references = json.loads((ROOT / "PROJECT_REFERENCES.json").read_text())
    cases, original = extract_cases(source)
    assert len(cases) == references["displayed_project_count"] == 32
    assert set(cases) == set(data["projects"])
    assert len(original) == references["project_count"] == 28
    for project in references["projects"]:
        assert Counter(original[project["source_index"]]["urls"]) == Counter(link["url"] for link in project["links"]), project["title"]
    assert sum(len(p["links"]) for p in references["projects"]) == 494
    all_codes = list(dict.fromkeys(c for p in cases.values() for c in p["post_codes"]))
    assert set(all_codes) == set(data["posts"])
    assert aggregate(all_codes, data["posts"]) == data["totals"]
    for cid, case in cases.items():
        assert aggregate(case["post_codes"], data["posts"]) == data["projects"][cid], cid
    assert sum(len(p["post_codes"]) for p in cases.values()) == 492
    assert legacy_source.count('class="post-link-copy"') == 492
    assert legacy_source.count('class="project-public-teaser"') == sum(bool(p["unique_posts"]) for p in data["projects"].values())
    assert source.count('class="instagram-total"') == 4
    from render_account_metrics import validate as validate_accounts
    accounts = json.loads((ROOT / "ACCOUNT_METRICS.json").read_text())
    validate_accounts(accounts)
    assert legacy_source.count('data-close-case=') == 32
    assert legacy_source.count('class="case-footer"') == 32
    assert len(re.findall(r'class="[^"]*\bproject-cover\b', legacy_source)) == 32
    assert render(source, data) == source, "Rendering must be idempotent"
    for code, post in data["posts"].items():
        assert post["shortcode"] == code
        assert post["source_url"] == f"https://www.instagram.com/p/{code}/"
        assert post["project_ids"] == [cid for cid, p in cases.items() if code in p["post_codes"]]
        for value in post["metrics"].values():
            assert value is None or (type(value) is int and value >= 0)
        if post["status"] != "available":
            assert all(value is None for value in post["metrics"].values())
    # Regression boundaries protect genuine zero and exclude hidden/sentinel data.
    assert valid_count(0) == 0 and valid_count(0.0) == 0
    for value in (-1, None, False, True, "10", float("nan"), float("inf"), 2.5):
        assert valid_count(value) is None
    if args.snapshot:
        assert build(json.loads(args.snapshot.read_text()), source, references) == data
    if args.baseline:
        baseline = args.baseline.read_text()
        old_links = Counter(re.findall(r'\bhref="([^"]+)"', baseline))
        new_links = Counter(re.findall(r'\bhref="([^"]+)"', source))
        assert not (old_links - new_links), "An original hyperlink was removed"
        def image_sources(text):
            return [re.sub(r'\sstyle="[^"]*"|\sdata-content-crop(?:="[^"]*")?', '', tag) for tag in re.findall(r'<img\b[^>]*>', text)]
        assert image_sources(source) == image_sources(baseline), "Image source or accessible description changed"
        previous_script = re.findall(r'<script>.*?</script>', baseline, re.S)
        current_script = re.findall(r'<script>.*?</script>', source, re.S)
        current_script = [re.sub(r'/\* portfolio-close-details:start \*/.*?/\* portfolio-close-details:end \*/\s*', '', s, flags=re.S) for s in current_script]
        assert current_script == previous_script, "Existing application JavaScript changed"
        for kind in ("case-description",):
            pattern = r'<p class="' + kind + r'"[^>]*>.*?</p>'
            assert re.findall(pattern, source, re.S) == re.findall(pattern, baseline, re.S), f"{kind} changed"
        assert re.findall(r'<dl>.*?</dl>', source, re.S) == re.findall(r'<dl>.*?</dl>', baseline, re.S), "Project descriptions or responsibility/result details changed"
    print(json.dumps({"passed": True, "cards": len(cases), "original_link_associations": 494, "instagram_reference_entries": 492, "unique_posts": len(data["posts"]), "metrics": data["totals"]["metrics"]}, indent=2))


if __name__ == "__main__":
    main()
