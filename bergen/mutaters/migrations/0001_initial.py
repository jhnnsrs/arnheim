# Generated by Django 2.2.9 on 2020-01-31 12:40

import uuid

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('transformers', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('drawing', '0002_auto_20200131_1240'),
        ('elements', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Mutater',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('channel', models.CharField(default=uuid.UUID('a7aaf020-56cd-4ed5-b660-121f969b258a'), max_length=100, unique=True)),
                ('settings', models.CharField(max_length=1000)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Reflection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shape', models.CharField(blank=True, max_length=100, null=True)),
                ('nodeid', models.CharField(blank=True, max_length=400, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='transformation_images')),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('experiment', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='elements.Experiment')),
                ('roi', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='drawing.ROI')),
                ('sample', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='elements.Sample')),
                ('transformation', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='transformers.Transformation')),
            ],
        ),
        migrations.CreateModel(
            name='Mutating',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('statuscode', models.IntegerField(blank=True, null=True)),
                ('statusmessage', models.CharField(blank=True, max_length=500, null=True)),
                ('settings', models.CharField(max_length=1000)),
                ('nodeid', models.CharField(blank=True, max_length=400, null=True)),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('mutater', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mutaters.Mutater')),
                ('sample', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='elements.Sample')),
                ('transformation', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='transformers.Transformation')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
