#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

""" 
Запустить локальный сервер:
python manage.py runserver

Создать приложение:
python manage.py startapp <Название приложения>
После создания нужно зарегистрировать приложение в settings.py,
то есть добавить "<Название приложения>" в массив INSTALLED_APPS

Для того, чтобы начать отслеживать url адрес,
нужно добавить path("", include("<Название приложения>.urls")) 
в urlpatterns в файле urls.py главного приложения проекта.
Далее нужно создать файл urls.py в созданном приложении с таким содержанием:
<from django.urls import path
from . import views

urlpatterns = [
    # Отслеживаем все, что после /singers/
    path("", views.<Метод в файле views (без ())>, name="<Метод в файле views (без ())>")
]>.

Убить:
control + c
"""

"""
Создать администратора:
python manage.py createsuperuser
"""

"""
Зарегистрировать таблицу в панели администратора:
Заходим в файл admin.py
"""



def main():
    """Run administrative tasks."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "albotracker.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
