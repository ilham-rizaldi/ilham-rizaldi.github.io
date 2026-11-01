"""Build approved Basketball additions from the retained audit, without refreshing earlier snapshots."""
import argparse
from datetime import datetime
import hashlib
import json
import math
from pathlib import Path
from zoneinfo import ZoneInfo
from update_instagram_metrics import aggregate, valid_count

ROOT = Path(__file__).resolve().parent.parent

DEFINITIONS = [
    {'id':'allegro_meta','audit_id':'allegro','case_id':'case-allegro-meta','display_number':36,'category':'brand',
     'title':'Allegro Meta: All Game. All Day.','eyebrow':'Ardiles Basketball / Product campaign / 2025',
     'description':'One pair for school, basketball, and time with friends. A product campaign built around the daily routine of student-athletes.',
     'outcome':'Student-athlete positioning & launch content','cover_code':'DMPqWfepRmE',
     'cover_alt':'Allegro Meta basketball shoes on the orange Ready Now launch artwork',
     'details':[
         ['Project overview','Allegro Meta connects school, basketball, and everyday wear through the All Game. All Day message.'],
         ['Campaign focus','A student-athlete routine: class in the morning, basketball after school, and time with friends in the same pair.'],
         ['Published work','The sequence combines teasers, the July product release, everyday-use stories, 360° carousels, size guidance, store information, and creator tutorials.'],
         ['Content results','The 23 linked posts span July–December 2025. Their counters include later creator content, so the figures below describe this product-content collection.']
     ]},
    {'id':'community_league','audit_id':'headshoes','case_id':'case-community-league','display_number':37,'category':'community',
     'title':'Ardiles Community League × Headshoes.','eyebrow':'Ardiles Basketball / Community event / 2023',
     'description':'A basketball gathering for communities, with Headshoes at The Breeze, BSD, on 5 March 2023.',
     'outcome':'Community partnership & event communication','cover_code':'Comok3ov2aB',
     'cover_alt':'Ardiles Community League and Headshoes event announcement for 5 March 2023 at The Breeze BSD',
     'details':[
         ['Project overview','Ardiles Community League with Headshoes brought basketball communities together at The Breeze, BSD, on 5 March 2023.'],
         ['Event focus','A place for emerging basketball communities to play and connect, as described in the event announcement.'],
         ['Published work','The five linked posts cover the announcement, a preparatory pickup game, event photography, a video recap, and participant testimonials.']
     ]},
    {'id':'spectra','audit_id':'spectra','case_id':'case-spectra','display_number':38,'category':'brand',
     'title':'Spectra: Lightspeed.','eyebrow':'Ardiles Basketball / Product campaign / 2025–2026',
     'description':'A speed-led product story for Spectra, bringing together launch information, product details, and creator content.',
     'outcome':'Lightspeed is a Mindset','cover_code':'DPQqPvzCakD',
     'cover_alt':'Spectra White Blue and Black Purple basketball shoes on the green Ready Now campaign artwork',
     'details':[
         ['Project overview','The Lightspeed idea connects Spectra with quick movement and lightweight performance.'],
         ['Published work','The October 2025 release sequence includes launch copy, colorway information, product details, and creator content, followed by additional product posts in 2026.'],
         ['Content results','Seven linked posts document this product-content sequence. One creator post also features Allegro Meta.']
     ]},
    {'id':'skills_lab','audit_id':'skills','case_id':'case-hdp-ball-handling','existing_case':True,
     'title':'Hustle! Hustle! Skills Lab','update_title':'Hustle! Hustle! Skills Lab with Coach Effendy',
     'description':'Two October 2026 tutorials presented by Ardiles Basketball with Coach Effendy: low-post moves and off-ball movement. This is a separate coaching collaboration alongside the HDP series above.'},
    {'id':'ibl_playground','audit_id':'playground','case_id':'case-uss-jsd','existing_case':True,
     'title':'IBL Playground at USS 2024','update_title':'IBL Playground at USS 2024',
     'description':'The USS 2024 program brought together 3×3 games, athlete challenges, a three-point contest, and the Invade the Floor dance competition. The posts below document the event across three days.'},
]

def build(audit_root):
    scan = json.loads((audit_root/'full-profile-scan.json').read_text())
    audit = json.loads((audit_root/'portfolio-opportunities.json').read_text())
    detailed = json.loads((audit_root/'candidate-details.json').read_text())
    ibl = json.loads((audit_root/'ibl-details.json').read_text())
    basic = {p['shortCode']:p for p in scan['items']}
    detailed_map = {p['shortCode']:p for p in detailed['items']+ibl['items']}
    groups = {r['id']:r for r in audit['recommendations']}
    preview_map = {p['shortcode']:p for p in json.loads((audit_root/'basketball-posts.json').read_text())}
    thumbnails = json.loads((ROOT/'THUMBNAILS.json').read_text())
    cover_codes = {d['cover_code'] for d in DEFINITIONS if not d.get('existing_case')}
    expected = set(c for d in DEFINITIONS for c in groups[d['audit_id']]['post_codes'])
    posts = {}
    collected = '2026-11-01T09:03:47.737Z'
    snapshot = {'collected_at':collected,'display_date':'1 Nov 2026, 16:03 WIB','timezone':'Asia/Jakarta',
                'source':'apify/instagram-post-scraper','run_id':'pkZ3ShK2mtkwgDqRT','dataset_id':'1H6gNSKc2rtgDyB6r'}
    for code in sorted(expected):
        b = basic[code]
        d = detailed_map.get(code)
        available = bool(d and not d.get('error'))
        duration = d.get('videoDuration') if d else None
        if type(duration) not in (int,float) or not math.isfinite(duration) or duration<0: duration=None
        record = {
            'shortcode':code,'id':str(d.get('id',b.get('id'))) if d else b.get('id'),
            'source_url':b['url'],'owner':d.get('ownerUsername',b.get('ownerUsername')) if d else b.get('ownerUsername'),
            'published_at':b.get('timestamp'),'type':b.get('type'),'duration_seconds':duration,
            'status':'available' if available else 'unavailable',
            'metrics':{key:valid_count(d.get(field)) if available else None for key,field in {'likes':'likesCount','comments':'commentsCount','plays':'videoPlayCount','views':'videoViewCount'}.items()},
            'caption_excerpt':' '.join(b.get('caption','').split())[:160],
            'image':None,'preview_atlas':None,'selection_basis':'Explicit caption match in the 871-post public profile audit; shortcode deduplicated.',
            'data_source':{'dataset_id':'NNqwbBwVMtJVUSRkd' if code in {x['shortCode'] for x in ibl['items']} else snapshot['dataset_id']},
        }
        p = preview_map.get(code)
        if p:
            record.update(width=p['width'],height=p['height'],preview_atlas={**{k:p[k] for k in ['column','row','columns','rows','tileSize']},'sheet':'assets/campaigns/basketball-posts.webp'})
        elif code in thumbnails['posts'] and 'sheet' in thumbnails['posts'][code]:
            p = thumbnails['posts'][code]
            record.update(width=p['source_dimensions'][0],height=p['source_dimensions'][1],preview_kind='legacy',preview_atlas={k:p[k] for k in ['sheet','column','row','columns','rows','tileSize']})
        if code in cover_codes:
            assert code in preview_map
            record['image'] = f'assets/campaigns/{code}.webp'
            record['width'],record['height'] = json.loads((audit_root/'cover-dimensions.json').read_text())[code]
            record['image_sha256'] = hashlib.sha256((ROOT/record['image']).read_bytes()).hexdigest()
        posts[code] = record
    campaigns=[]
    for definition in DEFINITIONS:
        codes=sorted(groups[definition['audit_id']]['post_codes'],key=lambda c:posts[c].get('published_at') or '')
        c={**definition,'post_codes':codes,'totals':aggregate(codes,posts),'snapshot':dict(snapshot)}
        if definition['id']=='ibl_playground':
            c['snapshot']={'collected_at':ibl.get('collected_at',collected),'display_date':'1 Nov 2026','timezone':'Asia/Jakarta','source':'apify/instagram-post-scraper','run_id':'MNOgEIhcnPPMFtvzw','dataset_id':'NNqwbBwVMtJVUSRkd'}
        c['published_from']=posts[codes[0]]['published_at'];c['published_to']=posts[codes[-1]]['published_at']
        campaigns.append(c)
        if c.get('existing_case'):continue
        p=posts[c['cover_code']]
        thumbnails['projects'][c['case_id']]={'title':c['title'],'source_kind':'Reviewed public campaign post','cover':{'kind':'image','src':p['image'],'width':p['width'],'height':p['height'],'alt':c['cover_alt'],'title':c['title']}}
    data={'schema_version':1,'snapshot':snapshot,
          'discovery':{'account':'ardilesbasketball','run_id':'t1p2pJmQeLQeuNicV','dataset_id':'rAWNUlgHoMQDjCibx','unique_posts_reviewed':871,'date_range':['2022-01-01','2026-10-29'],'saved_profile_count':878,'unreconciled_posts':7},
          'methodology':{'approval':'User requested publication of the audit recommendations on 1 November 2026.',
                         'scope':'Three new cases and two additions to existing cases. Caption-matched product-content collections, including later follow-through; no inferred campaign reporting window.',
                         'attribution':'Descriptions are limited to documented campaign focus and published outputs. No new personal ownership of partnership deals, budgets, sales, attendance, or production is claimed.',
                         'preservation':'ACCOUNT_METRICS.json, INSTAGRAM_METRICS.json, INSTAGRAM_METRICS.csv, and the earlier CAMPAIGN_ARCHIVE.json remain unchanged.',
                         'metrics':'Top-level detailed counters. Negative and missing fields are null. Shared posts appear in each relevant project and must not be added across projects.',
                         'assets':'Locally stored source covers and square-cropped source previews; no generated photography. Unavailable images retain exact source links.'},
          'campaigns':campaigns,'posts':posts}
    (ROOT/'BASKETBALL_ADDITIONS.json').write_text(json.dumps(data,ensure_ascii=False,indent=2,allow_nan=False)+'\n')
    (ROOT/'THUMBNAILS.json').write_text(json.dumps(thumbnails,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'new_cases':3,'expanded_cases':2,'posts':len(posts),'previews':sum(bool(p.get('preview_atlas')) for p in posts.values()),'campaigns':[{'id':c['id'],'posts':len(c['post_codes'])} for c in campaigns]},indent=2))

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('audit_root',type=Path)
    build(parser.parse_args().audit_root)
