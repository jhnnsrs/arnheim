# Generated by Django 2.2.5 on 2019-09-21 13:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('evaluators', '0003_auto_20190921_1346'),
    ]

    operations = [
        migrations.AddField(
            model_name='clusterdata',
            name='spatialunit',
            field=models.CharField(default='µm²', max_length=100),
            preserve_default=False,
        ),
    ]
