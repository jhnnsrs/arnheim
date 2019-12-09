# Generated by Django 2.2.6 on 2019-11-20 14:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('flow', '0003_foreignnoderequest_origin'),
    ]

    operations = [
        migrations.CreateModel(
            name='External',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('node', models.CharField(max_length=2000)),
                ('defaultsettings', models.CharField(max_length=2000)),
                ('status', models.CharField(max_length=200)),
                ('creator', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]