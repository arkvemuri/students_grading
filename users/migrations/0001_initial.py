# Generated by Django 2.1.4 on 2019-01-02 04:49

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('is_student', models.BooleanField(default=False)),
                ('is_teacher', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='School',
            fields=[
                ('school_name', models.CharField(default='Oakridge International School (Newton Campus)', max_length=40)),
                ('school_id', models.CharField(max_length=8, primary_key=True, serialize=False)),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('address', models.CharField(default='Nanakramguda Road, Cyberabad, Khajaguda, Manikonda', max_length=40)),
                ('city', models.CharField(default='Hyderabad', max_length=20)),
                ('state', models.CharField(default='Telangana', max_length=15)),
                ('postal_code', models.IntegerField(default=500008)),
                ('country', models.CharField(default='India', max_length=15)),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('first_name', models.CharField(default='Abhinav', max_length=30)),
                ('last_name', models.CharField(default='Vemuri', max_length=30)),
                ('email', models.CharField(default='abhi@gmail.com', max_length=30)),
                ('school_name', models.CharField(default='Oakridge International School', max_length=40)),
                ('grade', models.CharField(default='X', max_length=2)),
                ('gender', models.CharField(default='M', max_length=1)),
                ('section', models.CharField(default='A', max_length=1)),
                ('age', models.CharField(default='14', max_length=10)),
                ('mobile', models.CharField(default='7981764023', max_length=14)),
                ('dob', models.CharField(default='24-05-2004', max_length=14)),
                ('student_absence_days', models.IntegerField(default=0)),
                ('religion', models.CharField(default='Hindu', max_length=15)),
                ('spoken_lang', models.CharField(default='Telugu,English', max_length=20)),
                ('address', models.CharField(default='Lanco Hills 4LH 1504 Manikonda', max_length=30)),
                ('city', models.CharField(default='Hyderabad', max_length=30)),
                ('state', models.CharField(default='Telangana', max_length=15)),
                ('country', models.CharField(default='India', max_length=15)),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('student_id', models.CharField(max_length=8, primary_key=True, serialize=False)),
                ('GPA', models.FloatField(default=0.0, max_length=5)),
                ('school', models.ForeignKey(max_length=8, on_delete=django.db.models.deletion.CASCADE, to='users.School')),
            ],
        ),
        migrations.CreateModel(
            name='Student_Grades',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('SA1', models.FloatField(default=0.0, max_length=6)),
                ('SA2', models.FloatField(default=0.0, max_length=6)),
                ('SA3', models.FloatField(default=0.0, max_length=6)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.Student')),
            ],
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject_name', models.CharField(max_length=15)),
                ('subject_desc', models.CharField(max_length=30)),
                ('school', models.CharField(max_length=30)),
                ('grade', models.CharField(max_length=2)),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='Teacher_Students',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('school', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.School')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.Student')),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(default='default.jpg', upload_to='profile_pics')),
            ],
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('first_name', models.CharField(default='Ramakrishna', max_length=30)),
                ('last_name', models.CharField(default='Vemuri', max_length=30)),
                ('school_name', models.CharField(default='Oakridge International School', max_length=40)),
                ('grade', models.CharField(default='X', max_length=2)),
                ('section', models.CharField(default='A', max_length=3)),
                ('email', models.CharField(default='rkvemuri2000@yahoo.com', max_length=30)),
                ('mobile', models.CharField(default='9000600534', max_length=14)),
                ('spoken_lang', models.CharField(default='Telugu,English,Hindi', max_length=20)),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('school', models.ForeignKey(max_length=8, on_delete=django.db.models.deletion.CASCADE, to='users.School')),
            ],
        ),
        migrations.AddField(
            model_name='userprofile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='student_grades',
            name='subject_name',
            field=models.ForeignKey(max_length=20, on_delete=django.db.models.deletion.CASCADE, to='users.Subject'),
        ),
        migrations.AddField(
            model_name='student',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='user',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups'),
        ),
        migrations.AddField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions'),
        ),
        migrations.AddField(
            model_name='teacher_students',
            name='teacher',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.Teacher'),
        ),
        migrations.AddField(
            model_name='student_grades',
            name='teacher',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.Teacher'),
        ),
    ]