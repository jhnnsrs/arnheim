# Generated by Django 2.2.9 on 2019-12-25 23:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('elements', '0014_zarr'),
        ('bioconverter', '0005_auto_20191219_1530'),
    ]

    operations = [
        migrations.AddField(
            model_name='representation',
            name='zarr',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='elements.Zarr'),
        ),
    ]
