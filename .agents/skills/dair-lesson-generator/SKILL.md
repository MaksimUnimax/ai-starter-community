# lesson-generator

Source:
- https://raw.githubusercontent.com/dair-ai/dair-academy-plugins/main/plugins/lesson-generator/skills/lesson-generator/SKILL.md

Purpose:
- create compact standalone lesson and mini-course artifacts
- keep the artifact browser-ready and self-contained

When to use:
- interactive lesson
- mini-course
- study guide
- flashcards
- quiz
- knowledge check

Core workflow:
1. define the course title and topic
2. write a short description of the course goal
3. outline 6-8 ordered lessons by default
4. give each lesson a goal, key concepts, objectives, knowledge check, flashcards, quiz, and source links
5. keep the course compact so it stays responsive

Layout pattern:
- course overview
- lesson navigation or table of contents
- active lesson reader
- objectives block
- sources block
- flashcards
- quiz or knowledge check
- final review

Output files:
- `index.html`
- `styles.css`
- `script.js`

Constraints:
- self-contained browser artifact only
- do not depend on a backend or database
- do not write outside the artifact root
- keep lesson content short and structured
- keep quizzes and flashcards small enough to study comfortably

Not for:
- app integration work
- database work
- payment/access logic
- large unstructured essay output
