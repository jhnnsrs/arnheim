# Generated by Django 2.2.9 on 2020-01-28 13:06

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('mutaters', '0006_auto_20200123_1122'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mutater',
            name='channel',
            field=models.CharField(default=uuid.UUID('3d9310b9-9b0e-4052-8695-4e03ee015f73'), max_length=100, unique=True),
        ),
    ]
