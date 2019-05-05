# Generated by Django 2.0.9 on 2019-02-05 18:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='representation_images')),
            ],
        ),
        migrations.CreateModel(
            name='Dicom',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='representation_dicoms')),
            ],
        ),
        migrations.CreateModel(
            name='Filter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('path', models.CharField(max_length=500)),
                ('channel', models.CharField(blank=True, max_length=100, null=True)),
                ('inputmodel', models.CharField(blank=True, max_length=1000, null=True)),
                ('outputmodel', models.CharField(blank=True, max_length=1000, null=True)),
                ('defaultsettings', models.CharField(max_length=400)),
            ],
        ),
        migrations.CreateModel(
            name='Filtering',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('settings', models.CharField(max_length=1000)),
                ('nodeid', models.CharField(blank=True, max_length=400, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Nifti',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FilePathField()),
            ],
        ),
        migrations.CreateModel(
            name='NpArray',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FilePathField()),
                ('position', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Parsing',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('returnchannel', models.CharField(max_length=100)),
                ('settings', models.CharField(max_length=1000)),
                ('progress', models.IntegerField(blank=True, null=True)),
                ('inputvid', models.IntegerField()),
                ('outputvid', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Representation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('vid', models.IntegerField(blank=True, null=True)),
                ('shape', models.CharField(blank=True, max_length=100, null=True)),
                ('nodeid', models.CharField(blank=True, max_length=400, null=True)),
                ('meta', models.CharField(blank=True, max_length=6000, null=True)),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('dicom', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='filterbank.Dicom')),
            ],
        ),
    ]
