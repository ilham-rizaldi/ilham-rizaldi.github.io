#!/usr/bin/env python3
"""Build auditable public Instagram snapshots and static portfolio metrics.

Usage: python3 scripts/update_instagram_metrics.py instagram-source-snapshot.json
Input: {started_at, finished_at, actor, items:[Apify post records]}.
Only top-level public counters are used. No account credentials are required.
"""
from __future__ import annotations
import argparse
import csv
import hashlib
import html
import io
import json
import math
import re
from collections import Counter
from datetime import datetime
from pathlib import Path
from urllib.parse import urlsplit
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parent.parent
FIELDS = {"likes": "likesCount", "comments": "commentsCount", "plays": "videoPlayCount", "views": "videoViewCount"}
CASE_RE = re.compile(r'<details\b[^>]*class="[^\"]*\bcase\b[^\"]*"[^>]*>[\s\S]*?</details>')


def shortcode(url):
    if not isinstance(url, str):
        return None
    parsed = urlsplit(html.unescape(url))
    if parsed.hostname not in {"instagram.com", "www.instagram.com"}:
        return None
    match = re.search(r"/(?:p|reel|tv)/([A-Za-z0-9_-]+)(?:/|$)", parsed.path)
    return match.group(1) if match else None


def valid_count(value):
    # False, null, missing and the hidden-like sentinel -1 must never become 0.
    if type(value) not in (int, float) or not math.isfinite(value) or value < 0 or int(value) != value:
        return None
    return int(value)


def extract_cases(source):
    cases = {}
    original_indices = {}
    for match in CASE_RE.finditer(source):
        block = match.group()
        case_id = re.search(r'\bid="([^\"]+)"', block).group(1)
        if case_id in cases:
            raise ValueError(f"Duplicate case id: {case_id}")
        related = re.search(r'<ul class="related-links">([\s\S]*?)</ul>', block)
        urls = [html.unescape(u) for u in re.findall(r'<a\b[^>]*\bhref="([^\"]+)"', related.group(1))] if related else []
        cases[case_id] = {"urls": urls, "post_codes": list(dict.fromkeys(c for u in urls if (c := shortcode(u))))}
        original = re.search(r'\bdata-original-index="(\d+)"', block)
        if original:
            original_indices[int(original.group(1))] = {"case_id": case_id, "urls": urls}
    return cases, original_indices


def aggregate(codes, posts):
    codes = list(dict.fromkeys(codes))
    selected = [posts[c] for c in codes]
    videos = [p for p in selected if p["type"] == "Video"]
    metrics = {}
    for key in FIELDS:
        eligible = videos if key in {"plays", "views"} else selected
        values = [p["metrics"][key] for p in eligible if p["metrics"][key] is not None]
        metrics[key] = {"total": sum(values), "available": len(values), "eligible": len(eligible)}
    complete = sum(all(p["metrics"][k] is not None for k in ("likes", "comments")) for p in selected)
    any_component = sum(any(p["metrics"][k] is not None for k in ("likes", "comments")) for p in selected)
    metrics["interactions"] = {
        "total": metrics["likes"]["total"] + metrics["comments"]["total"],
        "available": any_component,
        "eligible": len(selected),
        "complete_posts": complete,
        "partial_posts": any_component - complete,
    }
    return {
        "unique_posts": len(codes),
        "available_posts": sum(p["status"] == "available" for p in selected),
        "unavailable_posts": sum(p["status"] != "available" for p in selected),
        "video_posts": len(videos),
        "image_posts": sum(p["type"] == "Image" for p in selected),
        "carousel_posts": sum(p["type"] == "Sidecar" for p in selected),
        "distinct_publishers": len({p["owner"] for p in selected if p["owner"]}),
        "metrics": metrics,
        "post_codes": codes,
    }


def build(snapshot, source, references):
    cases, original = extract_cases(source)
    if len(cases) != references["displayed_project_count"]:
        raise ValueError("Project count changed")
    expected_indices = {p["source_index"] for p in references["projects"]}
    if set(original) != expected_indices:
        raise ValueError("Original source project coverage changed")
    for project in references["projects"]:
        expected = Counter(link["url"] for link in project["links"])
        if Counter(original[project["source_index"]]["urls"]) != expected:
            raise ValueError(f"Original reference associations changed: {project['title']}")
    all_codes = list(dict.fromkeys(c for p in cases.values() for c in p["post_codes"]))
    posts = {}
    for item in snapshot["items"]:
        code = item.get("shortCode") or shortcode(item.get("url")) or shortcode(item.get("inputUrl"))
        if not code:
            raise ValueError("Source row without an Instagram post identifier")
        if code in posts:
            raise ValueError(f"Duplicate source row: {code}")
        metrics = {name: valid_count(item.get(field)) for name, field in FIELDS.items()}
        reasons = {}
        for name, field in FIELDS.items():
            if metrics[name] is None:
                reasons[name] = "hidden" if item.get(field) == -1 else "not_available"
        duration = item.get("videoDuration")
        if type(duration) not in (int, float) or not math.isfinite(duration) or duration < 0:
            duration = None
        posts[code] = {
            "shortcode": code,
            "id": str(item["id"]) if item.get("id") else None,
            "source_url": f"https://www.instagram.com/p/{code}/",
            "owner": item.get("ownerUsername"),
            "published_at": item.get("timestamp"),
            "type": item.get("type"),
            "duration_seconds": round(duration, 2) if duration is not None else None,
            "status": ("restricted" if item.get("error") == "restricted_page" else "unavailable") if item.get("error") else "available",
            "metrics": metrics,
            "missing_reasons": reasons,
        }
        if item.get("error"):
            posts[code]["metrics"] = dict.fromkeys(FIELDS)
            posts[code]["missing_reasons"] = dict.fromkeys(FIELDS, posts[code]["status"])
    if set(posts) != set(all_codes):
        raise ValueError(f"Snapshot/source mismatch: missing={set(all_codes)-set(posts)}, extra={set(posts)-set(all_codes)}")
    collected = datetime.fromisoformat(snapshot["finished_at"].replace("Z", "+00:00"))
    local = collected.astimezone(ZoneInfo("Asia/Jakarta"))
    projects = {cid: aggregate(case["post_codes"], posts) for cid, case in cases.items()}
    for code, post in posts.items():
        post["project_ids"] = [cid for cid, case in cases.items() if code in case["post_codes"]]
    return {
        "schema_version": 1,
        "snapshot": {
            "collected_from": snapshot["started_at"],
            "collected_at": snapshot["finished_at"],
            "display_date": f"{local.day} {local.strftime('%b %Y, %H:%M')} WIB",
            "timezone": "Asia/Jakarta",
            "source": snapshot["actor"],
            "source_documentation": "https://apify.com/apify/instagram-scraper",
            "project_reference_source_commit": references["source_commit"],
        },
        "methodology": {
            "scope": "Public counters on linked brand, creator and media posts. Not attributed individual results or unique audience.",
            "grain": "One Instagram post, carousel or video per shortcode. Carousel children are not counted separately.",
            "deduplication": "Each post counted once globally and once within each project. Project totals overlap and must not be added together.",
            "missing_values": "Negative, hidden, absent and restricted counts are null, not zero. Totals sum only reported nonnegative counters.",
            "likes_comments": "Recorded likes plus recorded comments, including partially measured posts. Not total engagement.",
            "video_counters": "videoPlayCount and videoViewCount are separate source fields. Never add them together or label either as reach. Plays can include replays.",
            "coverage": "Likes and comments use all linked unique posts as the denominator. Plays and views use posts identified as Video; restricted posts have unknown format.",
            "time_scope": "Counters at collection time, not a fixed campaign window. No growth or organic/paid split can be inferred from a single public snapshot.",
            "unavailable_metrics": ["shares", "saves", "reposts", "reach", "impressions", "watch_time", "link_clicks", "attributed_sales", "follower_based_engagement_rate"],
            "plays_reference": "https://about.fb.com/news/2023/11/new-ways-to-create-content-on-instagram/",
        },
        "totals": aggregate(all_codes, posts),
        "projects": projects,
        "posts": posts,
    }


def export_csv(data):
    out = io.StringIO(newline="")
    writer = csv.writer(out)
    writer.writerow(["shortcode", "source_url", "owner", "published_at", "type", "status", "likes", "comments", "video_plays", "video_views", "duration_seconds", "project_ids", "collected_at"])
    for code in sorted(data["posts"]):
        p = data["posts"][code]
        writer.writerow([code, p["source_url"], p["owner"], p["published_at"], p["type"], p["status"], p["metrics"]["likes"], p["metrics"]["comments"], p["metrics"]["plays"], p["metrics"]["views"], p["duration_seconds"], ";".join(p["project_ids"]), data["snapshot"]["collected_at"]])
    return out.getvalue()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("snapshot", type=Path)
    parser.add_argument("--source", type=Path, default=ROOT / "index.html")
    parser.add_argument("--data-only", action="store_true")
    args = parser.parse_args()
    source = args.source.read_text()
    snapshot = json.loads(args.snapshot.read_text())
    references = json.loads((ROOT / "PROJECT_REFERENCES.json").read_text())
    data = build(snapshot, source, references)
    (ROOT / "INSTAGRAM_METRICS.json").write_text(json.dumps(data, ensure_ascii=False, indent=2, allow_nan=False) + "\n")
    (ROOT / "INSTAGRAM_METRICS.csv").write_text(export_csv(data))
    if not args.data_only:
        from render_instagram_metrics import render
        (ROOT / "index.html").write_text(render(source, data))
    print(json.dumps({"snapshot": data["snapshot"], "totals": {k:v for k,v in data["totals"].items() if k != "post_codes"}}, indent=2))


if __name__ == "__main__":
    main()
