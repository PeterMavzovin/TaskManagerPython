# Task Manager с FastAPI и Gauge

Этот проект представляет собой простое приложение для управления задачами (Task Manager), реализованное с использованием FastAPI для API и Gauge для функционального тестирования.

## Функциональные требования

*   **CRUD операции:** Создание, получение по ID, получение списка, обновление и удаление задач.
*   **Модель задачи:** `uuid` (уникальный идентификатор), `title` (название), `description` (описание), `status` (статус задачи: `created`, `in progress`, `completed`).
*   **FastAPI:** Использование FastAPI для реализации RESTful API.
*   **Gauge:** Использование Gauge для написания функциональных тестов.
*   **Стандарты кода:** Соблюдение PEP8 и общих принципов чистого кода.

## Дополнительные возможности

*   **Swagger-документация:** FastAPI автоматически генерирует интерактивную документацию API (доступна по `/docs` или `/redoc`).
*   **Docker:** Контейнеризация приложения с использованием Docker для простого развертывания.

## Структура проекта
TaskManagerPython/
├── app/
│ ├── init.py
│ ├── main.py # Основное приложение FastAPI
│ └── models.py # Модели данных (Pydantic)
├── specs/
│ └── task_management.spec # Спецификации Gauge на естественном языке
├── step_impl/
│ └── task_steps.py # Реализация шагов Gauge
├── Dockerfile # Инструкции для сборки Docker-образа
├── docker-compose.yml # Конфигурация Docker Compose для запуска сервисов
├── requirements.txt # Зависимости Python
└── README.md # Этот файл


## Установка и запуск

Для запуска проекта у вас должен быть установлен Python 3.11+ и Docker.

### 1. Клонирование репозитория (если применимо)

```bash
git clone <URL_ВАШЕГО_РЕПОЗИТОРИЯ>
cd TaskManagerPython
```

### 2. Настройка виртуального окружения и установка зависимостей

```bash
python -m venv venv
# Для Windows:
.\venv\Scripts\activate
# Для macOS/Linux:
source venv/bin/activate

pip install -r requirements.txt
```

### 3. Запуск FastAPI приложения (без Docker)

Вы можете запустить приложение напрямую с помощью Uvicorn:

```bash
uvicorn app.main:app --reload
```
Приложение будет доступно по адресу `http://127.0.0.1:8000`.

### 4. Развертывание с использованием Docker

Убедитесь, что Docker Desktop запущен.

Для сборки образа и запуска приложения с Docker Compose:

```bash
docker-compose up --build
```
Приложение будет доступно по адресу `http://localhost:8000`.

Чтобы остановить контейнеры:

```bash
docker-compose down
```

### 5. Запуск тестов Gauge

Убедитесь, что ваше FastAPI приложение запущено (либо напрямую, либо через Docker).
Затем, в отдельном терминале (с активированным виртуальным окружением, если запускаете без Docker):

```bash
gauge install python # Если еще не установлен Python Runner для Gauge
gauge run specs/
```

После выполнения тестов Gauge сгенерирует отчеты в директории `reports/html-report/`. Откройте `reports/html-report/index.html` в вашем браузере, чтобы просмотреть подробный отчет.

## Swagger UI

После запуска FastAPI приложения (по адресу `http://127.0.0.1:8000` или `http://localhost:8000`), вы можете получить доступ к интерактивной документации API по следующим URL:

*   **Swagger UI:** `http://127.0.0.1:8000/docs`
*   **ReDoc:** `http://127.0.0.1:8000/redoc`

---
