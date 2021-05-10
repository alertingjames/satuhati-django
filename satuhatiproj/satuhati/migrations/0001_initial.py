# Generated by Django 3.0.3 on 2020-02-29 10:00

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SatuhatiMember',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('email', models.CharField(max_length=80)),
                ('password', models.CharField(max_length=30)),
                ('auth_status', models.CharField(max_length=30)),
                ('picture_url', models.CharField(max_length=1000)),
                ('latitude', models.CharField(max_length=50)),
                ('longitude', models.CharField(max_length=50)),
                ('registered_time', models.CharField(max_length=50)),
                ('status', models.CharField(max_length=20)),
            ],
        ),
    ]
