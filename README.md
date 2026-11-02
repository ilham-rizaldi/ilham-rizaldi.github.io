# Ilham Rizaldi · Portfolio

A responsive, buildless portfolio for Ilham Rizaldi, Brand Strategist at Ardiles.

- `index.html`: complete website, static content, styles, and optional interaction.
- `assets/logos/`: transparent organization logos used with role labels.
- `og.png`: 1200 × 630 social preview.
- `social-card.html`: source layout used to render the social preview.
- `CONTENT_REVIEW.md`: content sources, attribution decisions, and maintenance notes.
- `PROJECT_REFERENCES.json`: exact project groupings and related links recovered from the original portfolio.

Open `index.html` in a browser, or serve this directory with any static HTTP server. No package installation or build step is required.

## Current iteration

The page presents a short introduction, selected figures, the complete project catalog, work experience, personal background, and contact details. All 45 project cards appear by default. They include the six featured cases, every original project group, and two clearly labeled planning proposals. Category filters and search help visitors find specific work. Each project has an overview, individual responsibilities, documented results or published output, and related links.

Case studies and career content are present in the HTML. JavaScript adds project filters, deep-link opening, mobile-menu dismissal, reading progress, email copy, and printing. Important content remains accessible without JavaScript.

The print control uses the browser's print dialog and a dedicated career-profile stylesheet. It does not send information to a service.

## Visual dependencies

Project photography and thumbnails are stored locally in `assets/thumbnails/`. They use original project media, without relying on expiring Instagram image addresses. Responsive CSS crops photographs and atlas cells to fill their frames without displaying the letterbox padding in the original assets. Original media files and source links are preserved. Google Fonts use an external connection; the font stack includes system fallbacks. No Instagram embeds, analytics trackers, or third-party scripts load on this site.

## Publishing

Original repository: https://github.com/ilham-rizaldi/ilham-rizaldi.github.io

Live address: https://ilham-rizaldi.github.io/

This working copy was imported from `main` at `cb67513f80f54595cf05546ecfd5f43b134e297c`. The reviewed website is published through the existing GitHub Pages source on `main`. Keep the existing canonical URL when updating it.


## Navigation and accessibility update · 1 November 2026

- Direct project links reveal the chosen case and move keyboard focus to its summary.
- Mobile Work, Career, and Contact shortcuts remain available while reading.
- Reading text is 15–16px; primary touch controls have at least 44px hit areas.
- Native case disclosures show the correct View/Hide state and have concise accessible names.
- JavaScript-only controls stay hidden until initialization succeeds; static content, links, and disclosures remain usable without JavaScript.
- Existing skip navigation, reduced motion, focus visibility, print styles, and no-tracking behavior are preserved.


## Plain-language copy update · 1 November 2026

Headings, project summaries, role descriptions, and social previews use direct professional language based on the current CV and portfolio. Generic claims and the duplicated approach section were removed. Individual work, reported results, campaign periods, and category revenue context remain separate.

## Complete project restoration · 1 November 2026

All 28 original project groups and their 494 per-project reference-link entries are restored from commit `cb67513f80f54595cf05546ecfd5f43b134e297c`. The source contains 476 unique exact URLs; links shared by projects retain their original associations. Cleanstep and Polygon Helios planning decks are also restored as concept work. The original six featured cases remain intact. All cards use the same accessible disclosures and category filters; a search field works across titles, descriptions, responsibilities, and references. No project is hidden behind a separate abbreviated reference list.

## Project thumbnails · 1 November 2026

All 32 projects have a numbered cover. Related post links include compact image previews on phone and desktop, with the complete source frame preserved. There are 490 Instagram preview entries from 459 unique public images, plus four document-reference previews. Two unavailable public post previews retain their exact links and an explicit fallback label. Images load lazily and use 48 local WebP files totaling approximately 2.45 MiB. `THUMBNAILS.json` records source associations and asset provenance. Project descriptions, categories, and all original reference associations are preserved.

## Public Instagram metrics · 1 November 2026

Project summaries, project details, and individual related posts use the same dated public-data snapshot. `INSTAGRAM_METRICS.json` contains the normalized counters, coverage, definitions, and post-to-project mapping. `INSTAGRAM_METRICS.csv` provides one row per unique Instagram post. Both remain in the repository; their download links are removed from the public presentation. The main section uses the separate account-level snapshot described below.

The snapshot collected on 1 November 2026 at 02:18 WIB covers 461 unique linked posts: 459 available and two restricted. It records 1,573,524 likes, 12,928 comments, 92,554,082 video plays, and 135,612 video views. Coverage differs by field and is displayed alongside each aggregate. Likes and comments are not total engagement; plays and views are separate counters and are never combined or labeled as reach. These are lifetime public counters across linked brand, creator, and media posts, not attributed individual results or a campaign reporting window. Existing campaign-report figures remain separate.

To refresh, export the top-level Apify post records into a JSON object with `started_at`, `finished_at`, `actor`, and `items`, then run `python3 scripts/update_instagram_metrics.py /path/to/snapshot.json`. The script validates original project links, normalizes hidden/missing values, deduplicates by shortcode, rebuilds JSON/CSV, and renders the static page. It does not fetch credentials, schedule runs, or place API keys in the browser. `--data-only` updates exports without rendering. Keep any raw input export outside the published repository. `scripts/validate_instagram_metrics.py` checks source preservation and metric invariants.

## Account totals and compact presentation · 1 November 2026

The main section uses `ACCOUNT_METRICS.json`, covering Instagram @ardilesbasketball, @ardilesrunning, and @dblacademy; TikTok @ardilesperformance; and YouTube channel `UCRIhtf9Q5K-jK2UyqYpmSPA` (@ardilesofficial). The snapshot records 220,070 followers/subscribers summed across profiles, 6,294 profile-counted posts/videos, 187,000 TikTok account likes, and 13,958,907 YouTube channel views. Audience counts can overlap and public counters may be rounded. These current account totals include activity outside Ilham's role and are not personally attributed results.

Instagram lifetime likes, comments, views, reach, and impressions are unavailable in public profile metadata; these are excluded rather than extrapolated from recent posts. TikTok likes and YouTube views come from profile/channel totals, not the single videos retrieved to access that metadata. Exact source fields, collection times, runs, and dataset IDs are in the account JSON. Account data and linked-project data are independent snapshots.

The overview uses four compact 23–25px counters, reduced section spacing, and an expandable account/source table. `scripts/render_account_metrics.py` validates and renders the account totals; the Instagram renderer preserves them when refreshing project metrics.

All 32 project disclosures have a bottom Hide details button. Closing restores focus to the project summary and scrolls it into view, respecting reduced-motion preferences. Buttons are hidden until JavaScript initializes. `scripts/apply_portfolio_usability.py` keeps this behavior and responsive thumbnail crops idempotent across re-renders. Photo/atlas crops use the recorded source dimensions and container-relative CSS units; brand/logo layouts retain their original treatment.

## Introduction and community-growth copy · 1 November 2026

The introduction combines the user-supplied 5+ years summary with Ardiles role progression, supervision of a three-person team, campaign/partner work, performance analysis, and Nuansa Studio's commercial responsibilities. Current Ardiles scope is Running, Basketball, Futsal, and Soccer, as explicitly supplied by the user.

The overview uses “Explore the communities behind the work” and “A closer look at each account”. Requested explanatory paragraphs and source/download links are removed from the visible page; provenance remains in JSON and this review record. A three-column table presents account, community, and content without unavailable-total placeholders. Project links now say “Explore the accounts” rather than referring to a removed counting-method explanation.

Two compact growth highlights use the CV reread for this revision: 3–5× community growth jointly across Ardiles Running and Basketball during the 2023–2025 social media role, and +50% community growth within six months for DBL Academy. These are CV-reported community results, not new follower calculations from current profile totals. The source does not split the Ardiles range by account. `ACCOUNT_METRICS.json` records the exact source statements and their scope. Existing account counters and project/post metrics remain unchanged.


## Retail-footprint attribution correction · 1 November 2026

The user clarified that the 150+ national retail touchpoints belong to the sales team and must not be presented as his personal achievement. The figure is removed from the achievements strip, Ardiles project preview, and Ardiles work-scope text. The achievements strip instead shows the documented 13× return on ad spend for the three-day Sense Pro 2.0 CPAS campaign (visual portfolio p. 18). The Ardiles preview retains the supported three-person team and 30+ product launches. This correction supersedes earlier references to retail touchpoints in this record. Other public post counts, project references, and role details are preserved.


## User-supplied account starting points · 1 November 2026

The user supplied account-specific baselines: Ardiles Basketball 8,000; Ardiles Running 4,000; DBL Academy 28,000 to a specified 50,000 milestone; TikTok Ardiles Performance zero; YouTube Ardiles Official zero. These replace the earlier joint CV growth highlights in the account overview. Other endpoints use the existing public snapshot: 41,590, 73,491, 8,358, and 33,100 respectively. Growth is (end − start) / start, shown rounded to a whole percentage: +420%, +1,737%, and +79%. Accounts starting at zero show net followers/subscribers gained, with percentage left null. No baseline dates or growth time window were supplied. DBL's 50,000 milestone is labeled separately from its current public count of 63,531. The compact account table combines current followers, growth journey, and content counts; source details remain in ACCOUNT_METRICS.json.


## Current role and recent campaign archive · 1 November 2026

The current-role signature reads Ardiles Performance · Running, Basketball, Futsal, and Soccer. The role title is Lead Brand Strategist · Sports Marketing & Marcomm. Cyclist and Runner are removed from the professional descriptor. These changes follow the user’s explicit wording; unrelated project history is preserved.

Four requested campaign groups were matched against recent public profile-feed posts: Love & Hustle (38 posts), Runergize Black White (24), Drive Day Walker (8), and Run Into the Wild (9). The Love & Hustle case is expanded with a follow-through section; three new campaign cards bring the catalog to 35. The archive contains 79 unique source posts and 77 source-image previews. The existing 32-project snapshot, original 494 link associations, and its CSV remain unchanged. New counters use a separate dated snapshot in CAMPAIGN_ARCHIVE.json.

Campaign discovery uses the first 300 reviewed feed records, which extend before the August–October campaign windows for both requested accounts. Caption matches and reviewed adjoining teasers/recaps determine inclusion; this is not a web-wide or hashtag-wide census. Source media is compressed proportionally for covers and arranged in three thumbnail atlases for efficient delivery. Two unavailable image downloads retain source links and post counters. No attendance, new sales result, reach, attribution percentage, or ownership of sales-team work is inferred.

scripts/build_campaign_archive.py builds the normalized archive from the reviewed local selections, detailed snapshot, and media manifest. scripts/render_campaigns.py renders the supplemental case section and three cards. The existing renderer calls it when CAMPAIGN_ARCHIVE.json exists; legacy extraction deliberately excludes the supplemental cards, preserving the original snapshot’s scope. Raw discovery exports and temporary media URLs are not published.


## Growth cross-check and four-column account table · 1 November 2026

The user reconfirmed the starting counts and requested Account / Community / Content / Growth by numbers and percentage. The current overview now shows exact net additions and percentages rounded to one decimal: Basketball +33,590 (+419.9%), Running +69,491 (+1,737.3%), and DBL Academy +22,000 (+78.6%) to the user-supplied 50,000 milestone. TikTok +8,358 and YouTube +33,100 are gains from zero; percentage remains null and the visible label says From zero. The earlier joint 3–5× claim and DBL +50% summary are removed from current rendered experience copy. No start date or six-month window is inferred for these revised baselines. DBL's current public count remains separate from the specified 50,000 growth milestone. On phones the four columns stack into labeled account rows. This correction supersedes earlier overview-growth presentation notes in this document.


## Approved Basketball portfolio additions · 1 November 2026

Following the user-approved profile audit, the catalog now includes Allegro Meta: All Game. All Day (23 caption-matched posts), Ardiles Community League × Headshoes (5), and Spectra: Lightspeed (7). IBL Playground at USS 2024 expands the existing USS case (9 matched posts), while two Hustle! Hustle! Skills Lab tutorials with Coach Effendy appear within the Speedy Weeedy × Kevinswork: Love & Hustle case, as clarified by the user. The catalog contains 38 cards, all with bottom Hide details controls. Existing descriptions, responsibilities, figures, source associations, and previous supplemental campaigns are retained.

BASKETBALL_ADDITIONS.json independently records 45 unique posts, detailed counters, scope, source datasets, and the three new covers. One creator post belongs to both Allegro Meta and Spectra. The public profile audit retrieved 871 unique posts from January 2022–October 2026 against the saved profile counter of 878; the seven-post difference remains unexplained. The 2022 archive is not attributed to Ilham.

The Allegro figures cover July–December 2025 product content, including later creator tutorials, rather than a July launch reporting window. Headshoes includes preparation and event follow-through; Spectra includes October 2025 launch content and later 2026 posts. No new individual ownership of deals, event budgets, production, attendance, sales, or unique audience is inferred. The established account totals, original Instagram snapshot and CSV, and earlier CAMPAIGN_ARCHIVE.json remain unchanged.

Three local source covers and one square-cropped preview atlas add approximately 391 KiB. New and reused source atlases provide 34 previews for the 45 posts. The eleven unavailable image fetches retain exact post links and verified counters. The renderer supports per-campaign snapshot dates and distinct subsection titles. scripts/build_basketball_additions.py can rebuild the addition from the retained audit exports; no scraping credentials or expiring media URLs are published.


## Running audit additions and supporting work · 1 November 2026

The user requested publication of both profile audits, including the worth-considering items. Seven new Running cards cover Drive 2.0 × Cleo (14 posts), Gerbera creator features (10), Ardiles Running Club (7), Run & Recharge × EJ Sport (8), Metora 3.0 (8), We Are All Runners (1), and the Ardiles-sponsored PGL Films running series (4). The catalog now contains 45 project cards with source covers, reference links, public-post metrics, and bottom Hide details controls.

Gerbera Vol. 2: Dirty in Style is a separate two-announcement phase within the creator-program case; its published selection slots, footwear seeding, and announced prizes are not presented as completed campaign outcomes. The original 2025 Sense Pro launch adds 15 posts to the existing case. Runergize adds a nine-post activation set, with eight links already in the original case. The Short Escape community case gains a 17-post supporting archive covering Social Run 2023, City Run with Urbeat 2024, Mileage, Ramadan Active, and Run Your Limits challenges. The 2023 archive retains published creator and sponsor credits without asserting new personal production or authorship.

RUNNING_ADDITIONS.json records 94 unique posts from the 1,114-post public Running profile scan. Detailed counters come from datasets bzMIiITVF8QQ9TqfH and ohdvsBYl3XvzQd15E, collected on 1 November 2026. Each named cohort deduplicates shortcodes, excludes missing and negative counters, and keeps video plays separate from views. The original account totals, legacy Instagram JSON and CSV, CAMPAIGN_ARCHIVE.json, BASKETBALL_ADDITIONS.json, original project descriptions, and 494 original reference associations are preserved.

Seven proportional source covers and an 82-cell square preview atlas add about 862 KiB; two existing previews provide 84 previews across the 94 selected posts. Ten image downloads remain unavailable and retain their source links and counters. No expiring media URLs, credentials, invented sales impact, attendance, or individual ownership are published. scripts/build_running_additions.py rebuilds the source from the retained audit exports, and the combined renderer remains idempotent.


## Skills Lab campaign association · 1 November 2026

The user confirmed that Hustle! Hustle! Skills Lab belongs to Speedy Weeedy × Kevinswork: Love & Hustle. The two existing tutorials, Dd_r53_zSoR (6 low-post moves) and DeHGWADp9X8 (5 off-ball moves), are moved from the HDP coaching case into a dedicated Love & Hustle subsection. It credits Coach @Effendy.fnd and presenter @ardilesbasketball with the supplied profile links. The Love & Hustle program overview includes the coaching series alongside Streetball Showdown. The two-post dated snapshot remains separately scoped; no existing post counters or campaign aggregates are recalculated. BASKETBALL_ADDITIONS.json and its builder retain the corrected parent association and named post labels so future additions can extend the same series. The renderer supports unique subsection IDs and explicit linked credits. Other HDP material, all five programs, all 45 project cases, source links, and the existing Love & Hustle event highlights remain available.


## Strategy, research and marketing operations

Three case studies describe responsibilities in consumer insight, product messaging, launch communication, and marketing operations. They contain professional summaries only.

Internal research findings, source-record counts, budget details, spreadsheets, report downloads, and working-document links are excluded from both the page and STRATEGY_WORK.json. The strategy renderer requires the public-summary schema and rejects document links and proof-data payloads. Existing published campaign assets and project references remain available.
