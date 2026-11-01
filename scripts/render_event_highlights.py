"""Highlight the supplied Love & Hustle posts without recounting campaign metrics."""
from html import escape
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent.parent
CSS = """
/* portfolio-event-highlights:start */
.kol-event{border-top:1px solid var(--line);padding-top:24px;margin-top:24px}
.kol-event h4{font-size:20px;font-weight:500;letter-spacing:-.03em}
.kol-event>p{font-size:14px;line-height:1.8;color:var(--muted);margin:10px 0 20px}
.kol-lineup-grid{display:grid;grid-template-columns:minmax(170px,230px) minmax(0,1fr);gap:24px;align-items:start}
.kol-lineup-art{display:block}
.kol-lineup-art img{display:block;width:100%;height:auto}
.kol-lineup-art span{display:block;font-size:12px;color:var(--muted);padding:10px 0;line-height:1.6}
.kol-lineup-art:focus-visible{outline:2px solid var(--accent);outline-offset:5px}
.kol-lineup-grid h5{font-size:14px;font-weight:500;margin:0 0 12px}
.kol-lineup-names{display:flex;flex-wrap:wrap;gap:8px;list-style:none;padding:0;margin:0}
.kol-lineup-names li{font-size:13px;border:1px solid var(--line);padding:6px 10px;line-height:1.5}
.kol-event .kol-source-note{font-size:12px;color:var(--muted);margin-top:14px;line-height:1.7}
.kol-event .related-links{margin-top:24px}
@media(max-width:640px){.kol-lineup-grid{grid-template-columns:1fr}.kol-lineup-art{max-width:280px}}
/* portfolio-event-highlights:end */
"""


def render(source, archive=None):
    event_path = ROOT/'LOVE_HUSTLE_EVENT.json'
    if not event_path.exists():
        return source
    event = json.loads(event_path.read_text())
    if archive is None:
        archive = json.loads((ROOT/'CAMPAIGN_ARCHIVE.json').read_text())
    from render_campaigns import post_links
    source = re.sub(r'<!-- portfolio-event-highlights:start -->.*?<!-- portfolio-event-highlights:end -->', '', source, flags=re.S)
    source = re.sub(r'/\* portfolio-event-highlights:start \*/.*?/\* portfolio-event-highlights:end \*/\s*', '', source, flags=re.S)
    source = source.replace('</style>', CSS.strip()+'\n</style>', 1)
    posts = event['highlight_posts']
    links, count = post_links({'post_codes': [p['code'] for p in posts]}, archive['posts'])
    assert count == 4
    for i, post in enumerate(posts, 1):
        links = links.replace(f'Campaign post {i:02d}', escape(post['title']))
        links = links.replace(f'href="{escape(archive["posts"][post["code"]]["source_url"], quote=True)}"', f'href="{escape(post["url"], quote=True)}"')
    names = ''.join(f'<li>{escape(name)}</li>' for name in event['line_up'])
    panel = (
        '<!-- portfolio-event-highlights:start --><section class="kol-event" aria-labelledby="love-hustle-kol-title">'
        '<h4 id="love-hustle-kol-title">KOL collaborations at the event.</h4>'
        '<p>Love &amp; Hustle Streetball Showdown · 17 October 2026 · KYZN Kuningan. '
        'The Speedy Weeedy × Kevinswork collaboration extended onto the court with Widyanta Putra Teja, '
        'Kevinswork, and a published 16-person KOL line-up.</p>'
        '<div class="kol-lineup-grid"><a class="kol-lineup-art" href="assets/campaigns/love-hustle-kol-lineup.webp" '
        'target="_blank" rel="noopener noreferrer"><img src="assets/campaigns/love-hustle-kol-lineup.webp" '
        'width="1050" height="1400" alt="Official Love and Hustle Streetball Showdown artwork showing the sixteen-person line-up" '
        'loading="lazy" decoding="async"><span>View the published line-up ↗</span></a><div>'
        '<h5>Published KOL line-up</h5><ul class="kol-lineup-names">'+names+'</ul>'
        '<p class="kol-source-note">Names follow the official event invitation. Explore the event recap, '
        '1-on-1 challenge, invitation, and product story below.</p></div></div>'+links+
        '</section><!-- portfolio-event-highlights:end -->'
    )
    match = re.search(r'<details\b[^>]*id="case-love-hustle".*?</details>', source, re.S)
    assert match, 'Love & Hustle case must exist'
    body = match.group()
    body = body.replace('A signature basketball shoe collaboration with Widyanta Putra Teja and artist Kevinswork.',
                        'A signature basketball shoe collaboration with Widyanta Putra Teja and artist Kevinswork, followed by a KOL streetball activation.', 1)
    assert '</dl>' in body
    body = body.replace('</dl>', '</dl>'+panel, 1)
    return source[:match.start()]+body+source[match.end():]


if __name__ == '__main__':
    path = ROOT/'index.html'
    path.write_text(render(path.read_text()))
