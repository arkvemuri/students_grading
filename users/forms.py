from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User, Student, Teacher, UserProfile, School,  Student_Grades, Subject, Teacher_Students,Courses, SubjectScores
from django.db import transaction
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Button, ButtonHolder, Submit
from crispy_forms.bootstrap import *
from django.core.exceptions import ValidationError
from tempus_dominus.widgets import DatePicker, TimePicker, DateTimePicker
import datetime

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
    fjob_teacher=forms.IntegerField()
    father_edu=forms.IntegerField()
    age=forms.IntegerField()
    schoolsup_yes=forms.IntegerField()
    higher_yes=forms.IntegerField()

    def __init__(self, *args, **kwargs):
        super(GradingForm, self).__init__(*args, **kwargs)
        for key_name in self.fields:
            self.fields[key_name].widget.attrs['style'] = "width:10rem"

class StudentRegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=15)
    last_name = forms.CharField(max_length=15)
    email = forms.EmailField(max_length=60)
    school_id = forms.ModelChoiceField(queryset=School.objects.all(),empty_label=None,label='Your School') #CharField(max_length=50, initial='Oakridge International School (Newton Campus)', label='Your School')
    student_id = forms.CharField(max_length=8, label=' Student ID')
    grade = forms.CharField(max_length=2)
    section = forms.CharField(max_length=1)
    gender = forms.CharField(max_length=1)
    age = forms.CharField(required=False,max_length=10)
    mobile = forms.CharField(required=False,max_length=10)
    dob=forms.DateTimeField(
        widget=DateTimePicker(
            options={
                'minDate': (datetime.date.today() + datetime.timedelta(days=1)).strftime('%Y-%m-%d'),  # Tomorrow
                'useCurrent': True,
                'collapse': False,
            },
            attrs={
               'append': 'fa fa-calendar',
               'input_toggle': False,
               'icon_toggle': True,
            }
        ),
    )
    religion = forms.CharField(required=False,max_length=20)
    spoken_lang = forms.CharField(required=False,max_length=30)
    address = forms.CharField(widget=forms.Textarea(attrs={'rows': 3, 'cols': 85}), max_length=160)
    city = forms.CharField(required=False,max_length=30, initial='Hyderabad')
    state = forms.CharField(required=False,max_length=30, initial='Telangana')
    country = forms.CharField(required=False,max_length=30, initial='India')


    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(StudentRegistrationForm, self).__init__(*args, **kwargs)

        #for key_name in self.fields:
            #self.fields[key_name].widget.attrs['style'] = "width:15rem"


    class Meta(UserCreationForm.Meta):
        model = User

    def clean_student_id(self):
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

        school = self.cleaned_data.get('school_id')
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

        student = Student.objects.create(user_id=user.pk,
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
                                        school_id=school,
                                        )


        return user

class StudentUpdateForm(UserChangeForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class TeacherRegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=60, initial='rkvemuri2000@yahoo.com')
    first_name = forms.CharField(max_length=30, initial='Ramakrishna')
    last_name = forms.CharField(max_length=30, initial='Vemuri')
    grade = forms.CharField(max_length=2, initial='X')
    school = forms.ModelChoiceField(queryset=School.objects.all(), empty_label=None,label='Your School')
    subject=forms.ModelChoiceField(queryset=Subject.objects.all(),empty_label=None, label='Your Subject')

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(TeacherRegistrationForm, self).__init__(*args, **kwargs)
        for key_name in self.fields:
            self.fields[key_name].widget.attrs['style'] = "width:15rem"


    class Meta(UserCreationForm.Meta):
        model = User

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_teacher = True
        user.email = self.cleaned_data.get('email')
        user.save()

        email = self.cleaned_data.get('email')
        first_name = self.cleaned_data.get('first_name')
        last_name = self.cleaned_data.get('last_name')
        grade = self.cleaned_data.get('grade')
        school = self.cleaned_data.get('school')
        subject = self.cleaned_data.get('subject')

        teacher = Teacher.objects.create(user=user, email=email, first_name=first_name,
                                         last_name=last_name, grade=grade,school_id=school, subject_id=subject)

        if commit:
            user.save()
            teacher.save()
        return user

class TeacherUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    school = forms.CharField(max_length=30)
    firstname = forms.CharField(max_length=30)
    lastname = forms.CharField(max_length=30)
    grade = forms.CharField(max_length=2)

    class Meta:
        model = Teacher
        fields = ['email','first_name', 'last_name', 'grade','school','subject_id']

class Teacher_StudentsListFormHelper(FormHelper):
    form_id = 'teacher-students-search-form'
    form_class = 'form-inline'
    field_template = 'bootstrap4/layout/inline_field.html'
    field_class = 'col-xs-3'
    label_class = 'col-xs-3'
    form_show_errors = True
    help_text_inline = False
    html5_required = True
    layout = Layout(
                Fieldset(
                    '<i class="fa fa-search"></i> Search Records',
                    InlineField('id'),
                    InlineField('date_created'),
                    InlineField('school'),
                    InlineField('student'),
                    InlineField('teacher'),
                ),
                FormActions(
                    StrictButton(
                        '<i class="fa fa-search"></i> Search',
                        type='submit',
                        css_class='btn-primary',
                        style='margin-top:10px;')
                )
    )

class Student_GradesListFormHelper(FormHelper):
    form_id = 'student-grades-search-form'
    form_class = 'form-inline'
    field_template = 'bootstrap4/layout/inline_field.html'
    field_class = 'col-xs-3'
    label_class = 'col-xs-3'
    form_show_errors = True
    help_text_inline = False
    html5_required = True
    layout = Layout(
                Fieldset(
                    '<i class="fa fa-search"></i> Search Student Grades Records',
                    InlineField('student'),
                    InlineField('subject'),
                    InlineField('SA1'),
                    InlineField('SA2'),
                    InlineField('SA3'),
                ),
                FormActions(
                    StrictButton(
                        '<i class="fa fa-search"></i> Search',
                        type='submit',
                        css_class='btn-primary',
                        style='margin-top:10px;')
                )
    )

class Teacher_StudentsForm(forms.ModelForm):
    teacher = forms.ModelChoiceField(queryset=Teacher.objects.all(),to_field_name='user_id')
    student = forms.ModelChoiceField(queryset=Subject.objects.all(),to_field_name='student_id')
    school = forms.ModelChoiceField(queryset=School.objects.all(),to_field_name='school_id')

    def __init__(self, *args, **kwargs):
        super(Teacher_StudentsForm, self).__init__(*args, **kwargs)
        self.fields['teacher'].widget.attrs['style'] = "width:15rem"
        self.fields['student'].widget.attrs['style'] = "width:15rem"
        self.fields['school'].widget.attrs['style'] = "width:15rem"

    class Meta:
        model = Teacher_Students
        fields = '__all__'

class Student_GradesForm(forms.ModelForm):
    student = forms.ModelChoiceField(queryset=Teacher_Students.objects.all(),to_field_name='student_id')
    subject = forms.ModelChoiceField(queryset=Subject.objects.all())
    SA1 = forms.FloatField(required=False,initial=0.0)
    SA2 = forms.FloatField(required=False,initial=0.0)
    SA3 = forms.FloatField(required=False,initial=0.0)
    teacher = forms.ChoiceField(widget=forms.Select)


    def __init__(self, *args, **kwargs):
        super(Student_GradesForm, self).__init__(*args, **kwargs)
        for key_name in self.fields:
            self.fields[key_name].widget.attrs['style'] = "width:15rem"

    class Meta:
        model = Student_Grades
        fields = '__all__'

class SubjectScoresForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(SubjectScoresForm, self).__init__(*args, **kwargs)
        for key_name in self.fields:
            self.fields[key_name].widget.attrs['style'] = "width:15rem"

        self.helper = FormHelper(self)

        self.helper.add_input(Submit('submit', 'Recommend'))
        self.fields['subject'].queryset = Subject.objects.none()
        if 'student' in self.data:
            try:
                student_id = self.data.get('student')
                student = Student.objects.filter(student_id=student_id).first()
                self.fields['subject'].queryset = Subject.objects.filter(grade=student.grade).order_by('subject_name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['subject'].queryset = self.instance.subjectscores.subject_id_set.order_by('subject_id')


    class Meta:
        model = SubjectScores
        fields = ['student','subject','subject_score']

class CoursesForm(forms.ModelForm):
    courses = Courses.objects.all()
    choices = [(obj.pk, obj.course_name) for obj in courses]
    subject=forms.ModelChoiceField(queryset=Subject.objects.all())

    course_name=forms.CharField()
    course_link=forms.CharField(label='Link to Course')

    class Meta:
        model = Courses
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(CoursesForm, self).__init__(*args, **kwargs)