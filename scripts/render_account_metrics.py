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
.account-growth-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:16px;margin:5px 0 24px}
.account-growth{padding:14px 0;border-block:1px solid var(--line)}
.account-growth h3{font-size:12px;font-weight:500;line-height:1.5;letter-spacing:0;color:var(--ink)}
.account-growth strong{display:block;font-size:24px;font-weight:500;letter-spacing:-.03em;line-height:1.3;margin:6px 0 4px;font-variant-numeric:tabular-nums;color:var(--ink)}
.account-growth p{font-size:12px;line-height:1.6;color:var(--muted)}
.instagram-method{margin-top:12px;border-top:0}
.instagram-method>summary{font-size:12px;min-height:44px;padding:9px 0}
.instagram-method>summary::after{font-size:18px}
.instagram-method-body{font-size:13px;line-height:1.75;max-width:none;padding-bottom:16px}
.instagram-method-body>p{max-width:95ch}
.account-table-scroll{overflow-x:auto;margin:8px 0 18px}
.account-table{border-collapse:collapse;width:100%;font-size:12px;text-align:left;table-layout:fixed}
.account-table th:first-child{width:40%}.account-table th:nth-child(2){width:25%}.account-table th:nth-child(3){width:35%}
.account-table caption{text-align:left;color:var(--ink);font-size:13px;font-weight:500;margin-bottom:10px}
.account-table th,.account-table td{padding:10px 12px;border-bottom:1px solid var(--line);vertical-align:top}
.account-table th{font-weight:400;font-size:11px;color:var(--muted)}
.account-table th:first-child,.account-table td:first-child{padding-left:0}
.account-table td{font-variant-numeric:tabular-nums}
.account-table td:nth-child(2),.account-table td:nth-child(3){white-space:nowrap;color:var(--ink)}
.account-table .account-growth-cell{white-space:normal;min-width:0}
.account-growth-cell strong{font-size:18px;font-weight:500;letter-spacing:-.025em;line-height:1.4}
.account-growth-cell small{white-space:nowrap}
.account-table a{display:inline-flex;align-items:center;min-height:44px;color:var(--ink)}
.account-table a:hover{color:var(--lime)}
.account-table small{display:block;font-size:11px;color:var(--muted);line-height:1.5}
.account-table .account-platform{margin-top:-7px}
.instagram-source-links{gap:4px 20px;margin-top:12px}
.instagram-source-links a{font-size:12px}
@media(max-width:760px){.instagram-overview-header{display:flex;flex-wrap:wrap;gap:10px}.instagram-overview-header .instagram-snapshot{white-space:normal}.instagram-totals{grid-template-columns:repeat(2,minmax(0,1fr))}.instagram-total{padding:12px 14px}.instagram-total:nth-child(odd){padding-left:0}.instagram-total:nth-child(even){border-right:0}.instagram-total:nth-child(-n+2){border-bottom:1px solid var(--line)}.instagram-total strong{font-size:24px}.account-table th,.account-table td{padding:9px 8px}.account-table a{overflow-wrap:anywhere;word-break:break-word}.account-table td:first-child{width:49%}.account-growth-grid{gap:12px}.account-growth h3{font-size:12px}.account-growth strong{font-size:23px}.account-growth p{font-size:11px}}
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
        growth = a.get('growth')
        if growth:
            assert type(growth['start']) is int and growth['start'] >= 0
            assert type(growth['end']) is int and growth['end'] >= growth['start']
            assert growth['net_added'] == growth['end'] - growth['start']
            if growth['start'] == 0:
                assert growth['percent_change'] is None
            else:
                expected = growth['net_added'] / growth['start'] * 100
                assert abs(growth['percent_change'] - expected) < 0.000001
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
        ("Followers + subscribers", data["totals"]["audience"], "Across 5 accounts"),
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
        growth = a.get('growth')
        growth_html = ''
        if growth:
            if growth['start']:
                change = f'+{growth["percent_change"]:,.0f}%'
            else:
                change = '+' + compact(growth['net_added'])
            journey = f'{compact(growth["start"])} → {compact(growth["end"])}'
            detail = 'Milestone' if growth.get('is_milestone') else ('Follower growth' if growth['start'] else ('Followers gained' if a['platform'] != 'YouTube' else 'Subscribers gained'))
            growth_html = (f'<strong>{change}</strong><small>{journey}</small>'
                           f'<small>{detail}</small>')
        rows.append('<tr><td><a target="_blank" rel="noopener noreferrer" '
                    f'href="{escape(a["url"], quote=True)}">@{escape(a["handle"])}</a>'
                    f'<small class="account-platform">{escape(a["platform"])} · {a["content"]:,} {a["content_label"].lower()}</small></td>'
                    f'<td>{a["audience"]:,}<small>{escape(a["audience_label"])}</small></td>'
                    f'<td class="account-growth-cell">{growth_html}</td></tr>')
    return (
        '<!-- portfolio-instagram-overview:start -->\n'
        '<section class="instagram-overview" id="instagram-metrics" aria-labelledby="instagram-metrics-title"><div class="wrap">'
        '<div class="instagram-overview-header"><div><p class="kicker">Instagram · TikTok · YouTube</p>'
        '<h2 id="instagram-metrics-title">Account totals.</h2>'
        '<p>Current public totals across Ardiles Basketball, Ardiles Running, DBL Academy, Ardiles Performance, and Ardiles Official.</p></div>'
        f'<p class="instagram-snapshot">Snapshot<br><time datetime="{escape(data["snapshot"]["collected_at"], quote=True)}">{date}</time></p></div>'
        '<div class="instagram-totals">' + ''.join(cards) + '</div>'
        '<details class="instagram-method" id="instagram-metrics-method"><summary>Explore the communities behind the work</summary>'
        '<div class="instagram-method-body">'
        '<div class="account-table-scroll"><table class="account-table"><caption>A closer look at each account</caption>'
        '<thead><tr><th scope="col">Account</th><th scope="col">Community</th><th scope="col">Growth</th>'
        '</tr></thead><tbody>' + ''.join(rows) + '</tbody></table></div>'
        '</div></details></div></section>\n<!-- portfolio-instagram-overview:end -->\n'
    )
