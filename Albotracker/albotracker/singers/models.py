from django.db import models
from django.db.models.signals import pre_delete, pre_save, post_save
from django.dispatch import receiver
from django.db.models import Max
import os

# 1) Создание миграций:
# python manage.py makemigrations
#
# 2) Выполнение файлов миграции
# python manage.py migrate


class Genre(models.Model):
    genre_id = models.AutoField('Идентификатор жанра', primary_key=True)
    name = models.CharField('Название жанра', max_length=50, blank=False, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


def singer_photo_path(instance, filename):
    # Если id не None, значит, это редактирование
    if instance.singer_id:
        extension = filename.split('.')[-1]
        return os.path.join('singers', 'img', f'{instance.singer_id}_{instance.alias}_singer.{extension}')
    else:
        # Определение максимального id в базе данных
        max_id = Singer.objects.aggregate(Max('singer_id'))['singer_id__max'] or 0
        # Определение следующего доступного id
        next_id = max_id + 1

        # Получаем расширение файла
        extension = filename.split('.')[-1]
        # Формируем путь относительно медиа-каталога
        return os.path.join('singers', 'img', f'{next_id}_{instance.alias}_singer.{extension}')


class Singer(models.Model):
    singer_id = models.AutoField('Идентификатор исполнителя', primary_key=True)
    alias = models.CharField('Псевдоним исполнителя', max_length=50, blank=False, unique=True, default="")
    photo = models.ImageField('Фото исполнителя', upload_to=singer_photo_path, default="singers/img/0_img_singer.png")
    genres = models.ManyToManyField(Genre, related_name='singers', blank=False)

    def __str__(self):
        return self.alias

    class Meta:
        verbose_name = 'Исполнитель'
        verbose_name_plural = 'Исполнители'


@receiver(pre_delete, sender=Singer)
def singer_pre_delete(sender, instance, **kwargs):
    # Удаление файла при удалении исполнителя
    if instance.photo and instance.photo.name != "singers/img/0_img_singer.png":
        if os.path.isfile(instance.photo.path):
            os.remove(instance.photo.path)


# Добавление слушателя для события pre_save
@receiver(pre_save, sender=Singer)
def singer_pre_save(sender, instance, **kwargs):
    # Если у экземпляра Singer уже есть id и изображение было изменено
    if instance.singer_id and instance.photo and not instance.photo.name.startswith(f"singers/img/{instance.singer_id}_"):
        # Текущий файл изображения
        current_photo = Singer.objects.get(singer_id=instance.singer_id).photo
        # Проверяем, существует ли текущий файл и не является ли он стандартным
        if current_photo and not current_photo.name.startswith("singers/img/0_img_singer.png"):
            # Удаляем текущий файл изображения
            if os.path.isfile(current_photo.path):
                os.remove(current_photo.path)
    elif not instance.photo:  # Если фото не предоставлено, устанавливаем фото по умолчанию
        instance.photo.name = "singers/img/0_img_singer.png"


# Сигнал post_save, который будет вызываться после сохранения объекта Singer
@receiver(post_save, sender=Singer)
def add_photo_after_save(sender, instance, **kwargs):
    # Проверка, чтобы избежать бесконечной рекурсии
    if not getattr(instance, '_adding_photo', False):
        # Устанавливаем атрибут, чтобы избежать повторного вызова при сохранении
        instance._adding_photo = True

        # Формируем новое имя файла с учетом текущего id
        extension = instance.photo.name.split('.')[-1]
        new_filename = f"singers/img/{instance.singer_id}_{instance.alias}_singer.{extension}"

        # Получаем путь к текущему файлу изображения
        current_path = instance.photo.path
        print(current_path)

        if "/singers/img/0_img_singer.png" not in current_path:
            # Переименовываем файл
            os.rename(current_path, os.path.join('media', new_filename))

            # Обновляем поле 'photo' в объекте, чтобы отразить новое имя файла в базе данных
            instance.photo.name = new_filename
            instance.save(update_fields=['photo'])

        # Удаляем атрибут после выполнения
        del instance._adding_photo
