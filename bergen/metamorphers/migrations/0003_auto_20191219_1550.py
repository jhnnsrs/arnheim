# Generated by Django 2.2.7 on 2019-12-19 15:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('metamorphers', '0002_auto_20190920_1403'),
    ]

    operations = [
        migrations.AddField(
            model_name='metamorphing',
            name='statuscode',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='metamorphing',
            name='statusmessage',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]