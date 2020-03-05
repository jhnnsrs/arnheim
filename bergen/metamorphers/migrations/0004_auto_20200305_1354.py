# Generated by Django 2.2.11 on 2020-03-05 13:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('metamorphers', '0003_auto_20200305_1353'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='metamorpher',
            name='defaultsettings',
        ),
        migrations.AlterField(
            model_name='metamorpher',
            name='channel',
            field=models.CharField(default='Not active', max_length=100, unique=True),
        ),
    ]
