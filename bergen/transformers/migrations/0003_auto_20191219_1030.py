# Generated by Django 2.2.7 on 2019-12-19 10:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('transformers', '0002_transformation_inputtransformation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transformation',
            name='representation',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='bioconverter.Representation'),
        ),
    ]
