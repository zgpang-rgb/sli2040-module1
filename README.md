# sli2040-module1
Self-learning packing for IMLS personnel

## Module 1 — Operating Philosophy & the Three Sections

Open `index.html` directly in a browser. No build step, no server, no
external network calls. Progress, name, and capstone entries are saved in
the browser's `localStorage`.

## Module 5 — iLEARN Editor: Review

Open `module5.html` directly in a browser (or serve the folder locally,
e.g. `python3 -m http.server` and visit `/module5.html`). Same
requirements as Module 1: no build step, no backend, no external network
calls — progress and Review Log entries persist in `localStorage` on the
learner's own machine.

**Source:** built from the `M5_iLEARN_Editor_SLP.pptx` deck for the
iLEARN Editor platform's Module 5 ("Review") feature set.

**What's in v1:**
- Access Review Activities — the assigned/completed prerequisite gate that
  determines whether a submission appears in the Review queue.
- Accept for Review vs. Return for Rework — the core verdict, including the
  rubric-required/feedback-optional split for Accept and the
  feedback-required/rubric-optional split for Return.
- Verdict drift — the applied skill of noticing rubber-stamping and
  over-returning pulls, including one scenario with no clean answer, where
  both verdicts are shown as genuinely defensible.
- A live-response drill on a single submission state with four next-move
  options.
- The referral boundary — when to stop resolving something inside
  Accept/Return and escalate instead (suspected integrity issues, platform
  faults, learner support needs).
- Institutional framing — where Review sits among the six iLEARN Editor
  modules, and the learner-facing 100%-completion behaviour.
- A self-paced Review Log capstone (four of the learner's own review
  decisions, exportable as `.md`).

**What's explicitly deferred:**
- The other five iLEARN Editor modules (Create Class, Assign Content, Add &
  Manage Learners, Analytics Dashboard, Gradebook & Competency Wheel) —
  only glancing, contextual references appear here.
- Any SharePoint/M365 integration or backend/API of any kind.
- Formal assessment or certification tracking beyond local, self-reported
  progress.
