# Generated by Django 2.2.5 on 2019-09-10 13:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transformers', '0004_auto_20190910_1015'),
    ]

    operations = [
        migrations.AddField(
            model_name='numpy',
            name='shape',
            field=models.CharField(blank=True, max_length=400, null=True),
        ),
        migrations.DeleteModel(
            name='Mask',
        ),
    ]