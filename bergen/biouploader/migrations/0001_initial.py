# Generated by Django 2.0.9 on 2019-02-05 19:09

import biouploader.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('representations', '0001_initial'),
        ('filterbank', '0002_auto_20190205_1853'),
    ]

    operations = [
        migrations.CreateModel(
            name='Analyzer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('path', models.CharField(max_length=500)),
                ('inputmodel', models.CharField(blank=True, max_length=1000, null=True)),
                ('outputmodel', models.CharField(blank=True, max_length=1000, null=True)),
                ('name', models.CharField(max_length=100)),
                ('channel', models.CharField(blank=True, max_length=100, null=True)),
                ('defaultsettings', models.CharField(max_length=400)),
            ],
        ),
        migrations.CreateModel(
            name='Analyzing',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nodeid', models.CharField(blank=True, max_length=300, null=True)),
                ('settings', models.CharField(max_length=800)),
                ('analyzer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='biouploader.Analyzer')),
            ],
        ),
        migrations.CreateModel(
            name='BioImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('file', models.FileField(upload_to='bioimagefiles', verbose_name='bioimage')),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('experiment', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='bioimages', to='representations.Experiment')),
            ],
        ),
        migrations.CreateModel(
            name='BioSeries',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('index', models.IntegerField()),
                ('name', models.CharField(max_length=400)),
                ('image', models.ImageField(blank=True, null=True, upload_to='')),
                ('isconverted', models.BooleanField()),
                ('nodeid', models.CharField(blank=True, max_length=300, null=True)),
                ('bioimage', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='biouploader.BioImage')),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('experiment', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='representations.Experiment')),
                ('vid', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='bioseries', to='filterbank.Representation')),
            ],
        ),
        migrations.CreateModel(
            name='LargeFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(storage=biouploader.models.OverwriteStorage(), upload_to=biouploader.models.get_upload_to)),
                ('filename', models.CharField(max_length=255)),
                ('version', models.CharField(max_length=255)),
                ('size', models.BigIntegerField()),
                ('created_on', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.AddField(
            model_name='analyzing',
            name='bioimage',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='biouploader.BioImage'),
        ),
        migrations.AddField(
            model_name='analyzing',
            name='creator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='analyzing',
            name='experiment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='representations.Experiment'),
        ),
    ]
