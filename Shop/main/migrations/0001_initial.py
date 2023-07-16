# Generated by Django 4.2.3 on 2023-07-16 12:04

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('login', models.CharField(max_length=20, verbose_name='Логин')),
                ('password', models.CharField(max_length=20, verbose_name='Пароль')),
                ('email', models.CharField(max_length=30, verbose_name='Email')),
            ],
            options={
                'verbose_name': 'Пользователь',
                'verbose_name_plural': 'Пользователи',
            },
        ),
    ]
