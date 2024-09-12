#!/bin/bash

# Переход в рабочую директорию проекта
cd /root/site || exit

# Обновление репозитория
git fetch origin
git reset --hard origin/main

source venv/bin/activate

# Установка зависимостей
pip install -r requirements.txt

deactivate

# Выполнение миграций и других задач
python manage.py migrate
python manage.py collectstatic --noinput

# Перезагрузка сервера
systemctl restart gunicorn  # Замените на вашу службу, например, gunicorn или uwsgi
