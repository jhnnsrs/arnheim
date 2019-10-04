# Generated by Django 2.2.6 on 2019-10-01 16:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('answers', '0005_answer_creator'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('visualizers', '0003_visualizing_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExcelExport',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('signature', models.CharField(blank=True, max_length=300, null=True)),
                ('nodeid', models.CharField(blank=True, max_length=400, null=True)),
                ('vid', models.CharField(max_length=4000)),
                ('name', models.CharField(blank=True, max_length=4000, null=True)),
                ('excelfile', models.FileField(blank=True, null=True, upload_to='excels')),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('answer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='answers.Answer')),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]