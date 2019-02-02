from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User, Student, Teacher, UserProfile, School,  Student_Grades, Subject, Teacher_Students, Courses,SubjectScores
from django.db import transaction
from django.forms import ModelChoiceField
from django.utils.html import mark_safe
from django.urls import reverse
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Button, ButtonHolder, Submit
from crispy_forms.bootstrap import *

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['image']

class GradingForm(forms.Form):
    student_id=forms.CharField(max_length=8)
    subject_name = forms.CharField(max_length=15)
    failures=forms.IntegerField()
    mother_edu=forms.IntegerField()
    father_edu=forms.IntegerField()
    age=forms.IntegerField()
    schoolsup_yes=forms.IntegerField()
    higher_yes=forms.IntegerField()

    def __init__(self, *args, **kwargs):
        super(GradingForm, self).__init__(*args, **kwargs)
        self.fields['student_id'].widget.attrs['style'] = "width:10rem"
        self.fields['subject_name'].widget.attrs['style'] = "width:10rem"
        self.fields['failures'].widget.attrs['style'] = "width:10rem"
        self.fields['mother_edu'].widget.attrs['style'] = "width:10rem"
        self.fields['father_edu'].widget.attrs['style'] = "width:10rem"
        self.fields['age'].widget.attrs['style'] = "width:10rem"
        self.fields['schoolsup_yes'].widget.attrs['style'] = "width:10rem"
        self.fields['higher_yes'].widget.attrs['style'] = "width:10rem"

class StudentRegistrationForm(UserCreationForm):
    #username = forms.RegexField(label='Username', max_length=30, regex=r'^[\w-]+$', error_messages='This value must contain only letters, numbers, hyphens and underscores.')
    first_name = forms.CharField(max_length=15, initial='Abhinav')
    last_name = forms.CharField(max_length=15, initial='Vemuri')
    email = forms.EmailField(max_length=20, initial='abhi@gmail.com')
    schoolname = forms.CharField(max_length=50, initial='Oakridge International School (Newton Campus)', label='Your School')
    school_id = forms.HiddenInput()
    student_id = forms.CharField(max_length=8, initial='15H7115', label=' Student ID')
    grade = forms.CharField(max_length=2, initial='X')
    section = forms.CharField(max_length=1, initial='A')
    gender = forms.CharField(max_length=1, initial='M')
    age = forms.CharField(required=False,max_length=10, initial='14 Years')
    mobile = forms.CharField(required=False,max_length=10, initial= '7981764023')
    dob = forms.CharField(max_length=10, initial='24-05-2004', label='Date of Birth')
    religion = forms.CharField(required=False,max_length=10, initial='Hindu')
    spoken_lang = forms.CharField(required=False,max_length=20, initial='Telugu, English')
    address = forms.CharField(widget=forms.Textarea(attrs={'rows': 1, 'cols': 85}), max_length=160)
    city = forms.CharField(required=False,max_length=20, initial='Hyderabad')
    state = forms.CharField(required=False,max_length=20, initial='Telangana')
    country = forms.CharField(required=False,max_length=20, initial='India')

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(StudentRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['style'] = "width:15rem"
        self.fields['username'].initial=self.request.user.username
        self.fields['username'].help_text = False
        self.fields['password1'].widget.attrs['style'] = "width:15rem"
        self.fields['password2'].widget.attrs['style'] = "width:15rem"
        self.fields['first_name'].widget.attrs['style'] = "width:15rem"
        self.fields['last_name'].widget.attrs['style'] = "width:15rem"
        self.fields['email'].widget.attrs['style'] = "width:15rem"
        self.fields['dob'].widget.attrs['style'] = "width:10rem"
        self.fields['student_id'].widget.attrs['style'] = "width:10rem"
        self.fields['grade'].widget.attrs['style'] = "width:10rem"
        self.fields['gender'].widget.attrs['style'] = "width:3rem"
        self.fields['age'].widget.attrs['style'] = "width:10rem"
        self.fields['religion'].widget.attrs['style'] = "width:10rem"
        self.fields['section'].widget.attrs['style'] = "width:10rem"
        self.fields['spoken_lang'].widget.attrs['style'] = "width:10rem"
        self.fields['mobile'].widget.attrs['style'] = "width:10rem"
        self.fields['city'].widget.attrs['style'] = "width:10rem"
        self.fields['state'].widget.attrs['style'] = "width:10rem"
        self.fields['country'].widget.attrs['style'] = "width:10rem"

    class Meta(UserCreationForm.Meta):
        model = User

    def clean_student_id(self):

        from django.core.exceptions import ValidationError
        student_id = self.cleaned_data.get('student_id')

        if Student.objects.filter(student_id=student_id).exists():
            raise ValidationError('A Student with this ID already exists.')
        return student_id

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_student = True
        user.email =self.cleaned_data.get('email')
        user.save()

        school_name = self.cleaned_data.get('schoolname')
        school = School.objects.filter(school_name=school_name).first()

        student_id = self.cleaned_data.get('student_id')

        first_name = self.cleaned_data.get('first_name')
        last_name = self.cleaned_data.get('last_name')
        email = self.cleaned_data.get('email')
        grade = self.cleaned_data.get('grade')
        gender = self.cleaned_data.get('gender')
        section = self.cleaned_data.get('section')
        age = self.cleaned_data.get('age')
        mobile = self.cleaned_data.get('mobile')
        dob = self.cleaned_data.get('dob')
        religion = self.cleaned_data.get('religion')
        spoken_lang = self.cleaned_data.get('spoken_lang')
        address = self.cleaned_data.get('address')
        city = self.cleaned_data.get('city')
        state = self.cleaned_data.get('state')
        country = self.cleaned_data.get('country')


        student = Student.objects.create(user=user,school=school,school_name=school_name,
                                        student_id=student_id,
                                        first_name=first_name,
                                        last_name=last_name,
                                        email=email,
                                        grade=grade,
                                        gender=gender,
                                        section=section,
                                        age=age,
                                        mobile=mobile,
                                        dob=dob,
                                        religion=religion,
                                        spoken_lang=spoken_lang,
                                        address=address,
                                        city=city,
                                        state=state,
                                        country=country,
                                        )


        #student.save()

        return user

class StudentUpdateForm(UserChangeForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class TeacherRegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=30, initial='rkvemuri2000@yahoo.com')
    first_name = forms.CharField(max_length=30, initial='Ramakrishna')
    last_name = forms.CharField(max_length=30, initial='Vemuri')
    grade = forms.CharField(max_length=2, initial='X')
    schoolname = forms.CharField(max_length=50, initial='Oakridge International School (Newton Campus)', label='Your School')
    school_id = forms.HiddenInput()

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(TeacherRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['username'].initial = self.request.user.username
        self.fields['username'].help_text=False
        self.fields['username'].widget.attrs['style'] = "width:15rem"
        self.fields['password1'].widget.attrs['style'] = "width:15rem"
        self.fields['password2'].widget.attrs['style'] = "width:15rem"
        self.fields['first_name'].widget.attrs['style'] = "width:15rem"
        self.fields['last_name'].widget.attrs['style'] = "width:15rem"
        self.fields['email'].widget.attrs['style'] = "width:15rem"
        self.fields['grade'].widget.attrs['style'] = "width:10rem"

    class Meta(UserCreationForm.Meta):
        model = User

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_teacher = True
        user.email = self.cleaned_data.get('email')
        user.save()
        school_name = self.cleaned_data.get('schoolname')
        school = School.objects.filter(school_name=school_name).first()
        teacher = Teacher.objects.create(user=user, school=school)

        if commit:
            user.save()
        return user

class TeacherUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    school = forms.CharField(max_length=30)
    firstname = forms.CharField(max_length=30)
    lastname = forms.CharField(max_length=30)
    grade = forms.CharField(max_length=2)

    class Meta:
        model = User
        fields = ['username', 'email','first_name', 'last_name', 'grade','school']

class Student_GradesForm(forms.ModelForm):
    student = forms.ModelChoiceField(queryset=Teacher_Students.objects.all(),to_field_name='student_id')
    subject = forms.ModelChoiceField(queryset=Subject.objects.all())
    SA1 = forms.FloatField(required=False,initial=0.0)
    SA2 = forms.FloatField(required=False,initial=0.0)
    SA3 = forms.FloatField(required=False,initial=0.0)
    teacher = forms.ChoiceField(widget=forms.Select)

    def __init__(self, *args, **kwargs):
        super(Student_GradesForm, self).__init__(*args, **kwargs)
        self.fields['student'].widget.attrs['style'] = "width:15rem"
        self.fields['subject'].widget.attrs['style'] = "width:15rem"
        self.fields['SA1'].widget.attrs['style'] = "width:15rem"
        self.fields['SA2'].widget.attrs['style'] = "width:15rem"
        self.fields['SA3'].widget.attrs['style'] = "width:15rem"
        self.fields['teacher'].widget.attrs['style'] = "width:15rem"

    class Meta:
        model = Student_Grades
        fields = '__all__'

class SubjectScoresForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['GPA']
        # fields = ['student','subject1','score1','subject2','score2',
        #             'subject4', 'score4', 'subject3','score3',
        #           'subject5', 'score5','subject6','score6',
        #           'subject7', 'score7',]

    def __init__(self, *args, **kwargs):
        super(SubjectScoresForm, self).__init__(*args, **kwargs)
        #self.fields['student_id'].widget.attrs['style'] = "width:15rem"
        self.fields['GPA'].widget.attrs['style'] = "width:15rem"
        self.helper = FormHelper(self)
        self.fields['GPA'].required=False
        self.helper.add_input(Submit('submit', 'Recommend'))

class CoursesForm(forms.ModelForm):
    courses = Courses.objects.all()
    choices = [(obj.pk, obj.course_name) for obj in courses]
    course_name = forms.TypedChoiceField(
        label="Select your Course",
        choices=choices,
        coerce=lambda x: int(x),
        widget=forms.RadioSelect,
        required=True,
    )

    class Meta:
        model = Courses
        fields = ['course_name']

    def __init__(self, *args, **kwargs):
        super(CoursesForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        #self.helper.add_input(Submit('submit', 'Select'))
        self.helper.layout = Layout(
            Div(InlineRadios('course_name')),
        )
