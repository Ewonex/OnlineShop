# Generated by Django 4.2.3 on 2023-08-05 14:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_alter_item_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='description',
            field=models.CharField(max_length=1000, verbose_name='Описание товара'),
        ),
    ]