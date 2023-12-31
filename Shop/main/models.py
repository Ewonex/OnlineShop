from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth.models import AbstractUser, Permission, Group
from datetime import datetime


class User(AbstractUser):
    password = models.CharField('Пароль', max_length=200)
    email = models.CharField('Email', max_length=30)
    USERNAME_FIELD = 'username'
    def __str__(self):
        return self.username
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def save(self, *args, **kwargs):
        if self.password and (not self.pk or self._password != self.password):
            self.set_password(self.password)
        super().save(*args, **kwargs)

class Item(models.Model):
    brand = models.ForeignKey('Brand', on_delete=models.SET_NULL, null=True, default=None, blank=True)
    name = models.CharField('Название товара', max_length=100)
    price = models.FloatField('Цена товара', validators=[MinValueValidator(0), MaxValueValidator(999999999)], default=0)
    discount = models.IntegerField('Скидка на товар', default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    description = models.CharField('Описание товара', max_length=1000)
    pic = models.ImageField('Картинка товара')
    tags = models.CharField('Тэги', max_length=500, default='')
    forMales = models.BooleanField('Для мужчин', default=True)
    forFemales = models.BooleanField('Для женщин', default=True)
    forChildren = models.BooleanField('Для детей', default=False)
    category = models.CharField('Категория товара',  max_length=20, default='Одежда')
    mark = models.FloatField('Оценка товара', validators=[MinValueValidator(0), MaxValueValidator(5)], default=5)

    @property
    def discountPrice(self):
        return self.price * (100-self.discount)/100

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
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    item = models.ForeignKey('Item', on_delete=models.CASCADE)
    def __str__(self):
        return f'{self.user} - {self.item}'
    class Meta:
        verbose_name = 'Избранный товар'
        verbose_name_plural = 'Избранные товары'

class Vacansy(models.Model):
    title = models.CharField('Заголовок вакансии', max_length=30)
    post = models.CharField('Должность вакансии', max_length=30)
    description = models.CharField('Описание должности', max_length=300)
    skills = models.CharField('Навыки', max_length=300)
    salary = models.IntegerField('Примерная З.П.', default=0, validators=[MinValueValidator(0)])
    dateOfPublishment = models.DateField('Дата публикации')
    def __str__(self):
        return f'{self.title}'
    class Meta:
        verbose_name = 'Вакансия'
        verbose_name_plural = 'Вакансии'

class Article(models.Model):
    title = models.CharField('Заголовок статьи', max_length=100)
    theme = models.CharField('Тема статьи', max_length=400)
    text = models.CharField('Текст статьи', max_length=1000)
    pic = models.ImageField('Картинка для статьи', null=True, default=None, blank=True)
    dateOfPublish = models.DateField('Дата публикации', default=datetime.now)
    def __str__(self):
        return f'{self.title}'
    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'

class Review(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    item = models.ForeignKey('Item', on_delete=models.CASCADE)
    mark = models.IntegerField('Оценка', default=0, validators=[MinValueValidator(0), MaxValueValidator(5)])
    text = models.CharField('Текст отзыва', max_length=300)
    datetime = models.DateTimeField('Дата отзыва', default=datetime.now)
    def __str__(self):
        return f'{self.user} - {self.item} - {self.mark}'
    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

class ReturningRequest(models.Model):
    STATUS_CHOICES = [
        ('В обработке', 'В обработке'),
        ('Отклонен', 'Отклонен'),
        ('Подтвержден', 'Подтвержден'),
    ]

    user = models.ForeignKey('User', on_delete=models.CASCADE)
    item = models.ForeignKey('Item', on_delete=models.CASCADE)
    text = models.CharField('Причина вовзрата', max_length=500)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='В обработке')
    def __str__(self):
        return f'{self.user} - {self.item} - {self.status}'
    class Meta:
        verbose_name = 'Запрос'
        verbose_name_plural = 'Запросы'

class BucketItem(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    item = models.ForeignKey('Item', on_delete=models.CASCADE)
    amount = models.IntegerField('Количество', default=1, validators=[MinValueValidator(1), MaxValueValidator(500)])
    @property
    def totalPrice(self):
        return self.amount * self.item.discountPrice
    def __str__(self):
        return f"{self.user.username} - {self.item.name}"
    class Meta:
        verbose_name = 'Товар корзины'
        verbose_name_plural = 'Товары корзины'

class Order(models.Model):
    STATUS_CHOICES = [
        ('В обработке', 'В обработке'),
        ('Отклонен', 'Отклонен'),
        ('Подтвержден', 'Подтвержден'),
    ]

    user = models.ForeignKey('User', on_delete=models.CASCADE)
    datetime = models.DateTimeField('Дата отзыва', default=datetime.now)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='В обработке')
    totalPrice = models.IntegerField('Цена заказа', validators=[MinValueValidator(0), MaxValueValidator(999999999)], blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.id} - {self.status}"
    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

class ItemOfTheOrder(models.Model):
    order = models.ForeignKey('Order', on_delete=models.CASCADE)
    item = models.ForeignKey('Item', on_delete=models.CASCADE)
    amount = models.IntegerField('Количество', default=1, validators=[MinValueValidator(1), MaxValueValidator(500)])
    totalPrice = models.IntegerField('Цена заказа', validators=[MinValueValidator(0), MaxValueValidator(999999999)], blank=True)

    def __str__(self):
        return f"{self.order} - {self.item} - {self.amount}шт."
    class Meta:
        verbose_name = 'Продукт заказа'
        verbose_name_plural = 'Продукты заказов'