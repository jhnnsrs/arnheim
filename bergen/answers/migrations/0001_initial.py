# Generated by Django 2.2.9 on 2020-01-31 12:40

import uuid

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Oracle',
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
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=500)),
                ('querystring', models.TextField(blank=True, null=True)),
                ('nodeid', models.CharField(blank=True, max_length=400, null=True)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Answering',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('statuscode', models.IntegerField(blank=True, null=True)),
                ('statusmessage', models.CharField(blank=True, max_length=500, null=True)),
                ('settings', models.CharField(max_length=1000)),
                ('nodeid', models.CharField(blank=True, max_length=400, null=True)),
                ('override', models.BooleanField()),
                ('error', models.CharField(blank=True, max_length=300, null=True)),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('oracle', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='answers.Oracle')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='answers.Question')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('signature', models.CharField(blank=True, max_length=300, null=True)),
                ('nodeid', models.CharField(blank=True, max_length=400, null=True)),
                ('vid', models.CharField(max_length=4000)),
                ('shape', models.CharField(blank=True, max_length=400, null=True)),
                ('name', models.CharField(blank=True, max_length=4000, null=True)),
                ('key', models.CharField(max_length=4000)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
