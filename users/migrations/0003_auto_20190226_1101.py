# Generated by Django 2.1.5 on 2019-02-26 05:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_courses'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subject',
            name='subject_desc',
            field=models.CharField(max_length=60),
        ),
        migrations.AlterField(
            model_name='subject',
            name='subject_name',
            field=models.CharField(max_length=30),
        ),
    ]
