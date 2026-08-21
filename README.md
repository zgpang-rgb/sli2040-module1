# SLI 2040 — Self-Paced Learning Modules

Self-contained, browser-based internal training for IMLS personnel. Each module is a single static HTML file — no build step, no backend, no external assets. Progress is saved per-module in the browser's `localStorage`.

## Modules in this repo

- **`index.html`** — SLI 2040 Module 1: Operating Philosophy & the Three Sections.
- **`module4.html`** — iLEARN Educator Module 4: Analytics Dashboard.

## How to run

From the repo root:

```
python3 -m http.server 8000
```

Then open `http://localhost:8000/index.html` or `http://localhost:8000/module4.html` in a browser. Opening the file directly (`file://…`) also works in most browsers, though some (older Safari/Chrome security settings) restrict `localStorage` on `file://` — the local server avoids that.

## `module4.html` — iLEARN Educator Module 4: Analytics Dashboard

### What's in v1

Built from the iLEARN Educator "Module 4: Analytics Dashboard" source deck (`M4_iLEARN_Educator_SLP.pptx`), which teaches educators how to read the iLEARN LMS Analytics Dashboard and act on it. The module mirrors the deck's own three-part structure:

- **Part 1 — Monitor completion**: module-level and learner-level assignment status.
- **Part 2 — Monitor performance, competencies & feedback**: exam performance, the metacognition (conscious/unconscious competence) wheel, class-wide competency across modules, and learner survey feedback.
- **Part 3 — Make instructional decisions**: deciding which learning objectives need intervention, and which specific quiz/exam questions need revision.

Each of the 8 units pairs a short explainer with a mock dashboard view (built from the deck's real field names, with sanitized/illustrative data — a real learner name that appeared in one of the deck's example screenshots has been genericized) and one interactive check. Checks come in two forms:

- **Read-the-dashboard checks** — interpret a mock dashboard view correctly; wrong answers get feedback explaining what they miss, not just a red X.
- **Decide-the-action checks** — pick the right next instructional move given a data snapshot.

One check (Unit 07, "Decide Problematic Learning Objectives to Intervene") is deliberately built with **two equally defensible answers** — the module tells the learner this explicitly rather than picking a winner, because the underlying dashboard genuinely can't resolve that judgment call on its own.

The module is self-paced: all 8 units are reachable from the sidebar map in any order, a suggested Part 1 → 2 → 3 path is offered but not enforced, and progress (units visited/completed, answers chosen) persists in `localStorage` so a learner can leave and resume.

Every unit, each of the three parts, and the module as a whole show an estimated time — split into time to read the explainer and time to work through the check, since those are different kinds of effort. The whole module runs about 30 minutes at a typical pace. Estimates are derived from word counts and option counts, not measured usage, so treat them as a planning guide rather than a promise.

### What's explicitly deferred

- Content from the other iLEARN Educator modules visible in the source deck's own navigation (Module 1: Create Class, Module 2: Assign Content, Module 3: Add & Manage Learners, Module 5: Review, Module 6: Gradebook & Competency Wheel) — out of scope for this module.
- Any live connection to a real iLEARN instance — all dashboard views here are static, illustrative mock-ups, not real data.
- Certification or formal assessment scoring — the checks are formative (practice with feedback), not a graded exam.
- Multi-learner/shared progress tracking or an educator-facing analytics view of *how learners used this training module* — progress lives only in each learner's own browser.
