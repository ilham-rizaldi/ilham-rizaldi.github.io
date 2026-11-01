"""Build approved Running cases from retained public-source audit exports."""
import argparse
import hashlib
import json
import math
from pathlib import Path
from update_instagram_metrics import aggregate, valid_count

ROOT=Path(__file__).resolve().parent.parent
DEFINITIONS=[
 {'id':'cleo','case_id':'case-drive-cleo','display_number':39,'category':'brand',
  'title':'Drive 2.0 × Cleo.','eyebrow':'Ardiles Running / Product collaboration / 2026',
  'description':'A product collaboration connecting a lightness-led running message with Cleo Smart Run, creator content, and an online release.',
  'outcome':'Product collaboration & event activation','cover_code':'DbIpq9nTEmg','cover_alt':'Cleo and Ardiles collaboration reveal above a city skyline',
  'details':[['Project overview','Drive 2.0 × Cleo brings together running footwear and hydration through a message of lightness, freshness, and daily movement.'],['Published work','The July–August sequence covers the collaboration reveal, product details, launch at Cleo Smart Run in Bekasi, creator stories, online availability, and reviews.'],['Content results','The counters below cover 14 explicitly named Cleo posts from 22 July to 4 August 2026. Generic adjoining teasers are excluded.']]},
 {'id':'gerbera_creators','audit_id':'gerbera_challenge','phase':'features','case_id':'case-gerbera-creators','display_number':40,'category':'brand',
  'title':'Gerbera Challenge: Creative Video.','eyebrow':'Ardiles Running / Creator program / 2025–2026',
  'description':'A series of creator videos showing Gerbera in outdoor settings, followed by the Dirty in Style open call for a second edition.',
  'outcome':'Creator content & trail-product stories','cover_code':'DSJblf9EkGz','cover_alt':'Gerbera trail footwear shown on an outdoor route in a featured creator video',
  'details':[['Project overview','The Gerbera creative-video series features different creators and outdoor perspectives, showing the product in use beyond studio photography.'],['Published work','Ten creator features ran from December 2025 to January 2026. The later Dirty in Style Vol. 2 announcement appears below as a separate phase.'],['Content results','The first set of counters covers the ten featured videos only. It is separate from the Vol. 2 recruitment posts and the earlier Gerbera Cross Jumper launch.']]},
 {'id':'running_club','case_id':'case-running-club','display_number':41,'category':'community',
  'title':'Ardiles Running Club.','eyebrow':'Ardiles Running / Community program / 2026',
  'description':'A free, all-pace running club, introduced through coach profiles, registration, training updates, and race-related stories.',
  'outcome':'Club kickoff & recurring communication','cover_code':'DZHbAk3ADBj','cover_alt':'Ardiles Running Club kickoff announcement for 6 June 2026 in Jakarta',
  'details':[['Project overview','Ardiles Running Club invites beginners and experienced runners to train at their own pace, with coaches and free public registration.'],['Kickoff','The published invitation names 6 June 2026 at Chatime–Soulfull Hub by F&B ID, Hang Tuah, Jakarta. Coach introductions include Harris, Ariefin, and Rayhan.'],['Published work','The seven linked posts document the kickoff invitation, coach introductions, registration, later training communication, and marathon-related club stories.']]},
 {'id':'recharge','case_id':'case-run-recharge','display_number':42,'category':'community',
  'title':'Run & Recharge × EJ Sport.','eyebrow':'Ardiles Running / Partner activation / 2026',
  'description':'A free 5K fun run in Surabaya, supported by nutrition, apparel, and running-community partners.',
  'outcome':'EJ Sport · Kniel · Indorunners Surabaya','cover_code':'DUXqYLzktHy','cover_alt':'Run and Recharge 5K fun run invitation for 15 February 2026 at Fork Tunjungan',
  'details':[['Project overview','Run & Recharge connects a free 5K community run with partner communication around nutrition and apparel.'],['Event','The event invitation names 15 February 2026 at Fork Tunjungan, Surabaya. The published sequence features EJ Sport, Kniel, and Indorunners Surabaya.'],['Published work','Eight linked posts cover the invitation, partner announcements, participant preparation, and event recaps.']]},
 {'id':'metora','case_id':'case-metora-hybrid','display_number':43,'category':'brand',
  'title':'Metora 3.0: Hybrid Training.','eyebrow':'Ardiles Running / Product communication / 2026',
  'description':'Product stories connecting gym sessions, interval running, and hybrid training through Metora 3.0.',
  'outcome':'Gym & running product communication','cover_code':'DU3HHTJkkeO','cover_alt':'Metora 3.0 training shoes in the launch product artwork',
  'details':[['Project overview','Metora 3.0 is presented for training that moves between the gym and running, giving the product a different use case from race-day footwear.'],['Published work','Eight linked posts cover product introduction, gym and interval stories, product details, and later hybrid-training content.'],['Content scope','The collection spans February–June 2026. Its counters describe published product content across that period.']]},
 {'id':'brand_film','case_id':'case-we-are-all-runners','display_number':44,'category':'brand',
  'title':'We Are All Runners.','eyebrow':'Ardiles Running / Brand film / 2025',
  'description':'A brand message about everyday progress: running a little farther toward personal goals, one day at a time.',
  'outcome':'Run For Your Dream','cover_code':'DKRivyoSmBn','cover_alt':'Faces from the We Are All Runners brand film',
  'details':[['Project overview','The film brings the Run For Your Dream message into everyday life through the line We Are All Runners.'],['Published idea','The caption connects running with making progress toward personal goals, rather than presenting life only as a race.'],['Published work','The original brand film was published on 30 May 2025. The public counters below belong to that one post.']]},
 {'id':'pgl','case_id':'case-pgl-running-stories','display_number':45,'category':'brand',
  'title':'Running Stories with PGL Films.','eyebrow':'Ardiles Running / Sponsored creator series / 2023',
  'description':'Running-culture comedy and everyday observations from PGL Films, Pelari Galau, and their collaborators, sponsored by Ardiles.',
  'outcome':'Creator partnership & running culture','cover_code':'CpzqyzlsKwr','cover_alt':'Hansaluft in an episode of the Ardiles-sponsored running comedy series',
  'details':[['Project overview','Four published posts use running-culture humor and familiar everyday experiences to connect with runners.'],['Creator credits','The original captions identify PGL Films as producer and Ardiles Running as sponsor. They credit Hansaluft, Pelari Galau, and Tika Tatum across story, script, talent, and video roles.'],['Published work','The collection spans March–April 2023, including two running-comedy episodes and the series holiday message. Original creator credits remain with the source posts.']]},
 {'id':'gerbera_vol2','audit_id':'gerbera_challenge','phase':'vol2','case_id':'case-gerbera-creators','existing_case':True,
  'title':'Gerbera Challenge Vol. 2','update_title':'Vol. 2: Dirty in Style',
  'description':'Two May–June 2026 announcements introduce Dirty in Style: an open creator call, 30 creator slots, Gerbera footwear for selected creators, and three best-video prizes totaling Rp9 million. These are the published program mechanics; the counters below cover these two announcement posts separately.'},
 {'id':'sense_original','case_id':'case-sense-pro-launch','existing_case':True,
  'title':'Original Sense Pro 2.0 launch','update_title':'The original 2025 launch',
  'description':'Fifteen January–February 2025 posts document the original Sense Pro 2.0 release, product construction, and early creator tests. This launch phase has its own public-post counters, separate from the 2026 After Image update above and the paid CPAS case.'},
 {'id':'runergize_events','case_id':'case-runergize','existing_case':True,
  'title':'Runergize Stay Fast activations','update_title':'Stay Fast: product-trial activations',
  'description':'Nine explicitly named Stay Fast posts document product trials and city activations alongside Runergize communication. Eight source posts already appear in the original case; the additional link below completes this selected set. These counters describe this nine-post activation collection without replacing the original snapshot.'},
 {'id':'community_archive','audit_ids':['social_run','challenges','city_urbeat'],'case_id':'case-community','existing_case':True,
  'title':'Social runs and participation challenges','update_title':'More community programs: 2023–2026',
  'description':'Additional published work includes the 2023 Ardiles Social Run series, City Run with Urbeat in 2024, and Mileage, Ramadan Active, and Run Your Limits challenges. Invitations, participation mechanics, winner announcements, and recaps remain linked here. The public-post counters cover this selected archive, separately from Short Escape above.'},
]

def build(audit_root):
    scan=json.loads((audit_root/'full-profile-scan.json').read_text())
    audit=json.loads((audit_root/'portfolio-opportunities.json').read_text())
    first=json.loads((audit_root/'detailed-post-scan.json').read_text())
    extra=json.loads((audit_root/'extra-detailed-post-scan.json').read_text())
    basic={p['shortCode']:p for p in scan['items']}
    detailed={p['shortCode']:p for p in first['items']+extra['items']}
    groups={g['id']:g for g in audit['opportunities']}
    previews={p['shortcode']:p for p in json.loads((audit_root/'running-posts.json').read_text())}
    dimensions=json.loads((audit_root/'cover-dimensions.json').read_text())
    manifest=json.loads((ROOT/'THUMBNAILS.json').read_text())
    for c in DEFINITIONS:
        codes=set(code for gid in c.get('audit_ids',[c.get('audit_id',c['id'])]) for code in groups[gid]['postCodes'])
        if c.get('phase')=='features':codes={x for x in codes if basic[x]['timestamp'][:10]<'2026-02-01'}
        if c.get('phase')=='vol2':codes={x for x in codes if basic[x]['timestamp'][:10]>='2026-05-01'}
        c['post_codes']=sorted(codes,key=lambda x:basic[x]['timestamp'])
    expected={p for c in DEFINITIONS for p in c['post_codes']}
    assert len(expected)==94 and expected<=set(detailed)
    covers={c['cover_code'] for c in DEFINITIONS if not c.get('existing_case')}
    posts={}
    first_codes={p['shortCode'] for p in first['items']}
    for code in sorted(expected):
        b,d=basic[code],detailed[code]
        available=not d.get('error')
        duration=d.get('videoDuration')
        if type(duration) not in (int,float) or not math.isfinite(duration) or duration<0:duration=None
        p={'shortcode':code,'id':str(d.get('id',b.get('id'))),'source_url':b['url'],
           'owner':d.get('ownerUsername',b.get('ownerUsername')),'published_at':b['timestamp'],'type':b['type'],
           'duration_seconds':duration,'status':'available' if available else 'unavailable',
           'metrics':{k:valid_count(d.get(v)) if available else None for k,v in {'likes':'likesCount','comments':'commentsCount','plays':'videoPlayCount','views':'videoViewCount'}.items()},
           'caption_excerpt':' '.join(b.get('caption','').split())[:160],'image':None,'preview_atlas':None,
           'selection_basis':'Explicit caption and date-window match in the retained 1,114-post Running profile audit; shortcode deduplicated.',
           'data_source':{'run_id':first['run']['runId'] if code in first_codes else extra['run']['runId'],'dataset_id':'bzMIiITVF8QQ9TqfH' if code in first_codes else 'ohdvsBYl3XvzQd15E'}}
        if code in previews:
            a=previews[code];p.update(width=a['width'],height=a['height'],preview_atlas={**{k:a[k] for k in ['column','row','columns','rows','tileSize']},'sheet':'assets/campaigns/running-posts.webp'})
        elif code in manifest['posts'] and 'sheet' in manifest['posts'][code]:
            a=manifest['posts'][code];p.update(width=a['source_dimensions'][0],height=a['source_dimensions'][1],preview_kind='legacy',preview_atlas={k:a[k] for k in ['sheet','column','row','columns','rows','tileSize']})
        if code in covers:
            p.update(image=f'assets/campaigns/{code}.webp',width=dimensions[code][0],height=dimensions[code][1])
            p['image_sha256']=hashlib.sha256((ROOT/p['image']).read_bytes()).hexdigest()
        posts[code]=p
    snapshot={'collected_at':extra['run']['finishedAt'],'display_date':'1 Nov 2026','timezone':'Asia/Jakarta','source':'apify/instagram-post-scraper','run_ids':[first['run']['runId'],extra['run']['runId']],'dataset_ids':['bzMIiITVF8QQ9TqfH','ohdvsBYl3XvzQd15E']}
    campaigns=[]
    for definition in DEFINITIONS:
        c={**definition,'snapshot':dict(snapshot),'totals':aggregate(definition['post_codes'],posts)}
        c['published_from']=posts[c['post_codes'][0]]['published_at'];c['published_to']=posts[c['post_codes'][-1]]['published_at']
        campaigns.append(c)
        if not c.get('existing_case'):
            p=posts[c['cover_code']];assert p['image']
            manifest['projects'][c['case_id']]={'title':c['title'],'source_kind':'Reviewed public campaign post','cover':{'kind':'image','src':p['image'],'width':p['width'],'height':p['height'],'alt':c['cover_alt'],'title':c['title']}}
    data={'schema_version':1,'snapshot':snapshot,'discovery':{'account':'ardilesrunning','run_id':scan['scan']['runId'],'dataset_id':'NbDDmFOdn0AAJFotC','unique_posts_retrieved':1114,'saved_profile_count':1118,'unreconciled_posts':4,'date_range':['2022-09-01','2026-10-31']},
          'methodology':{'approval':'User requested that Basketball, Running, and the worth-considering audit items go live on 1 November 2026.',
             'scope':'Seven new cards, one separate Gerbera Vol. 2 phase, and expansions to three existing cases. Supporting social runs, City Run with Urbeat, and challenges are grouped in the existing community case.',
             'metrics':'Top-level public counters from two detailed datasets collected on the same day. Missing and negative fields are null. Counts remain scoped to each named post collection. Gerbera editions remain separate.',
             'attribution':'Descriptions state documented campaign ideas and published work. No new personal ownership of sales, deals, attendance, production, or creative credits is asserted. Published partner and creator credits are preserved.',
             'preservation':'Existing account totals, project snapshots, original source associations, and earlier supplemental archives are retained.',
             'assets':'Original public source frames, locally stored as WebP covers and square-cropped previews. Full source posts remain linked. Unavailable image downloads use existing previews where available.'},
          'campaigns':campaigns,'posts':posts}
    (ROOT/'RUNNING_ADDITIONS.json').write_text(json.dumps(data,ensure_ascii=False,indent=2,allow_nan=False)+'\n')
    (ROOT/'THUMBNAILS.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'new_cases':7,'expanded_existing_cases':3,'gerbera_separate_phases':2,'posts':len(posts),'previews':sum(bool(p.get('preview_atlas')) for p in posts.values()),'campaigns':[(c['id'],len(c['post_codes'])) for c in campaigns]}))

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('audit_root',type=Path)
    build(parser.parse_args().audit_root)
