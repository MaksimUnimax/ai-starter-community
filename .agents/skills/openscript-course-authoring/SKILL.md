---
name: openscript-course-authoring
description: Create OpenScript "Работа с ИИ" course lessons, answers, and reports in the DAIR lesson-generator style with ready answers, checkable tasks, and ChatGPT-designed prompts executed by Codex.
---

# OpenScript Course Authoring

Use this skill when writing course material for the OpenScript "Работа с ИИ" area.

## Core contract

- Use `DAIR lesson-generator` as the primary structure reference.
- Treat the course as content for non-programmers.
- ChatGPT designs the step; Codex executes the prepared prompt.
- The user runs the prompt and brings the report back to ChatGPT.
- ChatGPT explains the result and chooses the next step.

## Required lesson shape

Every real lesson must include:

- title
- audience
- goal
- simple explanation
- бытовая аналогия
- what the user sees
- step-by-step practice
- task
- ready answer
- self-check
- expected Codex report
- typical mistakes
- acceptance criteria
- next lesson bridge

## Do not do

- Do not create empty lessons.
- Do not create placeholder lessons.
- Do not leave "TODO later" as lesson content.
- Do not write long theory without practice.
- Do not ask the user to invent prompts from scratch.
- Do not ship tasks without ready answers.
- Do not ship tasks without pass/fail criteria.
- Do not change app, runtime, or DB unless a future prompt explicitly allows it.
- Do not call model/provider APIs unless a future prompt explicitly allows it.
- Do not keep accepted course source only in runtime state.

## Working pattern

1. Start from `templates/course.yaml`.
2. Draft each lesson with the reusable Russian headings from `templates/lesson.md`.
3. Put the checked answer in `templates/answer.md` format.
4. Use `templates/report.md` for the proof loop that comes back to ChatGPT.
5. Keep lessons practical, visual, step-by-step, and checkable.

## Scope reminder

- This skill is for OpenScript "Работа с ИИ" course content only.
- It is not a site change, not an auth change, and not a runtime task.
- Accepted course source will later live in the app repo as git-tracked source, not only in runtime.
