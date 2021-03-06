# Generated by Django 2.0.6 on 2018-07-29 23:48

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ability',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.IntegerField(default=-1)),
                ('description', models.CharField(default='', max_length=512)),
                ('ability_type', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='accounts.AbilityType')),
                ('benefactor', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='accounts.Benefactor')),
            ],
        ),
        migrations.CreateModel(
            name='DateInterval',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('begin_date', models.DateField(default=datetime.date(2018, 1, 1))),
                ('end_date', models.DateField(default=datetime.date(2018, 1, 1))),
                ('week_schedule', models.CharField(default='', max_length=512)),
                ('benefactor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.Benefactor')),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project_name', models.CharField(default='', max_length=256)),
                ('description', models.CharField(default='', max_length=2048)),
                ('project_state', models.CharField(default='open', max_length=64)),
                ('type', models.CharField(default='', max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='FinancialProject',
            fields=[
                ('project', models.OneToOneField(default='', on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='projects.Project')),
                ('target_money', models.FloatField(default=0.0)),
                ('current_money', models.FloatField(default=0.0)),
                ('start_date', models.DateField(default=datetime.date(2018, 1, 1))),
                ('end_date', models.DateField(default=datetime.date(2018, 1, 1))),
            ],
        ),
        migrations.CreateModel(
            name='NonFinancialProject',
            fields=[
                ('project', models.OneToOneField(default='', on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='projects.Project')),
                ('min_age', models.IntegerField(default=0)),
                ('max_age', models.IntegerField(default=200)),
                ('required_gender', models.CharField(max_length=128, null=True)),
                ('country', models.CharField(max_length=32, null=True)),
                ('province', models.CharField(max_length=32, null=True)),
                ('city', models.CharField(max_length=32, null=True)),
                ('ability_type', models.ForeignKey(default='', on_delete=django.db.models.deletion.DO_NOTHING, to='accounts.AbilityType')),
                ('request', models.OneToOneField(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='accounts.CooperationRequest')),
            ],
        ),
        migrations.AddField(
            model_name='project',
            name='benefactors',
            field=models.ManyToManyField(to='accounts.Benefactor'),
        ),
        migrations.AddField(
            model_name='project',
            name='charity',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='accounts.Charity'),
        ),
        migrations.AddField(
            model_name='dateinterval',
            name='non_financial_project',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='projects.NonFinancialProject'),
        ),
    ]
