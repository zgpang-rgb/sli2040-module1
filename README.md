# sli2040-module1

Self-learning packages for IMLS personnel. Each module is a single, self-contained HTML file — no build step, no server, no external dependencies or network calls.

## How to run

Open the HTML file directly in a browser (double-click it, or `file://` path). Chrome or Edge recommended, for reliable `localStorage` progress saving. No installation required.

- **`index.html`** — SLI 2040 Module 1: Operating Philosophy & the Three Sections
- **`module3.html`** — SLI 2040 Module 3: Add & Manage Learners (iLEARN Educator)

Progress in each module is saved separately in the browser's `localStorage`, keyed per module, so completing one doesn't affect the other. Each module links to the other from its sidebar.

## What's in v1

**Module 1** teaches IMLS's operating philosophy: the three sections (Learning Science, Learning Technology, Innovation Lab), Watch Areas, the Plan → Run → Measure operating loop, the six-stage short-cycle loop, the Trial Implementation Plan, and how it all maps to the SLI 2040 institutional framing. It ends in a capstone where the learner walks one of their own live projects through the short-cycle loop and exports it as a Markdown document.

**Module 3** teaches the iLEARN Educator platform's own "Add & Manage Learners" feature: individually adding learners vs. bulk CSV upload, reading the Healthy/Inactive/Invited learner-status indicators, and the retire-vs-delete distinction for both individual learners and whole classes. Diagrams are cropped directly from the source iLEARN Educator training slide pack (`assets/`) for fidelity to the platform's own screens and language.

Both modules share the same interaction pattern: flowing explainer prose, one scenario-based check per unit with branching feedback (including, in Module 3 Unit 3, a scenario the source material itself doesn't resolve to a single right answer), a collapsible self-paced module map, and a progress bar backed by `localStorage`.

## What's explicitly deferred

- The rest of the iLEARN Educator module sequence: Module 1 (Create Class), Module 2 (Assign Content), Module 4 (Analytics Dashboard), Module 5 (Review), Module 6 (Gradebook & Competency Wheel). Only "Add & Manage Learners" is built.
- A coaching-stance / conversation-practice curriculum (directive vs. coaching vs. reflective stance, stance drift, referral boundaries) was originally scoped as "Module 3" in an early build request. No source material for that curriculum was supplied — the documents provided were LMS software documentation for iLEARN Educator's own Module 3 feature, not coaching content — so it was not built. If that curriculum is still wanted, it needs its own source material and would ship as a separate module rather than overloading this "Module 3" name.
- Full ICF competency training, mentoring-programme mechanics, and any assessment/certification layer — none of these exist in the current v1 content for either module.
- No SharePoint/M365 integration, no external API calls, no backend of any kind, in either module.
