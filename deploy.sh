#!/bin/bash

# Логирование
su root

# Переход в рабочую директорию проекта
cd /root/site || exit

# Активация виртуального окружения
source venv/bin/activate

# Обновление репозитория
git fetch origin
git reset --hard origin/main

# Установка зависимостей
pip install -r requirements.txt

# Выполнение миграций и других задач
python manage.py migrate
python manage.py collectstatic --noinput

# Перезагрузка сервера
sudo systemctl restart gunicorn  # Замените на вашу службу, например, gunicorn или uwsgi
