# Generated by Django 2.2.6 on 2019-10-11 11:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('elements', '0010_animal_experimentalgroup'),
    ]

    operations = [
        migrations.AddField(
            model_name='experiment',
            name='description_long',
            field=models.TextField(blank=True, null=True),
        ),
    ]