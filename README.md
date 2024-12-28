# Academy Cloud Backend
Pet-проект: Система обучения по учебным дисциплинам Academy Cloud (BackEnd)

## Содержание
- [Технологии](#технологии)
- [Использование](#использование)
- [Deploy и CI/CD](#deploy-и-cicd)
- [Команда проекта](#команда-проекта)
- [Источники](#источники)

## Технологии
Для разработки был использован следующий стек:
- [Python](https://www.python.org/)
- [PostgreSQL Database](https://www.postgresql.org/)
- [Redis](https://redis.io/)
- [Poetry](https://python-poetry.org/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [Celery](https://docs.celeryq.dev/en/stable/)
- [Flower](https://flower.readthedocs.io/en/latest/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [Alembic](https://alembic.sqlalchemy.org/en/latest/)
- [Pydantic](https://docs.pydantic.dev/latest/)
- [OpenPyXl](https://openpyxl.readthedocs.io/en/stable/)


## Использование
Для использования проекта необходимо:

Убедиться в наличии пакетного менеджера **Poetry**:
```sh
$ poetry --version
```

Окрыть папку проекта в терминале

Установить все зависимости :
```sh
$ poetry install
```

Клонировать файл окружения и задать их значения:
```sh
$ cat env.sample > .env
```

#### Запуск производится следующим образом:
Для запуска API:
```sh
poetry run python3 -m app.main
```
Для запуска очереди задач Celery:
```sh
poetry run python3 -m app.celery
```
Для запуска дашборда Celery Flower:
```sh
poetry run python3 -m app.flower
```

## Deploy и CI/CD
Для развертки на сервере потребуется настроить [NGINX](https://nginx.org/en/)


### Зачем был разработан этот проект?
Проект изначально был создан как Pet, но позже был использован для защиты выпускной квалификационной работы.


## Команда проекта
- [Алексндр](https://t.me/grushev_works) — Основной разработчик

## Источники
Источниками вдохновения стали: мой предыдуший проект ([Математический тренажер Math](https://github.com/AlexeyGrushev/math_course_work)), сервисы по типу Skillbox, Getbrains, Duolingo. <br>
Frontend часть проекта вы сможете отыскать [здесь](https://github.com/AlexeyGrushev/academycloud_frontend)