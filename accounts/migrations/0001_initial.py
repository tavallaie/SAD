# Generated by Django 2.0.6 on 2018-07-29 23:48

import datetime
from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('is_charity', models.BooleanField(default=False)),
                ('is_benefactor', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='AbilityRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(default='', max_length=64)),
                ('name', models.CharField(default='', max_length=64)),
                ('description', models.CharField(max_length=2048, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='AbilityTag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=256)),
                ('description', models.CharField(default='', max_length=1024)),
            ],
        ),
        migrations.CreateModel(
            name='AbilityType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=256)),
                ('description', models.CharField(default='', max_length=2048)),
                ('tags', models.ManyToManyField(to='accounts.AbilityTag')),
            ],
        ),
        migrations.CreateModel(
            name='BenefactorScore',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.IntegerField(default=-1)),
                ('ability_type', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='accounts.AbilityType')),
            ],
        ),
        migrations.CreateModel(
            name='CharityScore',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.IntegerField(default=-1)),
            ],
        ),
        migrations.CreateModel(
            name='ContactInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country', models.CharField(max_length=30, null=True)),
                ('province', models.CharField(max_length=30, null=True)),
                ('city', models.CharField(max_length=30, null=True)),
                ('postal_code', models.CharField(max_length=30, null=True)),
                ('address', models.CharField(max_length=500, null=True)),
                ('phone_number', models.CharField(max_length=20, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='CooperationRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(default='', max_length=64)),
                ('state', models.CharField(default='On-Hold', max_length=16)),
                ('description', models.CharField(max_length=2048, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(default='', max_length=64)),
                ('date_time', models.DateTimeField(default=datetime.datetime(2018, 1, 1, 0, 0))),
                ('description', models.CharField(default='', max_length=2048)),
            ],
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(default='', max_length=128)),
                ('description', models.CharField(max_length=2048, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Benefactor',
            fields=[
                ('user', models.OneToOneField(default='', on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('first_name', models.CharField(default='', max_length=50)),
                ('last_name', models.CharField(default='', max_length=100)),
                ('gender', models.CharField(max_length=40, null=True)),
                ('age', models.IntegerField(null=True)),
                ('score', models.FloatField(default=-1)),
            ],
        ),
        migrations.CreateModel(
            name='Charity',
            fields=[
                ('user', models.OneToOneField(default='', on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('name', models.CharField(max_length=200)),
                ('score', models.FloatField(default=-1)),
                ('benefactor_history', models.ManyToManyField(to='accounts.Benefactor')),
            ],
        ),
        migrations.AddField(
            model_name='notification',
            name='user',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='log',
            name='first_actor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='log_first_actor', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='log',
            name='second_actor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='log_second_actor', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='user',
            name='contact_info',
            field=models.OneToOneField(default='', on_delete=django.db.models.deletion.DO_NOTHING, to='accounts.ContactInfo'),
        ),
        migrations.AddField(
            model_name='user',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups'),
        ),
        migrations.AddField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions'),
        ),
        migrations.AddField(
            model_name='cooperationrequest',
            name='benefactor',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='accounts.Benefactor'),
        ),
        migrations.AddField(
            model_name='cooperationrequest',
            name='charity',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='accounts.Charity'),
        ),
        migrations.AddField(
            model_name='charityscore',
            name='benefactor',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='accounts.Benefactor'),
        ),
        migrations.AddField(
            model_name='charityscore',
            name='charity',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='accounts.Charity'),
        ),
        migrations.AddField(
            model_name='benefactorscore',
            name='benefactor',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='accounts.Benefactor'),
        ),
        migrations.AddField(
            model_name='benefactorscore',
            name='charity',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='accounts.Charity'),
        ),
        migrations.AlterUniqueTogether(
            name='charityscore',
            unique_together={('benefactor', 'charity')},
        ),
        migrations.AlterUniqueTogether(
            name='benefactorscore',
            unique_together={('ability_type', 'benefactor', 'charity')},
        ),
    ]
