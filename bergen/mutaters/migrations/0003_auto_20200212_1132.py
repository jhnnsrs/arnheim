# Generated by Django 2.2.9 on 2020-02-12 11:32

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('mutaters', '0002_auto_20200131_1243'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mutater',
            name='channel',
            field=models.CharField(default=uuid.UUID('b3fa20f3-bc44-4576-a4be-8f3dbc5c4a32'), max_length=100, unique=True),
        ),
    ]
