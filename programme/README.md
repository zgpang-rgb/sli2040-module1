# Humanising Learning Materials and Analytics — Programme Site

The catalogue and launcher for the four self-directed modules owned by IMLS
Learning Design. Static HTML/CSS/vanilla JS — no backend, no accounts, no build
step.

This folder is self-contained and independent of the iLEARN Educator package at
the repository root (`../index.html` and `../modules/`). The two share nothing:
no files, no storage keys, no links.

## Structure

```
programme/
  index.html          Catalogue — stat band, outcome search, module filter,
                      and the four module cards
  modules/
    a1.html           SLI 2040 & the Three-Section Framework
    a2.html           Training Leadership — The Five Sections
    a3.html           Research Methodologies
    a4.html           Workplace Developmental Conversations
  analytics.html      All four analytics dashboards, and what each module records
  about.html          How the programme works, collection, the registry record
  assets/
    site.css          The whole visual system (light + dark + explicit override)
    identity.js       Link decoration and launch analytics
    catalogue.js      Search / filter / expand, on index.html only
```

## Launch links

Every launch link is written into the HTML, not injected by script, so the site
works with JavaScript disabled. Two things about these URLs are easy to get
wrong and must survive any edit:

- **a1's dashboard uses `?page=dashboard`.** a2, a3 and a4 use `?view=dashboard`.
- **a4's dashboard is a separate Apps Script deployment** from a4's module. The
  other three dashboards are the module's own deployment opened on its dashboard
  view.

| Module | Module URL (`Open the module`) | Dashboard URL |
|--------|-------------------------------|---------------|
| a1 | `.../AKfycbzxVsLxauMdDgx15seb4mJnxlt-8NWvaIsJPgPFLWbvJ-ZuEnDua9Q1dKRLlH64k5vz/exec` | same base + `?page=dashboard` |
| a2 | `.../AKfycbzhk8xZhrklN-RXsjxsvxSGWxmoxmlpDKDWX6LK0G_66SNBlevBGfDi07nEeWdJZX0dLQ/exec` | same base + `?view=dashboard` |
| a3 | `.../AKfycbzjEdhhoHncx6Ed0iwSxfDKfwQxoK6qo_FXPi7jvLNIpcQkYo-FUHlSxqj4KhlJb7KPUA/exec` | same base + `?view=dashboard` |
| a4 | `.../AKfycbxL1m7NMz-jNi_GzPO1ok8aJ0ldJx6RsASF8JzP1oM38rqkJXfzetxglDpP2Ese2sDF/exec` | `.../AKfycbz7OGbHqOwBbmGPMTp0AxtDqyfSoc-JddQ4vmKhWoOEgo9Lem7HXjSaGKuMcof-qS40/exec?view=dashboard` |

All prefixed `https://script.google.com/macros/s/`. Each module URL appears twice
(catalogue card and detail page); each dashboard URL three times (card, detail
page, analytics table). After changing any of them, check the set is still
exactly eight distinct URLs:

```
grep -oh 'https://script\.google\.com[^"]*' index.html modules/*.html analytics.html | sort -u
```

## Name and cohort

The catalogue's own intake form has been removed, so nothing on this site
currently writes a name or cohort. `identity.js` still reads one from the
`imls_identity` key in the visitor's own browser if present — set some other
way, such as a future intake or an outside integration writing that key
directly — and, on every page, appends it as `imls_lid` / `imls_ln` / `imls_ch`
to the `Open the module` links only; dashboards are an educator view and stay
undecorated. The original URL is stashed in `data-href` on first pass, so
re-decorating cannot double-append.

Everything degrades: if `localStorage` is blocked or the key is absent, every
link stays exactly as written in the HTML.

`identity.js` also emits `learning_material_opened`, `module_selected` and
`link_opened` through `window.IMLS`, which exists only when the site is served
behind the IMLS collection server. On a static host those calls never fire.

This site never touches `ilearn_hub_learner` or any `ilearn_*` / `imls_*_m*_v1`
key — those belong to the unrelated package at the repository root.

## Running locally

```
cd /path/to/repo
python3 -m http.server 8000
```

then open `http://localhost:8000/programme/`. Opening `index.html` straight off
disk also works; some browsers restrict `localStorage` on `file://` pages, in
which case links stay exactly as written in the HTML.

## Deploying

Static files only — host anywhere. On GitHub Pages with the repository root as
the source, this site is served at `https://<user>.github.io/<repo>/programme/`
and the existing iLEARN hub stays at the root. Keep `index.html`, `modules/` and
`assets/` together in the same relative structure; every internal link is
relative.
