# Generated by Django 2.2.5 on 2019-09-20 13:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('elements', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='numpy',
            name='vid',
            field=models.CharField(max_length=1000),
        ),
    ]