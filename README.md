# SLI 2040 — Self-Learning Packages for IMLS Personnel

Self-contained, browser-based training modules for IMLS staff. No backend, no build step, no external assets — each module is a single HTML file you can open directly in a browser.

## Modules in this repo

- **`index.html`** — SLI 2040 Module 1: Operating Philosophy & the Three Sections.
- **`module7.html`** — iLEARN Educator Module 7: Integrated Practical (Learner Activities 1–5).

## How to run

Open the file directly in a browser (double-click it, or `open module7.html` / `start module7.html`), or serve the folder locally, e.g.:

```
python3 -m http.server 8000
```

then visit `http://localhost:8000/module7.html`. Progress is saved to that browser's `localStorage`, keyed per module, so each module tracks progress independently and survives closing the tab.

## `module7.html` — what's in v1

An interactive walkthrough of **iLEARN Educator Module 7**, built from the source product-documentation deck (`M7_iLEARN_Educator_SLP.pptx`), a single hands-on practical class ("iLEARN Educator Learner Activity") that exercises Modules 1–6 together across five Learner Activities. Five units plus a capstone:

1. **Class & Communicator Basics** — creating a class, then opening it up with a Forum post and a Calendar event.
2. **Assigning Content** — assigning the same content package as Learning, Exam, or Questionnaire, and the four settings an Exam needs locked down before it behaves like one.
3. **Adding Learners** — individual add versus CSV upload, and the irreversible-invitation checkbox on the CSV path.
4. **Reviewing Work** — Accept for Review vs. Return for Rework as a gate before rubric grading, not a grading decision itself.
5. **Gradebook & Competency** — attaching a Competency Framework before or after enrolling learners, a genuine sequencing judgment call with two defensible answers.

Each unit pairs a short explainer with one scenario-based interactive check with branching feedback — four have a single defensible best move, one (Unit 5) is deliberately a toss-up between two reasonable sequences. Navigation is self-paced (a module map lets you jump to any unit), and progress persists in the browser via `localStorage` with a graceful in-memory fallback if storage is unavailable.

Screenshots embedded in the module are the actual iLEARN Educator UI from the source deck, resized and inlined as base64 so the file stays single-file and works offline.

## What's explicitly deferred

- Any assessment or certification of educator competency against this material.
- SharePoint / Microsoft 365 or any other external integration.
- Deeper LMS administration topics beyond the five Learner Activities covered here — bulk reporting, role/permission management, and anything not exercised by the source practical.
- A dedicated Module 1–6 build-out beyond what already exists in this repo; `module7.html` treats those as prerequisite skills, not content it re-teaches from scratch.

## A note on scope

The original brief for this module described a coaching-stance training topic (directive vs. reflective conversation stances, stance drift, referral boundaries). The attached source files — a 103-slide PPTX and the generic iSpring quiz-engine runtime it ships with — turned out to document the iLEARN Educator LMS feature set instead, with no coaching content in them at all. Per instruction to follow the source documents where they conflict with a summary, and per direction to treat this as the real Module 7 content, `module7.html` was built to match what the PPTX actually contains: a practical walkthrough of running an iLEARN Educator class end to end.
