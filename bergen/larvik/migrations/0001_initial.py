# Generated by Django 2.2.9 on 2020-03-02 15:23

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Zarr',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('store', models.FilePathField(max_length=600)),
                ('group', models.CharField(max_length=800)),
            ],
        ),
    ]
