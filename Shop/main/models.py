from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth.models import AbstractUser, Permission, Group


class User(AbstractUser):
    password = models.CharField('Пароль', max_length=20)
    email = models.CharField('Email', max_length=30)
    USERNAME_FIELD = 'username'
    def __str__(self):
        return self.username

    # groups = models.ManyToManyField(
    #     Group,
    #     verbose_name='Группы',
    #     blank=True,
    #     related_name='custom_user_set'
    # )
    #
    # user_permissions = models.ManyToManyField(
    #     Permission,
    #     verbose_name='Разрешения',
    #     blank=True,
    #     related_name='custom_user_set'
    # )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

class Item(models.Model):
    name = models.CharField('Название товара', max_length=20)
    price = models.IntegerField('Цена товара', validators=[MinValueValidator(0), MaxValueValidator(999999999)])
    discount = models.IntegerField('Скидка на товар', default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    description = models.CharField('Описание товара', max_length=250)
    pic = models.ImageField('Картинка товара')
    tags = models.CharField('Тэги', max_length=500, default='')
    forMales = models.BooleanField('Для мужчин', default=True)
    forChildren = models.BooleanField('Для детей', default=False)


    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'