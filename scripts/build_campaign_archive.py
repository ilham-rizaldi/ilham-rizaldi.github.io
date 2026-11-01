"""Build a public campaign archive from reviewed post selections and supplied snapshots."""
from datetime import datetime
import hashlib
import json
import math
from pathlib import Path
from zoneinfo import ZoneInfo
from update_instagram_metrics import aggregate, valid_count

ROOT=Path(__file__).resolve().parent.parent

DEFINITIONS=[
    {'id':'love_hustle','case_id':'case-love-hustle','existing_case':True,
     'title':'Speedy Weeedy × Kevinswork: Love & Hustle',
     'description':'The collaboration continued from the August product release into creator styling, product storytelling, and the Love & Hustle Streetball Showdown at KYZN Kuningan on 17 October 2026.',
     'cover_code':'Dbx4XKQpMcD'},
    {'id':'runergize_black','case_id':'case-runergize-black','category':'brand','display_number':33,
     'title':'Runergize Black White campaign','eyebrow':'Ardiles Running / Product campaign / 2026',
     'description':'A campaign for the Runergize Black White colorway, connecting performance storytelling, athlete content, and the August product release.',
     'outcome':'Product launch & campaign content','cover_code':'DcSXOmUTSwP',
     'cover_alt':'Runergize campaign film frame featuring an athlete and the Runergize wordmark',
     'details':[
         ['Project overview','A product campaign for the Black White edition of Runergize, using the Always Fast message across launch films, product details, athlete content, and partner communication.'],
         ['My work','Brand communication and campaign-content coordination within the Ardiles Running team.'],
         ['Published work','The public posts show teasers for the 25 August exclusive web release, product and technology content, the 31 August marketplace release, and the Runergize Showdown retailer-content competition in September.']
     ]},
    {'id':'drive_daywalker','case_id':'case-drive-daywalker','category':'brand','display_number':34,
     'title':'Drive Day Walker campaign','eyebrow':'Ardiles Running / Product campaign / 2026',
     'description':'Everyday movement, from work to an easy run, brought together in the Drive Day Walker product campaign.',
     'outcome':'Comfort to walk. Easy to run.','cover_code':'DeoNoaxvKgc',
     'cover_alt':'Drive Day Walker campaign film showing work and everyday movement in a split-screen scene',
     'details':[
         ['Project overview','A campaign presenting Drive Day Walker as a shoe for daily movement, work, casual outfits, and easy running.'],
         ['My work','Product messaging and campaign-content coordination within the Ardiles Running team.'],
         ['Published work','The October content sequence combines a product introduction, work-to-hangout styling, everyday-use stories, and creator posts around the Comfort to walk, easy to run message.']
     ]},
    {'id':'run_into_wild','case_id':'case-run-into-the-wild','category':'community','display_number':35,
     'title':'Run Into the Wild event activation','eyebrow':'Ardiles Running / Community activation / 2026',
     'description':'A team-running challenge connecting city activations with a savanna running experience in Banyuwangi.',
     'outcome':'Malang · Surabaya · Banyuwangi','cover_code':'DeW0gLHnx1a',
     'cover_alt':'Run Into the Wild participant handing a relay baton to a teammate at the Surabaya activation',
     'details':[
         ['Project overview','A community activation built around team racing and the opportunity for winning teams to join a running experience in the Banyuwangi savanna.'],
         ['My work','Event communication and campaign-content coordination within the Ardiles Running team.'],
         ['Published work','The posts document the 27 September Malang invitation, the 10 October Surabaya activation, participant stories and winner recaps, and the Banyuwangi experience shared at the end of October.']
     ]},
]


def build():
    selection=json.loads((ROOT/'campaign-source-snapshot.json').read_text())
    detail=json.loads((ROOT/'campaign-detail-snapshot.json').read_text())
    images={x['shortcode']:x for x in json.loads((ROOT/'campaign-optimized-images.json').read_text())}
    atlases=json.loads((ROOT/'campaign-atlas-map.json').read_text())
    covers={c['cover_code'] for c in DEFINITIONS if not c.get('existing_case')}
    basic={x['shortCode']:x for x in selection['items']}
    detailed={x['shortCode']:x for x in detail['items']}
    expected=set(c for codes in selection['selections'].values() for c in codes)
    assert set(detailed)==expected
    posts={}
    for code in sorted(expected):
        x=detailed[code]
        picture=images.get(code,{})
        duration=x.get('videoDuration')
        if type(duration) not in (int,float) or not math.isfinite(duration) or duration<0:duration=None
        metrics={k:valid_count(x.get(v)) for k,v in {'likes':'likesCount','comments':'commentsCount','plays':'videoPlayCount','views':'videoViewCount'}.items()}
        status='unavailable' if x.get('error') else 'available'
        if status!='available':metrics=dict.fromkeys(metrics)
        posts[code]={
            'shortcode':code,'id':str(x['id']) if x.get('id') else None,
            'source_url':f'https://www.instagram.com/p/{code}/','owner':x.get('ownerUsername'),
            'published_at':x.get('timestamp'),'type':x.get('type'),'duration_seconds':duration,
            'status':status,'metrics':metrics,
            'caption_excerpt':' '.join((x.get('caption') or basic[code].get('caption','')).split())[:140],
            'image':picture.get('image') if code in covers else None,'width':picture.get('width'),'height':picture.get('height'),
            'preview_atlas':atlases.get(code),
            'image_sha256':picture.get('image_sha256'),'source_image_sha256':picture.get('source_sha256'),
            'selection_basis':'Caption match to the named campaign, or reviewed adjoining teaser/recap in its dated campaign sequence.',
        }
    campaigns=[]
    for definition in DEFINITIONS:
        codes=sorted(selection['selections'][definition['id']],key=lambda c:posts[c].get('published_at') or '')
        record={**definition,'post_codes':codes,'totals':aggregate(codes,posts)}
        record['published_from']=min(posts[c]['published_at'] for c in codes)
        record['published_to']=max(posts[c]['published_at'] for c in codes)
        if not record.get('existing_case'):assert posts[record['cover_code']]['image']
        campaigns.append(record)
    run=detail['run'];collected=run['finishedAt']
    local=datetime.fromisoformat(collected.replace('Z','+00:00')).astimezone(ZoneInfo('Asia/Jakarta'))
    return {
        'schema_version':1,
        'snapshot':{'collected_at':collected,'display_date':f'{local.day} {local.strftime("%b %Y, %H:%M")} WIB','timezone':'Asia/Jakarta','source':'apify/instagram-post-scraper','run_id':run['runId'],'dataset_id':run['storages']['datasets']['default']['id']},
        'discovery':selection['scan'],
        'methodology':{'scope':'Reviewed posts associated with the four named campaigns on the two requested public profile feeds. Not an exhaustive hashtag or web-wide campaign census.','metrics':'Top-level counters only. Hidden/missing values are null. Plays and views remain separate. Carousel children are not extra posts.','legacy':'The previous 32-project snapshot and original reference associations are preserved. The Love & Hustle follow-through section has its own current scan, rather than rewriting the earlier case counters.','assets':'Source frames resized proportionally to at most 960 pixels and encoded as WebP for website delivery; no generated photography or fabricated reporting.','role_scope':'New role summaries use the user-requested campaign association and the established Ardiles brand/campaign coordination responsibilities; no new ownership of sales, production, budget, or attendance is inferred.'},
        'campaigns':campaigns,'posts':posts,
    }


if __name__=='__main__':
    data=build()
    (ROOT/'CAMPAIGN_ARCHIVE.json').write_text(json.dumps(data,ensure_ascii=False,indent=2,allow_nan=False)+'\n')
    manifest_path=ROOT/'THUMBNAILS.json'
    manifest=json.loads(manifest_path.read_text())
    for c in data['campaigns']:
        if c.get('existing_case'):continue
        p=data['posts'][c['cover_code']]
        manifest['posts'][c['cover_code']]={'source_url':p['source_url'],'source_dimensions':[p['width'],p['height']],'type':p['type']}
        manifest['projects'][c['case_id']]={'title':c['title'],'source_kind':'Reviewed public campaign post','cover':{'kind':'image','src':p['image'],'width':p['width'],'height':p['height'],'alt':c['cover_alt'],'title':c['title']}}
    manifest_path.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'campaigns':len(data['campaigns']),'new_projects':3,'posts':len(data['posts']),'previews':sum(bool(p['image'] or p['preview_atlas']) for p in data['posts'].values())}))
