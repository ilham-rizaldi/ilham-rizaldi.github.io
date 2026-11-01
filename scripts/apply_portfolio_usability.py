"""Apply bottom close controls and responsive crops without changing media files."""
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent.parent

CSS = r"""
/* portfolio-usability:start */
.case-footer{display:flex;justify-content:flex-end;border-top:1px solid var(--line);margin-top:24px;padding-top:14px}
.case-close{display:inline-flex;align-items:center;justify-content:flex-end;gap:14px;min-height:52px;padding:6px 7px 6px 16px;background:none;border:0;color:var(--muted);font-size:14px}
.case-close:hover{color:var(--ink)}
.close-diamond{display:grid;place-items:center;width:36px;height:36px;border:1px solid var(--line);transform:rotate(45deg)}
.close-diamond>span{font-size:23px;line-height:1;color:var(--ink);transform:rotate(-45deg)}
.case-media.project-cover,.post-preview-atlas{container-type:size}
.project-cover>img[data-content-crop],.post-preview-atlas>img[data-content-crop]{position:absolute;display:block;width:var(--crop-width)!important;height:auto!important;max-width:none!important;aspect-ratio:auto!important;left:50%!important;top:var(--crop-position,50%)!important;transform:translate(var(--crop-x,-50%),var(--crop-y,-50%))!important;object-fit:fill!important}
.case summary:hover .project-cover>img[data-content-crop]{transform:translate(var(--crop-x,-50%),var(--crop-y,-50%))!important}
.project-cover .image-duo img,.project-cover .collab-art img{object-fit:cover}
.post-preview-deck>img{object-fit:cover}
@media print{.case-footer{display:none!important}}
/* portfolio-usability:end */
"""

JS = r"""
/* portfolio-close-details:start */
document.querySelectorAll('[data-close-case]').forEach(button=>{
 button.addEventListener('click',()=>{
  const item=document.getElementById(button.dataset.closeCase);
  if(!item||!item.matches('details.case'))return;
  item.open=false;
  const summary=item.querySelector('summary');
  if(summary)summary.focus({preventScroll:true});
  const reduced=matchMedia('(prefers-reduced-motion: reduce)').matches;
  item.scrollIntoView({block:'start',behavior:reduced?'auto':'smooth'});
 });
});
/* portfolio-close-details:end */
"""


def crop_style(image_width, content_width, content_height, x=50, y=50):
    return (f'--crop-width:max({100*image_width/content_width:.5f}cqw,'
            f'{100*image_width/content_height:.5f}cqh);--crop-x:-{x:.5f}%;--crop-y:-{y:.5f}%')


def apply(source, manifest):
    source = re.sub(r'/\* portfolio-usability:start \*/.*?/\* portfolio-usability:end \*/\s*', '', source, flags=re.S)
    source = source.replace('</style>', CSS.strip() + '\n</style>', 1)
    source = re.sub(r'/\* portfolio-close-details:start \*/.*?/\* portfolio-close-details:end \*/\s*', '', source, flags=re.S)
    anchor = "document.querySelectorAll('[data-js-only]').forEach(control=>{control.hidden=false;});"
    assert anchor in source
    source = source.replace(anchor, JS.strip() + '\n' + anchor, 1)

    def replace_img(tag, style):
        tag = re.sub(r'\sstyle="[^"]*"|\sdata-content-crop(?:="[^"]*")?', '', tag)
        return tag[:-1] + f' data-content-crop style="{style}">'

    def project(match):
        body = match.group()
        cid = re.search(r'\bid="([^"]+)"', body).group(1)
        project = manifest['projects'][cid]
        cover = project['cover']
        if cover['kind'] != 'image':
            return body
        code = project.get('source_post_code')
        if code:
            sw, sh = manifest['posts'][code]['source_dimensions']
            iw, ih = cover['width'], cover['height']
            scale = min(iw/sw, ih/sh)
            cw, ch = sw*scale, sh*scale
        else:
            iw, ih = cover['width'], cover['height']
            cw, ch = iw, ih
        style = crop_style(iw, cw, ch)
        if cid == 'case-uss-jsd':
            style += ';--crop-position:0%;--crop-y:0%'
        # Only direct cover images use these crops; existing multi-image layouts use object-fit.
        pattern = r'(<div class="case-media project-cover"[^>]*>)(<img\b[^>]*>)'
        return re.sub(pattern, lambda m: m.group(1)+replace_img(m.group(2),style), body, count=1)
    source = re.sub(r'<details\b[^>]*class="case(?:\s[^"]*)?"[^>]*>.*?</details>', project, source, flags=re.S)

    def post(match):
        body = match.group()
        href = re.search(r'href="[^"]*instagram.com/(?:p|reel|tv)/([^/?"]+)', body)
        if not href or href.group(1) not in manifest['posts']:
            return body
        p = manifest['posts'][href.group(1)]
        if 'sheet' not in p:
            return body
        w,h = p['source_dimensions']
        tile = p['tileSize']
        scale = min(tile/w,tile/h)
        cw,ch = w*scale,h*scale
        style = crop_style(tile*p['columns'],cw,ch,
                           100*(p['column']+.5)/p['columns'],
                           100*(p['row']+.5)/p['rows'])
        return re.sub(r'(<span class="post-preview post-preview-atlas"[^>]*>)(<img\b[^>]*>)',
                      lambda m: m.group(1)+replace_img(m.group(2),style), body, count=1)
    source = re.sub(r'<a\b[^>]*>.*?</a>', post, source, flags=re.S)
    return source


if __name__ == '__main__':
    index = ROOT/'index.html'
    index.write_text(apply(index.read_text(),json.loads((ROOT/'THUMBNAILS.json').read_text())))
