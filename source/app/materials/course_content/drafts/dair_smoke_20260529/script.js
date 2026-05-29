const courseData = {
  title: "Работа с ИИ",
  subtitle: "Тестовая версия первого урока",
  sections: [
    {
      id: "overview",
      navLabel: "Обзор",
      navMeta: "Что будет в уроке",
      eyebrow: "Обзор урока",
      title: "Что ты получишь в этой версии",
      description:
        "Это тестовая версия первого урока курса. Она помогает понять роли ChatGPT, Codex и пользователя, а также увидеть навигацию, карточки и проверку знаний прямо в приложении.",
      objectives: [
        "Понять роли ChatGPT, Codex и пользователя.",
        "Увидеть структуру урока и блоки самопроверки.",
        "Понять, как отслеживать прогресс в уроке."
      ],
      keyConcepts: [
        "Роли: проектировщик, исполнитель, проверяющий",
        "Навигация по уроку",
        "Доказательства и самопроверка"
      ],
      practicalTask:
        "Открой урок 1, прочитай объяснение ролей и найди, где в примере видно результат, задачу и следующий шаг.",
      expectedAnswer:
        "Пользователь должен понять, как читать урок и быстро находить в нём важные доказательства и следующий шаг.",
      flashcards: [
        {
          front: "Почему урок маленький?",
          back: "Чтобы его было легко пройти и проверить без лишней сложности."
        },
        {
          front: "Что здесь является основой?",
          back: "Роли ChatGPT, Codex и пользователя, а также понятная проверка результата."
        }
      ],
      quiz: {
        prompt: "Что лучше всего описывает цель урока?",
        options: [
          "Подготовить большой релиз и закрыть весь курс сразу.",
          "Понять роли, навигацию и самопроверку в первом уроке.",
          "Заменить содержимое курса внешними ссылками."
        ],
        answerIndex: 1,
        explanation:
          "Первый урок нужен, чтобы спокойно разобраться в ролях, навигации и проверке результата."
      },
      reviewNotes: [
        "Сначала смотри цель урока, затем его практическую часть.",
        "Проверяй результат по фактам, а не по впечатлению.",
        "Если что-то непонятно, возвращайся к навигации."
      ]
    },
    {
      id: "lesson-1",
      navLabel: "Урок 1",
      navMeta: "Как мы работаем",
      eyebrow: "Урок 1",
      title: "Как мы работаем: ChatGPT проектирует, Codex выполняет, пользователь проверяет",
      description:
        "В этом уроке мы двигаемся маленькими безопасными шагами. ChatGPT объясняет, что нужно сделать, Codex выполняет узкую задачу в репозитории, а пользователь проверяет результат и приносит отчёт обратно.",
      objectives: [
        "Понять роли ChatGPT, Codex и пользователя.",
        "Увидеть, зачем нужен отчёт с полями и доказательствами.",
        "Понять, почему git, docs и tests важнее устных обещаний."
      ],
      keyConcepts: [
        "Роли: проектировщик, исполнитель, проверяющий",
        "Журнал изменений: git и docs",
        "Доказательства: tests, commit, files_changed"
      ],
      practicalTask:
        "Найди в рабочем примере отчёта каждое поле и назови, что оно доказывает. Если поля нет, run не считается достаточным для перехода дальше.",
      expectedAnswer:
        "Нужно быстро распознать RESULT, TASK_ID, files_changed, tests, commit, risks и next step, а потом понять, почему они нужны.",
      flashcards: [
        {
          front: "Кто проектирует шаг?",
          back: "ChatGPT: он объясняет, зачем нужен шаг и что именно должно измениться."
        },
        {
          front: "Кто выполняет узкую задачу?",
          back: "Codex: он меняет файлы в репозитории и показывает результат."
        },
        {
          front: "Кто проверяет доказательства?",
          back: "Пользователь: он смотрит отчёт, файлы, тесты и решает, что делать дальше."
        }
      ],
      quiz: {
        prompt: "Какой блок отчёта лучше всего показывает, что реально изменилось?",
        options: ["files_changed", "app_name", "hero_actions"],
        answerIndex: 0,
        explanation:
          "files_changed показывает конкретные файлы и помогает отличить реальный результат от словесного описания."
      },
      reviewNotes: [
        "Сначала ищем статус, потом файлы, потом тесты, потом commit.",
        "Если run не объясняется через доказательства, он ещё не закрыт.",
        "Не перепрыгивать через проверку."
      ]
    },
    {
      id: "review",
      navLabel: "Проверка",
      navMeta: "Самопроверка и следующий шаг",
      eyebrow: "Проверка",
      title: "Финальная проверка: что пользователь должен вынести из урока",
      description:
        "Этот блок помогает убедиться, что урок понят, навигация работает, карточки открываются, а следующий шаг можно определить по доказательствам, а не по интуиции.",
      objectives: [
        "Проверить, что урок открывается как обычная тестовая страница.",
        "Понять, что нужно для безопасного следующего шага.",
        "Отметить, что урок не обещает полный финальный курс."
      ],
      keyConcepts: [
        "Тестовая версия",
        "Навигация и проверка",
        "Следующий шаг",
        "Ограниченный scope"
      ],
      practicalTask:
        "Поставь галочки в списке проверки и убедись, что все элементы урока совпадают с ожиданиями.",
      expectedAnswer:
        "Пользователь подтверждает, что урок открыт в приложении, навигация работает, карточки переворачиваются, quiz даёт обратную связь, а прогресс обновляется.",
      flashcards: [
        {
          front: "Что означает тестовая версия?",
          back: "Файлы лежат в отдельной проверочной странице, а курс ещё не объявлен финальным."
        },
        {
          front: "Почему важно смотреть на доказательства?",
          back: "Потому что именно они показывают, что урок действительно работает."
        }
      ],
      quiz: {
        prompt: "Что должно быть правдой после прохождения урока?",
        options: [
          "Навигация, карточки и проверка знаний работают.",
          "Страница стала полноценным финальным курсом.",
          "Технические детали полностью исчезли из кода."
        ],
        answerIndex: 0,
        explanation:
          "Для тестовой версии важно, чтобы урок работал как урок, а не как обещание финального курса."
      },
      reviewQuiz: [
        {
          prompt: "Какой следующий шаг правильный, если урок понят, но нужен полноценный курс?",
          options: [
            "Оставить эту страницу как тестовую версию и отдельно готовить основной курс.",
            "Считать страницу финальным курсом и закрыть задачу.",
            "Убрать навигацию и оставить только заголовок."
          ],
          answerIndex: 0,
          explanation:
            "Тестовая версия помогает проверить урок, но не заменяет отдельную работу над полным курсом."
        },
        {
          prompt: "Что в этой версии доказывает, что страница действительно работает?",
          options: [
            "Структурированные данные урока и живая навигация.",
            "Наличие любого открытого таба в браузере.",
            "Короткое описание без интерактивных блоков."
          ],
          answerIndex: 0,
          explanation:
            "Проверяемые данные урока и интерактивные блоки делают страницу понятной и проверяемой."
        }
      ],
      reviewNotes: [
        "Курс не объявляется финальным и опубликованным.",
        "Доступы и платные сценарии не затрагиваются.",
        "Следующий шаг — только после доказательств."
      ]
    }
  ],
  reviewChecklist: [
    "Я понял роли ChatGPT, Codex и пользователя.",
    "Я нашёл практическое задание и ожидаемый ответ.",
    "Я проверил карточки и мини-викторину.",
    "Я понял, как отслеживать прогресс в уроке."
  ]
};

const state = {
  activeSectionId: "overview",
  visitedSections: new Set(["overview"]),
  flippedCards: new Set(),
  solvedQuestions: new Set(),
  answeredQuestions: {},
  checklist: new Set()
};

const navRoot = document.getElementById("lesson-nav");
const activeSectionRoot = document.getElementById("active-section");
const progressFill = document.getElementById("progress-fill");
const progressValue = document.getElementById("progress-value");
const progressLabel = document.getElementById("progress-label");
const checkpointList = document.getElementById("checkpoint-list");
const startLearningButton = document.getElementById("start-learning");
const openReviewButton = document.getElementById("open-review");

function escapeHTML(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll("\"", "&quot;");
}

function renderNavigation() {
  navRoot.innerHTML = courseData.sections
    .map((section) => {
      const activeClass = section.id === state.activeSectionId ? "is-active" : "";
      return `
        <button class="nav-button ${activeClass}" type="button" data-section="${section.id}">
          <span class="nav-title">${escapeHTML(section.navLabel)}</span>
          <span class="nav-meta">${escapeHTML(section.navMeta)}</span>
        </button>
      `;
    })
    .join("");
}

function flashcardKey(sectionId, index) {
  return `${sectionId}:${index}`;
}

function quizKey(sectionId, index) {
  return `${sectionId}:${index}`;
}

function renderFlashcards(section) {
  if (!section.flashcards || section.flashcards.length === 0) {
    return "";
  }

  return `
    <div class="module-grid">
      <div class="section-kicker">Карточки</div>
      <div class="flashcard-grid">
        ${section.flashcards
          .map((card, index) => {
            const key = flashcardKey(section.id, index);
            const flipped = state.flippedCards.has(key) ? "is-flipped" : "";
            return `
              <button class="flashcard ${flipped}" type="button" data-flashcard="${key}" aria-label="Перевернуть карточку">
                <span class="flashcard-inner">
                  <span class="flashcard-face flashcard-front">
                    <strong>${escapeHTML(card.front)}</strong>
                    <span>Нажми, чтобы увидеть ответ</span>
                  </span>
                  <span class="flashcard-face flashcard-back">
                    <strong>${escapeHTML(card.back)}</strong>
                    <span class="flashcard-note">Карточка перевёрнута в тестовой версии урока.</span>
                  </span>
                </span>
              </button>
            `;
          })
          .join("")}
      </div>
    </div>
  `;
}

function renderQuiz(section, quizList = [section.quiz].filter(Boolean)) {
  if (quizList.length === 0) {
    return "";
  }

  return `
    <div class="module-grid">
      <div class="section-kicker">Проверка знаний</div>
      <div class="quiz-list">
        ${quizList
          .map((quiz, quizIndex) => {
            const questionKey = quizKey(section.id, quizIndex);
            const selectedIndex =
              state.answeredQuestions[questionKey] === undefined
                ? null
                : state.answeredQuestions[questionKey];
            const answered = selectedIndex !== null;
            const selectedCorrect = answered && selectedIndex === quiz.answerIndex;
            return `
              <div class="quiz-card" data-quiz-card="${questionKey}">
                <strong>${escapeHTML(quiz.prompt)}</strong>
                <div class="quiz-options">
                  ${quiz.options
                    .map((option, optionIndex) => {
                      const isCorrect = answered && optionIndex === quiz.answerIndex;
                      const isWrong = answered && selectedIndex === optionIndex && selectedIndex !== quiz.answerIndex;
                      const classes = ["quiz-option"];
                      if (isCorrect) classes.push("is-correct");
                      if (isWrong) classes.push("is-wrong");
                      return `
                        <button
                          class="${classes.join(" ")}"
                          type="button"
                          data-quiz="${questionKey}"
                          data-option="${optionIndex}"
                          ${answered ? "disabled" : ""}
                        >
                          ${escapeHTML(option)}
                        </button>
                      `;
                    })
                    .join("")}
                </div>
                <div class="feedback" id="feedback-${questionKey}">
                  ${
                    answered
                      ? selectedCorrect
                        ? `<strong>Верно.</strong> ${escapeHTML(quiz.explanation)}`
                        : `<strong>Почти.</strong> ${escapeHTML(quiz.explanation)}`
                      : "Выбери ответ, чтобы получить мгновенную обратную связь."
                  }
                </div>
              </div>
            `;
          })
          .join("")}
      </div>
    </div>
  `;
}

function renderReviewChecklist() {
  return `
    <div class="module-grid">
      <div class="section-kicker">Прогресс / проверка</div>
      <div class="review-box">
        <strong>Проверка готовности урока</strong>
        <div class="review-grid">
          ${courseData.reviewChecklist
            .map((item, index) => {
              const key = `review-${index}`;
              const checked = state.checklist.has(key) ? "checked" : "";
              return `
                <label class="review-item">
                  <input type="checkbox" data-checkpoint="${key}" ${checked}>
                  <span>${escapeHTML(item)}</span>
                </label>
              `;
            })
            .join("")}
        </div>
        <div class="review-status" id="review-status"></div>
      </div>
    </div>
  `;
}

function renderSectionContent(section) {
  const flashcards = renderFlashcards(section);
  const quiz = renderQuiz(section, section.reviewQuiz ? [section.quiz, ...section.reviewQuiz] : [section.quiz]);
  const review = section.id === "review" ? renderReviewChecklist() : "";

  return `
    <article class="section-card">
      <header class="section-header">
        <p class="eyebrow">${escapeHTML(section.eyebrow)}</p>
        <h3>${escapeHTML(section.title)}</h3>
        <p class="muted">${escapeHTML(section.description)}</p>
      </header>

      <div class="section-body">
        <section class="info-grid">
          <div>
            <span class="block-label">Цели урока</span>
            <ul>
              ${section.objectives.map((item) => `<li>${escapeHTML(item)}</li>`).join("")}
            </ul>
          </div>
          <div>
            <span class="block-label">Ключевые понятия</span>
            <ul>
              ${section.keyConcepts.map((item) => `<li>${escapeHTML(item)}</li>`).join("")}
            </ul>
          </div>
        </section>

        <section class="callout">
          <span class="block-label">Практическое задание</span>
          <p>${escapeHTML(section.practicalTask)}</p>
        </section>

        <section class="callout">
          <span class="block-label">Ожидаемый ответ / самопроверка</span>
          <p>${escapeHTML(section.expectedAnswer)}</p>
        </section>

        ${flashcards}
        ${quiz}

        <section class="callout">
          <span class="block-label">Заметки для повторения</span>
          <ul>
            ${section.reviewNotes.map((item) => `<li>${escapeHTML(item)}</li>`).join("")}
          </ul>
        </section>

        ${review}
      </div>
    </article>
  `;
}

function updateProgress() {
  const totalSections = courseData.sections.length;
  const totalQuestions = courseData.sections.reduce((sum, section) => {
    const standardQuiz = section.quiz ? 1 : 0;
    const reviewQuiz = section.reviewQuiz ? section.reviewQuiz.length : 0;
    return sum + standardQuiz + reviewQuiz;
  }, 0);
  const totalChecklist = courseData.reviewChecklist.length;
  const visitedScore = (state.visitedSections.size / totalSections) * 50;
  const quizScore = totalQuestions === 0 ? 0 : (state.solvedQuestions.size / totalQuestions) * 30;
  const reviewScore = totalChecklist === 0 ? 0 : (state.checklist.size / totalChecklist) * 20;
  const progress = Math.min(100, Math.round(visitedScore + quizScore + reviewScore));

  progressFill.style.width = `${progress}%`;
  progressValue.textContent = `${progress}%`;

  if (progress < 35) {
    progressLabel.textContent = "Пока открыт обзор и базовая структура.";
  } else if (progress < 70) {
    progressLabel.textContent = "Урок открыт, но ещё не все проверки пройдены.";
  } else if (progress < 100) {
    progressLabel.textContent = "Осталось завершить проверку.";
  } else {
    progressLabel.textContent = "Проверка завершена.";
  }

  checkpointList.innerHTML = courseData.reviewChecklist
    .map((item, index) => {
      const key = `review-${index}`;
      const checked = state.checklist.has(key);
      return `
        <li>
          <input type="checkbox" data-checkpoint="${key}" ${checked ? "checked" : ""}>
          <span>${escapeHTML(item)}</span>
        </li>
      `;
    })
    .join("");

  const reviewStatus = document.getElementById("review-status");
  if (reviewStatus) {
    reviewStatus.textContent = `${state.checklist.size} из ${totalChecklist} пунктов проверки отмечено.`;
  }
}

function renderActiveSection() {
  const section = courseData.sections.find((item) => item.id === state.activeSectionId) || courseData.sections[0];
  activeSectionRoot.innerHTML = renderSectionContent(section);
  renderNavigation();
  updateProgress();
}

function setActiveSection(sectionId) {
  state.activeSectionId = sectionId;
  state.visitedSections.add(sectionId);
  renderActiveSection();
}

document.addEventListener("click", (event) => {
  const navButton = event.target.closest("[data-section]");
  if (navButton) {
    setActiveSection(navButton.dataset.section);
    return;
  }

  const flashcard = event.target.closest("[data-flashcard]");
  if (flashcard) {
    state.flippedCards.has(flashcard.dataset.flashcard)
      ? state.flippedCards.delete(flashcard.dataset.flashcard)
      : state.flippedCards.add(flashcard.dataset.flashcard);
    renderActiveSection();
    return;
  }

  const quizButton = event.target.closest("[data-quiz]");
  if (quizButton) {
    const questionKey = quizButton.dataset.quiz;
    const [sectionId, quizIndexText] = questionKey.split(":");
    const quizIndex = Number(quizIndexText);
    const section = courseData.sections.find((item) => item.id === sectionId);
    const quiz = section.reviewQuiz ? [section.quiz, ...section.reviewQuiz][quizIndex] : section.quiz;
    const selectedIndex = Number(quizButton.dataset.option);
    state.answeredQuestions[questionKey] = selectedIndex;
    if (selectedIndex === quiz.answerIndex) {
      state.solvedQuestions.add(questionKey);
    }
    renderActiveSection();
    return;
  }

  const startButton = event.target.closest("#start-learning");
  if (startButton) {
    setActiveSection("lesson-1");
    return;
  }

  const reviewButton = event.target.closest("#open-review");
  if (reviewButton) {
    setActiveSection("review");
    return;
  }
});

document.addEventListener("change", (event) => {
  const checkpoint = event.target.closest("[data-checkpoint]");
  if (!checkpoint) {
    return;
  }

  if (checkpoint.checked) {
    state.checklist.add(checkpoint.dataset.checkpoint);
  } else {
    state.checklist.delete(checkpoint.dataset.checkpoint);
  }

  updateProgress();
});

renderNavigation();
renderActiveSection();
