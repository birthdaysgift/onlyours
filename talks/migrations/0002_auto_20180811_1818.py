# Generated by Django 2.0.7 on 2018-08-11 15:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('talks', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='message',
            old_name='message',
            new_name='text',
        ),
    ]