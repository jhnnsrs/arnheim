# Generated by Django 2.0.9 on 2019-02-09 09:04

from django.db import migrations


class Migration(migrations.Migration):
    atomic = False

    dependencies = [
        ('mutaters', '0002_auto_20190205_1853'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Mutator',
            new_name='Mutater',
        ),
    ]
