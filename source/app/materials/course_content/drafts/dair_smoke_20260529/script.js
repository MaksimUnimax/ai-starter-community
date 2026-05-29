const courseData = {
  title: "Работа с ИИ",
  courseTitle: "Как разрабатывать с помощью ChatGPT и Codex",
  subtitle: "Тестовая версия курса",
  sections: [
    {
      id: "lesson-1",
      navLabel: "Урок 1",
      navMeta: "Роли и первый шаг",
      eyebrow: "Урок 1",
      title: "Проектная работа с ИИ: роль пользователя, ChatGPT и Codex",
      subtitle:
        "Вы не пишете код вручную, но управляете задачей, проверкой и принятием результата.",
      description:
        "В этом уроке мы разбираем первую и самую важную мысль курса: для работы над проектом не обязательно писать код вручную, но нужно понимать, как организована работа.",
      intro: [
        "Если пользователь просто говорит “Сделай мне сайт”, этого недостаточно. Не ясно, для кого страница нужна, какая у неё цель, какие блоки должны быть на ней и как проверить результат.",
        "Правильная работа начинается не с кода, а с постановки задачи: что нужно получить, какие есть ограничения, кто проверяет результат и какой отчёт должен вернуть исполнитель."
      ],
      learningOutcomeTitle: "После урока вы сможете",
      learningOutcome: [
        "Объяснить свою роль в разработке с ИИ.",
        "Отличить роль ChatGPT от роли Codex.",
        "Сформулировать первую безопасную задачу для страницы сайта.",
        "Понять, почему результат проверяется по фактам, а не по обещанию “Готово”.",
        "Подготовить основу для следующего шага разработки."
      ],
      roleTitle: "В работе участвуют три роли",
      roles: [
        {
          name: "Пользователь",
          label: "Пользователь — заказчик и владелец результата",
          lead: "заказчик и владелец результата",
          description:
            "Он формулирует цель, объясняет, какой результат нужен, проверяет готовую работу и принимает решение: подходит или нужно исправлять."
        },
        {
          name: "ChatGPT",
          label: "ChatGPT — ведущий программист, архитектор и технический руководитель",
          lead: "ведущий программист, архитектор и технический руководитель",
          description:
            "Он разбирает задачу, выбирает подход, инструменты и языки, планирует архитектуру, делит работу на безопасные шаги, пишет точные задания для Codex, контролирует отчёты и проверяет ход работы."
        },
        {
          name: "Codex",
          label: "Codex — исполнитель на сервере",
          lead: "исполнитель на сервере",
          description:
            "Он работает на сервере в нужном репозитории, читает файлы проекта, вносит изменения, запускает проверки, делает commit/push, если это входит в задачу, и возвращает отчёт."
        }
      ],
      processTitle: "Схема процесса",
      processScheme:
        "Пользователь ставит цель → ChatGPT проектирует технический шаг → Codex выполняет задачу на сервере → Codex возвращает отчёт → ChatGPT проверяет отчёт → пользователь смотрит результат и принимает решение.",
      processSteps: [
        "Пользователь ставит цель.",
        "ChatGPT проектирует технический шаг.",
        "Codex выполняет задачу на сервере.",
        "Codex возвращает отчёт.",
        "ChatGPT проверяет отчёт.",
        "Пользователь смотрит результат и принимает решение."
      ],
      importantExplanationTitle: "Почему это важно",
      importantExplanation:
        "Работа без ручного написания кода не означает работу без контроля. Пользователь может не знать, как устроены файлы и команды, но он должен понимать, что именно нужно сделать и как будет проверяться результат.",
      badExampleTitle: "Плохая постановка задачи",
      badExampleQuote: "Сделай мне сайт.",
      badExampleReasons: [
        "Не понятно, для кого сайт.",
        "Не понятно, какая цель страницы.",
        "Не понятно, какие блоки нужны.",
        "Не понятно, где должна быть форма.",
        "Не понятно, какие действия запрещены.",
        "Не понятно, как проверить результат."
      ],
      goodExampleTitle: "Профессиональная постановка задачи",
      goodExampleIntro:
        "Простую страницу сайта для записи на консультацию нужно спроектировать.",
      goodExampleText:
        "Страница должна объяснять услугу, показывать преимущества, отвечать на частые вопросы и вести пользователя к форме заявки.",
      goodExampleLimit:
        "На первом этапе не нужно подключать оплату, личный кабинет или сложную CRM.",
      goodExampleQuestionsTitle: "Нужно описать",
      goodExampleQuestions: [
        "Цель страницы.",
        "Для кого страница.",
        "Какие блоки должны быть на странице.",
        "Какие данные пользователь оставляет в форме.",
        "Что происходит после отправки заявки.",
        "Что нельзя трогать на сайте.",
        "Как проверить, что страница работает правильно."
      ],
      goodExampleResult:
        "Результат первого этапа — понятное описание страницы и структуры блоков, по которому потом можно дать Codex отдельную задачу на реализацию.",
      exampleBreakdownTitle: "Разбор примера",
      exampleBreakdown: [
        {
          label: "Цель",
          text: "Получить заявку на консультацию."
        },
        {
          label: "Аудитория",
          text: "Человек, которому нужна услуга."
        },
        {
          label: "Структура",
          text: "Заголовок, описание, преимущества, вопросы, форма."
        },
        {
          label: "Ограничение",
          text: "Не трогать оплату, личный кабинет и другие разделы."
        },
        {
          label: "Проверка",
          text: "Страница открывается, текст понятен, форма видна, путь пользователя логичен."
        }
      ],
      practiceTitle: "Практика: опишите страницу сайта",
      practiceIntro: "Ответьте на шесть вопросов и заполните поля ниже:",
      practiceFields: [
        { key: "audience", label: "Для кого нужна страница?" },
        { key: "goal", label: "Какую одну главную цель она должна решать?" },
        { key: "blocks", label: "Какие 3–5 блоков должны быть на странице?" },
        { key: "form", label: "Какие данные пользователь должен оставить в форме?" },
        { key: "forbidden", label: "Что нельзя трогать на сайте?" },
        { key: "check", label: "Как понять, что страница работает правильно?" }
      ],
      practiceHelper: "Заполните все поля. Затем нажмите кнопку проверки.",
      practiceSuccessText:
        "Практика заполнена. Теперь эту заготовку можно использовать для постановки задачи.",
      practiceErrorPrefix: "Заполните поля:",
      practiceQuestions: [
        "Для кого нужна страница?",
        "Какую одну главную цель она должна решать?",
        "Какие 3–5 блоков должны быть на странице?",
        "Какие данные пользователь должен оставить в форме?",
        "Что нельзя трогать на сайте?",
        "Как понять, что страница работает правильно?"
      ],
      exampleAnswerTitle: "Пример ответа",
      exampleAnswerParagraphs: [
        "Мне нужна простая страница сайта для записи на консультацию.",
        "Пользователь сразу понимает, что это за услуга и что он получит.",
        "Понятное описание задачи может выглядеть так:"
      ],
      exampleAnswerBullets: [
        "Кратко объяснить услугу;",
        "Показать преимущества;",
        "Ответить на частые вопросы;",
        "Вести к форме заявки;",
        "Проверить, что форма видна и путь пользователя понятен."
      ],
      exampleAnswerFooter:
        "На первом этапе не нужно подключать оплату, личный кабинет или сложную CRM. Результат считается правильным, если пользователь понял структуру страницы и следующий шаг.",
      commonMistakesTitle: "Типичные ошибки",
      commonMistakes: [
        "Просить “Сделай мне сайт” без описания цели.",
        "Не указывать, для кого эта страница.",
        "Не перечислять нужные блоки.",
        "Не говорить, что нельзя трогать.",
        "Не объяснять, как проверить результат."
      ],
      selfCheckTitle: "Проверьте себя",
      selfCheck: [
        "Я могу объяснить, для кого нужна страница.",
        "Я могу назвать одну главную цель страницы.",
        "Я понимаю, какие блоки должны быть на странице.",
        "Я понимаю, какие данные нужны в форме.",
        "Я указал, что нельзя трогать на сайте.",
        "Я понимаю, как проверить результат."
      ],
      flashcards: [
        {
          front: "Что делает пользователь?",
          back: "Формулирует цель, проверяет результат и принимает решение."
        },
        {
          front: "Что делает ChatGPT?",
          back: "Ведёт техническую работу: проектирует шаг, выбирает подход, готовит задание и проверяет отчёт."
        },
        {
          front: "Что делает Codex?",
          back: "Выполняет задачу на сервере в нужном репозитории и возвращает отчёт."
        },
        {
          front: "Почему фраза “Сделай мне сайт” плохая?",
          back: "В ней нет цели, аудитории, структуры, ограничений и проверки."
        }
      ],
      quiz: {
        prompt: "Что не так с задачей “Сделай мне сайт”?",
        options: [
          "Она не задаёт цель, аудиторию, структуру, ограничения и проверку.",
          "Она идеально подходит для Codex.",
          "В ней уже есть все нужные требования."
        ],
        answerIndex: 0,
        explanation:
          "Без цели, аудитории, структуры и проверки такую задачу нельзя безопасно передать в работу."
      },
      reviewQuiz: [
        {
          prompt: "Что должен сделать ChatGPT перед задачей для Codex?",
          options: [
            "Разобрать задачу, выбрать подход, ограничить scope и подготовить точное задание.",
            "Сразу писать большой код без обсуждения.",
            "Попросить пользователя вручную собрать весь сайт."
          ],
          answerIndex: 0,
          explanation:
            "ChatGPT должен сначала разложить задачу и только потом отдавать точную работу Codex."
        },
        {
          prompt: "Где работает Codex?",
          options: [
            "На сервере в нужном репозитории проекта.",
            "Только в браузере пользователя.",
            "В документах без доступа к проекту."
          ],
          answerIndex: 0,
          explanation:
            "Codex выполняет задачи именно на сервере в конкретном репозитории."
        },
        {
          prompt: "Что должен дать первый этап по странице сайта?",
          options: [
            "Понятное описание страницы и структуры блоков, а не сразу большой непроверенный код.",
            "Сразу большой готовый продукт без проверки.",
            "Секретные ключи и пароли."
          ],
          answerIndex: 0,
          explanation:
            "Сначала нужен понятный проектный результат, по которому можно дать Codex точную задачу."
        }
      ],
      finalTakeawayTitle: "Главный вывод урока",
      finalTakeaway:
        "Пользователь не пишет код вручную, но управляет целью и принимает результат. ChatGPT ведёт техническую работу как ведущий программист. Codex выполняет конкретную задачу на сервере и возвращает отчёт. Хорошая работа начинается с понятной постановки задачи, а не с просьбы “сделай всё”.",
      nextStepTitle: "Следующий шаг",
      nextStepText:
        "В следующем уроке разберём роли пользователя, ChatGPT и Codex подробнее: кто принимает решения, кто проектирует техническую работу и кто выполняет задачу на сервере.",
      nextStepButtonLabel: "Перейти к уроку 2",
      objectives: [
        "Понять, как задавать работу для проекта.",
        "Отличить роль пользователя, ChatGPT и Codex.",
        "Понять, почему нужен контроль и проверка."
      ],
      keyConcepts: [
        "Постановка задачи",
        "Роли в проекте",
        "Безопасный шаг",
        "Отчёт и проверка"
      ],
      practicalTask:
        "Опишите страницу сайта по шести вопросам из урока.",
      expectedAnswer:
        "Профессиональный ответ описывает цель, аудиторию, структуру, ограничения, проверку и следующий шаг, а не просит “сделать сайт” без деталей.",
      reviewNotes: [
        "В начале важнее постановка задачи, чем код.",
        "Пользователь отвечает за цель и проверку результата."
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
};

const state = {
  activeSectionId: "lesson-1",
  visitedSections: new Set(["lesson-1"]),
  flippedCards: new Set(),
  solvedQuestions: new Set(),
  answeredQuestions: {},
  practiceAnswers: {},
  practiceValidated: false,
  practiceFeedback: ""
};

const lessonNavTitles = {
  "lesson-1": "Проектная работа с ИИ",
  "lesson-2": "Роли пользователя, ChatGPT и Codex",
  "lesson-3": "Документы как память проекта",
  "lesson-4": "Новый диалог после перерыва",
  "lesson-5": "Обновление документации",
  "lesson-6": "ТЗ и roadmap",
  "lesson-7": "Git и deploy key",
  "lesson-8": "Один безопасный шаг разработки",
  review: "Отчёт Codex"
};

const navRoot = document.getElementById("lesson-nav");
const activeSectionRoot = document.getElementById("active-section");
const progressFill = document.getElementById("progress-fill");
const progressValue = document.getElementById("progress-value");
const progressLabel = document.getElementById("progress-label");
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
      const navTitle = lessonNavTitles[section.id] || section.title;
      return `
        <button class="nav-button ${activeClass}" type="button" data-section="${section.id}">
          <span class="nav-number">${escapeHTML(section.navLabel)}</span>
          <span class="nav-title">${escapeHTML(navTitle)}</span>
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

function getLessonOneQuestionCount() {
  const lessonOne = courseData.sections.find((section) => section.id === "lesson-1");
  const reviewQuizCount = lessonOne?.reviewQuiz ? lessonOne.reviewQuiz.length : 0;
  return 1 + reviewQuizCount;
}

function getLessonOneSolvedCount() {
  const questionCount = getLessonOneQuestionCount();
  let solvedCount = 0;
  for (let index = 0; index < questionCount; index += 1) {
    if (state.solvedQuestions.has(quizKey("lesson-1", index))) {
      solvedCount += 1;
    }
  }
  return solvedCount;
}

function getPracticeFields() {
  const lessonOne = courseData.sections.find((section) => section.id === "lesson-1");
  return lessonOne?.practiceFields || [];
}

function renderPracticeField(field) {
  const value = state.practiceAnswers[field.key] || "";
  return `
    <label class="practice-field">
      <span>${escapeHTML(field.label)}</span>
      <textarea data-practice-input="${escapeHTML(field.key)}" rows="3" placeholder="Кратко и по делу">${escapeHTML(value)}</textarea>
    </label>
  `;
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

function renderLessonOne(section) {
  const flashcards = renderFlashcards(section);
  const quiz = renderQuiz(section, section.reviewQuiz ? [section.quiz, ...section.reviewQuiz] : [section.quiz]);
  const processScheme = section.processScheme || section.processSteps.join(" → ");
  const practiceFields = getPracticeFields();
  const practiceFeedback = `<div class="practice-feedback ${
    state.practiceFeedback ? (state.practiceValidated ? "is-success" : "is-error") : ""
  }">${
    escapeHTML(state.practiceFeedback || "Пока ничего не проверено.")
  }</div>`;

  return `
    <article class="section-card lesson-one">
      <header class="section-header">
        <p class="eyebrow">${escapeHTML(section.eyebrow)}</p>
        <h3>${escapeHTML(section.title)}</h3>
        <p class="muted">${escapeHTML(section.subtitle)}</p>
        <p class="muted">${escapeHTML(section.description)}</p>
      </header>

      <div class="section-body">
        <section class="callout">
          <span class="block-label">Вступление</span>
          ${section.intro.map((paragraph) => `<p>${escapeHTML(paragraph)}</p>`).join("")}
        </section>

        <section class="info-grid">
          <div>
            <span class="block-label">${escapeHTML(section.learningOutcomeTitle)}</span>
            <ul>
              ${section.learningOutcome.map((item) => `<li>${escapeHTML(item)}</li>`).join("")}
            </ul>
          </div>

          <div>
            <span class="block-label">${escapeHTML(section.roleTitle)}</span>
            <div class="role-grid">
              ${section.roles
                .map(
                  (role) => `
                    <div class="role-card">
                      <span class="summary-label">${escapeHTML(role.name)}</span>
                      <strong>${escapeHTML(role.label || `${role.name} — ${role.lead}`)}</strong>
                      <p class="muted">${escapeHTML(role.description)}</p>
                    </div>
                  `
                )
                .join("")}
            </div>
          </div>
        </section>

        <section class="callout">
          <span class="block-label">${escapeHTML(section.processTitle)}</span>
          <div class="process-flow">
            ${section.processSteps
              .map(
                (step, index) => `
                  <div class="process-step">
                    <span class="process-step-index">${index + 1}</span>
                    <strong>${escapeHTML(step)}</strong>
                  </div>
                `
              )
              .join("")}
          </div>
          <p class="process-summary">${escapeHTML(processScheme)}</p>
        </section>

        <section class="callout">
          <span class="block-label">${escapeHTML(section.importantExplanationTitle)}</span>
          <p>${escapeHTML(section.importantExplanation)}</p>
        </section>

        <section class="example-grid">
          <div class="example-card">
            <span class="block-label">${escapeHTML(section.badExampleTitle)}</span>
            <p class="muted">“${escapeHTML(section.badExampleQuote)}”</p>
            <ul>
              ${section.badExampleReasons.map((reason) => `<li>${escapeHTML(reason)}</li>`).join("")}
            </ul>
          </div>

          <div class="example-card">
            <span class="block-label">${escapeHTML(section.goodExampleTitle)}</span>
            <p>${escapeHTML(section.goodExampleIntro)}</p>
            <p>${escapeHTML(section.goodExampleText)}</p>
            <p>${escapeHTML(section.goodExampleLimit)}</p>
            <strong>${escapeHTML(section.goodExampleQuestionsTitle)}</strong>
            <ul>
              ${section.goodExampleQuestions.map((item) => `<li>${escapeHTML(item)}</li>`).join("")}
            </ul>
            <p>${escapeHTML(section.goodExampleResult)}</p>
          </div>
        </section>

        <section class="callout">
          <span class="block-label">${escapeHTML(section.exampleBreakdownTitle)}</span>
          <div class="breakdown-grid">
            ${section.exampleBreakdown
              .map(
                (item) => `
                  <div class="breakdown-card">
                    <span class="summary-label">${escapeHTML(item.label)}</span>
                    <strong>${escapeHTML(item.text)}</strong>
                  </div>
                `
              )
              .join("")}
          </div>
        </section>

        <section class="callout">
          <span class="block-label">${escapeHTML(section.practiceTitle)}</span>
          <p>${escapeHTML(section.practiceIntro)}</p>
          <div class="practice-grid">
            ${practiceFields.map((field) => renderPracticeField(field)).join("")}
          </div>
          <p class="muted">${escapeHTML(section.practiceHelper)}</p>
          <button class="primary-button practice-button" type="button" data-practice-submit>Проверить практику</button>
          ${practiceFeedback}
        </section>

        <section class="callout">
          <span class="block-label">${escapeHTML(section.exampleAnswerTitle)}</span>
          ${section.exampleAnswerParagraphs.map((paragraph) => `<p>${escapeHTML(paragraph)}</p>`).join("")}
          <ul>
            ${section.exampleAnswerBullets.map((item) => `<li>${escapeHTML(item)}</li>`).join("")}
          </ul>
          <p>${escapeHTML(section.exampleAnswerFooter)}</p>
        </section>

        <section class="callout">
          <span class="block-label">${escapeHTML(section.commonMistakesTitle)}</span>
          <ol>
            ${section.commonMistakes.map((item) => `<li>${escapeHTML(item)}</li>`).join("")}
          </ol>
        </section>

        <section class="callout">
          <span class="block-label">${escapeHTML(section.selfCheckTitle)}</span>
          <ul>
            ${section.selfCheck.map((item) => `<li>${escapeHTML(item)}</li>`).join("")}
          </ul>
        </section>

        ${flashcards}
        ${quiz}

        <section class="callout">
          <span class="block-label">${escapeHTML(section.finalTakeawayTitle)}</span>
          <p>${escapeHTML(section.finalTakeaway)}</p>
        </section>

        <section class="next-step-card">
          <div>
            <span class="block-label">${escapeHTML(section.nextStepTitle)}</span>
            <p>${escapeHTML(section.nextStepText)}</p>
          </div>
          <button class="primary-button" type="button" data-section="lesson-2">${escapeHTML(section.nextStepButtonLabel)}</button>
        </section>
      </div>
    </article>
  `;
}

function renderSectionContent(section) {
  if (section.id === "lesson-1") {
    return renderLessonOne(section);
  }

  const flashcards = renderFlashcards(section);
  const quiz = renderQuiz(section, section.reviewQuiz ? [section.quiz, ...section.reviewQuiz] : [section.quiz]);

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

      </div>
    </article>
  `;
}

function updateProgress() {
  const totalQuestions = getLessonOneQuestionCount();
  const solvedQuestions = getLessonOneSolvedCount();
  const quizScore = totalQuestions === 0 ? 0 : (solvedQuestions / totalQuestions) * 80;
  const practiceScore = state.practiceValidated ? 20 : 0;
  const progress = Math.min(100, Math.round(quizScore + practiceScore));

  progressFill.style.width = `${progress}%`;
  progressValue.textContent = `${progress}%`;

  if (progress === 0) {
    progressLabel.textContent = "Пока ничего не проверено.";
  } else if (progress < 100) {
    progressLabel.textContent = "Идёт проверка урока.";
  } else {
    progressLabel.textContent = "Проверка завершена.";
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
  activeSectionRoot.scrollIntoView({ behavior: "smooth", block: "start" });
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

  const practiceSubmit = event.target.closest("[data-practice-submit]");
  if (practiceSubmit) {
    const practiceFields = getPracticeFields();
    const missingFields = practiceFields
      .filter((field) => !String(state.practiceAnswers[field.key] || "").trim())
      .map((field) => field.label);

    if (missingFields.length > 0) {
      state.practiceValidated = false;
      state.practiceFeedback = `${courseData.sections[0].practiceErrorPrefix} ${missingFields.join(", ")}.`;
    } else {
      state.practiceValidated = true;
      state.practiceFeedback = courseData.sections[0].practiceSuccessText;
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

document.addEventListener("input", (event) => {
  const practiceInput = event.target.closest("[data-practice-input]");
  if (!practiceInput) {
    return;
  }
  state.practiceAnswers[practiceInput.dataset.practiceInput] = practiceInput.value;
});

renderNavigation();
renderActiveSection();
