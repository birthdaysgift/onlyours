# Generated by Django 2.1.7 on 2019-04-14 18:17

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('photos', '0004_auto_20190414_1654'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='UserPhoto',
            new_name='PostedPhoto',
        ),
    ]
