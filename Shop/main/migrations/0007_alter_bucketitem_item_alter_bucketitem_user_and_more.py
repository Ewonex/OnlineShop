# Generated by Django 4.2.3 on 2023-08-07 13:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_alter_item_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bucketitem',
            name='item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.item'),
        ),
        migrations.AlterField(
            model_name='bucketitem',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='favoriteitem',
            name='item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.item'),
        ),
        migrations.AlterField(
            model_name='favoriteitem',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='itemoftheorder',
            name='item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.item'),
        ),
        migrations.AlterField(
            model_name='order',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='returningrequest',
            name='item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.item'),
        ),
        migrations.AlterField(
            model_name='returningrequest',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='review',
            name='item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.item'),
        ),
        migrations.AlterField(
            model_name='review',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
