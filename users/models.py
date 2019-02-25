from django.db import models
#from django.contrib.auth.models import User
from PIL import Image
from django.urls import reverse
from django.utils import timezone
from django.conf import settings
from django.contrib.auth.models import AbstractUser, UserManager
from django.utils.html import escape, mark_safe

class User(AbstractUser):
     is_student = models.BooleanField(default=False)
     is_teacher = models.BooleanField(default=False)

     def get_absolute_url(self):
        return reverse('user-detail', kwargs={'pk': self.pk})

class School(models.Model):
    school_name = models.CharField(max_length=60, default='Oakridge International School (Newton Campus)')
    school_id = models.CharField(max_length=8, primary_key=True)
    date_created = models.DateTimeField(default=timezone.now)
    address = models.CharField(max_length=40, default='Nanakramguda Road, Cyberabad, Khajaguda, Manikonda')
    city = models.CharField(max_length=20,default='Hyderabad')
    state = models.CharField(max_length=15, default='Telangana')
    postal_code = models.IntegerField(default=500008)
    country = models.CharField(max_length=15,default='India')

    def __str__(self):
        return self.school_name

    def get_absolute_url(self):
        return reverse('school-detail', kwargs={'pk': self.pk})

class Student(models.Model):
    student_id = models.CharField(max_length=8, primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    school_id = models.ForeignKey(School, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30, default='Abhinav')
    last_name = models.CharField(max_length=30, default='Vemuri')
    email = models.CharField(max_length=30, default='abhi@gmail.com')
    grade = models.CharField(max_length=2, default='X')
    gender = models.CharField(max_length=1,default='M')
    section = models.CharField(max_length=1,default='A')
    age = models.CharField(max_length=10,default='14')
    mobile = models.CharField(max_length=14,default='7981764023')
    dob = models.CharField(max_length=14, default='24-05-2004')
    student_absence_days = models.IntegerField(default=0)
    religion = models.CharField(max_length=15,default='Hindu')
    spoken_lang = models.CharField(max_length=20,default='Telugu,English')
    address = models.CharField(max_length=30, default='Lanco Hills 4LH 1504 Manikonda')
    city = models.CharField(max_length=30,default='Hyderabad')
    state = models.CharField(max_length=15,default='Telangana')
    country = models.CharField(max_length=15,default='India')
    date_created = models.DateTimeField(default=timezone.now)
    GPA = models.FloatField(max_length=5, default=0.0)

    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        return reverse('student-detail', kwargs={'pk': self.pk})


class Subject(models.Model):
    subject_name = models.CharField(max_length=15)
    subject_desc = models.CharField(max_length=30)
    school_id = models.ForeignKey(School, on_delete=models.CASCADE)
    grade = models.CharField(max_length=2)
    date_created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return "%s" % (self.subject_name)

    def get_absolute_url(self):
        reverse('subject-detail', kwargs={'pk': self.pk})

class Courses(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    course_name=models.CharField(max_length=50)
    course_link=models.CharField(max_length=100)

    def __str__(self):
        return "%s %s %s" % (self.subject, self.course_name,self.course_link)

    def get_absolute_url(self):
        return reverse('course-detail', kwargs={'pk': self.pk})

class SubjectScores(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    subject_score=models.FloatField(max_length=6,default=0.0)
    date_created = models.DateTimeField(default=timezone.now)

    @property
    def fields(self):
        return [f.name for f in self._meta.fields + self._meta.many_to_many]

    def __str__(self):
        #return '%s %s %s %s %s %s %s %s' % (self.student,self.subject1,self.subject2,self.subject3,self.subject4,self.subject5,self.subject6,self.subject7)
        return '%s %s' % (self.student,self.subject)

    def get_absolute_url(self):
        reverse('subject-scores-detail', kwargs={'pk': self.pk})

class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,primary_key=True)
    school_id = models.ForeignKey(School, max_length=8, on_delete=models.CASCADE)
    subject_id = models.ForeignKey(Subject, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30, default='Ramakrishna')
    last_name = models.CharField(max_length=30, default='Vemuri')
    grade = models.CharField(max_length=2, default='X')
    section = models.CharField(max_length=3,default='A')
    email = models.CharField(max_length=30, default='rkvemuri2000@yahoo.com')
    mobile = models.CharField(max_length=14,default='9000600534')
    spoken_lang = models.CharField(max_length=20,default='Telugu,English,Hindi')
    date_created = models.DateTimeField(default=timezone.now)

    def get_absolute_url(self):
        return reverse('teacher-detail', kwargs={'pk': self.pk})

class Student_Grades(models.Model):
    student = models.ForeignKey(Student,  on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, max_length=20)
    SA1 = models.FloatField(max_length=6,default=0.0)
    SA2 = models.FloatField(max_length=6,default=0.0)
    SA3 = models.FloatField(max_length=6,default=0.0)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse('grade-detail', kwargs={'pk': self.pk})

class Teacher_Students(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    date_created = models.DateTimeField(default=timezone.now)

    def get_absolute_url(self):
        return reverse('teacher_student_linkup', kwargs={'pk': self.pk})

class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)
