from django.contrib.auth.models import AbstractUser, Group
from django.db import models
from django.db.models.signals import pre_delete, pre_save, post_save
from django.dispatch import receiver
import os


def user_photo_path(instance, filename):
    # Если id не None, значит, это редактирование
    if instance.user_id:
        extension = filename.split('.')[-1]
        return os.path.join('users', 'img', f'{instance.user_id}_{instance.username}_user.{extension}')
    else:
        # Определение максимального id в базе данных
        max_id = CustomUser.objects.aggregate(models.Max('user_id'))['user_id__max'] or 0
        # Определение следующего доступного id
        next_id = max_id + 1

        # Получаем расширение файла
        extension = filename.split('.')[-1]
        # Формируем путь относительно медиа-каталога
        return os.path.join('users', 'img', f'{next_id}_{instance.username}_user.{extension}')


class CustomUser(AbstractUser):
    user_id = models.BigAutoField('Идентификатор пользователя', primary_key=True)
    username = models.CharField('Никнэйм', max_length=150, unique=True, blank=False, default="")
    email = models.EmailField('Адрес электронной почты', unique=True, blank=False, default="")
    first_name = models.CharField('Имя', max_length=30, default="")
    last_name = models.CharField('Фамилия', max_length=30, default="")
    user_photo = models.ImageField('Фото пользователя', upload_to=user_photo_path, default="users/img/0_img_user.png")

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


@receiver(pre_delete, sender=CustomUser)
def user_pre_delete(sender, instance, **kwargs):
    # Удаление файла при удалении пользователя
    if instance.user_photo and instance.user_photo.name != "users/img/0_img_user.png":
        if os.path.isfile(instance.user_photo.path):
            os.remove(instance.user_photo.path)


@receiver(pre_save, sender=CustomUser)
def user_pre_save(sender, instance, **kwargs):
    # Если у экземпляра CustomUser уже есть id и изображение было изменено
    if instance.user_id and instance.user_photo and not instance.user_photo.name.startswith(f"users/img/{instance.user_id}_"):
        # Текущий файл изображения
        current_photo = CustomUser.objects.get(user_id=instance.user_id).user_photo
        # Проверяем, существует ли текущий файл и не является ли он стандартным
        if current_photo and not current_photo.name.startswith("users/img/0_img_user.png"):
            # Удаляем текущий файл изображения
            if os.path.isfile(current_photo.path):
                os.remove(current_photo.path)
    elif not instance.user_photo:  # Если фото не предоставлено, устанавливаем фото по умолчанию
        instance.user_photo.name = "users/img/0_img_user.png"


@receiver(post_save, sender=CustomUser)
def add_photo_after_save_user(sender, instance, **kwargs):
    # Проверка, чтобы избежать бесконечной рекурсии
    if not getattr(instance, '_adding_user_photo', False):
        # Устанавливаем атрибут, чтобы избежать повторного вызова при сохранении
        instance._adding_user_photo = True

        # Формируем новое имя файла с учетом текущего id
        extension = instance.user_photo.name.split('.')[-1]
        new_filename = f"users/img/{instance.user_id}_{instance.username}_user.{extension}"

        # Получаем путь к текущему файлу изображения
        current_path = instance.user_photo.path
        print(current_path)

        if "/users/img/0_img_user.png" not in current_path:
            # Переименовываем файл
            os.rename(current_path, os.path.join('media', new_filename))

            # Обновляем поле 'user_photo' в объекте, чтобы отразить новое имя файла в базе данных
            instance.user_photo.name = new_filename
            instance.save(update_fields=['user_photo'])

        # Удаляем атрибут после выполнения
        del instance._adding_user_photo


@receiver(post_save, sender=CustomUser)
def add_to_default_group(sender, instance, created, **kwargs):
    if created:
        # Проверяем, что пользователь только что создан
        default_group_name = 'registered'

        try:
            # Пытаемся получить группу
            default_group = Group.objects.get(name=default_group_name)
        except Group.DoesNotExist:
            # Если группа не существует, создаем ее
            default_group = Group.objects.create(name=default_group_name)

        # Проверяем, что пользователь не состоит уже в этой группе
        if not instance.groups.filter(name=default_group_name).exists():
            instance.groups.add(default_group)
