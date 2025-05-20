# Base Project Template

## Описание

Этот репозиторий — базовый шаблон для Python-проектов на FastAPI с поддержкой Dependency Injection, конфигурируемым логированием, модульной архитектурой и удобной структурой для масштабирования. Используйте как стартовую точку для своих сервисов и API.

---

## Структура проекта

```
base_project/
├── app/
│   ├── api/         # API слой: роуты, схемы, модели, адаптеры
│   │   ├── routes/      # Файлы с роутами FastAPI
│   │   ├── server/      # Инициализация FastAPI-приложения
│   │   ├── schemas/     # Pydantic-схемы
│   │   ├── models/      # Модели (например, ORM)
│   │   ├── adapters/    # Адаптеры для интеграций
│   │   └── deps.py      # Зависимости для роутов
│   ├── core/        # Ядро: DI, логгер, командер, базовые сервисы
│   │   ├── base/        # Базовые сервисы (logger, commander, container)
│   │   └── application/ # CoreApplication и инициализация
│   ├── domains/     # Бизнес-логика (доменные сущности)
│   ├── services/    # Сервисы (интерфейсы к доменам, интеграции)
│   └── scripts/     # Скрипты для обслуживания/миграций
├── config/
│   └── root_config/ # Основные YAML-конфиги
├── logs/            # Логи приложения
├── main.py          # Точка входа, запуск API
├── requirements.txt # Зависимости
├── .gitignore       # Исключения для git
├── .python-version  # Версия Python
├── .root            # Маркер корня проекта
└── README.md        # Документация
```

---

## Быстрый старт

1. **Установите зависимости:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Настройте конфиг:**
   - Основной конфиг: `config/root_config/root_config.yaml`
   - Пример параметров:
     ```yaml
     application:
       name: "base_project"
       version: "0.1.0"
     api:
       host: "0.0.0.0"
       port: 8000
       debug: true
     logging:
       level: "DEBUG"
       handlers: [console, file]
     commander:
       timeout: 300
     ```

3. **Запустите сервер:**
   ```bash
   python main.py
   ```
   По умолчанию сервер будет доступен на http://0.0.0.0:8000

4. **Документация API:**
   - Swagger UI: http://localhost:8000/docs

---

## Основные компоненты

- **Dependency Injection:**
  Используется [dependency-injector](https://python-dependency-injector.ets-labs.org/) для управления зависимостями через контейнер `app/core/base/container/container.py`.

- **Логгер:**
  Гибкая настройка логирования (цветной вывод, ротация файлов, уровни) через YAML-конфиг и модуль `app/core/base/logger/`.

- **Командер:**
  Универсальный исполнитель shell-команд с поддержкой таймаутов и логирования (`app/core/base/commander/`).

- **API:**
  FastAPI-приложение, роуты подключаются из `app/api/routes/`.

---

## Расширение проекта

- **Добавление роутов:**
  Создайте новый файл в `app/api/routes/` и зарегистрируйте роутер в сервере.
- **Бизнес-логика:**
  Помещайте доменные сущности в `app/domains/`, сервисы — в `app/services/`.
- **Скрипты:**
  Для вспомогательных задач используйте `app/scripts/`.
- **Конфигурация:**
  Все параметры — через YAML-файлы в `config/root_config/`.

---

## Зависимости

Основные библиотеки:
- fastapi
- uvicorn
- dependency-injector
- pydantic
- colorlog
- PyYAML
- starlette

Полный список — в `requirements.txt`.

---

## .gitignore (фрагмент)

```
__pycache__/
*.pyc
*.log
logs/
.env
venv/
.idea/
.vscode/
.DS_Store
local_config.yaml
```

---

## Лицензия

Apache License 2.0 — свободная лицензия, разрешающая использовать, изменять и распространять проект (в том числе в коммерческих целях) при сохранении уведомления об авторских правах и самой лицензии. Подробнее см. файл LICENSE и https://www.apache.org/licenses/LICENSE-2.0
