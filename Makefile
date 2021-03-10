PROJECT_NAME = Yamdb

all:
	@echo "make docker		- Скрипт для установки docker и docker-compose"
	@echo "make run		- Запуск контейнеров "
	@echo "make migrate		- Выполнить миграции "
	@echo "make fixtures		- Загрузить дамп fixtures.json в БД "
	@echo "make superuser		- Создать суперпользователя "
	@echo "make web		- Консоль web контейнера."
	@echo "make postgresql		- Консоль Posgresql контейнера."
	@echo "make nginx		- Консоль nginx контейнера."
	@echo "make stop		- Выключение контейнера."


install docker :
	#Загружаем скрипт для установки Docker-engine.
	curl -fsSL https://get.docker.com -o get-docker.sh
	#Запускаем скрипт для установки Docker-engine.
	sh get-docker.sh

run: 
	#docker-compose up Команда для сборки и запуска контейнера.
	#--build Сборка образа перед запуском контейнера.
	#-d Detached mode.
	docker-compose up --build -d 

web:
	#Запуск консоли для управления веб-контейнером. 
	docker-compose exec web bash

postgresql:
	#Запуск консоли для управления postgresql-контейнером.
	docker-compose exec db bash

nginx:
	#Запуск консоли для управления nginx-контейнером.
	docker-compose exec nginx bash

stop:
	#Остановка и удаление контейнеров, запущенных docker-compose up.
	docker-compose down

migrate:
	#Подключение к консоли веб-контейнера для создания миграций.
	docker-compose run web python manage.py makemigrations
	docker-compose run web python manage.py migrate

fixture:
	#Подключение к консоли веб-контейнера для загрузки бэкапа в базу данных.
	docker-compose run web python manage.py loaddata fixtures.json
	
superuser:
	#Подключение к консоли веб-контейнера для создания Суперпользователя(администратор).
	docker-compose run web python manage.py createsuperuser


