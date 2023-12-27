from django.db import models
from django.db.models.signals import pre_delete, pre_save, post_save
from django.dispatch import receiver
from django.db.models import Max
from singers.models import Singer, Genre
from django.core.validators import FileExtensionValidator
import os


def track_photo_path(instance, filename):
    if instance.track_id:
        extension = filename.split('.')[-1]
        return os.path.join('tracks', 'img', f'{instance.track_id}_{instance.title}_track.{extension}')
    else:
        max_id = Track.objects.aggregate(Max('track_id'))['track_id__max'] or 0
        next_id = max_id + 1

        extension = filename.split('.')[-1]
        return os.path.join('tracks', 'img', f'{next_id}_{instance.title}_track.{extension}')


def track_audio_path(instance, filename):
    if instance.track_id:
        extension = filename.split('.')[-1]
        return os.path.join('tracks', 'audio', f'{instance.track_id}_{instance.title}_track.{extension}')
    else:
        max_id = Track.objects.aggregate(Max('track_id'))['track_id__max'] or 0
        next_id = max_id + 1

        extension = filename.split('.')[-1]
        return os.path.join('tracks', 'audio', f'{next_id}_{instance.title}_track.{extension}')


class Track(models.Model):
    track_id = models.AutoField('Идентификатор трека', primary_key=True)
    title = models.CharField('Название трека', max_length=50, blank=False, default="")
    release_year = models.IntegerField('Год выпуска трека', blank=False)
    cover = models.ImageField('Обложка трека', upload_to=track_photo_path, default="tracks/img/0_img_track.png")
    audio = models.FileField(
        'Аудио запись трека',
        upload_to=track_audio_path,
        blank=False,
        validators=[
            FileExtensionValidator(allowed_extensions=['mp3', 'wav', 'ogg', 'flac', 'mp4'])  # Добавьте нужные расширения
        ]
    )
    genres = models.ManyToManyField(Genre, related_name='tracks', blank=False)
    singers = models.ManyToManyField(Singer, related_name='tracks', blank=False)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Трек'
        verbose_name_plural = 'Треки'


@receiver(pre_delete, sender=Track)
def track_pre_delete(sender, instance, **kwargs):
    if instance.cover and instance.cover.name != "tracks/img/0_img_track.png":
        if os.path.isfile(instance.cover.path):
            os.remove(instance.cover.path)

    if instance.audio:
        if os.path.isfile(instance.audio.path):
            os.remove(instance.audio.path)


@receiver(pre_save, sender=Track)
def track_pre_save(sender, instance, **kwargs):
    if instance.track_id and instance.cover and not instance.cover.name.startswith(f"tracks/img/{instance.track_id}_"):
        current_cover = Track.objects.get(track_id=instance.track_id).cover
        if current_cover and not current_cover.name.startswith("tracks/img/0_img_track.png"):
            if os.path.isfile(current_cover.path):
                os.remove(current_cover.path)
    elif not instance.cover:  # Если фото не предоставлено, устанавливаем фото по умолчанию
        instance.cover.name = "tracks/img/0_img_track.png"

    # if instance.track_id and instance.audio and not instance.audio.name.startswith(
    #         f"tracks/audio/{instance.track_id}_"):
    #     current_audio = Track.objects.get(track_id=instance.track_id).audio
    #     if current_audio:
    #         if os.path.isfile(current_audio.path):
    #             os.remove(current_audio.path)


@receiver(post_save, sender=Track)
def add_files_after_save(sender, instance, **kwargs):
    if not getattr(instance, '_adding_files', False):
        instance._adding_files = True

        extension_cover = instance.cover.name.split('.')[-1]
        new_cover_filename = f"tracks/img/{instance.track_id}_{instance.title}_track.{extension_cover}"

        current_cover_path = instance.cover.path
        print(current_cover_path)

        if "/tracks/img/0_img_track.png" not in current_cover_path:
            os.rename(current_cover_path, os.path.join('media', new_cover_filename))
            instance.cover.name = new_cover_filename
            instance.save(update_fields=['cover'])

        extension_audio = instance.audio.name.split('.')[-1]
        new_audio_filename = f"tracks/audio/{instance.track_id}_{instance.title}_track.{extension_audio}"

        current_audio_path = instance.audio.path
        print(current_audio_path)

        os.rename(current_audio_path, os.path.join('media', new_audio_filename))
        instance.audio.name = new_audio_filename
        instance.save(update_fields=['audio'])

        del instance._adding_files

