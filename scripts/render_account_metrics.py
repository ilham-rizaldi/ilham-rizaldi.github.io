"""Render verified account totals separately from project/post snapshots."""
from datetime import datetime
from html import escape
from zoneinfo import ZoneInfo

CSS = r"""
.instagram-overview{padding-block:28px}
.instagram-overview-header{gap:16px;margin-bottom:16px}
.instagram-overview h2{font-size:24px;line-height:1.25;margin-top:5px;letter-spacing:-.03em}
.instagram-overview-header p:not(.kicker){font-size:13px;line-height:1.65;margin-top:8px;max-width:76ch}
.instagram-overview-header .instagram-snapshot{font-size:11px;margin-top:0;padding-top:2px}
.instagram-overview .kicker{font-size:10px;letter-spacing:.09em}
.instagram-totals{grid-template-columns:repeat(4,minmax(0,1fr));gap:0;border-block:1px solid var(--line)}
.instagram-total{padding:14px 16px;border:0;border-right:1px solid var(--line);background:transparent}
.instagram-total:first-child{padding-left:0}
.instagram-total:last-child{border-right:0}
.instagram-total h3{font-size:12px;line-height:1.5}
.instagram-total strong{font-size:25px;line-height:1.2;margin:6px 0 4px;letter-spacing:-.035em}
.instagram-total p{font-size:11px;line-height:1.5;margin:0}
.account-context{font-size:12px;line-height:1.65;color:var(--muted);margin-top:12px;max-width:95ch}
.instagram-method{margin-top:12px;border-top:0}
.instagram-method>summary{font-size:12px;min-height:44px;padding:9px 0}
.instagram-method>summary::after{font-size:18px}
.instagram-method-body{font-size:13px;line-height:1.75;max-width:none;padding-bottom:16px}
.instagram-method-body>p{max-width:95ch}
.account-table-scroll{overflow-x:auto;margin:8px 0 18px}
.account-table{border-collapse:collapse;width:100%;font-size:12px;text-align:left}
.account-table caption{text-align:left;color:var(--ink);font-size:13px;font-weight:500;margin-bottom:10px}
.account-table th,.account-table td{padding:10px 12px;border-bottom:1px solid var(--line);vertical-align:top}
.account-table th{font-weight:400;font-size:11px;color:var(--muted)}
.account-table th:first-child,.account-table td:first-child{padding-left:0}
.account-table td{font-variant-numeric:tabular-nums}
.account-table td:nth-child(2),.account-table td:nth-child(3){white-space:nowrap;color:var(--ink)}
.account-table a{display:inline-flex;align-items:center;min-height:44px;color:var(--ink)}
.account-table a:hover{color:var(--lime)}
.account-table small{display:block;font-size:11px;color:var(--muted);line-height:1.5}
.account-table .account-platform{margin-top:-7px}
.instagram-source-links{gap:4px 20px;margin-top:12px}
.instagram-source-links a{font-size:12px}
@media(max-width:760px){.instagram-overview-header{display:flex;flex-wrap:wrap;gap:10px}.instagram-overview-header .instagram-snapshot{white-space:normal}.instagram-totals{grid-template-columns:repeat(2,minmax(0,1fr))}.instagram-total{padding:12px 14px}.instagram-total:nth-child(odd){padding-left:0}.instagram-total:nth-child(even){border-right:0}.instagram-total:nth-child(-n+2){border-bottom:1px solid var(--line)}.instagram-total strong{font-size:24px}.account-table th,.account-table td{padding:9px 8px}.account-table th:last-child,.account-table td:last-child{display:none}.account-table a{overflow-wrap:anywhere;word-break:break-word}.account-table td:first-child{width:49%}}
@media(max-width:390px){.instagram-total h3{font-size:11px}.instagram-total strong{font-size:23px}.instagram-total p{font-size:11px}.instagram-overview h2{font-size:22px}.account-table{font-size:11px}}
"""

EXPECTED = {
    ("Instagram", "ardilesbasketball"), ("Instagram", "ardilesrunning"),
    ("Instagram", "dblacademy"), ("TikTok", "ardilesperformance"),
    ("YouTube", "ardilesofficial"),
}


def validate(data):
    accounts = data["accounts"]
    assert len(accounts) == 5
    assert {(a["platform"], a["handle"]) for a in accounts} == EXPECTED
    for a in accounts:
        for key in ("audience", "content", "likes", "views"):
            assert a[key] is None or (type(a[key]) is int and a[key] >= 0)
        assert a["audience"] is not None and a["content"] is not None
        assert a["source"]["collected_at"] and a["source"]["fields"]
    assert data["totals"] == {
        "accounts": 5, "audience": sum(a["audience"] for a in accounts),
        "content": sum(a["content"] for a in accounts),
    }


def compact(value):
    for divisor, suffix in ((1_000_000, "M"), (1_000, "K")):
        if value >= divisor:
            return f"{value / divisor:.2f}".rstrip("0").rstrip(".") + suffix
    return f"{value:,}"


def overview(data, projects):
    validate(data)
    accounts = data["accounts"]
    tt = next(a for a in accounts if a["platform"] == "TikTok")
    yt = next(a for a in accounts if a["platform"] == "YouTube")
    stamp = datetime.fromisoformat(data["snapshot"]["collected_at"].replace("Z", "+00:00")).astimezone(ZoneInfo("Asia/Jakarta"))
    date = f"{stamp.day} {stamp.strftime('%b %Y, %H:%M')} WIB"
    metrics = [
        ("Followers + subscribers", data["totals"]["audience"], "5 account counts · audiences may overlap"),
        ("Posts + videos", data["totals"]["content"], "Published content across 5 accounts"),
        ("TikTok · total likes", tt["likes"], "@ardilesperformance"),
        ("YouTube · total views", yt["views"], "Ardiles Official channel"),
    ]
    cards = []
    for label, value, note in metrics:
        number = compact(value) if value is not None else "Unavailable"
        exact = f"{value:,} reported" if value is not None else "Not available from public profile"
        cards.append(f'<div class="instagram-total"><h3>{escape(label)}</h3>'
                     f'<strong title="{exact}" aria-label="{exact}">{number}</strong><p>{escape(note)}</p></div>')
    rows = []
    for a in accounts:
        other = []
        if a["likes"] is not None:
            other.append(f'{a["likes"]:,} total likes')
        if a["views"] is not None:
            other.append(f'{a["views"]:,} total views')
        rows.append('<tr><td><a target="_blank" rel="noopener noreferrer" '
                    f'href="{escape(a["url"], quote=True)}">@{escape(a["handle"])}</a>'
                    f'<small class="account-platform">{escape(a["platform"])}</small></td>'
                    f'<td>{a["audience"]:,}<small>{escape(a["audience_label"])}</small></td>'
                    f'<td>{a["content"]:,}<small>{escape(a["content_label"])}</small></td>'
                    f'<td>{" · ".join(other) if other else "Not publicly provided"}</td></tr>')
    ps = projects["snapshot"]
    return (
        '<!-- portfolio-instagram-overview:start -->\n'
        '<section class="instagram-overview" id="instagram-metrics" aria-labelledby="instagram-metrics-title"><div class="wrap">'
        '<div class="instagram-overview-header"><div><p class="kicker">Instagram · TikTok · YouTube</p>'
        '<h2 id="instagram-metrics-title">Account totals.</h2>'
        '<p>Current public totals across Ardiles Basketball, Ardiles Running, DBL Academy, Ardiles Performance, and Ardiles Official.</p></div>'
        f'<p class="instagram-snapshot">Snapshot<br><time datetime="{escape(data["snapshot"]["collected_at"], quote=True)}">{date}</time></p></div>'
        '<div class="instagram-totals">' + ''.join(cards) + '</div>'
        '<p class="account-context">Account context across all published activity, including periods outside my role. '
        'Project-specific figures are shown within each project.</p>'
        '<details class="instagram-method" id="instagram-metrics-method"><summary>Account breakdown, sources, and counting method</summary>'
        '<div class="instagram-method-body"><div class="account-table-scroll">'
        '<table class="account-table"><caption>Public profile totals · exact reported counts</caption>'
        '<thead><tr><th scope="col">Account</th><th scope="col">Audience</th><th scope="col">Published</th>'
        '<th scope="col">Other account totals</th></tr></thead><tbody>' + ''.join(rows) + '</tbody></table></div>'
        '<p><strong>Account scope.</strong> Followers and subscribers are added across the five profiles. '
        'People can follow several accounts, so this is not unique audience, reach, or follower growth. '
        'Public figures may be rounded. Posts and videos use each platform’s profile counter.</p>'
        f'<p><strong>Platform totals.</strong> TikTok reports {tt["likes"]:,} account likes; '
        f'YouTube reports {yt["views"]:,} channel views. These are account-level counters, '
        'not sums or projections from a sample of videos. They remain separate measures.</p>'
        '<p><strong>Unavailable totals.</strong> Instagram profile metadata does not provide lifetime likes, comments, '
        'video views, reach, or impressions. TikTok account-wide views and YouTube account-wide likes are also '
        'unavailable in this profile snapshot. These values are excluded, rather than estimated or treated as zero.</p>'
        '<p><strong>Attribution.</strong> Current account totals include team activity and may include periods before '
        'or after my work. They do not establish my personal contribution, paid versus organic results, or sales impact.</p>'
        f'<p><strong>Project and post figures.</strong> The existing linked-content snapshot '
        f'({escape(ps["display_date"])}) remains unchanged inside each project. '
        'Each project deduplicates its linked Instagram posts by shortcode; the same post may appear in several projects. '
        'Likes and comments exclude unavailable values. Plays and views remain separate and are not unique viewers. '
        'Campaign-report figures keep their original scope and are not added to the account totals.</p>'
        '<nav class="instagram-source-links" aria-label="Metric data and definitions">'
        '<a href="ACCOUNT_METRICS.json" download>Account data (JSON)</a>'
        '<a href="INSTAGRAM_METRICS.csv" download>Project post data (CSV)</a>'
        '<a href="INSTAGRAM_METRICS.json" download>Project source record (JSON)</a>'
        '<a href="https://apify.com/apify/instagram-profile-scraper" target="_blank" rel="noopener noreferrer">Instagram source ↗</a>'
        '<a href="https://apify.com/clockworks/tiktok-profile-scraper" target="_blank" rel="noopener noreferrer">TikTok source ↗</a>'
        '<a href="https://apify.com/streamers/youtube-channel-scraper" target="_blank" rel="noopener noreferrer">YouTube source ↗</a>'
        '<a href="https://apify.com/apify/instagram-scraper" target="_blank" rel="noopener noreferrer">Project collection source ↗</a>'
        '<a href="https://about.fb.com/news/2023/11/new-ways-to-create-content-on-instagram/" target="_blank" rel="noopener noreferrer">About video plays ↗</a>'
        '</nav></div></details></div></section>\n<!-- portfolio-instagram-overview:end -->\n'
    )
