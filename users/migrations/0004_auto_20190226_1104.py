# Generated by Django 2.1.5 on 2019-02-26 05:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20190226_1101'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subject',
            name='subject_desc',
            field=models.CharField(max_length=120),
        ),
    ]
