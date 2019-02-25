from django.shortcuts import render,redirect, render_to_response
from django.contrib import messages
from .forms import UserRegistrationForm,UserUpdateForm,ProfileUpdateForm, SubjectScoresForm,\
    TeacherRegistrationForm, StudentRegistrationForm, Student_GradesForm, GradingForm, CoursesForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AdminPasswordChangeForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from requests import request
from .filters import Student_GradesListFilter, Teacher_StudentsListFilter
from .utils import PagedFilteredTableView
from .forms import Student_GradesListFormHelper, Teacher_StudentsListFormHelper
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from social_django.models import UserSocialAuth
from django_tables2.views import SingleTableView
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    DeleteView,
    UpdateView
)
from django.contrib.auth.views import LogoutView
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from django.apps import apps
from django.contrib.auth import login, logout
from django.shortcuts import render, get_object_or_404
from .models import *
from django.contrib.auth import authenticate, login
from datetime import datetime

from multi_form_view import MultiFormView as MultiFormView
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from django_tables2.config import RequestConfig
from .tables import *


@login_required
def home(request):
    return render(request, 'users/home.html')

class SignUpView(TemplateView):
    template_name = 'users/signup.html'

class StudentSignUpView(CreateView):
    model = User
    form_class = StudentRegistrationForm

    template_name = 'users/signup_form.html'

    def get_form_kwargs(self):
        kw = super(StudentSignUpView, self).get_form_kwargs()
        kw['request'] = self.request  # the trick!
        return kw
    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'student'
        self.get_form_class()
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user,'django.contrib.auth.backends.ModelBackend')
        messages.success(self.request, f'Your Student Account bas been created! You can login with username { user.username }! ')
        return redirect('student-list')

    success_url = '/'
class TeacherSignUpView(CreateView):
    model = User
    form_class = TeacherRegistrationForm
    template_name = 'users/signup_form.html'

    def get_form_kwargs(self):
        kw = super(TeacherSignUpView, self).get_form_kwargs()
        kw['request'] = self.request  # the trick!
        return kw
    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'teacher'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user, 'django.contrib.auth.backends.ModelBackend')
        messages.success(self.request, f'Your Teacher Account bas been created! You can login with username { user.username }! ')
        return redirect('teacher-list')
    success_url = '/'

def formView(request):
    if 'username' in request.COOKIES and 'last_connection' in request.COOKIES:
        username = request.COOKIES['username']

        last_connection = request.COOKIES['last_connection']
        last_connection_time = datetime.strptime(last_connection[:-7],
                                                          "%Y-%m-%d %H:%M:%S")

        if (datetime.now() - last_connection_time).seconds < 10:
            return render(request, 'grading-home', {"username": username})
        else:
            return render(request, 'users/login.html', {})

    else:
        return render(request, 'users/login.html', {})

def loginUser(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)

    return redirect('grading-home')

def logoutUser(request):
    try:
        del request.session['username']
    except:
        pass
    logout(request)
    return redirect('login')

def student_signup(request):
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your Account bas been created! You can login with username { username }! ')
            return redirect('login')
    else:
        form = StudentRegistrationForm()
    return render(request, 'student/sregister.html',{'form': form})

def teacher_signup(request):
    if request.method == 'POST':
        form = TeacherRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your Account bas been created! You can login with username { username }! ')
            return redirect('login')
    else:
        form = TeacherRegistrationForm()
    return render(request, 'teacher/tregister.html',{'form': form})

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your Account bas been created! You can login with username { username }! ')
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'users/register.html',{'form': form})

@login_required
def profile(request):
     if request.method == 'POST':
         u_form = UserUpdateForm(request.POST, instance=request.user)
         p_form = ProfileUpdateForm(request.POST,
                                    request.FILES,
                                    instance=request.user.userprofile)
         if u_form.is_valid and p_form.is_valid:
             u_form.save()
             p_form.save()
             messages.success(request, f'Your Account bas been Updated! ')
             return redirect('profile')
     else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.userprofile)

        context = {
         'u_form': u_form,
         'p_form': p_form

        }
        return render(request,'users/profile.html',context)

@login_required
def settings(request):
    user = request.user

    try:
        github_login = user.social_auth.get(provider='github')
    except UserSocialAuth.DoesNotExist:
        github_login = None

    try:
        twitter_login = user.social_auth.get(provider='twitter')
    except UserSocialAuth.DoesNotExist:
        twitter_login = None

    try:
        facebook_login = user.social_auth.get(provider='facebook')
    except UserSocialAuth.DoesNotExist:
        facebook_login = None

    can_disconnect = (user.social_auth.count() > 1 or user.has_usable_password())

    return render(request, 'users/settings.html', {
        'github_login': github_login,
        'twitter_login': twitter_login,
        'facebook_login': facebook_login,
        'can_disconnect': can_disconnect
    })

@login_required
def password(request):
    if request.user.has_usable_password():
        PasswordForm = PasswordChangeForm
    else:
        PasswordForm = AdminPasswordChangeForm

    if request.method == 'POST':
        form = PasswordForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordForm(request.user)
    return render(request, 'users/password.html', {'form': form})


class StudentListView(LoginRequiredMixin, ListView):
    model = Student
    template_name = 'student/home.html'

    context_object_name = 'student'
    #ordering = ['-date_created']

    def get_queryset(self):
        queryset = Student.objects.filter(user=self.request.user).first()
        return queryset

class StudentDetailView(LoginRequiredMixin,DetailView):
    model = Student
    template_name = 'users/student_detail.html'
    context_object_name = 'student'

def student_detail(request, pk):
    student = get_object_or_404(Student, pk=pk)
    return render(request, 'users/student_detail.html', {'student': student})

def teacher_detail(request, pk):
    teacher = get_object_or_404(Teacher, pk=pk)
    return render(request, 'users/teacher_detail.html', {'teacher': teacher})

class StudentCreateView(CreateView):
    model = Student

    fields = ['username','password','confirm_password','first_name', 'last_name',
              'email', 'school', 'grade', 'section', 'gender', 'age', 'mobile', 'dob',
              'religion', 'spoken_lang', 'address', 'city', 'state', 'country', 'student_id' ]

    def form_valid(self, form):
        form.instance.student = self.request.user
        return super().form_valid(form)
        #return redirect('user-home')

class StudentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Student

    fields = ['first_name', 'last_name', 'email',  'grade', 'section',
               'spoken_lang']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def test_func(self):
        #student = self.get_object()
        if self.request.user.is_student or self.request.user.is_superuser:
            return True
        return False

class StudentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Student
   #success_url = '/'
    def test_func(self):
        #student = self.get_object()
        if self.request.user.is_superuser:
            return True
        return False

class StudentGradesView(TemplateView):
    template_name = 'users/grades.html'

@login_required
def grades(request):
    if request.user.is_student:
        try:
            student = Student.objects.filter(user=request.user).first()
        except ObjectDoesNotExist:
            raise TypeError('Student Doesnt exist')
        try:
            if Student_Grades.objects.filter(student=student).exists():
                grades=Student_Grades.objects.filter(student=student)
                table = StudentGradesTable(grades)
                RequestConfig(request).configure(table)
                return render(request, 'users/list_student_grades.html', {'table': table})
            else:
                messages.error(request,"No grades listed for the student.")
                return render(request, 'users/list_student_grades.html')
        except ObjectDoesNotExist:
            grades=None
            messages.error(request, "No grades listed for the student.")
    elif request.user.is_teacher:
        if Student_Grades.objects.all().exists():
            table = StudentGradesTable(Student_Grades.objects.all())
            RequestConfig(request).configure(table)
            return render(request, 'users/list_student_grades.html', {'table': table})
        else:
            messages.error(request, "No grades listed for the student.")
            return render(request, 'users/list_student_grades.html')
    else:
        messages.error(request, "No grades listed for the student.")
        return render(request, 'users/list_student_grades.html')

class StudentGradesListView(LoginRequiredMixin, PagedFilteredTableView):
    model = Student_Grades
    template_name = 'users/student_grades_list.html'
    table_class = Student_GradesTable
    ordering = ['-id']
    filter_class = Student_GradesListFilter
    formhelper_class = Student_GradesListFormHelper

    context_object_name = 'student_grades'

    def get_queryset(self):
        qs = super(StudentGradesListView, self).get_queryset()
        return qs

    def post(self, request, *args, **kwargs):
        return PagedFilteredTableView.as_view()(request)

    def get_context_data(self, **kwargs):
        context = super(StudentGradesListView, self).get_context_data(**kwargs)
        context['nav_student_grades'] = True
        search_query = self.get_queryset()

        table = Student_GradesTable(search_query)
        RequestConfig(self.request, paginate={'per_page': 7}).configure(table)
        context['table'] = table
        return context

class StudentGradesDetailView(DetailView):
    model = Student_Grades

class StudentGradesCreateView(LoginRequiredMixin, CreateView):
    model = Student_Grades
    form = Student_GradesForm()

    fields = ['student','subject','SA1', 'SA2', 'SA3']

    def get_context_data(self, **kwargs):
        context = super(StudentGradesCreateView, self).get_context_data(**kwargs)
        context['form'].fields['student'].queryset = Teacher_Students.objects.values_list("student_id", flat=True)

        return context

    def form_valid(self, form):
        subject = form.cleaned_data.get('subject')

        student = form.cleaned_data.get('student')

        form.instance.student=Student.objects.filter(student_id=student.pk).first()
        form.instance.teacher_id=self.request.user.teacher.pk

        student_grades = form.save(commit=False)

        student_grades.subject = Subject.objects.filter(subject_name=subject).first()

        student_grades.save()
        messages.success(self.request, 'Student Grades are successfully entered.')
        return redirect('teacher-student-grades-list')

class StudentGradesDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Student_Grades

    def test_func(self):
        student_grades = self.get_object()
        if student_grades.teacher_id == Teacher.objects.filter(user=self.request.user).first().pk:
            return True
        return False

    success_url = '/'

class StudentGradesUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Student_Grades

    fields = ['student', 'subject', 'SA1', 'SA2', 'SA3']

    def form_valid(self, form):
        form.instance.teacher_id = self.request.user.teacher
        return super().form_valid(form)

    def test_func(self):
        student_grades = self.get_object()

        if student_grades.teacher_id == Teacher.objects.filter(user=self.request.user).first().pk:
            return True
        return False

    success_url = '/'
class TeacherListView(ListView):
    model = Teacher
    template_name = 'teacher/home.html'
    context_object_name = 'teacher'
    #ordering = ['-date_created']


class TeacherDetailView(DetailView):
    model = Teacher

class TeacherCreateView(CreateView):
    model = Teacher

    fields = ['first_name', 'last_name', 'school_id', 'email',  'grade', 'section', 'spoken_lang']

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return redirect('user-home')

class TeacherDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Teacher

    def test_func(self):
        teacher = self.get_object()
        if self.request.user.is_superuser:
            return True
        return False

class TeacherUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Teacher

    fields = ['first_name', 'last_name', 'school_id', 'email',  'grade', 'section', 'spoken_lang']

    def form_valid(self, form):
        form.instance.user.teacher = self.request.user.teacher
        return super().form_valid(form)

    def test_func(self):
        teacher = self.get_object()
        if self.request.user.teacher == teacher:
            return True
        return False


class TeacherStudentCreateView(LoginRequiredMixin, CreateView):
    model = Teacher_Students

    fields = ['student']

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'teacher'
        return super().get_context_data(**kwargs)

    def get_initial(self):
        return {'student_id': Student.objects.all().values_list('student_id', flat=True)}

    def form_valid(self, form):
        ls1 = Teacher_Students.objects.all().values_list('student_id', flat=True)
        ls2 = Student.objects.all().values_list('student_id', flat=True)

        form.instance.teacher_id = self.request.user.teacher.pk
        form.instance.school_id=self.request.user.teacher.school_id.pk
        form.instance.user=self.request.user

        if set(ls1) != set(ls2):
            teacher_students = form.save()
            teacher_students.school_id=self.request.user.teacher.school_id
            teacher_students.save()
            messages.success(self.request, 'Student is successfully linked to the teacher.')
            return redirect('teacher-student-list')
        else:
            return render(self.request,template_name='users/error.html')

def teacher_students_list(request):
    table = TeacherStudentsTable(Teacher_Students.objects.all())

    return render(request, 'users/list_teacher_students.html', {'table': table})

class TeacherStudentsListView(LoginRequiredMixin, PagedFilteredTableView):
    model = Teacher_Students
    template_name = 'users/teacher_students_list.html'
    table_class = Teacher_StudentsTable
    ordering = ['-id']
    filter_class = Teacher_StudentsListFilter
    formhelper_class =Teacher_StudentsListFormHelper

    context_object_name = 'teacher_students'

    def get_queryset(self):
        qs = super(TeacherStudentsListView, self).get_queryset()
        return qs

    def post(self, request, *args, **kwargs):
        return PagedFilteredTableView.as_view()(request)

    def get_context_data(self, **kwargs):
        context = super(TeacherStudentsListView, self).get_context_data(**kwargs)
        context['nav_teacher_students'] = True
        search_query = self.get_queryset()

        table = Teacher_StudentsTable(search_query)
        RequestConfig(self.request, paginate={'per_page': 1}).configure(table)
        context['table'] = table
        return context

class TeacherStudentDetailView(DetailView):
    model = Teacher_Students
    template_name = 'users/teacher_students_detail.html'
    context_object_name = 'teacher_students'

class TeacherStudentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Teacher_Students

    def test_func(self):
        teacher_students = self.get_object()
        if self.request.user.teacher == teacher_students.teacher:
            return True
        return False
    success_url = '/'

class UserStudentListView(DetailView):
    model = Student

    template_name = "student/home.html"
    context_object_name = 'student'
    paginate_by = 2

    def get_object(self):
        return self.request.user.student

    def get_queryset(self):
        #user = get_object_or_404(User, username=self.kwargs.get('username'))
        user = User.objects.filter(username=self.kwargs.get('username'))
        student = Student.objects.filter(username=user).first()
        #print (student)
        return student

class CoursesListView(ListView):
    model = Courses

    context_object_name = 'courses'
    paginate_by = 4

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['courses'] = [(field.name, field.value_to_string(self)) for field in Courses._meta.fields]
        return context

class CoursesDetailView(DetailView):
    model = Courses

class CoursesCreateView(LoginRequiredMixin, CreateView):
    model = Courses

    fields = ['subject', 'course_name','course_link']

    def form_valid(self, form):
        subject = form.cleaned_data.get('subject')
        course_name=form.cleaned_data.get('course_name')
        course_link = form.cleaned_data.get('course_link')

        messages.success(self.request, '{subject} Course is successfully created.')
        return super().form_valid(form)

    success_url = '/'

class CoursesUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Courses
    success_url = '/'
    fields = ['subject', 'course_name', 'course_link']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def test_func(self):
        if self.request.user.is_superuser:
            return True
        return False

class CoursesDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Courses
    success_url = '/'
    def test_func(self):
        if self.request.user.is_superuser:
            return True
        return False
class SubjectScoresListView(ListView):
    model = SubjectScores

    #template_name = 'grading/home.html'
    context_object_name = 'subjectscores'
    paginate_by = 4

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #context['fields'] = [field.name for field in SubjectScores._meta.get_fields()]
        context['subjectscores'] = [(field.name, field.value_to_string(self)) for field in SubjectScores._meta.fields]
        return context

class SubjectScoresDetailView(DetailView):
    model = SubjectScores

class SubjectScoresCreateView(LoginRequiredMixin, CreateView):
    model = SubjectScores

    fields = ['student', 'subject']

    def form_valid(self, form):
        student = form.cleaned_data.get('student')
        form.instance.student=Student.objects.filter(student_id=student.pk).first()
        messages.success(self.request, 'Subject is successfully added to the Student.')
        return super().form_valid(form)

    success_url = '/'

class SubjectListView(ListView):
    model = Subject

    template_name = 'grading/home.html'
    context_object_name = 'subjects'
    paginate_by = 4

    #ordering = ['-date_created']

class SubjectDetailView(DetailView):
     model = Subject
     #template_name = 'users/subject_detail.html'


class SubjectCreateView(LoginRequiredMixin, CreateView):
    model = Subject

    fields = ['subject_name', 'subject_desc', 'school_id', 'grade']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    success_url = '/'

class SubjectUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Subject
    success_url = '/'
    fields = ['subject_name', 'subject_desc', 'school_id', 'grade']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def test_func(self):
        subject = self.get_object()
        if self.request.user.is_superuser:
            return True
        return False

class SubjectDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Subject
    success_url = '/'
    def test_func(self):
        #subject = self.get_object()
        if self.request.user.is_superuser:
            return True
        return False

@login_required
def grades_predictor(request):

    if request.method == 'POST':
        f = GradingForm(request.POST)
        if f.is_valid():
            student_id      = f['student_id'].value()
            subject_name    = f['subject_name'].value()
            failures        = float(f['failures'].value())
            mother_edu      = float(f['mother_edu'].value())
            father_edu      = float(f['father_edu'].value())
            Fjob_teacher    = float(f['fjob_teacher'].value())
            age             = float(f['age'].value())
            schoolsup_yes   = float(f['schoolsup_yes'].value())
            higher_yes      = float(f['higher_yes'].value())

            #FinalGrade = 4.27 + -0.38 * failures + 0.08 * mother_edu + 0.08 * father_edu + -0.13 * age + 0.67 * schoolsup_yes + 0.27 * higher_yes
            FinalGrade = 4.27 - 0.38 * failures + 0.14 * mother_edu + 0.33 * Fjob_teacher + 0.14 * father_edu - 0.13 * age + 0.67 * schoolsup_yes + 0.27 * higher_yes
            print(f'{FinalGrade:9.4f}')

            messages.success(request, f'{student_id}\'s  predicted grade in {subject_name} is {FinalGrade:9.4f}! ')
            return redirect('grades-prediction')
    else:
        f=GradingForm()
    return render(request, 'users/grading.html', {'form': f})

class UserSubjectListView(ListView):
    model = Subject

    template_name = "grading/user_subjects.html"
    context_object_name = 'subjects'
    paginate_by = 2


    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Subject.objects.filter(username=user)


class MainView(TemplateView):
    template_name = 'users/career_options.html'

    def get(self, request, *args, **kwargs):
        subjectscores_form = SubjectScoresForm(self.request.GET or None)
        context = self.get_context_data(**kwargs)
        context['subjectscores_form'] = subjectscores_form
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        subjectscores_form = SubjectScoresForm(self.request.POST)
        context = self.get_context_data(**kwargs)
        context['subjectscores_form'] = subjectscores_form
        if subjectscores_form.is_valid():
            student = subjectscores_form.cleaned_data.get('student')
            subject = subjectscores_form.cleaned_data.get('subject')
            subject_score = subjectscores_form.cleaned_data.get('subject_score')
            if (int(subject_score) < 50):
                courses = Courses.objects.filter(subject=subject)
                context['courses'] = courses
                messages.success(request, f'{student}\'s  recommended courses in {subject} are  ')
        return self.render_to_response(context)

class SubjectScores_FormView(FormView):
    form_class = SubjectScoresForm
    template_name = 'users/courses_list.html'
    success_url = '/'

    def post(self, request, *args, **kwargs):
        subjectscores_form = self.form_class(request.POST)
        if subjectscores_form.is_valid():
            subjectscores_form.save()
            return self.render_to_response(
                self.get_context_data(
                    success=True
                )
            )
        else:
            return self.render_to_response(
                self.get_context_data(
                    subjectscores_form=subjectscores_form
                )
            )
