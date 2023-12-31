"""
Django settings for albotracker project.

Generated by 'django-admin startproject' using Django 5.0.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""
import os
from pathlib import Path


# Полный путь к проекту
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# Секретный ключ приложения, перед выгрузкой на сервер, поменять
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-zf6gtj=e77ff^^5dkb=-=q&9^6ki1jp+54&d7b9r=22lwaa=pq"

# Если тру - все ошибки, которые будут возникать, будут показаны на страничке веб-сайта
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Доменные имена на которы будет разрешено опубликовать данный проект
ALLOWED_HOSTS = []

AUTH_USER_MODEL = 'users.CustomUser'

# LOGOUT_REDIRECT_URL = 'users/users_login'

# Application definition

# Набор установленных приложений, которые есть в проекте
INSTALLED_APPS = [
    "main",
    "singers",
    "tracks",
    "albums_singles",
    "users",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

# Промежуточное ПО - те классы/плагины/библиотеки, которые обеспечивают
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",  # безопасность внутри проекта
    "django.contrib.sessions.middleware.SessionMiddleware",  # работу с сессиями
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",  # поддержку csr токенов
    "django.contrib.auth.middleware.AuthenticationMiddleware",  # классы для авторизации внутри проекта
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# Основной файл urls для всего проекта
ROOT_URLCONF = "albotracker.urls"

# Шаблоны
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "albotracker.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = "ru"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
