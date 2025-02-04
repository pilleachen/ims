# Generated by Django 5.0.6 on 2024-07-10 15:42

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0008_examtimetable'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClassTimetable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course', models.CharField(max_length=255)),
                ('semester', models.IntegerField()),
                ('day', models.CharField(choices=[('Monday', 'Monday'), ('Tuesday', 'Tuesday'), ('Wednesday', 'Wednesday'), ('Thursday', 'Thursday'), ('Friday', 'Friday')], max_length=9)),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.subject')),
            ],
        ),
    ]
