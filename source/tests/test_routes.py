def test_landing_page(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "OpenScript — программы, боты и MVP без знаний и опыта" in response.text
    assert (
        '<meta name="description" content="OpenScript помогает людям без технического опыта создавать простые программы, боты, MVP, помощников, агентов и автоматизации под свои задачи.">'
        in response.text
    )
    assert "Пришло новое время для тех, кто хочет создавать" in response.text
    assert "Создание программ перестало быть закрытой территорией" in response.text
    assert "видеть потребности людей, замечать тренды" in response.text
    assert "даже если у вас нет технических знаний и опыта" in response.text
    assert "Начать работу" in response.text
    assert "Как устроена работа" in response.text
    assert "Модель работы OpenScript" not in response.text
    assert 'href="#how-it-works"' in response.text
    assert response.text.count("Для кого OpenScript") == 1
    assert "Для кого OpenScript" in response.text
    assert "Для тех, у кого есть идея MVP" in response.text
    assert "Для малого бизнеса и самозанятых" in response.text
    assert "Для селлеров и онлайн-продавцов" in response.text
    assert "Для тех, кто хочет сменить траекторию" in response.text
    assert "Для тех, кому давно интересно программирование" in response.text
    assert "Для тех, кто работает с таблицами и отчётами" in response.text
    assert "собирать данные, считать показатели, находить изменения" in response.text
    assert response.text.count("Какие задачи можно решать с OpenScript") == 1
    assert "Какие задачи можно решать с OpenScript" in response.text
    assert "OpenScript нужен не для абстрактного" not in response.text
    assert "Например:" not in response.text
    assert "Такие агенты" not in response.text
    assert "Агентов можно использовать" in response.text
    assert "Вы не обязаны сами писать код" not in response.text
    assert "Ответы на вопросы через чаты" not in response.text
    assert "VPN" not in response.text
    assert "ВПН" not in response.text
    assert "Честно о результате" not in response.text
    assert "Начните с первой простой задачи" not in response.text
    assert response.text.count("Что входит в полный доступ") == 1
    assert (
        "В полный доступ входят подписка на ChatGPT Plus на 1 месяц и аренда сервера на 1 месяц."
        in response.text
    )
    assert "подписка на ChatGPT Plus на 1 месяц" in response.text
    assert "аренда сервера на 1 месяц" in response.text
    assert "Полный доступ — 4 990 ₽" in response.text
    assert "Продлевать подписку ChatGPT Plus и аренду сервера можно по отдельности в личном кабинете" in response.text
    assert "Стартовый набор рабочей среды: инструмент и сервер" not in response.text
    assert "инструмент и сервер" not in response.text
    assert "Цена" not in response.text
    assert response.text.count("Вопросы перед стартом") == 1
    assert "Вопросы перед стартом" in response.text
    assert "Какие программы и какое железо нужны для работы?" in response.text
    assert "браузера Google Chrome" in response.text
    assert "стандартного терминала вашей операционной системы" in response.text
    assert "Мощное железо, отдельная видеокарта и сложная установка программ не нужны" in response.text
    assert "основная работа проходит через браузер и терминал ОС" in response.text
    assert "подключённые сервисы" not in response.text
    assert "Создавайте свои первые программы без знаний и опыта" not in response.text
    assert "Вы получаете рабочую среду" not in response.text
    assert "Регистрируетесь" not in response.text
    assert "Получаете полный доступ" not in response.text
    assert "Настраиваете рабочую среду" not in response.text
    assert "Выбираете первую задачу" not in response.text
    assert "Двигаетесь по инструкции" not in response.text
    assert "Если застряли — задаёте вопрос" not in response.text
    assert "OpenScript рассчитан на людей, которым нужен понятный способ начать делать свои инструменты без длинного входа в профессию." not in response.text
    assert "Можно ли проверить идею перед дорогой разработкой?" not in response.text
    assert "Юридическая информация" in response.text
    assert "ИП Ягофаров М.Р." in response.text
    assert "Индивидуальный предприниматель Ягофаров Максим Ринатович" not in response.text
    assert "ИНН: 741705866660" in response.text
    assert "ОГРНИП: 320745600093211" in response.text
    assert "Email: OpenScripts@yandex.com" in response.text
    assert "/static/styles.css" in response.text
    assert "/register" in response.text


def test_login_and_register_pages(client):
    login_response = client.get("/login")
    login_head_response = client.head("/login")
    register_response = client.get("/register")
    check_email_response = client.get("/check-email")
    resend_response = client.get("/resend-verification")
    cabinet_response = client.get("/cabinet", follow_redirects=False)
    assert login_response.status_code == 200
    assert login_head_response.status_code == 200
    assert register_response.status_code == 200
    assert check_email_response.status_code == 200
    assert resend_response.status_code == 200
    assert cabinet_response.status_code == 303
    assert cabinet_response.headers["location"] == "/login"
    assert "Вход в аккаунт" in login_response.text
    assert "Регистрация" in register_response.text
    assert "Нет аккаунта?" in login_response.text
    assert "Зарегистрироваться" in login_response.text
    assert "Забыли пароль?" in login_response.text
    assert "Уже есть аккаунт?" in register_response.text
    assert "Войти" in register_response.text
    assert "Проверьте почту" in check_email_response.text
    assert "Не пришло письмо подтверждения?" in check_email_response.text
    assert "/resend-verification" in check_email_response.text
    assert "Повторная отправка письма подтверждения" in resend_response.text
    assert "Регистрация временно закрыта" not in register_response.text
    assert "Создание аккаунта" in register_response.text
    assert '<form class="form" method="post" action="/register">' in register_response.text
    assert 'name="email"' in register_response.text
    assert 'name="login"' in register_response.text
    assert "/static/styles.css" in login_response.text
    assert "/static/styles.css" in register_response.text
    assert "Электронная почта или логин" in login_response.text
    assert "Электронная почта" in register_response.text
    assert "Подтверждение почты" not in login_response.text
    assert "Не пришло письмо подтверждения?" not in login_response.text
    assert "Отправить письмо подтверждения" not in login_response.text


def test_auth_utility_pages_use_shared_base_and_styles(client):
    check_email_response = client.get("/check-email")
    verify_email_response = client.get("/verify-email/example-token")
    forgot_response = client.get("/forgot-password")
    reset_response = client.get("/reset-password/example-token")
    resend_response = client.get("/resend-verification")

    assert check_email_response.status_code == 200
    assert verify_email_response.status_code == 200
    assert forgot_response.status_code == 200
    assert reset_response.status_code == 200
    assert resend_response.status_code == 200

    for response in (
        check_email_response,
        verify_email_response,
        forgot_response,
        reset_response,
        resend_response,
    ):
        assert "/static/styles.css" in response.text
        assert "Главная" in response.text
        assert "Вход / регистрация" in response.text
        assert "Юридическая информация" in response.text
        assert "ИП Ягофаров М.Р." in response.text
        assert "Индивидуальный предприниматель Ягофаров Максим Ринатович" not in response.text
        assert "ИНН: 741705866660" in response.text
        assert "ОГРНИП: 320745600093211" in response.text
        assert "Email: OpenScripts@yandex.com" in response.text
        assert "Личный кабинет" not in response.text
        assert "Работа с ИИ" not in response.text
        assert "Админ-панель" not in response.text

    assert "Не пришло письмо подтверждения?" in check_email_response.text
    assert "Укажите адрес электронной почты, чтобы мы смогли найти ваш аккаунт." in forgot_response.text
    assert "Если такой адрес электронной почты зарегистрирован" not in forgot_response.text
    assert "Подтвердить почту" not in forgot_response.text
    assert "Вернуться ко входу" in forgot_response.text
    assert "Войти" in reset_response.text or "Вернуться ко входу" in reset_response.text
    assert "Повторная отправка письма подтверждения" in resend_response.text


def test_placeholder_post_routes_redirect(client):
    login_response = client.post(
        "/login",
        data={"email_or_login": "user@example.com", "password": "secret"},
        follow_redirects=False,
    )
    register_response = client.post(
        "/register",
        data={
            "email": "user@example.com",
            "login": "user123",
            "password": "Secret123",
            "repeat_password": "Secret123",
        },
        follow_redirects=False,
    )
    logout_response = client.post("/logout", follow_redirects=False)
    assert login_response.status_code == 200
    assert register_response.status_code == 303
    assert logout_response.status_code == 303
