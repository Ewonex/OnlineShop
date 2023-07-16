from django.db import models
from django.contrib.auth.models import AbstractUser, Permission, Group


class User(AbstractUser):
    username = models.CharField('Логин', max_length=20)
    password = models.CharField('Пароль', max_length=20)
    email = models.CharField('Email', max_length=30)
    USERNAME_FIELD = 'username'
    def __str__(self):
        return self.username

    groups = models.ManyToManyField(
        Group,
        verbose_name='Группы',
        blank=True,
        related_name='custom_user_set'
    )

    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='Разрешения',
        blank=True,
        related_name='custom_user_set'
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'