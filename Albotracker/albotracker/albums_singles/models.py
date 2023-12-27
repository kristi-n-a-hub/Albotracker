from django.db import models
from django.db.models.signals import pre_delete, pre_save, post_save
from django.dispatch import receiver
from django.db.models import Max
from tracks.models import Track
import os


class Single(models.Model):
    single_id = models.AutoField('Идентификатор сингла', primary_key=True)  # Идентификатор сингла

    # Связь один к одному с моделью Track (каждый сингл относится к одному треку)
    track = models.OneToOneField(Track, on_delete=models.CASCADE, related_name='singles', blank=False)

    class Meta:
        verbose_name = 'Сингл'
        verbose_name_plural = 'Синглы'


def album_cover_path(instance, filename):
    # Если id не None, значит, это редактирование
    if instance.album_id:
        extension = filename.split('.')[-1]
        return os.path.join('albums', 'img', f'{instance.album_id}_{instance.title}_album.{extension}')
    else:
        # Определение максимального id в базе данных
        max_id = Album.objects.aggregate(Max('album_id'))['album_id__max'] or 0
        # Определение следующего доступного id
        next_id = max_id + 1

        # Получаем расширение файла
        extension = filename.split('.')[-1]
        # Формируем путь относительно медиа-каталога
        return os.path.join('albums', 'img', f'{next_id}_{instance.title}_album.{extension}')


class Album(models.Model):
    album_id = models.AutoField('Идентификатор альбома', primary_key=True)
    title = models.CharField('Название альбома', max_length=50, blank=False, default="")
    release_year = models.IntegerField('Год выпуска альбома', blank=False)
    cover = models.ImageField('Обложка альбома', upload_to=album_cover_path, default="albums/img/0_img_album.png")  # Обложка альбома (картинка)
    tracks = models.ManyToManyField(Track, related_name='albums', blank=False)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Альбом'
        verbose_name_plural = 'Альбомы'


@receiver(pre_delete, sender=Album)
def album_pre_delete(sender, instance, **kwargs):
    # Удаление файла при удалении альбома
    if instance.cover and instance.cover.name != "albums/img/0_img_album.png":
        if os.path.isfile(instance.cover.path):
            os.remove(instance.cover.path)


# Добавление слушателя для события pre_save
@receiver(pre_save, sender=Album)
def album_pre_save(sender, instance, **kwargs):
    # Если у экземпляра Album уже есть id и изображение было изменено
    if instance.album_id and instance.cover and not instance.cover.name.startswith(f"albums/img/{instance.album_id}_"):
        # Текущий файл обложки
        current_cover = Album.objects.get(album_id=instance.album_id).cover
        # Проверяем, существует ли текущий файл и не является ли он стандартным
        if current_cover and not current_cover.name.startswith("albums/img/0_img_album.png"):
            # Удаляем текущий файл обложки
            if os.path.isfile(current_cover.path):
                os.remove(current_cover.path)


# Сигнал post_save, который будет вызываться после сохранения объекта Album
@receiver(post_save, sender=Album)
def add_cover_after_save(sender, instance, **kwargs):
    # Проверка, чтобы избежать бесконечной рекурсии
    if not getattr(instance, '_adding_cover', False):
        # Устанавливаем атрибут, чтобы избежать повторного вызова при сохранении
        instance._adding_cover = True

        # Формируем новое имя файла с учетом текущего id
        extension = instance.cover.name.split('.')[-1]
        new_filename = f"albums/img/{instance.album_id}_{instance.title}_album.{extension}"

        # Получаем путь к текущему файлу обложки
        current_path = instance.cover.path

        if "/albums/img/0_img_album.png" not in current_path:
            # Переименовываем файл
            os.rename(current_path, os.path.join('media', new_filename))

            # Обновляем поле 'cover' в объекте, чтобы отразить новое имя файла в базе данных
            instance.cover.name = new_filename
            instance.save(update_fields=['cover'])

        # Удаляем атрибут после выполнения
        del instance._adding_cover
