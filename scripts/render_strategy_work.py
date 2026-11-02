"""Render public-safe strategy cases without changing the campaign snapshots."""
from html import escape
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent.parent

CSS = r"""
/* portfolio-strategy-work:start */
.portfolio-explore{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px;margin:0 0 36px}
.portfolio-explore a{display:flex;justify-content:space-between;gap:14px;border:1px solid var(--line);padding:16px 18px;min-height:68px;align-items:center;font-size:13px;line-height:1.5}
.portfolio-explore small{display:block;font-size:11px;color:var(--muted);margin-top:4px}
.portfolio-explore a>span:last-child{color:var(--lime);font-size:19px}
.portfolio-explore a:hover{border-color:var(--lime)}
.strategy-work{margin-bottom:60px;scroll-margin-top:110px}
.strategy-intro{display:grid;grid-template-columns:1fr 1fr;gap:45px;margin-bottom:27px;align-items:end}
.strategy-intro h3{font-size:clamp(28px,3.4vw,43px);font-weight:500;letter-spacing:-.045em;line-height:1.15;max-width:18ch}
.strategy-intro>p{font-size:14px;line-height:1.8;color:var(--muted);max-width:63ch}
.strategy-stack{border-top:1px solid var(--line)}
.strategy-case{border-bottom:1px solid var(--line);scroll-margin-top:110px}
.strategy-case>summary{display:grid;grid-template-columns:65px minmax(0,1fr) 38px;gap:22px;padding:25px 0;align-items:center;cursor:pointer;list-style:none}
.strategy-case>summary::-webkit-details-marker{display:none}
.strategy-case>summary::marker{content:''}
.strategy-case>summary:focus-visible{outline:2px solid var(--lime);outline-offset:6px}
.strategy-number{font:25px/1.2 monospace;color:var(--dim);letter-spacing:-.06em}
.strategy-category{font-size:10px;line-height:1.6;letter-spacing:.075em;text-transform:uppercase;color:var(--lime);margin-bottom:7px}
.strategy-summary h4{font-size:clamp(21px,2.3vw,28px);font-weight:500;line-height:1.25;letter-spacing:-.03em}
.strategy-summary>p:last-child{font-size:13px;line-height:1.75;color:var(--muted);margin-top:8px;max-width:85ch}
.strategy-expand{display:grid;place-items:center;width:34px;height:34px;border:1px solid var(--line);font-size:22px}
.strategy-case[open] .strategy-number{color:var(--lime)}
.strategy-case[open] .strategy-expand{color:var(--lime);border-color:var(--lime)}
.strategy-case[open] .strategy-expand span{transform:rotate(45deg)}
.strategy-body{margin:0 0 30px 87px;padding-top:21px;border-top:1px solid var(--line)}
.strategy-status{display:inline-block;font-size:10px;line-height:1.6;letter-spacing:.04em;color:var(--muted);border:1px solid var(--line);padding:6px 9px;margin-bottom:22px}
.strategy-overview{display:grid;grid-template-columns:minmax(0,1.25fr) minmax(220px,.75fr);gap:40px;margin-bottom:27px}
.strategy-story h5,.strategy-delivered h5{font-size:10px;line-height:1.6;font-weight:500;letter-spacing:.1em;text-transform:uppercase;color:var(--lime);margin-bottom:8px}
.strategy-story p{font-size:14px;line-height:1.85;color:var(--muted);margin-bottom:19px}
.strategy-story p:last-child{margin-bottom:0}
.strategy-proof{background:var(--panel);padding:22px 24px;border-left:2px solid var(--lime)}
.strategy-proof>strong{display:block;font-size:52px;line-height:1.1;font-weight:500;letter-spacing:-.055em;margin-bottom:7px}
.strategy-proof>span{display:block;font-size:13px;line-height:1.7;color:var(--ink)}
.strategy-proof .strategy-proof-note{font-size:11px;line-height:1.8;color:var(--muted);margin-top:15px}
.strategy-proof-secondary{font-size:11px;line-height:1.7;color:var(--muted);margin-top:12px}
.strategy-word-comparison{display:grid;grid-template-columns:1fr 18px 1fr;gap:8px;align-items:center;margin-top:19px;padding-top:15px;border-top:1px solid var(--line)}
.strategy-word-comparison b{display:block;font-size:21px;font-weight:500;letter-spacing:-.03em}
.strategy-word-comparison small{display:block;font-size:10px;color:var(--muted);line-height:1.7}
.strategy-word-comparison>span:nth-child(2){color:var(--lime)}
.strategy-copy-reduction{font-size:12px;line-height:1.7;color:var(--lime);margin-top:11px}
.strategy-modules{display:grid;grid-template-columns:1fr 1fr;gap:0 30px}
.strategy-module{border-top:1px solid var(--line);padding:19px 0}
.strategy-module h5{font-size:15px;line-height:1.55;letter-spacing:-.015em;font-weight:500}
.strategy-module-status{display:inline-block;font-size:10px;line-height:1.7;color:var(--lime);margin:6px 0 8px}
.strategy-module>p:last-of-type{font-size:13px;line-height:1.85;color:var(--muted)}
.strategy-module>a{font-size:12px;min-height:44px;display:inline-flex;gap:15px;align-items:center;color:var(--ink);margin-top:6px}
.strategy-module>a:hover{color:var(--lime)}
.strategy-delivered{border-top:1px solid var(--line);padding-top:20px;margin-top:5px}
.strategy-delivered p{font-size:13px;line-height:1.85;color:var(--muted);max-width:90ch}
.strategy-footer{display:flex;align-items:center;justify-content:space-between;gap:20px;margin-top:17px}
.strategy-related{display:flex;gap:8px 22px;flex-wrap:wrap}
.strategy-related a,.strategy-close{display:inline-flex;gap:12px;align-items:center;font-size:12px;line-height:1.5;min-height:44px;color:var(--muted)}
.strategy-close{border:0;background:none;cursor:pointer;padding:8px;flex-shrink:0}
.strategy-related a:hover,.strategy-close:hover{color:var(--lime)}
.strategy-connection{border-top:1px solid var(--line);padding-top:18px;margin-top:22px;scroll-margin-top:110px}
.strategy-connection h4{font-size:15px;font-weight:500;line-height:1.6;letter-spacing:-.015em}
.strategy-connection p{font-size:13px;line-height:1.85;color:var(--muted);margin:8px 0}
.strategy-connection a{font-size:12px;display:inline-flex;align-items:center;gap:14px;min-height:44px;color:var(--lime)}
.project-archive-heading{scroll-margin-top:110px}
@media(max-width:760px){.strategy-intro{grid-template-columns:1fr;gap:16px}.strategy-overview{grid-template-columns:1fr;gap:22px}.strategy-body{margin-left:0}.strategy-case>summary{grid-template-columns:40px minmax(0,1fr) 30px;gap:15px}.strategy-expand{width:28px;height:30px}.portfolio-explore{gap:8px}.portfolio-explore a{padding:13px 12px;font-size:12px}.strategy-proof>strong{font-size:44px}}
@media(max-width:520px){.portfolio-explore{grid-template-columns:1fr;gap:7px;margin-bottom:28px}.portfolio-explore a{min-height:52px;padding:10px 13px}.portfolio-explore small{display:inline;margin-left:8px;font-size:10px}.strategy-work{margin-bottom:40px}.strategy-case>summary{grid-template-columns:28px minmax(0,1fr) 25px;gap:10px;padding:22px 0}.strategy-number{font-size:18px}.strategy-category{font-size:9px;letter-spacing:.045em}.strategy-summary h4{font-size:21px}.strategy-summary>p:last-child{font-size:12px}.strategy-modules{grid-template-columns:1fr}.strategy-overview{gap:20px}.strategy-footer{align-items:flex-start}.strategy-related{flex-direction:column;gap:0}.strategy-status{font-size:9px}.strategy-proof{padding:20px}.strategy-expand{width:25px}}
@media print{.portfolio-explore,.strategy-work,.strategy-connection{display:none!important}}
/* portfolio-strategy-work:end */
"""

JS = r"""
/* portfolio-strategy-work:start */
document.querySelectorAll('[data-close-strategy]').forEach(button=>button.addEventListener('click',()=>{
 const item=document.getElementById(button.dataset.closeStrategy);
 if(!item)return;
 item.open=false;
 item.querySelector('summary').focus({preventScroll:true});
 item.scrollIntoView({block:'start',behavior:matchMedia('(prefers-reduced-motion: reduce)').matches?'auto':'smooth'});
}));
/* portfolio-strategy-work:end */
"""


def proof(item):
    p=item['proof']
    extra=''
    if p['kind']=='copy':
        extra=('<div class="strategy-word-comparison" aria-label="Word count before and after the copy revision">'
               f'<span><b>{p["before"]:,}</b><small>words before</small></span><span aria-hidden="true">→</span>'
               f'<span><b>{p["after"]:,}</b><small>words after</small></span></div>'
               f'<p class="strategy-copy-reduction">Approximately {escape(p["reduction"])} less text</p>')
    if p.get('secondary'):
        extra+=f'<p class="strategy-proof-secondary">{escape(p["secondary"])}</p>'
    return ('<aside class="strategy-proof" aria-label="Documented work scope">'
            f'<strong>{escape(p["value"])}</strong><span>{escape(p["label"])}</span>'+extra+
            f'<p class="strategy-proof-note">{escape(p["note"])}</p></aside>')


def case_html(item,index):
    cid=item['id']
    modules=[]
    for module in item['modules']:
        link=module.get('link')
        more=(f'<a href="{escape(link["url"],quote=True)}" target="_blank" rel="noopener noreferrer">{escape(link["label"])}<span aria-hidden="true">↗</span></a>' if link else '')
        modules.append('<article class="strategy-module">'+f'<h5>{escape(module["title"])}</h5>'
                       f'<p class="strategy-module-status">{escape(module["status"])}</p><p>{escape(module["text"])}</p>'+more+'</article>')
    related=''.join(f'<a href="#{escape(r["target"],quote=True)}">{escape(r["label"])}<span aria-hidden="true">↗</span></a>' for r in item['related'])
    return (
        f'<details class="strategy-case" id="{cid}" name="portfolio-strategy"'+(' open' if index==0 else '')+'>'
        f'<summary aria-labelledby="{cid}-category {cid}-title" aria-describedby="{cid}-summary">'
        f'<span class="strategy-number" aria-hidden="true">{escape(item["number"])}</span><div class="strategy-summary">'
        f'<p class="strategy-category" id="{cid}-category">{escape(item["category"])}</p><h4 id="{cid}-title">{escape(item["title"])}</h4>'
        f'<p id="{cid}-summary">{escape(item["summary"])}</p></div><span class="strategy-expand" aria-hidden="true"><span>+</span></span></summary>'
        f'<div class="strategy-body"><p class="strategy-status">{escape(item["status"])}</p><div class="strategy-overview">'
        f'<div class="strategy-story"><h5>The challenge</h5><p>{escape(item["challenge"])}</p><h5>My work</h5><p>{escape(item["role"])}</p></div>'
        +proof(item)+'</div><div class="strategy-modules">'+''.join(modules)+'</div>'
        f'<div class="strategy-delivered"><h5>Delivered work</h5><p>{escape(item["deliverable"])}</p></div>'
        f'<div class="strategy-footer"><nav class="strategy-related" aria-label="Related work for {escape(item["title"],quote=True)}">{related}</nav>'
        f'<button type="button" class="strategy-close" data-close-strategy="{cid}" aria-controls="{cid}" aria-label="Close case study: {escape(item["title"],quote=True)}" data-js-only hidden>Close case study <span aria-hidden="true">×</span></button>'
        '</div></div></details>'
    )


def render(source):
    data_path=ROOT/'STRATEGY_WORK.json'
    if not data_path.exists():
        return source
    data=json.loads(data_path.read_text())
    source=re.sub(r'<!-- portfolio-strategy-work:start -->.*?<!-- portfolio-strategy-work:end -->\s*','',source,flags=re.S)
    source=re.sub(r'<!-- portfolio-strategy-connection:start -->.*?<!-- portfolio-strategy-connection:end -->','',source,flags=re.S)
    source=re.sub(r'/\* portfolio-strategy-work:start \*/.*?/\* portfolio-strategy-work:end \*/\s*','',source,flags=re.S)
    source=source.replace('</style>',CSS.strip()+'\n</style>',1)
    project_count=len(re.findall(r'<details\b[^>]*class="case(?:\s[^"]*)?"',source))
    programs_count=len(re.findall(r'<details\b[^>]*class="program-story"',source))
    section=(
        '<!-- portfolio-strategy-work:start --><nav class="portfolio-explore" aria-label="Explore the portfolio">'
        f'<a href="#strategy-work"><span>Strategy &amp; research<small>{len(data["cases"])} case studies</small></span><span aria-hidden="true">↘</span></a>'
        f'<a href="#campaign-programs"><span>Product programs<small>{programs_count} connected programs</small></span><span aria-hidden="true">↘</span></a>'
        f'<a href="#project-archive"><span>Project archive<small>{project_count} detailed projects</small></span><span aria-hidden="true">↘</span></a></nav>'
        '<section class="strategy-work" id="strategy-work" aria-labelledby="strategy-work-title"><div class="strategy-intro"><div>'
        f'<p class="kicker">Strategy / Research / Operations</p><h3 id="strategy-work-title">{escape(data["title"])}</h3></div><p>{escape(data["intro"])}</p></div>'
        '<div class="strategy-stack">'+''.join(case_html(item,index)for index,item in enumerate(data['cases']))+'</div></section>'
        '<!-- portfolio-strategy-work:end -->\n'
    )
    anchor='<!-- portfolio-product-programs:start -->'
    assert source.count(anchor)==1,'Connected product programs must exist'
    source=source.replace(anchor,section+anchor,1)
    source=source.replace('<div class="project-archive-heading">','<div class="project-archive-heading" id="project-archive">',1)
    for c in data['connections']:
        pattern=r'<details\b[^>]*id="'+re.escape(c['case_id'])+r'".*?</details>'
        match=re.search(pattern,source,re.S);assert match,c['case_id']
        case=match.group();assert '</dl>' in case,c['case_id']
        identity=f' id="{escape(c["id"],quote=True)}"' if c.get('id')else ''
        connection=('<!-- portfolio-strategy-connection:start --><section class="strategy-connection"'+identity+'>'
                    f'<h4>{escape(c["title"])}</h4><p>{escape(c["text"])}</p>'
                    f'<a href="#{c["target"]}">Explore the strategic work<span aria-hidden="true">↗</span></a></section><!-- portfolio-strategy-connection:end -->')
        case=case.replace('</dl>','</dl>'+connection,1)
        source=source[:match.start()]+case+source[match.end():]
    source=source.replace('.case,.program-story,.strategy-case','.case,.program-story')
    source=source.replace('.case,.program-story','.case,.program-story,.strategy-case')
    source=source.replace(',a[href^="#strategy-"]','')
    selector='a[href^="#case-"],a[href^="#program-"],a[href="#love-hustle-kol-title"]'
    assert selector in source,'Expected program navigation must exist'
    source=source.replace(selector,selector+',a[href^="#strategy-"]',1)
    init="document.querySelectorAll('[data-js-only]').forEach(control=>{control.hidden=false;});"
    assert init in source
    return source.replace(init,JS.strip()+'\n'+init,1)


if __name__=='__main__':
    path=ROOT/'index.html'
    path.write_text(render(path.read_text()))
