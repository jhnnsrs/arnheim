# Generated by Django 2.2.9 on 2020-01-23 11:22

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('bioconverter', '0006_auto_20200123_1109'),
    ]

    operations = [
        migrations.AlterField(
            model_name='converter',
            name='channel',
            field=models.CharField(default=uuid.UUID('658d0254-d773-44c9-a2ad-a8c7ef66fbf5'), max_length=100, unique=True),
        ),
    ]