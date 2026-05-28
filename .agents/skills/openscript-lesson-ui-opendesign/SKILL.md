---
name: openscript-lesson-ui-opendesign
description: Improve OpenScript interactive lesson page UI and rendering using OpenDesign-style principles, with real browser-visible proof, quiz controls, answer reveal, and clickable checklist behavior. Use when polishing lesson layouts, fixing raw markdown artifacts, or validating interactive lesson UI without changing lesson meaning.
---

# OpenScript Lesson UI OpenDesign

Use this skill for UI and rendering polish on OpenScript lesson pages.

## Separation of responsibilities

- This skill is separate from `openscript-course-authoring`.
- `openscript-course-authoring` writes lesson content and answers.
- `openscript-lesson-ui-opendesign` improves lesson interface, rendering, and visual quality.
- Do not mix the two in one uncontrolled run.

## Local reference only

- Use the bundled local reference copy: `references/manalkaff_opendesign_SKILL.md`.
- Do not read external upstream docs as a working dependency.
- Do not rely on external URLs when a local file exists.

## Required UI outcomes

### Browser-visible quality

- No raw markdown artifacts in the browser.
- No visible `**bold**`.
- No visible unprocessed `:::check`, `:::task`, `:::quiz`, `:::checklist`.
- No raw `.md` answer links on the user-facing lesson page.

### Real interaction

- Quiz has choices.
- Quiz has a `Проверить` button.
- Quiz has a feedback area.
- Answer reveal works inline.
- Checklist is clickable, not disabled.

### OpenDesign-style structure

- Use role cards or comparison blocks.
- Make the task card visually distinct.
- Keep report examples readable.
- Keep checklist visually clear.
- Preserve strong visual hierarchy and spacing.
- Keep the layout mobile-friendly.
- Avoid text-wall presentation.

### Accessibility

- Buttons must be keyboard-usable.
- Controls must have visible labels.
- Headings hierarchy must be sensible.
- Contrast and readability must not be worsened.

### Security

- Escape raw HTML from lesson markdown.
- Do not allow unsafe script injection from lesson content.
- Do not add external scripts or packages unless a future prompt explicitly allows it.

### Proof

- Tests must inspect rendered HTML, not source markdown only.
- Prefer browser proof if a browser tool is available.
- If browser proof is unavailable, report that and provide HTML/test/manual proof.
- Screenshot proof is preferred when tooling exists, but do not install packages without approval.

## Do not do

- Do not ship fake interactive controls that do nothing.
- Do not keep `.md` answer links as the primary user-facing path.
- Do not say "looks okay" without test, browser, or HTML proof.
- Do not change course meaning while fixing UI.
- Do not install packages without explicit approval.
- Do not touch auth, DB, payment, progress, or admin work in a UI polish run.
- Do not mix this skill with course-authoring changes unless a future prompt explicitly allows it.

## Required proof loop

When using this skill, provide:

- rendered HTML proof or browser proof
- a visual QA checklist
- a browser proof report
- tests that verify the rendered output

## When to read bundled templates

- `templates/lesson_ui_blocks.md` for preferred lesson UI blocks
- `templates/visual_qa_checklist.md` for visual review
- `templates/browser_proof_report.md` for browser proof reporting
