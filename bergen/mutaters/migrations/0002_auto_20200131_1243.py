# Generated by Django 2.2.9 on 2020-01-31 12:43

import uuid

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mutaters', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mutater',
            name='channel',
            field=models.CharField(default=uuid.UUID('603c3eaa-6882-496e-96ce-b4522e7c5653'), max_length=100, unique=True),
        ),
    ]