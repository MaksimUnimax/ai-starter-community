# Preferred Lesson UI Blocks

Use these blocks as the default interface vocabulary for OpenScript lesson pages.

## Role cards

```md
:::role-card
User: владелец результата
ChatGPT: проектировщик и объяснитель следующего шага
Codex: исполнитель точной задачи
Git/docs: журнал и память проекта
Tests: проверка
:::
```

## Task card

```md
:::task
title: Найди поля в отчёте
input:
<sample report>
questions:
- Где RESULT?
- Где TASK_ID?
- Какие файлы изменились?
answer_ref: ../answers/01-kak-my-rabotaem.md
:::
```

## Quiz card

```md
:::quiz
question: Что показывает RESULT?
choices:
- Итог run
- Название файла
- Список рисков
correct: Итог run
feedback: RESULT показывает итог выполнения run.
button: Проверить
:::
```

## Answer reveal

```md
:::check
question: Что должно быть в готовом ответе?
answer: Конкретный worked example, объяснение, pass/fail checklist и что делать если failed.
:::
```

## Clickable checklist

```md
:::checklist
- [ ] Я нашёл RESULT
- [ ] Я нашёл TASK_ID
- [ ] Я нашёл tests
- [ ] Я нашёл commit
:::
```

## Warning or help callouts

```md
:::callout
type: warning
title: Что делать если failed
Повтори чтение отчёта и вернись к ChatGPT с конкретным полем, которое не удалось найти.
:::
```

## Report example block

```md
:::report-example
RESULT: SUCCESS
TASK_ID: example
files_changed: a.md, b.md
tests: 12 passed
commit: deadbeef
risks: none
next: lesson 2
:::
```
