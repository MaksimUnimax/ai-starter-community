# OpenScript Lesson UI OpenDesign Skill

This is a repo-scoped Codex skill for improving the UI and rendering quality of OpenScript interactive lesson pages.

## Use it when

- polishing lesson pages for readability and visual hierarchy
- removing raw markdown artifacts from rendered lesson views
- adding real quiz controls, answer reveal, and clickable checklist behavior
- validating browser-visible proof for lesson UI changes

## Do not use it when

- writing lesson content itself
- changing auth, registration, password reset, or email verification
- changing the DB, migrations, payments, progress, or admin flows
- calling model/provider APIs
- installing packages without explicit approval

## How it differs from `openscript-course-authoring`

- `openscript-course-authoring` writes the lesson content and answer content.
- `openscript-lesson-ui-opendesign` improves how those lessons render and behave in the browser.
- Use them separately unless a future prompt explicitly asks to combine them.

## Local OpenDesign reference bundled here

- `references/manalkaff_opendesign_SKILL.md`

This local copy is the reference input for future UI work. It is not an external dependency.

## Activate it later

Use this repo-scoped skill explicitly:

```text
$openscript-lesson-ui-opendesign

Read and follow:
- /opt/ai-starter-community/.agents/skills/openscript-lesson-ui-opendesign/SKILL.md

STOP_SKILL_NOT_FOUND:
If the skill file is missing, stop before making UI changes.
```

## This run

This run only creates the active skill scaffold. It does not apply the skill to Lesson 1 yet.
