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

Content is sourced from the uploaded `M1_iLEARN_Editor_SLP.pptx` deck,
which names the three Create Class features but has no screenshots or
step-level detail (its own video/interaction slides are empty
placeholders). The mock settings panels, exact wording, and all scenario
detail in this module are original teaching content written to explain
the named features correctly — **confirm exact labels and behaviour
against the live iLEARN Editor console** before configuring a real
class.

## What's explicitly deferred

- **Real screenshots or a screen recording of the live iLEARN Editor console** — the mock UI panels here are stylised, not pixel-accurate, because none were available in the source material. If screenshots/video become available, the mock panels should be swapped for the real thing.
- **Modules 2–6 of iLEARN Editor** (Assign Content, Add & Manage Learners, Analytics Dashboard, Review, Gradebook & Competency Wheel) — out of scope for this module.
- **Assessment / certification** — this is a practice module with formative feedback, not a scored or certifying assessment.
- **SCORM/LMS packaging** — this runs as a standalone static page, not published into iSpring/SCORM tooling.
