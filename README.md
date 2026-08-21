# SLI 2040 — Self-Learning Packages for IMLS Personnel

Self-contained, browser-based training modules for IMLS staff. No backend, no build step, no external assets — each module is a single HTML file you can open directly in a browser.

## Modules in this repo

- **`index.html`** — SLI 2040 Module 1: Operating Philosophy & the Three Sections.
- **`module6.html`** — iLEARN Educator Module 6: Gradebook & Competency Wheel.

## How to run

Open the file directly in a browser (double-click it, or `open module6.html` / `start module6.html`), or serve the folder locally, e.g.:

```
python3 -m http.server 8000
```

then visit `http://localhost:8000/module6.html`. Progress is saved to that browser's `localStorage`, keyed per module, so each module tracks progress independently and survives closing the tab.

## `module6.html` — what's in v1

An interactive walkthrough of **iLEARN Educator Module 6: Gradebook & Competency Wheel**, built from the source product-documentation deck (`M6_iLEARN_Educator_SLP.pdf`) and its Pick Goal Wheel excerpt (`M6_05_Pick_Goal_Wheel.pdf`). Six units plus a capstone:

1. **Frameworks & Goals** — picking the Competency Framework a class actually needs.
2. **Visibility Options** — Hidden / Visible / Visible After, including a judgment-call scenario with two defensible answers.
3. **Manual Entry of Grades** — for competencies with no online exam, plus evidence upload and the Grades Report.
4. **Tag Competencies to Assignments** — linking an assignment's score to the right framework branch.
5. **The Competency Wheel** — reading the wheel (an illustrative SVG diagram plus real UI screenshots), including why weight ≠ performance.
6. **Capstone** — walk one of your own classes through the whole setup (framework, visibility, grading method, wheel), saved locally and exportable as a `.md` file.

Each unit pairs a short explainer with one scenario-based interactive check with branching feedback — most have a single defensible best move, one is deliberately a toss-up between two reasonable answers. Navigation is self-paced (a module map lets you jump to any unit), and progress persists in the browser via `localStorage` with a graceful in-memory fallback if storage is unavailable.

Screenshots embedded in the module are the actual iLEARN Educator UI from the source deck, resized and inlined as base64 so the file stays single-file and works offline.

## What's explicitly deferred

- **iLEARN Educator Modules 1–5** (Create Class, Assign Content, Add & Manage Learners, Analytics Dashboard, Review) — this module covers Module 6 only.
- Any assessment or certification of educator competency against this material.
- SharePoint / Microsoft 365 or any other external integration.
- Bulk/admin tooling for migrating or managing frameworks and wheels across many classes at once.

## A note on scope

An earlier brief for this repo described a different training topic (coaching stances, stance drift, referral boundaries). The attached source PDFs turned out to document the iLEARN Educator LMS feature set instead, with no coaching content in them at all. Per instruction to follow the source documents where they conflict with a summary, `module6.html` was built to match what the PDFs actually contain.
