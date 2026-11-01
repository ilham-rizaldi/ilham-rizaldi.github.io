"""Present connected product programs while retaining every detailed project."""
from html import escape
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent.parent

CSS = r"""
/* portfolio-product-programs:start */
.program-showcase{margin:8px 0 56px;scroll-margin-top:110px}
.program-intro{display:grid;grid-template-columns:1.05fr 1fr;gap:48px;margin-bottom:30px}
.program-intro h3{font-size:clamp(28px,3.4vw,43px);line-height:1.14;font-weight:500;letter-spacing:-.045em;max-width:18ch}
.program-intro p:not(.kicker){font-size:15px;line-height:1.8;color:var(--muted);margin-top:14px;max-width:65ch}
.program-pillars{display:grid;gap:20px;align-content:start;padding-top:4px}
.program-pillar{display:grid;grid-template-columns:30px 1fr;gap:14px;border-top:1px solid var(--line);padding-top:16px}
.program-pillar>span{font:12px/1.6 monospace;color:var(--lime)}
.program-pillar h4{font-size:16px;font-weight:500;line-height:1.5;letter-spacing:-.02em}
.program-pillar p{font-size:13px!important;margin-top:5px!important;line-height:1.7!important}
.program-index{display:flex;flex-wrap:wrap;gap:8px;margin:0 0 24px;list-style:none;padding:0}
.program-index a{display:flex;align-items:center;gap:14px;min-height:44px;border:1px solid var(--line);padding:9px 13px;font-size:13px;line-height:1.5}
.program-index a:hover,.program-index a:focus-visible{border-color:var(--lime);color:var(--lime)}
.program-stack{border-top:1px solid var(--line)}
.program-story{border-bottom:1px solid var(--line);scroll-margin-top:106px}
.program-story>summary{display:grid;grid-template-columns:112px 1fr 40px;gap:25px;padding:23px 0;align-items:center;cursor:pointer;list-style:none}
.program-story>summary::-webkit-details-marker{display:none}
.program-story>summary::marker{content:''}
.program-story>summary:focus-visible{outline:2px solid var(--lime);outline-offset:7px}
.program-media{position:relative;display:block;width:112px;aspect-ratio:1;overflow:hidden;container-type:size;background:#20221c}
.program-media img{display:block;position:absolute;width:var(--crop-width,100%);height:auto;max-width:none;left:50%;top:50%;transform:translate(var(--crop-x,-50%),var(--crop-y,-50%));object-fit:cover}
.program-media img:not([data-content-crop]){width:100%;height:100%;object-fit:cover}
.program-kind{display:flex;align-items:center;flex-wrap:wrap;gap:9px;font-size:10px;text-transform:uppercase;letter-spacing:.08em;color:var(--lime);margin-bottom:7px;line-height:1.6}
.program-kind b{font-family:monospace;font-weight:400;color:var(--muted)}
.program-summary h4{font-size:clamp(21px,2.2vw,28px);font-weight:500;line-height:1.22;letter-spacing:-.03em}
.program-subtitle{font-size:13px;line-height:1.6;color:var(--muted);margin-top:5px}
.program-summary-copy{font-size:13px;line-height:1.7;color:var(--muted);margin-top:8px;max-width:75ch}
.program-expand{display:grid;place-items:center;width:36px;height:36px;border:1px solid var(--line);font-size:22px;font-weight:400;color:var(--ink)}
.program-story[open] .program-expand{color:var(--lime);border-color:var(--lime)}
.program-story[open] .program-expand span{transform:rotate(45deg)}
.program-body{margin:0 0 28px 137px;padding-top:20px;border-top:1px solid var(--line)}
.program-strategy-label{font-size:10px;text-transform:uppercase;letter-spacing:.1em;color:var(--lime);margin-bottom:8px}
.program-strategy{font-size:15px;line-height:1.8;max-width:82ch;margin-bottom:24px}
.program-body-grid{display:grid;grid-template-columns:1fr 1fr;gap:36px}
.program-body h5{font-size:12px;line-height:1.5;letter-spacing:.04em;text-transform:uppercase;font-weight:500;color:var(--muted);margin-bottom:14px}
.program-release-list,.program-activation-list{list-style:none;padding:0;margin:0}
.program-release-list>li{position:relative;padding:0 0 18px 31px}
.program-release-list>li::before{content:'';position:absolute;left:9px;top:18px;bottom:0;width:1px;background:var(--line)}
.program-release-list>li:last-child::before{display:none}
.program-step{position:absolute;left:0;top:1px;color:var(--lime);font:11px/1.6 monospace}
.program-role{display:block;font-size:10px;line-height:1.5;color:var(--muted);text-transform:uppercase;letter-spacing:.055em;margin-bottom:5px}
.program-item a{display:flex;justify-content:space-between;gap:12px;align-items:start;min-height:44px;padding:0 0 6px;font-size:15px;line-height:1.55;font-weight:500}
.program-item a:hover{color:var(--lime)}
.program-item a>span:last-child{color:var(--lime);font-size:17px}
.program-item p{font-size:12px;line-height:1.75;color:var(--muted);margin:0}
.program-activation-list>li{padding:0 0 17px;margin-bottom:17px;border-bottom:1px solid var(--line)}
.program-activation-list>li:last-child{border:0;margin-bottom:0}
.program-touchpoints{margin-top:22px;border-top:1px solid var(--line);padding-top:20px}
.program-touchpoints>p{font-size:11px;color:var(--muted);margin-bottom:10px}
.program-touchpoints ul{display:flex;flex-wrap:wrap;gap:8px;list-style:none;padding:0;margin:0}
.program-touchpoints li{font-size:11px;line-height:1.5;border:1px solid var(--line);padding:6px 9px}
.program-footer{display:flex;justify-content:space-between;gap:20px;align-items:center;margin-top:22px}
.program-footer a,.program-footer button{font-size:12px;min-height:44px;display:inline-flex;align-items:center;gap:16px;color:var(--muted)}
.program-footer button{background:transparent;border:0;cursor:pointer;padding:8px}
.program-footer a:hover,.program-footer button:hover{color:var(--lime)}
.project-archive-heading{border-top:1px solid var(--line);padding-top:28px;margin:8px 0 20px}
.project-archive-heading h3{font-size:23px;font-weight:500;letter-spacing:-.03em}
.project-archive-heading p{font-size:13px;line-height:1.7;color:var(--muted);margin-top:7px}
.case-preview .program-membership{font-size:10px;line-height:1.7;letter-spacing:.025em;color:var(--lime);margin:11px 0}
.case-body .program-context{display:flex;flex-wrap:wrap;align-items:center;gap:8px 15px;margin:0 0 23px;border-bottom:1px solid var(--line);padding:0 0 16px;font-size:11px;color:var(--muted)}
.program-context a{min-height:44px;display:inline-flex;align-items:center;gap:12px;color:var(--lime);font-size:12px}
@media(max-width:760px){.program-intro{grid-template-columns:1fr;gap:23px}.program-pillars{grid-template-columns:1fr 1fr;gap:20px}.program-body{margin-left:0}.program-body-grid{gap:24px}.program-story>summary{grid-template-columns:85px 1fr 32px;gap:16px}.program-media{width:85px}.program-expand{width:30px;height:30px}.program-summary-copy{font-size:12px}.program-intro h3{max-width:21ch}}
@media(max-width:520px){.program-showcase{margin-bottom:36px}.program-pillars{grid-template-columns:1fr;gap:16px}.program-story>summary{grid-template-columns:65px minmax(0,1fr) 25px;gap:12px;padding:20px 0}.program-media{width:65px}.program-kind{font-size:9px;letter-spacing:.045em}.program-summary h4{font-size:20px}.program-subtitle{font-size:12px}.program-summary-copy{display:none}.program-expand{width:25px;height:30px}.program-body-grid{grid-template-columns:1fr;gap:22px}.program-strategy{font-size:14px}.program-footer{align-items:flex-start}.program-index{gap:6px}.program-index a{font-size:12px;padding:8px 10px}.program-touchpoints li{font-size:10px}}
@media print{.program-showcase,.program-membership,.program-context,.project-archive-heading{display:none!important}}
/* portfolio-product-programs:end */
"""

JS = r"""
/* portfolio-product-programs:start */
document.querySelectorAll('[data-close-program]').forEach(button=>button.addEventListener('click',()=>{
 const program=document.getElementById(button.dataset.closeProgram);
 if(!program)return;
 program.open=false;
 program.querySelector('summary').focus({preventScroll:true});
 program.scrollIntoView({block:'start',behavior:matchMedia('(prefers-reduced-motion: reduce)').matches?'auto':'smooth'});
}));
/* portfolio-product-programs:end */
"""


def entry(item, number=None):
    step = f'<span class="program-step" aria-hidden="true">{number:02d}</span>' if number is not None else ''
    return ('<li class="program-item">'+step+f'<span class="program-role">{escape(item["role"])}</span>'
            f'<a href="#{escape(item["target"], quote=True)}"><span>{escape(item["label"])}</span><span aria-hidden="true">↗</span></a>'
            f'<p>{escape(item["description"])}</p></li>')


def program_card(program, number, source):
    cid=program['cover_case']
    case=re.search(r'<details\b[^>]*id="'+re.escape(cid)+r'".*?</details>',source,re.S)
    assert case, cid
    img=re.search(r'<img\b[^>]+>',case.group()).group()
    img=re.sub(r'\sdata-preview-image\b','',img)
    releases=''.join(entry(item,i) for i,item in enumerate(program['releases'],1))
    activations=''.join(entry(item) for item in program['activations'])
    touches=''.join(f'<li>{escape(t)}</li>' for t in program['touchpoints'])
    title=escape(program['title']);pid=program['id']
    return (
        f'<details class="program-story" id="{pid}" name="portfolio-programs"'+(' open' if number==1 else '')+'>'
        f'<summary aria-labelledby="{pid}-kind {pid}-title" aria-describedby="{pid}-subtitle">'
        f'<span class="program-media" aria-hidden="true">{img}</span><div class="program-summary">'
        f'<p class="program-kind" id="{pid}-kind"><b>{number:02d}</b>{escape(program["kind"])}</p>'
        f'<h4 id="{pid}-title">{title}</h4><p class="program-subtitle" id="{pid}-subtitle">{escape(program["subtitle"])}</p>'
        f'<p class="program-summary-copy">{escape(program["summary"])}</p></div>'
        '<span class="program-expand" aria-hidden="true"><span>+</span></span></summary><div class="program-body">'
        f'<p class="program-strategy-label">My strategy</p><p class="program-strategy">{escape(program["strategy"])}</p>'
        '<div class="program-body-grid"><div><h5>'+('Product release sequence' if len(program['releases'])>1 else 'Main product & launch')+'</h5>'
        '<ol class="program-release-list">'+releases+'</ol></div><div><h5>Supporting campaigns & activations</h5>'
        '<ul class="program-activation-list">'+activations+'</ul></div></div><div class="program-touchpoints">'
        '<p>Connected marketing touchpoints</p><ul>'+touches+'</ul></div><div class="program-footer">'
        f'<a href="#{program["releases"][0]["target"]}">Open the product case <span aria-hidden="true">↗</span></a>'
        f'<button type="button" data-close-program="{pid}" aria-controls="{pid}" aria-label="Close program: {escape(program["title"],quote=True)}" data-js-only hidden>Close program <span aria-hidden="true">×</span></button>'
        '</div></div></details>'
    )


def render(source):
    path=ROOT/'PRODUCT_PROGRAMS.json'
    if not path.exists():
        return source
    data=json.loads(path.read_text())
    source=re.sub(r'<!-- portfolio-product-programs:start -->.*?<!-- portfolio-product-programs:end -->\s*','',source,flags=re.S)
    source=re.sub(r'<!-- portfolio-program-membership:start -->.*?<!-- portfolio-program-membership:end -->','',source,flags=re.S)
    source=re.sub(r'<!-- portfolio-program-context:start -->.*?<!-- portfolio-program-context:end -->','',source,flags=re.S)
    source=re.sub(r'/\* portfolio-product-programs:start \*/.*?/\* portfolio-product-programs:end \*/\s*','',source,flags=re.S)
    source=source.replace('</style>',CSS.strip()+'\n</style>',1)
    programs=data['programs']
    nav=''.join(f'<li><a href="#{p["id"]}">{escape(p["title"])}<span aria-hidden="true">↘</span></a></li>' for p in programs)
    block=(
        '<!-- portfolio-product-programs:start --><section class="program-showcase" id="campaign-programs" aria-labelledby="programs-title">'
        '<div class="program-intro"><div><p class="kicker">How the work connects</p>'
        f'<h3 id="programs-title">{escape(data["heading"])}</h3><p>{escape(data["intro"])}</p></div>'
        '<div class="program-pillars"><div class="program-pillar"><span>01</span><div><h4>Integrated product marketing</h4>'
        '<p>Connect digital campaigns, events, community activation, KOLs, retail activity, and institutional partnerships around a product.</p></div></div>'
        '<div class="program-pillar"><span>02</span><div><h4>Product series &amp; release strategy</h4>'
        '<p>Carry a product family through successive launches, with a distinct communication role for each release.</p></div></div></div></div>'
        '<nav aria-label="Explore connected product programs"><ul class="program-index">'+nav+'</ul></nav>'
        '<div class="program-stack">'+''.join(program_card(p,i,source) for i,p in enumerate(programs,1))+'</div></section>'
        '<div class="project-archive-heading"><h3>Project archive.</h3><p>Explore the detailed work, responsibilities, published content, and results behind each program, alongside my other projects.</p></div>'
        '<!-- portfolio-product-programs:end -->\n'
    )
    anchor='<nav class="project-jump"'
    assert source.count(anchor)==1
    source=source.replace(anchor,block+anchor,1)
    for p in programs:
        for cid in p['members']:
            pattern=r'<details\b[^>]*id="'+re.escape(cid)+r'".*?</details>'
            m=re.search(pattern,source,re.S);assert m,cid
            body=m.group()
            badge='<!-- portfolio-program-membership:start --><p class="program-membership">'+escape(p['kind'])+' · '+escape(p['title'])+'</p><!-- portfolio-program-membership:end -->'
            body=re.sub(r'(<p class="case-description"[^>]*>.*?</p>)',lambda m:m.group(1)+badge,body,count=1,flags=re.S)
            context=('<!-- portfolio-program-context:start --><nav class="program-context" aria-label="Connected product program">'
                     f'<span>Part of the wider program</span><a href="#{p["id"]}">{escape(p["title"])} <span aria-hidden="true">↗</span></a></nav><!-- portfolio-program-context:end -->')
            body=body.replace('<div class="case-body">','<div class="case-body">'+context,1)
            source=source[:m.start()]+body+source[m.end():]
    # Extend existing deep links to program summaries and subsections inside a case.
    old=r"function revealLinkedCase\(\)\{.*?\n\}\ndocument\.querySelectorAll\('[^']*#case-[^']*'\)\.forEach\(link=>link\.addEventListener\('click',\(\)=>\{.*?\n\}\)\);"
    replacement="""function revealLinkedCase(){
 const target=document.getElementById(location.hash.slice(1));
 if(!target)return;
 const item=target.matches('.case,.program-story')?target:target.closest('.case,.program-story');
 if(!item)return;
 if(item.matches('.case'))selectFilter('all',true);
 item.open=true;
 requestAnimationFrame(()=>{
  const focus=target===item?item.querySelector('summary'):target;
  focusTarget(focus);
  (target===item?item:target).scrollIntoView({block:'start',behavior:matchMedia('(prefers-reduced-motion: reduce)').matches?'auto':'smooth'});
 });
}
document.querySelectorAll('a[href^="#case-"],a[href^="#program-"],a[href="#love-hustle-kol-title"]').forEach(link=>link.addEventListener('click',()=>{
 const target=document.getElementById(link.hash.slice(1));
 const item=target&&(target.matches('.case,.program-story')?target:target.closest('.case,.program-story'));
 if(item){if(item.matches('.case'))selectFilter('all',true);item.open=true;}
 if(location.hash===link.hash)revealLinkedCase();
}));"""
    source,count=re.subn(old,lambda m:replacement,source,count=1,flags=re.S)
    assert count==1,'Existing deep-link behavior must be recognized'
    init="document.querySelectorAll('[data-js-only]').forEach(control=>{control.hidden=false;});"
    assert init in source
    source=source.replace(init,JS.strip()+'\n'+init,1)
    source=source.replace('Product launches, campaigns, partnerships, events, content, and photography. Each project includes an overview, my work, and related posts or decks. Planning proposals are labeled separately.',
                          'Integrated product marketing, successive launches, and the projects behind them. Explore how campaigns, communities, creators, and partners connect around a product.')
    return source


if __name__=='__main__':
    path=ROOT/'index.html'
    path.write_text(render(path.read_text()))
