# Foodgram
[![Python](https://img.shields.io/badge/-Python-464646?style=flat-square&logo=Python)](https://www.python.org/)
[![Django](https://img.shields.io/badge/-Django-464646?style=flat-square&logo=Django)](https://www.djangoproject.com/)
[![Django REST Framework](https://img.shields.io/badge/-Django%20REST%20Framework-464646?style=flat-square&logo=Django%20REST%20Framework)](https://www.django-rest-framework.org/)
[![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-464646?style=flat-square&logo=PostgreSQL)](https://www.postgresql.org/)
[![Nginx](https://img.shields.io/badge/-NGINX-464646?style=flat-square&logo=NGINX)](https://nginx.org/ru/)
[![gunicorn](https://img.shields.io/badge/-gunicorn-464646?style=flat-square&logo=gunicorn)](https://gunicorn.org/)
[![docker](https://img.shields.io/badge/-Docker-464646?style=flat-square&logo=docker)](https://www.docker.com/)
[![GitHub%20Actions](https://img.shields.io/badge/-GitHub%20Actions-464646?style=flat-square&logo=GitHub%20actions)](https://github.com/features/actions)

Foodgram создан для публикации и просмотра рецептов. 
В нем пользователи могут создавать рецепты, добавлять их в избранное, а так же в список покупок и скачивать его.
Можно подписываться на любимых авторов.

Сайт доступен по [ссылке](http://foodgramloshch.ddns.net/)

## Запуск приложения на удаленном сервере
### Клонируйте репозиторий на локалку:
```
git clone https://github.com/nikitaloshch/foodgram-project-react.git
```

- Зайдите на удаленный сервер

- Скопируйте `docker-compose.yml`, `nginx.conf` из директории infra на сервер:
```
scp docker-compose.yml <username>@<host>:/home/<username>/docker-compose.yml
scp nginx.conf <username>@<host>:/home/<username>/nginx.conf
```

- Создайте .env файл
```
touch .env
```

- И заполните его по примеру

```
POSTGRES_ENGINE=django.db.backends.postgresql
POSTGRES_NAME=postgres # Имя БД
POSTGRES_USER=postgres # Пользователь БД
POSTGRES_PASSWORD=postgres #Пароль от БД
POSTGRES_HOST=db 
POSTGRES_PORT=5432

SECRET_KEY='' # Секретный ключ проекта из настроек
```
- Так же понадобиться добавить переменные в Action Secrets для работы с Workflow:
```
DOCKER_PASSWORD # Пароль от вашего акка на ДокерХабе
DOCKER_USERNAME # Ваш ник на ДокерХабе

USER # Username для подключения к серверу
HOST # IP сервера
PASSPHRASE # Пароль для сервера
SSH_KEY # Ваш SSH ключ

POSTGRES_ENGINE=django.db.backends.postgresql
POSTGRES_NAME=postgres # Имя БД
POSTGRES_USER=postgres # Пользователь БД
POSTGRES_PASSWORD=postgres #Пароль от БД
POSTGRES_HOST=db 
POSTGRES_PORT=5432

SECRET_KEY='' # Секретный ключ проекта из настроек

TELEGRAM_TO # ID чата, куда придет уведомление об успешном деплое.
TELEGRAM_TOKEN # Токен вашего бота
```

* После успешной сборки на сервере выполните команды:
    - Соберите статику:
    ```
    sudo docker compose exec backend python manage.py collectstatic
    ```
    - Примените миграции:
    ```
    sudo docker compose exec backend python manage.py migrate
    ```
    - Загрузите ингридиенты  в базу данных:  
    ```
       sudo docker compose exec backend python manage.py load_ingredients_data
    ```
    - Создать суперпользователя Django:
    ```
    sudo docker compose exec backend python manage.py createsuperuser
    ```
    - Проект будет доступен по вашему IP
