# Generated by Django 4.2.3 on 2023-07-24 14:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_item_forchildren_item_formales_item_tags_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='forFemales',
            field=models.BooleanField(default=True, verbose_name='Для женщин'),
        ),
        migrations.AlterField(
            model_name='item',
            name='forMales',
            field=models.BooleanField(default=True, verbose_name='Для мужчин'),
        ),
        migrations.AlterField(
            model_name='item',
            name='name',
            field=models.CharField(max_length=30, verbose_name='Название товара'),
        ),
    ]
