# Generated by Django 2.2.6 on 2019-11-20 18:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flow', '0011_external_ports'),
    ]

    operations = [
        migrations.AddField(
            model_name='external',
            name='links',
            field=models.CharField(default='[]', max_length=6000),
            preserve_default=False,
        ),
    ]