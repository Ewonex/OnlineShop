# Generated by Django 4.2.3 on 2023-07-26 12:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_brand'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='password',
            field=models.CharField(max_length=200, verbose_name='Пароль'),
        ),
    ]