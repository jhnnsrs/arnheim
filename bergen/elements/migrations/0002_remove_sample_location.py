# Generated by Django 2.2.9 on 2020-03-02 15:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('elements', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sample',
            name='location',
        ),
    ]