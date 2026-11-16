# OpsFlow - Service Desk API

Асинхронный REST API сервис для управления внутренними заявками и процессами согласования (запрос оборудования, выдача доступов, ИТ-поддержка).

## Cтек

* **Backend:** Python 3.12, FastAPI, Pydantic v2, pydantic-settings
* **БД и ORM:** PostgreSQL 16, SQLAlchemy 2.0 (asyncpg), Alembic
* **Безопасность:** JWT Bearer Authentication (PyJWT), Argon2 (pwdlib)
* **Инфраструктура:** Docker, Docker Compose, uv

## Архитектура проекта

```text
src/opsflow/
├── api/            # Роуты (v1) и зависимости (Depends, Auth)
├── core/           # Конфигурация приложения и криптография (JWT, хеширование)
├── database/       # Настройка асинхронного движка и сессий SQLAlchemy
├── models/         # ORM-модели таблиц (User, Ticket)
├── schemas/        # Pydantic-схемы валидации запросов и ответов
└── main.py         # Точка входа FastAPI

```

## Быстрый запуск

1. Клонируйте репозиторий и создайте файл окружения из шаблона:
```bash
git clone https://github.com/reclacc/opsflow
cd opsflow
cp .env.example .env

```


2. Запустите сервисы через Docker Compose (миграции БД применятся автоматически):
```bash
docker compose up --build -d

```


3. Интерактивная документация Swagger UI будет доступна по адресу:
* `http://localhost:8000/docs`


## Реализованные эндпоинты (MVP)

* `GET /health` — проверка работоспособности сервиса
* `POST /api/v1/auth/register` — регистрация нового пользователя
* `POST /api/v1/auth/login` — аутентификация и получение JWT-токена
* `GET /api/v1/auth/me` — получение профиля текущего пользователя
* `POST /api/v1/tickets` — создание новой заявки
* `GET /api/v1/tickets` — получение списка заявок (с фильтрацией прав: пользователь видит свои, администратор — все)
* `PATCH /api/v1/tickets/{ticket_id}/status` — изменение статуса заявки с проверкой ролей

## Roadmap

* [x] Каркас приложения, конфигурация через `pydantic-settings` и асинхронная работа с PostgreSQL
* [x] Аутентификация по JWT и хеширование паролей
* [x] Базовый жизненный цикл заявок (создание, просмотр, смена статусов) и ролевое разделение доступа
* [x] Контейнеризация приложения и БД через Docker Compose с автомиграциями
* [ ] Вынесение бизнес-логики и запросов в сервисный слой и паттерн Repository
* [ ] Конечный автомат (FSM) для валидации графа переходов статусов и таблица истории изменений
* [ ] Кэширование справочников и категорий заявок в Redis
* [ ] Фоновые задачи контроля SLA-дедлайнов
* [ ] Покрытие интеграционными тестами (`pytest` + `pytest-asyncio` + `httpx`)
* [ ] Внедрение Refresh-токенов (ротация, хранение в HttpOnly cookies) и поддержка OAuth 2.1 (Authorization Code + PKCE)