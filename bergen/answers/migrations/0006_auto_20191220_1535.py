# Generated by Django 2.2.7 on 2019-12-20 15:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('answers', '0005_answer_creator'),
    ]

    operations = [
        migrations.AddField(
            model_name='answering',
            name='statuscode',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='answering',
            name='statusmessage',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]
