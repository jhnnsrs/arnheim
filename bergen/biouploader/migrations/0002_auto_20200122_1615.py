# Generated by Django 2.2.9 on 2020-01-22 16:15

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('biouploader', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='analyzer',
            name='channel',
            field=models.CharField(default=uuid.UUID('9e0b6cb4-5ebb-4867-a77c-934a6383cf77'), max_length=100, unique=True),
        ),
    ]