# Generated by Django 2.2.7 on 2019-12-19 10:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flow', '0015_external_uniqueid'),
    ]

    operations = [
        migrations.AddField(
            model_name='external',
            name='graphname',
            field=models.CharField(default='old', max_length=200),
            preserve_default=False,
        ),
    ]
