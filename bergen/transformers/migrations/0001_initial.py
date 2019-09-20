# Generated by Django 2.2.5 on 2019-09-20 12:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('elements', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('bioconverter', '0001_initial'),
        ('drawing', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transformer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('channel', models.CharField(blank=True, max_length=100, null=True)),
                ('defaultsettings', models.CharField(max_length=400)),
            ],
        ),
        migrations.CreateModel(
            name='Transforming',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('settings', models.CharField(max_length=1000)),
                ('nodeid', models.CharField(blank=True, max_length=400, null=True)),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('experiment', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='elements.Experiment')),
                ('representation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bioconverter.Representation')),
                ('roi', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='drawing.ROI')),
                ('sample', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='elements.Sample')),
                ('transformer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='transformers.Transformer')),
            ],
        ),
        migrations.CreateModel(
            name='Transformation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=1000)),
                ('vid', models.CharField(max_length=200)),
                ('nodeid', models.CharField(blank=True, max_length=400, null=True)),
                ('shape', models.CharField(blank=True, max_length=100, null=True)),
                ('signature', models.CharField(blank=True, max_length=300, null=True)),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('experiment', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='elements.Experiment')),
                ('numpy', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='elements.Numpy')),
                ('representation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bioconverter.Representation')),
                ('roi', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transformations', to='drawing.ROI')),
                ('sample', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transformations', to='elements.Sample')),
            ],
        ),
    ]
