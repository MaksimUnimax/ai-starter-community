# OpenScript Course Authoring Skill

This is a repo-scoped Codex Skill for writing course content for the OpenScript "Работа с ИИ" section.

## Use it when

- drafting a new lesson
- refining a lesson sequence
- preparing ready answers and checkable tasks
- turning a course idea into a structured course plan

## Do not use it when

- changing the live site UI
- changing auth, registration, password reset, or email verification
- changing the DB or migrations
- generating course content directly into runtime-only state
- calling model/provider APIs

## Relation to the imported tool docs

- `DAIR lesson-generator` is the primary structure reference for lesson shape and compact course flow.
- `ClassBuild` is a later option for richer batch generation and teaching packs.
- `HyperFrames` is a later reference for visual or video snippets.
- `Skill-Anything` is a later reference for source-to-study-pack workflows.
- `LiaScript` is a fallback Markdown-first interactive format.
- `Codex Skills` is the mechanism that makes this workflow reusable as a local skill.

## Workflow boundary

- This skill only creates the scaffold and contract for later course work.
- The first accepted course source will later live in `/opt/ai-starter-community` as git-tracked app source.
- This run does not create real lesson content.

## Files in this skill

- `SKILL.md`
- `templates/course.yaml`
- `templates/lesson.md`
- `templates/answer.md`
- `templates/report.md`
