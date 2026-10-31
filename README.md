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

The work photography references stable, public media paths from Ilham's existing published Canva portfolio. These are source assets, not temporary signed thumbnail links. Images and Google Fonts need an internet connection; the font stack includes system fallbacks. No Instagram embeds, analytics trackers, or third-party scripts load on this site.

For longer-term independence, download those original images into this repository and update their `src` values. Image transfer was unavailable in the editing environment; loading the published originals was verified in the browser.

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
