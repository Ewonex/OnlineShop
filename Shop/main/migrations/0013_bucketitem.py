# Generated by Django 4.2.3 on 2023-07-30 18:10

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0012_returningrequest'),
    ]

    operations = [
        migrations.CreateModel(
            name='BucketItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField(default=1, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(500)], verbose_name='Количество')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='main.item')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Товар корзины',
                'verbose_name_plural': 'Товары корзины',
            },
        ),
    ]
