# sli2040-module1

Self-learning packages for internal educator training. No backend, no accounts — each module is a single self-contained HTML file. Open it directly in a browser (double-click, or `file://` path) — no build step, no server.

## What's here

### `index.html` — SLI 2040 Module 1: The Operating Philosophy
Teaches the three-section operating model (Learning Science / Learning Technology / Innovation Lab), Watch Areas, the Plan → Run → Measure operating loop, the short-cycle loop, the Trial Implementation Plan, and how these map onto the SLI 2040 institutional framing. Six scenario checks plus a capstone that walks a learner's own live project through the short-cycle loop.

### `stances.html` — Module 1: Conversational Stances
Teaches which stance to take in a developmental conversation — directing (**Telling**) vs. inviting the other person to reason it through (**Asking**) — and how to hold it under pressure. Covers: the two stances and what defines them (who owns the agenda, who owns the answer, what the person needs); a diagnostic for choosing between them (competence/commitment, the type of gap, time pressure and risk, rank as a constraint); stance drift as the core applied skill (noticing the pull, naming it, recovering or switching deliberately); and the referral boundary (recognising when a conversation has moved past what either stance can address, and routing it appropriately).

Five units, self-paced, enterable in any order via the module map. Two check formats: stance-call scenarios (pick a stance, get the case *for* it, not a right/wrong verdict) and live-response drills (pick your next line from four move types — advising / leading / reflective / open — and see what each does to who owns the conversation). One unit is built deliberately with no clean answer, and says so.

**Progress:** name (optional) and unit-completion markers are stored in the browser's `localStorage` under the key `edu_stances_m1_v1`, scoped to this file, this browser, this device. Nothing is transmitted anywhere.

**Provisional content:** the stance labels ("Telling" / "Asking") and the framework text throughout `stances.html` are a working draft built for this trial, not institutional terminology — flagged in-app on every unit. They're placeholders pending an authoritative source document; swap in the real framework language when it's supplied.

## What's explicitly deferred (out of scope for this trial)

- Full competency-framework training (e.g. ICF-style competency coverage) — this module is a single applied-judgment module, not a certification course.
- Mentoring-programme mechanics (matching, cadence, programme administration).
- Assessment or certification of learners — the checks are formative (feedback-only), not graded.
- A second module, shared navigation between modules, or any cross-module state — each HTML file is independent by design.
- Any backend, account system, or external integration (no SharePoint/M365, no APIs). All state is local-browser-only.
