# iLEARN Educator Self-Learning Package

Self-paced training for IMLS Educator staff, covering the iLEARN Educator platform
end to end across 8 modules. Fully static — no backend, no accounts, no build step.

## Structure

```
index.html              the hub / launcher — lists all 8 modules with live status
modules/
  module-0.html          Getting Started
  module-1.html          Create Class
  module-2.html          Assign Content
  module-3.html          Add & Manage Learners
  module-4.html          Analytics Dashboard
  module-5.html          Review
  module-6.html          Gradebook & Competency Wheel
  module-7.html          Integrated Practical
```

Each module is a self-contained HTML/CSS/vanilla-JS file. Modules are non-linear —
open any module directly, in any order. Each module tracks its own progress in the
browser's `localStorage`, per device, with no login or name entry required. The hub
reads those same `localStorage` keys to show a status badge (Not Started / In
Progress / Complete) on each module card, plus an overall "X of 8 complete" summary
at the top.

Every module page has a small "← Back to Hub" bar at the very top linking back to
`index.html`, added without changing any of that module's own content, styling, or
progress logic.

## Running locally

No server, database, or build step is required. Two options:

1. **Open directly**: double-click `index.html` (or open it with your browser's
   File → Open). Some browsers restrict `localStorage` for `file://` pages — if a
   module's sidebar shows a storage warning, use option 2 instead.
2. **Local static server** (recommended, avoids `file://` storage restrictions):
   ```
   cd /path/to/this/folder
   python3 -m http.server 8000
   ```
   then open `http://localhost:8000/` in your browser.

## Deploying as a single shareable link

Because this is a plain static site (one folder, no build step, no server-side
code), it can be hosted anywhere that serves static files:

- **GitHub Pages**: push this folder's contents to a repo, enable Pages on the
  branch/folder in the repo settings, and share the resulting `https://<user>.github.io/<repo>/`
  URL. `index.html` at the root is picked up automatically.
- **SharePoint / internal file share**: upload the whole folder (keeping the
  `modules/` subfolder alongside `index.html`) to a document library or site
  pages location that serves HTML directly, and share the link to `index.html`.
- **Zip and hand off**: zip the whole folder as-is; anyone can unzip it and open
  `index.html` locally, or drop it onto any static host.

In all cases, keep `index.html` and the `modules/` folder together in the same
relative structure — the hub links to modules with relative paths
(`modules/module-N.html`), and each module links back with `../index.html`.

## Progress & privacy

All progress is stored only in each staff member's own browser, on their own
device — nothing is uploaded, synced, or shared. Clearing that browser's site
data for this page resets progress for every module.
