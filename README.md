# Ilham Rizaldi · Portfolio

A responsive, buildless portfolio for brand strategy, go-to-market, and growth.

- `index.html`: complete website, static content, styles, and optional interaction.
- `og.png`: 1200 × 630 social preview.
- `social-card.html`: source layout used to render the social preview.
- `CONTENT_REVIEW.md`: content sources, attribution decisions, and maintenance notes.

Open `index.html` in a browser, or serve this directory with any static HTTP server. No package installation or build step is required.

## Current iteration

The visitor journey is positioning → achievements → selected work → approach → experience → personal context → contact. Six selected cases replace the previous unranked catalogue. Further work remains accessible through public references and the complete visual portfolio.

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
- Native case disclosures show the correct Read/Close state and have concise accessible names.
- JavaScript-only controls stay hidden until initialization succeeds; static content, links, and disclosures remain usable without JavaScript.
- Existing skip navigation, reduced motion, focus visibility, print styles, and no-tracking behavior are preserved.
