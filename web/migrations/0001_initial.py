# Generated by Django 5.1.5 on 2025-01-26 19:32

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Institute',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Speciality',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('institute', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.institute')),
            ],
        ),
        migrations.CreateModel(
            name='StudyPlan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('speciality', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.speciality')),
            ],
        ),
        migrations.CreateModel(
            name='Discipline',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('code', models.CharField(max_length=100)),
                ('course', models.SmallIntegerField()),
                ('semester', models.SmallIntegerField()),
                ('by_choice', models.BooleanField()),
                ('exam', models.BooleanField()),
                ('test', models.BooleanField()),
                ('lecture', models.IntegerField()),
                ('practice', models.IntegerField()),
                ('lab', models.IntegerField()),
                ('study_plan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.studyplan')),
            ],
        ),
    ]
