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

The page presents a short introduction, selected figures, the complete project catalog, work experience, personal background, and contact details. All 32 project cards appear by default. They include the six featured cases, every original project group, and two clearly labeled planning proposals. Category filters and search help visitors find specific work. Each project has an overview, individual responsibilities, documented results or published output, and related links.

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
