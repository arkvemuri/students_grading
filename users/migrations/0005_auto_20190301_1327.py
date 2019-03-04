# Generated by Django 2.1.5 on 2019-03-01 07:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20190226_1104'),
    ]

    operations = [
        migrations.AlterField(
            model_name='school',
            name='address',
            field=models.CharField(default='Nanakramguda Road, Cyberabad, Khajaguda, Manikonda', max_length=60),
        ),
        migrations.AlterField(
            model_name='school',
            name='state',
            field=models.CharField(default='Telangana', max_length=25),
        ),
        migrations.AlterField(
            model_name='student',
            name='country',
            field=models.CharField(default='India', max_length=25),
        ),
        migrations.AlterField(
            model_name='student',
            name='email',
            field=models.CharField(default='abhi@gmail.com', max_length=60),
        ),
        migrations.AlterField(
            model_name='student',
            name='state',
            field=models.CharField(default='Telangana', max_length=25),
        ),
        migrations.AlterField(
            model_name='subject',
            name='subject_name',
            field=models.CharField(max_length=60),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='email',
            field=models.CharField(default='rkvemuri2000@yahoo.com', max_length=60),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='spoken_lang',
            field=models.CharField(default='Telugu,English,Hindi', max_length=30),
        ),
    ]