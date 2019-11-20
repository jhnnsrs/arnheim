# Generated by Django 2.2.6 on 2019-11-20 15:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('flow', '0006_external_created_at'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExternalRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_created=True)),
                ('data', models.CharField(max_length=6000)),
                ('port', models.CharField(max_length=2000)),
                ('instance', models.CharField(max_length=2000)),
                ('model', models.CharField(max_length=200)),
                ('origin', models.CharField(max_length=400)),
                ('creator', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('external', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='flow.External')),
            ],
        ),
    ]
