# WEB сервис FOODGRAM
![Build Status](https://github.com/Vadim3x4/yamdb_final/workflows/Yamdb-app%20workflow/badge.svg)

#### Проверить сервис можно по адресу - http://http://178.154.195.50/

FOODGRAM это онлайн-сервис для публикации рецептов. В функционал сервиса входит: публикация рецептов, возможность подписываться на других пользователей, добавлять понравившиеся рецепты в список «Избранное». Также доступна функция скачивания списка продуктов, для выбранных рецептов.

## Быстрая установка используя make.
```bash
make                    - Показать доступные команды
make docker		- Запуск скрипта для установки docker и docker-compose
make run		- Запуск контейнеров 
make migrate		- Выполнить миграции 
make fixtures		- Загрузить дамп fixtures.json в БД 
make superuser		- Создать суперпользователя 
make web		- Консоль web контейнера.
make postgresql		- Консоль Posgresql контейнера.
make nginx		- Консоль nginx контейнера.
make stop		- Выключение контейнера.

```
## Ручная установка.

### 1. Установка docker и docker-compose:
Для запуска проекта требуется установка Docker и Docker-compose
(https://docs.docker.com/engine/install/).

### 2. По данному шаблону создайте файл .env в основной директории:
```bash
DB_NAME=
POSTGRES_USER=
POSTGRES_PASSWORD=
DB_HOST=
DB_PORT=
```
### 3. Запуск контейнера:
```bash
docker-compose up --build -d
```
### 4. Миграции:
Для входа в контейнер выполните команду:
```bash
docker-compose exec web bash
```
Выполните миграции 
```bash
python manage.py makemigrations
python manage.py migrate
```
### 5. Запуск автотестов:
```bash
pytest
```
### 6. Инициализации стартовых данных:
```bash
python manage.py loaddata fixtures.json
```
### 7. Создание суперпользователя:
```bash
python manage.py createsuperuser
```
### 8. Выйти из контейнера:
```bash
exit
```
### 9. Остановить контейнер:
```bash
docker-compose down
```

### Используемые технологии: Python 3.8.5, Django, Django REST, PostgreSQL, Nginx, Docker.
### Авторы [Vadim3x4](https://github.com/Vadim3x4)


