# Generated by Django 4.2.3 on 2023-07-16 13:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_alter_user_managers_user_date_joined_user_first_name_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='login',
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(max_length=20, verbose_name='Логин'),
        ),
    ]
