# sli2040-module1
Self-learning packages for IMLS personnel.

## How to run

Each module is a single self-contained HTML file — no build step, no server, no external network calls. Open it directly in a browser:

- `index.html` — SLI 2040 Module 1: Operating Philosophy & the Three Sections
- `module2.html` — iLEARN Educator Module 2: Assign Content

Progress and capstone entries save to the browser's `localStorage`, scoped per file, so you can close the tab and resume later on the same machine/browser. If storage is unavailable (e.g. a locked-down browser profile), the module still works but progress won't persist between sessions — a banner in the sidebar will say so.

## What's in `module2.html` (v1)

An interactive walkthrough of the iLEARN Educator "Assign Content" screen, built from the platform's own SLP source material: Content Type & Assignment Type; Active From & Due Date; Assign To, Previous Progress & Refresh Knowledge; Ordering & deployment control (Card Order / Assign Order / Lock the Order of the Modules / ASAP, and which belong to the Educator vs. the Curator); interface controls (Hide Coach Panel, Hide Self-Assessment Tile, New Content Policy); Exam/Questionnaire settings (Objectives with Content, General/Advanced Exam Settings, Questionnaire Mode); and Practice Set's Tag Structure Name dependency. Each unit pairs a short explainer with a scenario check; one scenario (Unit 03) is a deliberate judgment call with no single correct setting.

## SCORM packaging (`module2.html` only)

`module2.html` can also run inside a SCORM 1.2-compliant LMS. The repo root includes:

- `imsmanifest.xml` — SCORM 1.2 manifest declaring `module2.html` as the single SCO.
- `lms.js` — a vendor runtime supplied by the requester for this purpose. **Provenance is unconfirmed**: it's a minified/Closure-compiled bundle with no license header; its global export names (`ISPlayer`, `ISPQuizPlayer`, `ISPScenarioPlayer`, `ISPBookPlayer`, `ISPInteractionPlayerCore`, `launchMode`) strongly suggest it's iSpring Suite/iSpring Learn's player runtime rather than a general-purpose SCORM library. It's included as-is at the requester's explicit direction. `module2.html` does not rely on this file's internal behavior — it runs its own small, self-written SCORM 1.2 wrapper alongside it (see below), so actual progress/completion reporting to the LMS is independent of what `lms.js` does internally.
- A self-contained SCORM 1.2 wrapper inside `module2.html` (search for "SCORM 1.2" in the script): it looks for a `window.API` object up the frame/opener chain, calls `LMSInitialize`/`LMSSetValue`/`LMSCommit`/`LMSFinish`, and reports `cmi.core.lesson_status` (`incomplete` → `completed`) and `cmi.core.score.raw` (percent of units complete) using the same completion state already tracked for the in-browser progress bar. Every call is wrapped so a missing `API` object — i.e. opening the file standalone with no LMS — is silently inert; nothing about the standalone experience changes.

To build the package: zip `module2.html`, `lms.js`, and `imsmanifest.xml` together (flat, no subfolder) and upload the zip to your SCORM 1.2-compliant LMS.

## What's explicitly deferred

- The rest of the iLEARN Educator suite: Module 1 (Create Class), Module 3 (Add & Manage Learners), Module 4 (Analytics Dashboard), Module 5 (Review), and Module 6 (Gradebook & Competency Wheel).
- Curator-side workflows, including how to actually build a Tag Structure or package content for bulk deployment — this module is Educator-facing only.
- Any formal assessment, certification, or completion tracking beyond the in-browser self-checks and capstone worksheet.
