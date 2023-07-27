from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth.models import AbstractUser, Permission, Group


class User(AbstractUser):
    password = models.CharField('Пароль', max_length=200)
    email = models.CharField('Email', max_length=30)
    USERNAME_FIELD = 'username'
    def __str__(self):
        return self.username
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

class Item(models.Model):
    name = models.CharField('Название товара', max_length=30)
    price = models.IntegerField('Цена товара', validators=[MinValueValidator(0), MaxValueValidator(999999999)])
    discount = models.IntegerField('Скидка на товар', default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    description = models.CharField('Описание товара', max_length=250)
    pic = models.ImageField('Картинка товара')
    tags = models.CharField('Тэги', max_length=500, default='')
    forMales = models.BooleanField('Для мужчин', default=True)
    forFemales = models.BooleanField('Для женщин', default=True)
    forChildren = models.BooleanField('Для детей', default=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

class Brand(models.Model):
    name = models.CharField('Имя бренда', max_length=30)
    siteLink = models.CharField('Ссылка на сайт', max_length=250)
    pic = models.ImageField('Картинка бренда')
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = 'Бренд'
        verbose_name_plural = 'Бренды'

class FavoriteItem(models.Model):
    user = models.ForeignKey('User', on_delete=models.PROTECT)
    item = models.ForeignKey('Item', on_delete=models.PROTECT)
    def __str__(self):
        return f'{self.user} - {self.item}'
    class Meta:
        verbose_name = 'Избранный товар'
        verbose_name_plural = 'Избранные товары'