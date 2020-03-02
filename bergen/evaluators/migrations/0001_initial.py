# Generated by Django 2.2.9 on 2020-03-02 15:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('elements', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Data',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('signature', models.CharField(blank=True, max_length=300, null=True)),
                ('nodeid', models.CharField(blank=True, max_length=400, null=True)),
                ('vid', models.CharField(max_length=300)),
                ('name', models.CharField(max_length=4000)),
                ('type', models.CharField(max_length=100)),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Evaluator',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('settings', models.CharField(max_length=1000)),
                ('name', models.CharField(max_length=100)),
                ('channel', models.CharField(blank=True, max_length=100, null=True)),
                ('defaultsettings', models.CharField(max_length=400)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ClusterData',
            fields=[
                ('data_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='evaluators.Data')),
                ('clusternumber', models.IntegerField()),
                ('clusterareapixels', models.IntegerField()),
                ('clusterarea', models.FloatField()),
            ],
            bases=('evaluators.data',),
        ),
        migrations.CreateModel(
            name='LengthData',
            fields=[
                ('data_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='evaluators.Data')),
                ('pixellength', models.IntegerField()),
                ('physicallength', models.FloatField()),
                ('distancetostart', models.IntegerField()),
                ('physicaldistancetostart', models.FloatField()),
                ('distancetoend', models.IntegerField()),
                ('physicaldistancetoend', models.FloatField()),
            ],
            bases=('evaluators.data',),
        ),
        migrations.CreateModel(
            name='VolumeData',
            fields=[
                ('data_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='evaluators.Data')),
                ('b4channel', models.IntegerField()),
                ('aisstart', models.IntegerField()),
                ('aisend', models.IntegerField()),
                ('pixellength', models.IntegerField()),
                ('physicallength', models.FloatField()),
                ('vectorlength', models.FloatField()),
                ('diameter', models.IntegerField()),
                ('threshold', models.FloatField()),
                ('userdefinedstart', models.IntegerField()),
                ('userdefinedend', models.IntegerField()),
                ('intensitycurves', models.CharField(max_length=5000)),
            ],
            bases=('evaluators.data',),
        ),
        migrations.CreateModel(
            name='Evaluating',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('statuscode', models.IntegerField(blank=True, null=True)),
                ('statusmessage', models.CharField(blank=True, max_length=500, null=True)),
                ('settings', models.CharField(max_length=1000)),
                ('nodeid', models.CharField(blank=True, max_length=400, null=True)),
                ('override', models.BooleanField()),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('evaluator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='evaluators.Evaluator')),
                ('experiment', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='elements.Experiment')),
                ('roi', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='elements.ROI')),
                ('sample', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='elements.Sample')),
                ('transformation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='elements.Transformation')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='data',
            name='evaluating',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='evaluators.Evaluating'),
        ),
        migrations.AddField(
            model_name='data',
            name='experiment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='elements.Experiment'),
        ),
        migrations.AddField(
            model_name='data',
            name='representation',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='elements.Representation'),
        ),
        migrations.AddField(
            model_name='data',
            name='roi',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='datas', to='elements.ROI'),
        ),
        migrations.AddField(
            model_name='data',
            name='sample',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='datas', to='elements.Sample'),
        ),
        migrations.AddField(
            model_name='data',
            name='transformation',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='datas', to='elements.Transformation'),
        ),
    ]
