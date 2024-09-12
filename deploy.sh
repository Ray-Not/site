#!/bin/bash

# Переход в рабочую директорию проекта
cd /root/site || exit

# Обновление репозитория
git fetch origin
git reset --hard origin/main

# Установка зависимостей
pip install -r requirements.txt

# Выполнение миграций и других задач
python3 manage.py migrate
python3 manage.py collectstatic --noinput

# Перезагрузка сервера
systemctl restart gunicorn  # Замените на вашу службу, например, gunicorn или uwsgi
