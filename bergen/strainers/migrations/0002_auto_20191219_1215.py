# Generated by Django 2.2.7 on 2019-12-19 12:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('strainers', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='straining',
            name='settings',
            field=models.CharField(max_length=10000),
        ),
    ]