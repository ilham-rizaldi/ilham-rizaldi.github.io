#!/usr/bin/env python3
"""Render a reviewed Instagram snapshot into the static portfolio.

No API calls occur in the browser. This module only renders supplied values;
the snapshot builder owns normalization, deduplication, and calculations.
"""
from __future__ import annotations

import argparse
from datetime import datetime
from html import escape, unescape
import json
from pathlib import Path
import re
from zoneinfo import ZoneInfo
from render_account_metrics import CSS as ACCOUNT_CSS, overview as account_overview

METRIC_LABELS = {
    "likes": "Likes",
    "comments": "Comments",
    "plays": "Video plays",
    "views": "Video views",
    "interactions": "Recorded likes + comments",
}

CSS = r"""
/* portfolio-instagram-metrics:start */
.instagram-overview{padding-block:48px;border-top:1px solid var(--line);background:var(--bg)}
.instagram-overview-header{display:flex;align-items:flex-start;justify-content:space-between;gap:24px;margin-bottom:24px}
.instagram-overview h2{font-size:clamp(28px,3vw,42px);line-height:1.15;margin-top:10px;max-width:24ch}
.instagram-overview-header p:not(.kicker){font-size:14px;line-height:1.75;color:var(--muted);max-width:65ch;margin-top:14px}
.instagram-overview-header .instagram-snapshot{font-size:12px;color:var(--muted);white-space:nowrap;padding-top:4px;margin-top:0}
.instagram-totals{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px}
.instagram-total{padding:20px;border:1px solid var(--line);background:var(--panel);min-width:0}
.instagram-total h3{font-size:13px;line-height:1.5;letter-spacing:0;font-weight:500;color:var(--muted)}
.instagram-total strong{display:block;font-size:clamp(30px,3.5vw,46px);font-weight:500;letter-spacing:-.045em;line-height:1.2;margin:12px 0 6px;font-variant-numeric:tabular-nums}
.instagram-total .metric-exact{display:block;font-size:12px;color:var(--ink);overflow-wrap:anywhere}
.instagram-total p{font-size:12px;color:var(--muted);line-height:1.6;margin-top:5px}
.instagram-method{border-block:1px solid var(--line);margin-top:22px}
.instagram-method>summary{cursor:pointer;display:flex;justify-content:space-between;align-items:center;gap:20px;min-height:48px;padding:12px 0;font-size:14px;list-style:none}
.instagram-method>summary::-webkit-details-marker{display:none}
.instagram-method>summary::after{content:'+';font-size:22px;color:var(--lime)}
.instagram-method[open]>summary::after{content:'−'}
.instagram-method-body{padding:5px 0 22px;max-width:88ch;color:var(--muted);font-size:14px;line-height:1.8}
.instagram-method-body p+p{margin-top:12px}
.instagram-method-body strong{font-weight:500;color:var(--ink)}
.instagram-source-links{display:flex;gap:12px 24px;flex-wrap:wrap;margin-top:18px}
.instagram-source-links a{display:inline-flex;align-items:center;min-height:44px;border-bottom:1px solid var(--line);color:var(--ink);font-size:13px}
.instagram-source-links a:hover{color:var(--lime)}
.project-public-metrics{margin-bottom:25px;padding-bottom:24px;border-bottom:1px solid var(--line)}
.project-public-metrics h4{font-size:14px;line-height:1.5;letter-spacing:0;font-weight:550}
.project-public-metrics>p{font-size:12px;color:var(--muted);line-height:1.7;margin-top:6px}
.project-public-teaser{font-size:12px;line-height:1.7;color:var(--muted);margin-top:13px;overflow-wrap:anywhere}
.project-public-teaser>span:first-child{display:block;color:var(--ink);font-size:11px;margin-bottom:3px}
.project-metric-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:14px 18px;margin-top:16px}
.project-metric{min-width:0}
.project-metric strong{display:block;font-size:19px!important;font-weight:500;line-height:1.3;font-variant-numeric:tabular-nums;letter-spacing:-.03em;overflow-wrap:anywhere}
.project-metric span{display:block;color:var(--muted);font-size:12px;line-height:1.5;margin-top:3px}
.project-metric small{display:block;color:var(--muted);font-size:11px;line-height:1.5;margin-top:2px}
.case-featured .project-metric-grid{grid-template-columns:repeat(5,minmax(0,1fr))}
.related-links a .post-link-copy{min-width:0;display:block}
.related-links a .post-owner,.related-links a .post-date{display:block;color:var(--muted);font-size:11px;line-height:1.55;overflow-wrap:anywhere;margin-top:2px}
.related-links a .post-counter-list{display:flex;flex-direction:column;gap:2px;margin-top:7px;font-size:12px;line-height:1.5;color:var(--ink)}
.related-links a .post-counter{display:block;font-size:12px;line-height:1.5;overflow-wrap:normal}
.related-links a .post-counter b{font-weight:550;font-variant-numeric:tabular-nums;white-space:nowrap}
.related-links a .post-counter-unavailable{font-size:11px;line-height:1.5;color:var(--muted)}
.related-links a.related-link-with-preview{align-items:start}
.related-links a .post-preview{align-self:start}
.related-links a .related-external-arrow{align-self:center}
@media(max-width:760px){.instagram-overview-header{display:block}.instagram-snapshot{display:block;margin-top:14px;white-space:normal}.instagram-totals{grid-template-columns:repeat(2,minmax(0,1fr))}.instagram-total{padding:16px}.instagram-total strong{font-size:32px}.case-featured .project-metric-grid{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media(max-width:390px){.instagram-total{padding:12px}.instagram-total h3{font-size:12px}.instagram-total strong{font-size:28px}.instagram-total .metric-exact,.instagram-total p{font-size:11px}.project-metric-grid{gap:14px 10px}.project-metric strong{font-size:18px!important}.related-links a .post-owner,.related-links a .post-date{font-size:11px}}
@media print{.instagram-overview,.project-public-metrics,.post-counter-list,.post-owner,.post-date{display:none!important}}
/* portfolio-instagram-metrics:end */
"""


def num(value: int | float | None) -> str:
    if value is None:
        return "Not available"
    return f"{int(value):,}"


def compact(value: int | float | None) -> str:
    if value is None:
        return "—"
    value = int(value)
    for divisor, suffix in ((1_000_000_000, "B"), (1_000_000, "M"), (10_000, "K")):
        if value >= divisor:
            scale = 1000 if suffix == "K" else divisor
            return f"{value / scale:.2f}".rstrip("0").rstrip(".") + suffix
    return num(value)


def shortcode(url: str) -> str | None:
    match = re.search(r"/(?:p|reel|reels|tv)/([A-Za-z0-9_-]+)", unescape(url))
    return match.group(1) if match else None


def date_label(value: str | None) -> str:
    if not value:
        return ""
    try:
        date = datetime.fromisoformat(value.replace("Z", "+00:00")).astimezone(ZoneInfo("Asia/Jakarta"))
    except (ValueError, TypeError):
        return ""
    return f"{date.day} {date.strftime('%b %Y')}"


def duration_label(value: float | None) -> str:
    if not isinstance(value, (float, int)) or value < 0:
        return ""
    seconds = round(value)
    return f"{seconds // 60}:{seconds % 60:02d}"


def coverage(metric: dict, *, video: bool = False) -> str:
    noun = "videos" if video else "posts"
    return f"{metric['available']:,}/{metric['eligible']:,} {noun} with data"


def total_card(label: str, value: int | None, note: str) -> str:
    exact = f'<span class="metric-exact">{num(value)} recorded</span>' if value is not None else ""
    return (
        '<div class="instagram-total">'
        f'<h3>{escape(label)}</h3><strong aria-label="{escape(num(value))}">{compact(value)}</strong>'
        f'{exact}<p>{escape(note)}</p></div>'
    )


def linked_overview(data: dict) -> str:
    totals = data["totals"]
    snapshot = data["snapshot"]
    metrics = totals["metrics"]
    snapshot_label = escape(snapshot["display_date"])
    collected_at = escape(snapshot["collected_at"], quote=True)
    cards = [
        total_card("Unique Instagram posts", totals["unique_posts"],
                   f"{totals['available_posts']:,} available · {totals['unavailable_posts']:,} unavailable"),
    ]
    for key in ("likes", "comments", "plays", "views", "interactions"):
        metric = metrics[key]
        note = coverage(metric, video=key in ("plays", "views"))
        if key == "interactions":
            note = "Known likes + known comments; incomplete where likes are hidden"
        cards.append(total_card(METRIC_LABELS[key], metric["total"] if metric["available"] else None, note))
    return (
        '<!-- portfolio-instagram-overview:start -->\n'
        '<section class="instagram-overview" id="instagram-metrics" aria-labelledby="instagram-metrics-title"><div class="wrap">'
        '<div class="instagram-overview-header"><div><p class="kicker">Instagram / Linked portfolio content</p>'
        '<h2 id="instagram-metrics-title">Public content metrics.</h2>'
        '<p>Public counters from the brand, creator, and media posts linked in this portfolio. '
        'Each post is counted once in these totals.</p></div>'
        f'<p class="instagram-snapshot">Snapshot<br><time datetime="{collected_at}">{snapshot_label}</time></p></div>'
        '<div class="instagram-totals">' + "".join(cards) + '</div>'
        '<details class="instagram-method" id="instagram-metrics-method"><summary>Sources, coverage, and counting method</summary>'
        '<div class="instagram-method-body">'
        f'<p><strong>Scope.</strong> {totals["unique_posts"]:,} unique linked Instagram posts, including '
        f'{totals["video_posts"]:,} identified videos. {totals["available_posts"]:,} posts returned public data; '
        f'{totals["unavailable_posts"]:,} were unavailable. Values were collected on {snapshot_label} '
        'and are a dated snapshot, not a live counter.</p>'
        '<p><strong>What the totals mean.</strong> Likes and comments are the reported top-level post counters. '
        '“Recorded likes + comments” adds only the known values; it excludes saves, shares, and other interactions. '
        'Hidden or missing values remain unavailable and are excluded from sums. Zero is shown only when returned by the source.</p>'
        '<p><strong>Video counts.</strong> Plays and views are separate source fields and are never added together. '
        'Plays can include replays. Neither total is unique people, reach, or impressions.</p>'
        '<p><strong>Attribution.</strong> These are counters on linked brand, creator, and media content, '
        'not a claim of personally generated results. The snapshot does not separate paid and organic activity '
        'or establish sales impact. A post can belong to several projects; project totals overlap, '
        'while the main totals deduplicate posts by Instagram shortcode. Carousel slides are not separate posts.</p>'
        '<p><strong>Metrics not available here.</strong> Saves, shares, reposts, reach, impressions, watch time, '
        'profile visits, link clicks, follower growth, and sales are not in this public snapshot. '
        'These require a verified source such as an authorized Insights export. '
        'Existing campaign-report figures retain their own stated scope and are not added to these totals.</p>'
        '<nav class="instagram-source-links" aria-label="Instagram metric sources">'
        '<a href="INSTAGRAM_METRICS.csv" download>Download post data (CSV)</a>'
        '<a href="INSTAGRAM_METRICS.json" download>Download source record (JSON)</a>'
        '<a href="https://apify.com/apify/instagram-scraper" target="_blank" rel="noopener noreferrer">Collection source ↗</a>'
        '<a href="https://about.fb.com/news/2023/11/new-ways-to-create-content-on-instagram/" target="_blank" rel="noopener noreferrer">About video plays ↗</a>'
        '</nav></div></details></div></section>\n'
        '<!-- portfolio-instagram-overview:end -->\n'
    )


def project_metrics(project: dict, snapshot: dict) -> str:
    if not project.get("unique_posts"):
        return ""
    cells = []
    for key in ("likes", "comments", "plays", "views", "interactions"):
        metric = project["metrics"][key]
        # Preserve missingness, and avoid empty video metrics on non-video projects.
        if key in ("plays", "views") and not project["video_posts"]:
            continue
        detail = coverage(metric, video=key in ("plays", "views"))
        if key == "interactions":
            detail = "Known values only"
        value = num(metric["total"]) if metric["available"] else "Not available"
        cells.append('<div class="project-metric">'
                     f'<strong>{value}</strong><span>{METRIC_LABELS[key]}</span>'
                     f'<small>{escape(detail)}</small></div>')
    return (
        '<!-- portfolio-instagram-project:start -->'
        '<section class="project-public-metrics" aria-label="Public Instagram metrics for this project">'
        '<h4>Public Instagram metrics</h4>'
        f'<p>{project["unique_posts"]:,} unique linked posts · Snapshot {escape(snapshot["display_date"])}</p>'
        '<div class="project-metric-grid">' + "".join(cells) + '</div>'
        '<p>Public counters on linked content. Project totals can overlap. '
        '<a href="#instagram-metrics-method">Counting method ↗</a></p>'
        '</section><!-- portfolio-instagram-project:end -->'
    )


def project_teaser(project: dict) -> str:
    if not project.get('unique_posts'):
        return ''
    values = []
    for key, label in (('likes', 'likes'), ('comments', 'comments'), ('plays', 'plays'), ('views', 'views')):
        metric = project['metrics'][key]
        if not metric['available']:
            continue
        partial = ''
        if metric['available'] < metric['eligible']:
            noun = ' videos' if key in ('plays', 'views') else ''
            partial = f' ({metric["available"]}/{metric["eligible"]}{noun})'
        values.append(f'<span title="{num(metric["total"])} {label}">{compact(metric["total"])} {label}{partial}</span>')
    if not values:
        values = ['Public counters unavailable']
    return ('<!-- portfolio-instagram-teaser:start --><p class="project-public-teaser">'
            f'<span>Public counters · {project["available_posts"]}/{project["unique_posts"]} linked posts</span>'
            + ' · '.join(values) + '</p><!-- portfolio-instagram-teaser:end -->')


def post_copy(label_html: str, post: dict) -> str:
    lines = []
    owner = post.get("owner")
    if owner:
        lines.append(f'<small class="post-owner">@{escape(owner)}</small>')
    metadata = []
    date = date_label(post.get("published_at"))
    if date:
        metadata.append(date)
    kind = {"Image": "Photo", "Sidecar": "Carousel", "Video": "Video"}.get(post.get("type"))
    if kind:
        metadata.append(kind)
    duration = duration_label(post.get("duration_seconds"))
    if duration and post.get("type") == "Video":
        metadata.append(duration)
    if metadata:
        lines.append(f'<small class="post-date">{escape(" · ".join(metadata))}</small>')
    metrics = post.get("metrics", {})
    if post.get("status") != "available":
        lines.append('<span class="post-counter-list"><span class="post-counter-unavailable">Public metrics unavailable</span></span>')
    else:
        counters = []
        for key, label in (("likes", "likes"), ("comments", "comments"), ("plays", "plays"), ("views", "views")):
            value = metrics.get(key)
            if value is None:
                if key in ("likes", "comments"):
                    counters.append(f'<span class="post-counter-unavailable">{label.capitalize()} not available</span>')
                continue
            counters.append(f'<span class="post-counter"><b>{num(value)}</b> {label}</span>')
        lines.append('<span class="post-counter-list">' + "".join(counters) + '</span>')
    return ('<!-- portfolio-instagram-post:start --><span class="post-link-copy">'
            + label_html + "".join(lines) + '</span><!-- portfolio-instagram-post:end -->')


def overview(data: dict) -> str:
    account_path = Path(__file__).resolve().parent.parent / 'ACCOUNT_METRICS.json'
    if account_path.exists():
        return account_overview(json.loads(account_path.read_text()), data)
    return linked_overview(data)


def render(source_html: str, data: dict) -> str:
    """Return HTML with metrics added, preserving existing project material."""
    html = re.sub(r'/\* portfolio-instagram-metrics:start \*/.*?/\* portfolio-instagram-metrics:end \*/\s*', '', source_html, flags=re.S)
    html = re.sub(r'<!-- portfolio-instagram-overview:start -->.*?<!-- portfolio-instagram-overview:end -->\s*', '', html, flags=re.S)
    html = re.sub(r'<!-- portfolio-instagram-project:start -->.*?<!-- portfolio-instagram-project:end -->', '', html, flags=re.S)
    html = re.sub(r'<!-- portfolio-instagram-teaser:start -->.*?<!-- portfolio-instagram-teaser:end -->', '', html, flags=re.S)
    # Restore the original short link label before a repeated render.
    def restore_post(match: re.Match) -> str:
        label = re.search(r'<b>[^<]+</b>', match.group(0))
        if not label:
            raise ValueError('Cannot restore a previous post label')
        return f'<span>{label.group(0)}<small>Instagram post</small></span>'
    html = re.sub(r'<!-- portfolio-instagram-post:start -->.*?<!-- portfolio-instagram-post:end -->', restore_post, html, flags=re.S)

    if html.count('</style>') != 1:
        raise ValueError('Expected one stylesheet')
    combined_css = CSS.replace('/* portfolio-instagram-metrics:end */', ACCOUNT_CSS + '\n/* portfolio-instagram-metrics:end */')
    html = html.replace('</style>', combined_css.strip() + '\n</style>', 1)
    work_anchor = '<section class="section work-section"'
    if html.count(work_anchor) != 1:
        raise ValueError('Expected one portfolio section')
    html = html.replace(work_anchor, overview(data) + work_anchor, 1)

    case_count = 0
    def add_project(match: re.Match) -> str:
        nonlocal case_count
        body = match.group(0)
        case_id = re.search(r'\bid="([^"]+)"', body).group(1)
        if case_id not in data['projects']:
            raise ValueError(f'Missing project metrics: {case_id}')
        case_count += 1
        insertion = project_metrics(data['projects'][case_id], data['snapshot'])
        if insertion:
            anchor = '<div class="case-body">'
            if body.count(anchor) != 1:
                raise ValueError(f'Expected a case body: {case_id}')
            body = body.replace(anchor, anchor + insertion, 1)
            teaser = project_teaser(data['projects'][case_id])
            match_ref = re.search(r'<p class="project-ref-count"[^>]*>.*?</p>', body, re.S)
            match_description = re.search(r'<p class="case-description"[^>]*>.*?</p>', body, re.S)
            after = match_ref or match_description
            if not after:
                raise ValueError(f'Expected a case preview description: {case_id}')
            body = body[:after.end()] + teaser + body[after.end():]
        if 'data-close-case=' not in body:
            title = re.search(r'<h3[^>]*>(.*?)</h3>', body, re.S)
            name = unescape(re.sub('<[^>]*>', '', title.group(1))) if title else 'project'
            footer = ('<div class="case-footer"><button class="case-close" type="button" '
                      f'data-close-case="{case_id}" aria-controls="{case_id}" '
                      f'aria-label="{escape("Hide details: " + name, quote=True)}" data-js-only hidden>'
                      'Hide details<span class="close-diamond" aria-hidden="true"><span>×</span></span>'
                      '</button></div>')
            body = re.sub(r'</div></details>$', footer + '</div></details>', body)
        return body
    html = re.sub(r'<details\b[^>]*class="case(?:\s[^"]*)?"[^>]*>.*?</details>', add_project, html, flags=re.S)
    if case_count != 32:
        raise ValueError(f'Expected 32 project cards, found {case_count}')

    post_count = 0
    def add_post(match: re.Match) -> str:
        nonlocal post_count
        attrs, body = match.group(1), match.group(2)
        href = re.search(r'\bhref="([^"]*)"', attrs)
        if not href or 'instagram.com/' not in unescape(href.group(1)):
            return match.group(0)
        code = shortcode(href.group(1))
        label = re.search(r'<span>(<b>[^<]+</b>)<small>Instagram (?:post|reel)[^<]*</small></span>', body)
        if not label:
            return match.group(0)
        if code not in data['posts']:
            raise ValueError(f'Missing post snapshot: {code}')
        post_count += 1
        body = body[:label.start()] + post_copy(label.group(1), data['posts'][code]) + body[label.end():]
        return '<a' + attrs + '>' + body + '</a>'
    html = re.sub(r'<a\b([^>]*)>(.*?)</a>', add_post, html, flags=re.S)
    if post_count != 492:
        raise ValueError(f'Expected 492 Instagram reference entries, found {post_count}')
    manifest = Path(__file__).resolve().parent.parent / 'THUMBNAILS.json'
    if manifest.exists():
        from apply_portfolio_usability import apply
        html = apply(html, json.loads(manifest.read_text()))
    return html


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('index', type=Path)
    parser.add_argument('snapshot', type=Path)
    args = parser.parse_args()
    html = render(args.index.read_text(), json.loads(args.snapshot.read_text()))
    args.index.write_text(html)
    print(json.dumps({'project_cards': 32, 'instagram_reference_entries': 492, 'output': str(args.index)}))


if __name__ == '__main__':
    main()
