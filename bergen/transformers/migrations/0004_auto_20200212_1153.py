# Generated by Django 2.2.9 on 2020-02-12 11:53

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('transformers', '0003_auto_20200212_1132'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transformer',
            name='channel',
            field=models.CharField(default=uuid.UUID('c38fc301-633c-4783-a7c0-22da801fc9f7'), max_length=100, unique=True),
        ),
    ]
