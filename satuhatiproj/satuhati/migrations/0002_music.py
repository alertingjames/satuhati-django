# Generated by Django 3.0.3 on 2020-02-29 21:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('satuhati', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Music',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('member_id', models.CharField(max_length=11)),
                ('member_name', models.CharField(max_length=50)),
                ('name', models.CharField(max_length=50)),
                ('url', models.CharField(max_length=1000)),
                ('time', models.CharField(max_length=100)),
                ('likes', models.CharField(max_length=11)),
                ('status', models.CharField(max_length=20)),
                ('liked', models.CharField(max_length=20)),
            ],
        ),
    ]