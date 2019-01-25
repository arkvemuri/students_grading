from django.urls import path
from . import views
from django.conf.urls import url, include
from .views import(
    StudentListView,
    StudentDetailView,
    StudentCreateView,
    StudentDeleteView,
    StudentUpdateView,
    TeacherListView,
    TeacherDetailView,
    TeacherCreateView,
    TeacherDeleteView,
    TeacherUpdateView,
    SignUpView,
    TeacherStudentCreateView,
    StudentSignUpView,
    TeacherSignUpView,
    StudentGradesListView,
    StudentGradesCreateView,
    StudentGradesDeleteView,
    StudentGradesDetailView,
    StudentGradesUpdateView,
    UserStudentListView,
    SubjectListView,
    SubjectDetailView,
    SubjectCreateView,
    SubjectDeleteView,
    SubjectUpdateView,
    UserSubjectListView,
    TeacherStudentListView,
    TeacherStudentDetailView,
    StudentGradesListView,
    StudentGradesDetailView,
    StudentGradesView,
    TeacherStudentDeleteView,
)

urlpatterns = [
    path('student/grades', StudentGradesView.as_view(), name='teacher-student-grades'),
    path('student/grades/list/', StudentGradesListView.as_view(), name='teacher-student-grades-list'),
    path('student/grades/<int:pk>/', StudentGradesDetailView.as_view(), name='teacher-student-grades-detail'),
    path('student/grades/new/', StudentGradesCreateView.as_view(), name='teacher-student-grades-new'),
    path('student/grades/<int:pk>/update/', StudentGradesUpdateView.as_view(), name='teacher-student-grades-update'),
    path('student/grades/<int:pk>/delete/', StudentGradesDeleteView.as_view(), name='teacher-student-grades-delete'),

    url(r'^student/(?P<pk>[\w-]+)/update/', StudentUpdateView.as_view(), name='student-update'),
    path('student/', StudentListView.as_view(), name='student-list'),
    url(r'^student/(?P<pk>[\w-]+)/$', StudentDetailView.as_view() , name='student-detail'),

    path('teacher_student/new/', TeacherStudentCreateView.as_view(), name='teacher_student_link'),
    path('teacher_student/', TeacherStudentListView.as_view(), name='teacher-student-list'),
    path('teacher_student/<int:pk>/', TeacherStudentDetailView.as_view(), name='teacher-student-detail'),
    url(r'^teacher_student/(?P<pk>[\w-]+)/delete/', TeacherStudentDeleteView.as_view(), name='teacher-student-delete'),

    path('signup/', SignUpView.as_view(), name='signup'),
    path('signup/student/new/', StudentSignUpView.as_view(), name='student_signup'),
    path('signup/teacher/new/', TeacherSignUpView.as_view(), name='teacher_signup'),

    path('teacher/', TeacherListView.as_view(), name='teacher-list'),
    url(r'^teacher/(?P<pk>[\w-]+)/update/', TeacherUpdateView.as_view(), name='teacher-update'),
    url(r'^teacher/(?P<pk>[\w-]+)/delete/', TeacherDeleteView.as_view(), name='teacher-delete'),
    path('teacher/<int:pk>/', TeacherDetailView.as_view(), name='teacher-detail'),


    path('subject/', SubjectListView.as_view(), name='subject-list'),
    path('subject/new/', SubjectCreateView.as_view(), name='subject-create'),
    path('subject/<int:pk>/', SubjectDetailView.as_view(), name='subject-detail'),
    path('subject/<int:pk>/update/', SubjectUpdateView.as_view(), name='subject-update'),
    path('subject/<int:pk>/delete/', SubjectDeleteView.as_view(), name='subject-delete'),

    path('grading/', views.grades_predictor, name='grades-prediction'),
    url(r'^career/<int:pk>', views.show_choices, name='career-choices'),
]