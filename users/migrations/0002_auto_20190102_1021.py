# Generated by Django 2.1.4 on 2019-01-02 04:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='student_grades',
            old_name='subject_name',
            new_name='subject',
        ),
    ]
