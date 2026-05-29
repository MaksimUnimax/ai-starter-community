const courseData = {
  title: "Работа с ИИ",
  courseTitle: "Как разрабатывать с помощью ChatGPT и Codex",
  subtitle: "Тестовая версия курса",
  sections: [
    {
      id: "lesson-1",
      navLabel: "Урок 1",
      navMeta: "Без знания кода",
      eyebrow: "Урок 1",
      title: "Как теперь можно делать проекты без знания кода",
      description:
        "Пользователь не пишет код вручную, но понимает процесс, задаёт цель и проверяет результат вместе с ChatGPT и Codex.",
      objectives: [
        "Понять, где пользователь участвует в процессе.",
        "Увидеть, что код вручную писать не обязательно.",
        "Понять, как выглядит безопасный первый шаг."
      ],
      keyConcepts: [
        "Процесс важнее ручного кода",
        "Проверка результата",
        "Пользователь как участник работы"
      ],
      practicalTask:
        "Объясни, почему можно делать проект без ручного написания кода, но нельзя без понимания процесса.",
      expectedAnswer:
        "Пользователь понимает цель, читает подсказки ChatGPT, даёт контекст Codex и проверяет результат.",
      flashcards: [
        {
          front: "Можно ли обойтись без ручного кода?",
          back: "Да, если пользователь понимает процесс и проверяет результат."
        },
        {
          front: "Что остаётся обязательным?",
          back: "Понимание шагов, контекста и результата."
        }
      ],
      quiz: {
        prompt: "Что важно в проекте без знания кода?",
        options: [
          "Можно ничего не понимать, если есть ChatGPT.",
          "Пользователь понимает процесс и проверяет результат.",
          "Код всегда пишется вручную."
        ],
        answerIndex: 1,
        explanation:
          "Без ручного кода всё равно нужен человек, который понимает шаги и проверяет результат."
      },
      reviewNotes: [
        "Не путай отсутствие ручного кода с отсутствием контроля.",
        "Понимание процесса остаётся обязательным."
      ]
    },
    {
      id: "lesson-2",
      navLabel: "Урок 2",
      navMeta: "Как мы работаем",
      eyebrow: "Урок 2",
      title: "Кто что делает: пользователь, ChatGPT и Codex",
      description:
        "Мы разводим роли: пользователь задаёт цель и проверяет результат, ChatGPT проектирует шаг, Codex выполняет точную задачу.",
      objectives: [
        "Понять, кто задаёт цель.",
        "Понять, кто проектирует шаг.",
        "Понять, кто вносит изменения в репозиторий."
      ],
      keyConcepts: [
        "Пользователь",
        "ChatGPT",
        "Codex"
      ],
      practicalTask:
        "Назови роль каждого участника в одном безопасном шаге разработки.",
      expectedAnswer:
        "Пользователь ставит цель, ChatGPT предлагает план, Codex делает изменения, пользователь проверяет результат.",
      flashcards: [
        {
          front: "Кто ставит цель?",
          back: "Пользователь."
        },
        {
          front: "Кто выполняет точную задачу?",
          back: "Codex."
        },
        {
          front: "Кто проектирует шаг?",
          back: "ChatGPT."
        }
      ],
      quiz: {
        prompt: "Кто что делает в курсе?",
        options: [
          "Пользователь ничего не делает, ChatGPT всё делает сам.",
          "Пользователь задаёт цель, ChatGPT проектирует, Codex выполняет.",
          "Codex только читает документы, а пользователь пишет код."
        ],
        answerIndex: 0,
        explanation:
          "Правильная схема работы строится вокруг трёх ролей: цель, проектирование и выполнение."
      },
      reviewNotes: [
        "Не смешивай роли в одну.",
        "Каждый участник отвечает за свой шаг."
      ]
    },
    {
      id: "lesson-3",
      navLabel: "Урок 3",
      navMeta: "Документы как память",
      eyebrow: "Урок 3",
      title: "Почему проект начинается с документов",
      description:
        "Документы хранят память проекта: что мы строим, почему так и что уже решили.",
      objectives: [
        "Понять, зачем проекту нужна память.",
        "Отличить документы от случайных заметок.",
        "Понять, где хранить важные решения."
      ],
      keyConcepts: [
        "Память проекта",
        "Документы как источник правды",
        "Решения и контекст"
      ],
      practicalTask:
        "Скажи, какие три вещи должны быть в документах, чтобы проект не потерялся.",
      expectedAnswer:
        "В документах фиксируют цель, текущие решения и следующий шаг.",
      flashcards: [
        {
          front: "Зачем нужны документы?",
          back: "Они сохраняют память проекта."
        },
        {
          front: "Что нельзя хранить только в голове?",
          back: "Важные решения и договорённости."
        }
      ],
      quiz: {
        prompt: "Почему проект начинается с документов?",
        options: [
          "Потому что документы помогают помнить, что уже решили.",
          "Потому что документы заменяют работу Codex.",
          "Потому что документы важнее результата."
        ],
        answerIndex: 0,
        explanation:
          "Документы нужны, чтобы проект не терял память и не зависел от случайных переписок."
      },
      reviewNotes: [
        "Документы не дублируют работу, а сохраняют её смысл.",
        "Память проекта не должна жить только в переписке."
      ]
    },
    {
      id: "lesson-4",
      navLabel: "Урок 4",
      navMeta: "Новый диалог",
      eyebrow: "Урок 4",
      title: "Как начинать новый диалог после перерыва",
      description:
        "После паузы сначала восстанавливаем контекст, а уже потом продолжаем работу.",
      objectives: [
        "Понять, что нужно восстановить в первую очередь.",
        "Не терять контекст между диалогами.",
        "Собирать только то, что важно для продолжения."
      ],
      keyConcepts: [
        "Контекст",
        "Краткое восстановление",
        "Продолжение работы"
      ],
      practicalTask:
        "Сформулируй короткое вступление для нового диалога после паузы.",
      expectedAnswer:
        "Нужно напомнить цель, текущее состояние и ближайший шаг.",
      flashcards: [
        {
          front: "Что делаем первым после перерыва?",
          back: "Восстанавливаем контекст."
        },
        {
          front: "Что не нужно делать?",
          back: "Начинать с нуля, если контекст уже есть."
        }
      ],
      quiz: {
        prompt: "С чего начать новый диалог после паузы?",
        options: [
          "Сразу просить новый дизайн без контекста.",
          "Сначала восстановить цель, состояние и следующий шаг.",
          "Игнорировать прошлую работу."
        ],
        answerIndex: 1,
        explanation:
          "Сначала возвращаем контекст, иначе новый диалог будет терять смысл."
      },
      reviewNotes: [
        "Контекст важнее случайного первого вопроса.",
        "Новый диалог должен опираться на память проекта."
      ]
    },
    {
      id: "lesson-5",
      navLabel: "Урок 5",
      navMeta: "Обновление docs",
      eyebrow: "Урок 5",
      title: "Как обновляется документация во время работы",
      description:
        "Документацию обновляют после важных решений, результатов и новых фактов, а не в конце по памяти.",
      objectives: [
        "Понять, когда менять документацию.",
        "Отметить, что docs живут вместе с работой.",
        "Не оставлять важные изменения только в чате."
      ],
      keyConcepts: [
        "Важные решения",
        "Итоги работы",
        "Документация как результат"
      ],
      practicalTask:
        "Назови момент, когда документация должна обновиться в реальном проекте.",
      expectedAnswer:
        "Docs обновляются после значимых решений и после подтверждённого результата.",
      flashcards: [
        {
          front: "Когда обновлять docs?",
          back: "После важных решений и результатов."
        },
        {
          front: "Почему не в конце по памяти?",
          back: "Память теряет детали, docs должны фиксировать факты."
        }
      ],
      quiz: {
        prompt: "Когда лучше всего обновлять документацию?",
        options: [
          "Когда уже всё забыли.",
          "После важного решения или подтверждённого результата.",
          "Только перед релизом."
        ],
        answerIndex: 1,
        explanation:
          "Docs обновляют по ходу работы, когда появляется важное решение или подтверждённый результат."
      },
      reviewNotes: [
        "Документация и работа идут вместе.",
        "Факты фиксируют сразу, а не откладывают."
      ]
    },
    {
      id: "lesson-6",
      navLabel: "Урок 6",
      navMeta: "ТЗ и roadmap",
      eyebrow: "Урок 6",
      title: "Зачем нужны ТЗ и roadmap",
      description:
        "ТЗ говорит, что именно строим, а roadmap говорит, в каком порядке это делаем.",
      objectives: [
        "Различать ТЗ и roadmap.",
        "Понимать, что они решают разные задачи.",
        "Не смешивать цель и порядок работ."
      ],
      keyConcepts: [
        "ТЗ = что строим",
        "Roadmap = в каком порядке",
        "Планирование"
      ],
      practicalTask:
        "Скажи, что из этого описывает цель, а что — порядок: ТЗ или roadmap.",
      expectedAnswer:
        "ТЗ описывает, что строим. Roadmap описывает, в каком порядке идём.",
      flashcards: [
        {
          front: "Что делает ТЗ?",
          back: "Описывает, что мы строим."
        },
        {
          front: "Что делает roadmap?",
          back: "Описывает порядок шагов."
        }
      ],
      quiz: {
        prompt: "Что верно про ТЗ и roadmap?",
        options: [
          "Они делают одно и то же.",
          "ТЗ отвечает за что, roadmap — за порядок.",
          "Roadmap нужен только для дизайна."
        ],
        answerIndex: 1,
        explanation:
          "ТЗ и roadmap связаны, но решают разные задачи: цель и порядок."
      },
      reviewNotes: [
        "Не путай цель с очередностью.",
        "План помогает работать без хаоса."
      ]
    },
    {
      id: "lesson-7",
      navLabel: "Урок 7",
      navMeta: "Git и deploy key",
      eyebrow: "Урок 7",
      title: "Git простыми словами",
      description:
        "Git помогает хранить историю изменений и возвращаться к нужной точке. Дополнительная тема урока — Как дать Codex право отправлять проект в GitHub. Если Codex работает на сервере и должен пушить в GitHub, нужен deploy key — отдельный SSH-ключ только для одного репозитория.",
      objectives: [
        "Понять Git как историю и точку отката.",
        "Понять, зачем нужен deploy key.",
        "Понять безопасный порядок работы с публичным и приватным ключом."
      ],
      keyConcepts: [
        "Git = история и точка отката",
        "deploy key",
        "публичный ключ",
        "приватный ключ"
      ],
      practicalTask:
        "Объясни порядок: Codex создаёт ключ на сервере, показывает только публичный ключ, пользователь добавляет его в GitHub, включает Allow write access при необходимости и возвращается к Codex, чтобы проверить доступ и запушить.",
      expectedAnswer:
        "Публичный ключ можно вставить в GitHub Deploy keys. Приватный ключ остаётся только на сервере и никогда не показывается в чат. Allow write access включают, если Codex нужно пушить изменения.",
      flashcards: [
        {
          front: "Что такое deploy key?",
          back: "SSH-ключ, который даёт серверу доступ только к одному репозиторию."
        },
        {
          front: "Что нельзя показывать?",
          back: "Приватный ключ."
        },
        {
          front: "Когда нужен Allow write access?",
          back: "Если Codex должен пушить изменения в этот репозиторий."
        }
      ],
      quiz: {
        prompt: "Что лучше всего описывает Git?",
        options: [
          "Это только список файлов без истории.",
          "Это история изменений и точка отката.",
          "Это способ скрыть правки."
        ],
        answerIndex: 1,
        explanation:
          "Git нужен, чтобы видеть историю и при необходимости откатываться."
      },
      reviewQuiz: [
        {
          prompt: "Что можно вставить в GitHub Deploy keys?",
          options: ["публичный ключ", "приватный ключ", "любой случайный текст"],
          answerIndex: 0,
          explanation: "В Deploy keys вставляют только публичный ключ."
        },
        {
          prompt: "Что нельзя показывать GPT, Codex или вставлять в чат?",
          options: ["публичный ключ", "приватный ключ", "README"],
          answerIndex: 1,
          explanation: "Приватный ключ остаётся только на сервере."
        },
        {
          prompt: "Зачем нужен Allow write access?",
          options: [
            "Чтобы Codex мог пушить изменения в репозиторий",
            "Чтобы ключ выглядел длиннее",
            "Чтобы GitHub сменил тему"
          ],
          answerIndex: 0,
          explanation: "Allow write access нужен, если Codex должен пушить изменения."
        },
        {
          prompt: "Что должен сделать Codex после того, как пользователь добавил ключ в GitHub?",
          options: [
            "Проверить доступ и запушить",
            "Удалить ключ",
            "Начать новый проект"
          ],
          answerIndex: 0,
          explanation: "После добавления ключа Codex проверяет доступ и делает push."
        }
      ],
      reviewNotes: [
        "Private key остаётся только на сервере.",
        "Deploy key даёт доступ к одному репозиторию, а не ко всему аккаунту."
      ]
    },
    {
      id: "lesson-8",
      navLabel: "Урок 8",
      navMeta: "Безопасный шаг",
      eyebrow: "Урок 8",
      title: "Как идёт один безопасный шаг разработки",
      description:
        "Один безопасный шаг идёт по цепочке: пользователь -> GPT -> Codex -> отчёт -> GPT -> визуальная проверка -> обновление docs.",
      objectives: [
        "Понять порядок безопасного шага.",
        "Увидеть, где появляется отчёт.",
        "Понять, когда нужна визуальная проверка и обновление docs."
      ],
      keyConcepts: [
        "Пользователь",
        "GPT и Codex",
        "Отчёт",
        "Визуальная проверка",
        "Обновление документации"
      ],
      practicalTask:
        "Повтори цепочку безопасного шага без пропусков.",
      expectedAnswer:
        "Сначала пользователь ставит цель, потом GPT проектирует, Codex выполняет, затем идёт отчёт, визуальная проверка и обновление документации.",
      flashcards: [
        {
          front: "Что идёт после выполнения Codex?",
          back: "Отчёт."
        },
        {
          front: "Что идёт после отчёта?",
          back: "GPT и визуальная проверка."
        }
      ],
      quiz: {
        prompt: "Какой порядок безопасного шага верный?",
        options: [
          "User -> GPT -> Codex -> report -> GPT -> visual check -> docs update",
          "Codex -> user -> report -> docs update -> GPT",
          "Docs update -> Codex -> visual check -> user"
        ],
        answerIndex: 0,
        explanation:
          "Безопасный шаг идёт через проектирование, выполнение, отчёт, проверку и обновление docs."
      },
      reviewNotes: [
        "Нельзя пропускать отчёт.",
        "Визуальная проверка нужна перед обновлением документации."
      ]
    },
    {
      id: "review",
      navLabel: "Урок 9",
      navMeta: "Отчёт Codex",
      eyebrow: "Урок 9",
      title: "Что значит отчёт Codex",
      description:
        "GPT объясняет отчёт, а пользователю не нужно глубоко разбирать весь технический текст: достаточно понимать, что изменилось и что делать дальше.",
      objectives: [
        "Понять роль отчёта в диалоге.",
        "Не теряться в технических деталях.",
        "Считать отчёт опорой для следующего шага."
      ],
      keyConcepts: [
        "Отчёт как сигнал",
        "Что изменилось",
        "Следующий шаг"
      ],
      practicalTask:
        "Скажи, зачем нужен отчёт Codex в конце безопасного шага разработки.",
      expectedAnswer:
        "Отчёт показывает, что изменилось, что проверять дальше и какой следующий шаг нужен.",
      flashcards: [
        {
          front: "Кто объясняет отчёт?",
          back: "GPT."
        },
        {
          front: "Нужно ли пользователю глубоко разбирать весь текст?",
          back: "Нет, достаточно понимать смысл и следующий шаг."
        }
      ],
      quiz: {
        prompt: "Что лучше всего описывает отчёт Codex?",
        options: [
          "Это случайный текст без пользы.",
          "Это структурированный сигнал о том, что изменилось и что делать дальше.",
          "Это замена проверке результата."
        ],
        answerIndex: 1,
        explanation:
          "Отчёт нужен, чтобы быстро понять результат и следующий шаг."
      },
      reviewNotes: [
        "Отчёт помогает перейти к проверке, а не заменяет её.",
        "Пользователю важен смысл, а не глубокая техническая детализация."
      ]
    }
  ],
  reviewChecklist: [
    "Я понял, как делать проекты без ручного кода.",
    "Я могу назвать роли пользователя, ChatGPT и Codex.",
    "Я понимаю, зачем нужны документы, Git и deploy key.",
    "Я вижу, как читается отчёт Codex и следующий шаг."
  ]
};

const state = {
  activeSectionId: "lesson-1",
  visitedSections: new Set(["lesson-1"]),
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
