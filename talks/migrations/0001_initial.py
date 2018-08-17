# Generated by Django 2.0.7 on 2018-08-16 06:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth_custom', '0001_initial'),
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
                ('receiver', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='receiver', to='auth_custom.User')),
            ],
            bases=('talks.publicmessage',),
        ),
        migrations.AddField(
            model_name='publicmessage',
            name='sender',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.DO_NOTHING, related_name='sender', to='auth_custom.User'),
        ),
    ]
