# Generated by Django 2.1.5 on 2019-01-24 08:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20190124_1348'),
    ]

    operations = [
        migrations.AddField(
            model_name='courses',
            name='id',
            field=models.AutoField(auto_created=True, default=1, primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='courses',
            name='course_name',
            field=models.CharField(max_length=50),
        ),
    ]
