# Generated by Django 5.0.6 on 2024-07-09 13:26

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0005_attendance'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('BCA', 'Bachelor of Computer Application'), ('CS', 'B.Sc. Computer Science'), ('ELC', 'B.Sc. Electronics'), ('TAX', 'B.COM. Taxation'), ('FIN', 'B.COM. Finance'), ('BBA', ' Bachelor of Business Administration')], max_length=3, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Syllabus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('syllabus_file', models.FileField(upload_to='syllabi/')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.course')),
                ('uploaded_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
