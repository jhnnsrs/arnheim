# Generated by Django 2.2.9 on 2020-01-31 12:40

import uuid

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models

import larvik.discover


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='External',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('uniqueid', models.CharField(blank=True, max_length=400, null=True, unique=True)),
                ('node', models.CharField(max_length=2000)),
                ('defaultsettings', models.CharField(max_length=2000)),
                ('origin', models.CharField(max_length=2000)),
                ('links', models.CharField(max_length=6000)),
                ('ports', models.CharField(blank=True, max_length=7000, null=True)),
                ('status', models.CharField(max_length=200)),
                ('graphname', models.CharField(max_length=200)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('creator', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Flow',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=100)),
                ('name', models.CharField(default='Not Set', max_length=100, null=True)),
                ('diagram', models.CharField(max_length=50000)),
                ('description', models.CharField(default='Add a Description', max_length=50000)),
                ('creator', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('group', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='auth.Group')),
            ],
        ),
        migrations.CreateModel(
            name='Node',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('entityid', models.IntegerField(blank=True, null=True)),
                ('hash', models.CharField(default=larvik.discover.createUniqeNodeName, max_length=300, unique=True)),
                ('variety', models.CharField(blank=True, max_length=100, null=True)),
                ('name', models.CharField(max_length=100)),
                ('nodeclass', models.CharField(default='classic-node', max_length=300)),
                ('path', models.CharField(max_length=500)),
                ('channel', models.CharField(blank=True, max_length=100, null=True)),
                ('inputmodel', models.CharField(blank=True, max_length=1000, null=True)),
                ('outputmodel', models.CharField(blank=True, max_length=1000, null=True)),
                ('defaultsettings', models.CharField(max_length=5000)),
                ('creator', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Layout',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('layout', models.TextField()),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('flows', models.ManyToManyField(to='flow.Flow')),
            ],
        ),
        migrations.CreateModel(
            name='ExternalRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.CharField(max_length=6000)),
                ('port', models.CharField(max_length=2000)),
                ('instance', models.CharField(max_length=2000)),
                ('model', models.CharField(max_length=200)),
                ('origin', models.CharField(max_length=400)),
                ('kind', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('creator', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('external', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='flow.External')),
            ],
        ),
    ]
