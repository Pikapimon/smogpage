# Generated by Django 2.2.7 on 2020-01-21 16:22

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='day_record',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sortid', models.IntegerField(default=0)),
                ('province', models.CharField(default=None, max_length=50)),
                ('city', models.CharField(default=None, max_length=50)),
                ('AQI', models.IntegerField(default=0)),
                ('air_quality', models.CharField(default=None, max_length=50)),
                ('PM', models.IntegerField(default=0)),
                ('key_pollution', models.CharField(default=None, max_length=50)),
                ('release_time', models.DateField()),
                ('last_update_time', models.DateField(auto_now_add=True)),
            ],
        ),
    ]
