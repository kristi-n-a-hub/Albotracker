# Generated by Django 5.0 on 2023-12-26 02:49

import singers.models
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Genre",
            fields=[
                (
                    "genre_id",
                    models.AutoField(
                        primary_key=True,
                        serialize=False,
                        verbose_name="Идентификатор жанра",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        max_length=50, unique=True, verbose_name="Название жанра"
                    ),
                ),
            ],
            options={
                "verbose_name": "Жанр",
                "verbose_name_plural": "Жанры",
            },
        ),
        migrations.CreateModel(
            name="Singer",
            fields=[
                (
                    "singer_id",
                    models.AutoField(
                        primary_key=True,
                        serialize=False,
                        verbose_name="Идентификатор исполнителя",
                    ),
                ),
                (
                    "alias",
                    models.CharField(
                        default="",
                        max_length=50,
                        unique=True,
                        verbose_name="Псевдоним исполнителя",
                    ),
                ),
                (
                    "photo",
                    models.ImageField(
                        default="singers/img/0_img_singer.png",
                        upload_to=singers.models.singer_photo_path,
                        verbose_name="Фото исполнителя",
                    ),
                ),
                (
                    "genres",
                    models.ManyToManyField(related_name="singers", to="singers.genre"),
                ),
            ],
            options={
                "verbose_name": "Исполнитель",
                "verbose_name_plural": "Исполнители",
            },
        ),
    ]