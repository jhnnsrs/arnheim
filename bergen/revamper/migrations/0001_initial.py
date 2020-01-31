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
        ('elements', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Mask',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nodeid', models.CharField(blank=True, max_length=400, null=True)),
                ('vectors', models.CharField(max_length=3000)),
                ('color', models.CharField(blank=True, max_length=100, null=True)),
                ('signature', models.CharField(blank=True, max_length=300, null=True)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='masks', to=settings.AUTH_USER_MODEL)),
                ('experiment', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='masks', to='elements.Experiment')),
                ('sample', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='masks', to='elements.Sample')),
                ('transformation', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='masks', to='transformers.Transformation')),
            ],
        ),
        migrations.CreateModel(
            name='Revamper',
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
            name='Revamping',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('statuscode', models.IntegerField(blank=True, null=True)),
                ('statusmessage', models.CharField(blank=True, max_length=500, null=True)),
                ('settings', models.CharField(max_length=1000)),
                ('nodeid', models.CharField(blank=True, max_length=400, null=True)),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('mask', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='revamper.Mask')),
                ('revamper', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='revamper.Revamper')),
                ('sample', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='elements.Sample')),
                ('transformation', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='transformers.Transformation')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
