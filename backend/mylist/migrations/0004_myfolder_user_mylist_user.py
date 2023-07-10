# Generated by Django 4.2.2 on 2023-07-07 05:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mylist', '0003_alter_mylist_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='myfolder',
            name='user',
            field=models.ForeignKey(default='none', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, to_field='user_id'),
        ),
        migrations.AddField(
            model_name='mylist',
            name='user',
            field=models.ForeignKey(default='none', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, to_field='user_id'),
        ),
    ]
