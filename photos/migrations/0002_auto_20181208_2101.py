# Generated by Django 2.0.7 on 2018-12-08 18:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('photos', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photodislike',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='photodislike',
            name='userphoto',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='photos.UserPhoto'),
        ),
        migrations.AlterField(
            model_name='photolike',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='photolike',
            name='userphoto',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='photos.UserPhoto'),
        ),
        migrations.AlterField(
            model_name='userphoto',
            name='date',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='userphoto',
            name='photo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='photos.Photo'),
        ),
        migrations.AlterField(
            model_name='userphoto',
            name='time',
            field=models.TimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='userphoto',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
