# Generated by Django 2.2.9 on 2020-01-22 16:44

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('importer', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='importer',
            name='channel',
            field=models.CharField(default=uuid.UUID('90947be2-8d23-462f-887c-e341fd193b12'), max_length=100, unique=True),
        ),
    ]
