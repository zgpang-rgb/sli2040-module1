# iLEARN Editor — Educator Training · Module 1: Create Class

Self-paced, browser-based training for IMLS educator staff on the three
configuration decisions made when creating a class in iLEARN Editor.

## How to run it

Just open `index.html` in a browser — no build step, no server required.

```
open index.html          # macOS
xdg-open index.html      # Linux
```

Or, if you'd rather serve it locally:

```
python3 -m http.server
# then visit http://localhost:8000
```

No external network calls are made; the page is fully self-contained
(inline CSS/JS, no CDN links). Progress is saved in the browser's
`localStorage` — closing the tab and coming back later resumes where you
left off. If storage is unavailable (e.g. some locked-down browser
profiles), the module still works but progress won't persist between
sessions, and a note in the sidebar says so.

## What's in v1

Four units, self-paced and non-linear (jump to any unit from the sidebar
at any time):

1. **Orientation** — what the three Create Class decisions are and why they interact.
2. **Forum & Calendar** — the two opt-in class-space toggles, a mock settings panel, and a scenario check.
3. **Learner Discovery & Shared-Educator Data Access** — the two visibility/privacy toggles, plus a scenario with **no single right answer** (a co-teaching, minors-in-class data-access judgment call) — the feedback explicitly says so, rather than forcing a lookup-table answer.
4. **Current Owner, Second Owner & Shared Educators** — the three-tier ownership/access model, a scenario check, and a closing quick-decision drill that combines all three features in one setup.

Content is sourced from the uploaded `M1_iLEARN_Educator_SLP` pptx and
PDF, which name the three Create Class features. The PDF export
includes real console screenshots and two authoritative feature
definitions (Allow Learners to Discover Each Other; Current Owner) —
those are embedded and quoted directly in the relevant units. Any
learner/educator names visible in the original screenshots were
replaced with fictitious placeholders before embedding, since the
originals looked like real production data, not test fixtures. The
deck's own video/interaction slides don't cover Second Owner, Shared
Educators, or the Data Access definitions in full, so the clickable
mock toggle panels, those definitions, and all scenario detail remain
original teaching content — **confirm exact labels and behaviour
against the live iLEARN Editor console** before configuring a real
class.

## What's explicitly deferred

- **Full-fidelity screenshots for Second Owner, Shared Educators, and the Data Access definition** — the source PDF's interactive slides only captured their default (first) panel state, so those three definitions are still original teaching content rather than quoted source text. The Forum & Calendar and Discovery/Owner-fields figures are real screenshots; the clickable mock toggle panels remain stylised recreations for practice.
- **Modules 2–6 of iLEARN Editor** (Assign Content, Add & Manage Learners, Analytics Dashboard, Review, Gradebook & Competency Wheel) — out of scope for this module.
- **Assessment / certification** — this is a practice module with formative feedback, not a scored or certifying assessment.
- **SCORM/LMS packaging** — this runs as a standalone static page, not published into iSpring/SCORM tooling.
