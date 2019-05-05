# Generated by Django 2.0.9 on 2019-02-05 19:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('drawing', '0002_auto_20190205_1853'),
        ('representations', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BioImageFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('file', models.FileField(upload_to='bioimagefiles', verbose_name='bioimage')),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Conversing',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('override', models.BooleanField()),
                ('settings', models.CharField(max_length=1000)),
                ('nodeid', models.CharField(blank=True, max_length=300, null=True)),
                ('outputvid', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='ConversionRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('settings', models.CharField(max_length=1000)),
                ('nodeid', models.CharField(blank=True, max_length=300, null=True)),
                ('outputvid', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Converter',
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
            name='ConvertToSampleRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location', models.CharField(max_length=100)),
                ('name', models.CharField(max_length=100)),
                ('settings', models.CharField(max_length=1000)),
                ('outputvid', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='JobRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('experiment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='representations.Experiment')),
                ('sample', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='drawing.Sample')),
            ],
        ),
    ]