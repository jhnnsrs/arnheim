# Generated by Django 2.2.6 on 2019-11-21 11:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flow', '0012_external_links'),
    ]

    operations = [
        migrations.AddField(
            model_name='externalrequest',
            name='kind',
            field=models.CharField(default='in', max_length=100),
            preserve_default=False,
        ),
    ]