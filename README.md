# Сервис рассылки

## Содержание

- [Описание](#описание)
- [Технологии](#технологии)
- [Запуск проекта](#запуск-проекта)
- [Запуск в docker-контейнере](#запуск-в-docker-контейнере)
- [Тестирование](#тестирование)
- [Документация](#просмотр-документации)

## Описание

API приложение для отправки уведомлений пользователям на email или в telegram.

Являться частью микросервисной архитектуры, которая обеспечивает работу большого проекта.

Реализует метод:

post .../api/notify/ - Создает уведомление и запускает задачу отправки пользователям на Email или в Telegram

Тело запроса включает следующие параметры:

```
{
  "message": string(1024),
  "recepient": string(150) | list[string(150)],
  "delay": int
}
```

При получении запроса сообщение сохраняется в БД.

При рассылке записывается лог о попытке отправки в БД.

## Технологии

- Python
- Django
- DRF
- PostgreSQL
- drf-yasg
- Redis
- Celery
- Docker
- Docker Compose

## Запуск проекта

1. Клонируйте проект

```
git clone git@github.com:aleksandrasilina/mailing_service.git
```

2. Установите зависимости

```
pip install -r requirements.txt
```

3. Создайте файл .env в соответствии с шаблоном .env.sample
4. Примените миграции

```
python manage.py migrate
```

5. Запустите проект

```
python manage.py runserver
```

6. Запустите redis

```
redis-server
```

7. Запустите celery worker:

```
celery -A config worker -l INFO -P eventlet
```

## Запуск в docker-контейнере

1. Установите в .env:

- POSTGRES_HOST=db,
- CELERY_BROKER_URL=redis://redis:6379/0
- CELERY_RESULT_BACKEND=redis://redis:6379/0

2.

```
docker-compose build
```

3.

```
docker-compose up -d
```

## Тестирование:

```
python manage.py test
```

Подсчет покрытия

```
coverage run --source='.' manage.py test
coverage report -m
```

## Просмотр документации

http://127.0.0.1:8000/swagger/

http://127.0.0.1:8000/redoc/
