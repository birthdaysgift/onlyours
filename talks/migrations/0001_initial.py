# Generated by Django 2.0.5 on 2018-08-15 06:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='PublicMessage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now_add=True)),
                ('time', models.TimeField(auto_now_add=True)),
                ('text', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='PrivateMessage',
            fields=[
                ('publicmessage_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='talks.PublicMessage')),
                ('receiver', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='receiver', to=settings.AUTH_USER_MODEL)),
            ],
            bases=('talks.publicmessage',),
        ),
        migrations.AddField(
            model_name='publicmessage',
            name='sender',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.DO_NOTHING, related_name='sender', to=settings.AUTH_USER_MODEL),
        ),
    ]
