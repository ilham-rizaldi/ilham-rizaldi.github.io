"""Render recent campaign records without rewriting the legacy portfolio snapshot."""
from html import escape
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent.parent

CSS = r"""
/* portfolio-campaigns:start */
.campaign-update{border-top:1px solid var(--line);padding-top:24px;margin-top:26px}
.campaign-update>h4{font-size:17px;font-weight:500;letter-spacing:-.02em}
.campaign-update>p{font-size:13px;line-height:1.75;color:var(--muted);margin:8px 0 18px;max-width:78ch}
.campaign-links .post-preview-photo>img{width:100%;height:100%;object-fit:cover}
.campaign-post-atlas>img{position:absolute;display:block;max-width:none;aspect-ratio:auto;object-fit:fill}
.campaign-links .post-caption{display:block;font-size:12px;color:var(--muted);line-height:1.6;margin-top:6px}
.campaign-project .project-cover>img{object-fit:cover}
.campaign-project .project-metric-grid{grid-template-columns:repeat(2,minmax(0,1fr))}
/* portfolio-campaigns:end */
"""


def remove(source):
    source = re.sub(r'<!-- portfolio-campaign-cases:start -->.*?<!-- portfolio-campaign-cases:end -->\s*', '', source, flags=re.S)
    source = re.sub(r'<!-- portfolio-campaign-update:start -->.*?<!-- portfolio-campaign-update:end -->', '', source, flags=re.S)
    return source


def post_links(campaign, posts, omitted=()):
    from render_instagram_metrics import post_copy
    links = []
    for code in campaign['post_codes']:
        if code in omitted:
            continue
        p = posts[code]
        number = len(links)+1
        media = p.get('image')
        if p.get('preview_atlas'):
            a=p['preview_atlas']
            preview=('<span class="post-preview campaign-post-atlas" aria-hidden="true">'
                     f'<img src="{a["sheet"]}" width="{a["columns"]*a["tileSize"]}" height="{a["rows"]*a["tileSize"]}" '
                     f'style="width:{a["columns"]*100}%;height:{a["rows"]*100}%;left:-{a["column"]*100}%;top:-{a["row"]*100}%" '
                     'alt="" loading="lazy" decoding="async" data-preview-image>'
                     '<span class="preview-unavailable" hidden>Preview unavailable</span></span>')
        elif media:
            preview = ('<span class="post-preview post-preview-photo" aria-hidden="true">'
                       f'<img src="{escape(media, quote=True)}" width="{p["width"]}" height="{p["height"]}" '
                       'alt="" loading="lazy" decoding="async" data-preview-image>'
                       '<span class="preview-unavailable" hidden>Preview unavailable</span></span>')
        else:
            preview = '<span class="post-preview post-preview-document" aria-hidden="true"><span class="document-symbol">↗</span></span>'
        text = post_copy(f'<b>Campaign post {number:02d}</b>', p).replace('portfolio-instagram-post', 'portfolio-campaign-post')
        links.append('<li><a class="related-link-with-preview" '
                     f'href="{escape(p["source_url"], quote=True)}" target="_blank" rel="noopener noreferrer">'
                     f'{preview}{text}<span class="related-external-arrow" aria-hidden="true">↗</span></a></li>')
    return '<ul class="related-links campaign-links">' + ''.join(links) + '</ul>', len(links)


def metrics(campaign, snapshot):
    from render_instagram_metrics import coverage, num
    cells=[]
    for key,label in [('likes','Likes'),('comments','Comments'),('plays','Video plays'),('views','Video views')]:
        metric=campaign['totals']['metrics'][key]
        if not metric['available']:continue
        note=coverage(metric,video=key in ('plays','views'))
        cells.append('<div class="project-metric">'
                     f'<strong>{num(metric["total"])}</strong><span>{label}</span><small>{note}</small></div>')
    return ('<!-- portfolio-campaign-project:start --><section class="project-public-metrics" aria-label="Campaign post metrics">'
            f'<h4>Campaign post metrics</h4><p>{campaign["totals"]["unique_posts"]} matched posts · Snapshot {escape(snapshot["display_date"])}</p>'
            '<div class="project-metric-grid">'+''.join(cells)+'</div></section><!-- portfolio-campaign-project:end -->')


def close_button(cid, title):
    return ('<div class="case-footer"><button class="case-close" type="button" '
            f'data-close-case="{cid}" aria-controls="{cid}" aria-label="{escape("Hide details: "+title, quote=True)}" data-js-only hidden>'
            'Hide details<span class="close-diamond" aria-hidden="true"><span>×</span></span></button></div>')


def new_case(campaign, data):
    from render_instagram_metrics import project_teaser
    cid = campaign['case_id']
    title = campaign['title']
    cover = data['posts'][campaign['cover_code']]
    teaser = project_teaser(campaign['totals']).replace('portfolio-instagram-teaser','portfolio-campaign-teaser')
    links, count = post_links(campaign,data['posts'])
    dl = ''.join(f'<div><dt>{escape(label)}</dt><dd>{escape(value)}</dd></div>' for label,value in campaign['details'])
    return (
        f'<details class="case campaign-project" id="{cid}" data-category="{campaign["category"]}" data-campaign-id="{campaign["id"]}">'
        f'<summary aria-labelledby="{cid}-context {cid}-title" aria-describedby="{cid}-description {cid}-references">'
        '<div class="case-media project-cover" data-cover-kind="image">'
        f'<img src="{escape(cover["image"],quote=True)}" width="{cover["width"]}" height="{cover["height"]}" '
        f'alt="{escape(campaign["cover_alt"],quote=True)}" loading="lazy" decoding="async" data-preview-image>'
        '<span class="media-unavailable" hidden>Preview unavailable</span>'
        f'<span class="case-number mono" aria-hidden="true">{campaign["display_number"]:02d}</span></div>'
        f'<div class="case-preview"><p class="case-eyebrow" id="{cid}-context">{escape(campaign["eyebrow"])}</p>'
        f'<h3 id="{cid}-title">{escape(title)}</h3><p class="case-description" id="{cid}-description">{escape(campaign["description"])}</p>'
        f'<p class="project-ref-count" id="{cid}-references">{count} campaign posts</p>{teaser}'
        f'<div class="case-bottom"><span class="case-outcome">{escape(campaign["outcome"])}</span>'
        '<span class="case-toggle"><span class="read-label"><span class="when-closed">View details</span>'
        '<span class="when-open">Hide details</span></span><span class="plus" aria-hidden="true">+</span></span></div></div></summary>'
        f'<div class="case-body">{metrics(campaign,data["snapshot"])}<dl>{dl}</dl>'
        f'<section class="related-work" aria-labelledby="{cid}-links-title"><h4 id="{cid}-links-title">Campaign posts <span>({count})</span></h4>{links}</section>'
        f'{close_button(cid,title)}</div></details>\n'
    )


def render(source, data):
    source = remove(source)
    source = re.sub(r'/\* portfolio-campaigns:start \*/.*?/\* portfolio-campaigns:end \*/\s*','',source,flags=re.S)
    source = source.replace('</style>',CSS.strip()+'\n</style>',1)
    new = [c for c in data['campaigns'] if not c.get('existing_case')]
    cards = '<!-- portfolio-campaign-cases:start -->\n' + ''.join(new_case(c,data) for c in new) + '<!-- portfolio-campaign-cases:end -->\n'
    anchor = '</div>\n<div class="work-footer">'
    assert source.count(anchor)==1
    source = source.replace(anchor,cards+anchor,1)
    for c in data['campaigns']:
        if not c.get('existing_case'):
            continue
        pattern = r'<details\b[^>]*id="'+re.escape(c['case_id'])+r'".*?</details>'
        match = re.search(pattern,source,re.S)
        assert match
        body = match.group()
        original_codes = set(re.findall(r'instagram.com/(?:p|reel|tv)/([A-Za-z0-9_-]+)',body))
        links,count = post_links(c,data['posts'],original_codes)
        update = ('<!-- portfolio-campaign-update:start --><section class="campaign-update" '
                  f'aria-labelledby="{c["case_id"]}-campaign-update-title">'
                  f'<h4 id="{c["case_id"]}-campaign-update-title">Product launch to streetball activation</h4>'
                  f'<p>{escape(c["description"])}</p>{metrics(c,data["snapshot"])}'
                  f'<h4>Additional campaign posts <span>({count})</span></h4>{links}</section><!-- portfolio-campaign-update:end -->')
        anchor = '<div class="case-footer">'
        assert body.count(anchor)==1
        body=body.replace(anchor,update+anchor,1)
        source=source[:match.start()]+body+source[match.end():]
    total=32+len(new)
    source = re.sub(r'(<span class="project-count"[^>]*>)\d+ projects',lambda m:m.group(1)+f'{total} projects',source)
    return source


if __name__=='__main__':
    path=ROOT/'index.html'
    source=render(path.read_text(),json.loads((ROOT/'CAMPAIGN_ARCHIVE.json').read_text()))
    from apply_portfolio_usability import apply
    path.write_text(apply(source,json.loads((ROOT/'THUMBNAILS.json').read_text())))
