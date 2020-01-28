# Generated by Django 2.2.9 on 2020-01-22 16:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('biouploader', '0001_initial'),
        ('elements', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Converter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('settings', models.CharField(max_length=1000)),
                ('name', models.CharField(max_length=100)),
                ('channel', models.CharField(default=uuid.UUID('324fe85b-8250-4076-ae86-2344143981a4'), max_length=100, unique=True)),
                ('defaultsettings', models.CharField(max_length=1000)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Representation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=1000)),
                ('vid', models.CharField(blank=True, max_length=1000, null=True)),
                ('shape', models.CharField(blank=True, max_length=100, null=True)),
                ('nodeid', models.CharField(blank=True, max_length=400, null=True)),
                ('meta', models.CharField(blank=True, max_length=6000, null=True)),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('experiment', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='elements.Experiment')),
                ('inputrep', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='bioconverter.Representation')),
                ('sample', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='representations', to='elements.Sample')),
                ('zarr', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='elements.Zarr')),
            ],
        ),
        migrations.CreateModel(
            name='Conversing',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('statuscode', models.IntegerField(blank=True, null=True)),
                ('statusmessage', models.CharField(blank=True, max_length=500, null=True)),
                ('settings', models.CharField(max_length=1000)),
                ('nodeid', models.CharField(blank=True, max_length=400, null=True)),
                ('bioserie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='biouploader.BioSeries')),
                ('converter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bioconverter.Converter')),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('experiment', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='elements.Experiment')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
