# AI Starter Community

Это изолированный корень для проекта AI Starter Community.

Правила размещения:
- существующие проекты не использовать как зависимости по пути или через symlink;
- пути Bridge, OpenScript и autopostmanager защищены и не должны затрагиваться;
- nginx, docker, systemd и доменная настройка здесь пока не выполняются;
- исходный код позже будет лежать в `source/`;
- `runtime/`, `state/`, `logs/` и `backups/` разделены между собой.

Этот репозиторий предназначен для кода реализации AI Starter Community.
Рабочие TZ, roadmap, module map и handoff остаются в ChatGPT, пока их явно не экспортируют отдельно.
Каталоги `runtime/`, `state/`, `logs/`, `backups/` и `tmp/` не являются source of truth и игнорируются.
