# DAIR smoke artifact

This folder contains a standalone browser-ready smoke artifact for the AI Starter Community course area.

What this proves:

- The local repo-scoped `dair-lesson-generator` skill was used from:
  `/opt/ai-starter-community/.agents/skills/dair-lesson-generator/SKILL.md`
- The skill was not extracted into a separate copy.
- No upstream docs were downloaded for this run.
- No separate UI/interface/tool was installed.
- Existing course files were not modified.
- The artifact is isolated to this new folder only.

Files in this folder:

- `index.html`
- `styles.css`
- `script.js`
- `README.md`

How to open:

- Open `index.html` directly in a browser.
- If you prefer a local server, serve only this folder from the repo root, but that is not required for the smoke proof.

Smoke checks performed in this run:

- Confirmed the required source inputs existed and were read.
- Confirmed the artifact is placed in an isolated allowed folder.
- Confirmed `index.html` links to `styles.css` and `script.js`.
- Confirmed `script.js` contains structured lesson data.
- Confirmed the artifact includes navigation, flashcards, quiz, and progress/review blocks.
- Confirmed the local app repo skill path was used instead of any external or upstream source.

Notes:

- This is a smoke artifact, not a production site integration.
- It does not claim published access, payment flow readiness, or runtime deployment.
- The existing course content under `source/app/materials/course_content/` was not changed.
