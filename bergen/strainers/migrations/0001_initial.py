# Generated by Django 2.2.7 on 2019-12-16 19:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('transformers', '0002_transformation_inputtransformation'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('elements', '0012_experiment_linked_paper'),
    ]

    operations = [
        migrations.CreateModel(
            name='Strainer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('channel', models.CharField(blank=True, max_length=100, null=True)),
                ('defaultsettings', models.CharField(max_length=400)),
            ],
        ),
        migrations.CreateModel(
            name='Straining',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('settings', models.CharField(max_length=1000)),
                ('nodeid', models.CharField(blank=True, max_length=400, null=True)),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('experiment', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='elements.Experiment')),
                ('sample', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='elements.Sample')),
                ('strainer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='strainers.Strainer')),
                ('transformation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='transformers.Transformation')),
            ],
        ),
    ]