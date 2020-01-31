# Generated by Django 2.2.9 on 2020-01-31 12:40

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('answers', '0001_initial'),
        ('elements', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='answer',
            name='pandas',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='elements.Pandas'),
        ),
        migrations.AddField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='answers.Question'),
        ),
    ]
