# Generated by Django 2.2.5 on 2019-09-20 14:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('revamper', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='revamper',
            name='path',
        ),
    ]