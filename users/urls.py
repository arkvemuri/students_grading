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
    TeacherStudentsCreateView,
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
    SubjectScoresListView,
    SubjectScoresDetailView,
    SubjectScoresCreateView,
    UserSubjectListView,
    TeacherStudentsDetailView,
    StudentGradesListView,
    StudentGradesDetailView,
    StudentGradesView,
    TeacherStudentsDeleteView,
    TeacherStudentsListView,
    CoursesCreateView,
    CoursesDeleteView,
    CoursesDetailView,
    CoursesUpdateView,
    CoursesListView,
    StudentReportsView,
)
#from django.conf import settings

urlpatterns = [
    path('student/grades', StudentGradesView.as_view(), name='teacher-student-grades'),
    path('student/grades/list/', StudentGradesListView.as_view(), name='teacher-student-grades-list'),
    path('student/grades/<int:pk>/', StudentGradesDetailView.as_view(), name='teacher-student-grades-detail'),
    path('student/grades/new/', StudentGradesCreateView.as_view(), name='teacher-student-grades-new'),
    path('student/grades/<int:pk>/update/', StudentGradesUpdateView.as_view(), name='teacher-student-grades-update'),
    path('student/grades/<int:pk>/delete/', StudentGradesDeleteView.as_view(), name='teacher-student-grades-delete'),

    url(r'^student/(?P<pk>[\w-]+)/update/', StudentUpdateView.as_view(), name='student-update'),
    url(r'^student/(?P<pk>[\w-]+)/delete/', StudentDeleteView.as_view(), name='student-delete'),
    url(r'^student/list/', StudentListView.as_view(), name='student-list'),
    url(r'^student/(?P<pk>[\w-]+)/$', StudentDetailView.as_view() , name='student-detail'),
    url(r'^student/reports/view/', views.StudentReportsView , name='student-reports'),
    path('students/reports/upload/', views.UploadReports, name='upload-reports'),

    path('teacher/student/new/', TeacherStudentsCreateView.as_view(), name='link-teacher-student'),
    #path('teacher_student/', TeacherStudentListView.as_view(), name='teacher-student-list'),
    #path('teacher_student/list/', views.teacher_students_list, name='list-teacher-students'),
    path('teacher/student/list/', TeacherStudentsListView.as_view(), name='list-teacher-students'),
    path('teacher/student/<int:pk>/', TeacherStudentsDetailView.as_view(), name='teacher-student-detail'),
    url(r'^teacher/student/(?P<pk>[\w-]+)/delete/', TeacherStudentsDeleteView.as_view(), name='teacher-student-delete'),

    path('signup/', SignUpView.as_view(), name='signup'),
    path('signup/student/new/', StudentSignUpView.as_view(), name='student_signup'),
    path('signup/teacher/new/', TeacherSignUpView.as_view(), name='teacher_signup'),
    url(r'^ajax/validate_username/$', views.validate_username, name='validate_username'),

    url(r'^teacher/list/', TeacherListView.as_view(), name='teacher-list'),
    url(r'^teacher/(?P<pk>[\w-]+)/update/', TeacherUpdateView.as_view(), name='teacher-update'),
    url(r'^teacher/(?P<pk>[\w-]+)/delete/', TeacherDeleteView.as_view(), name='teacher-delete'),
    url(r'^teacher/(?P<pk>[\w-]+)/', TeacherDetailView.as_view(), name='teacher-detail'),

    path('subject/scores', SubjectScoresListView.as_view(), name='subject-scores-list'),
    path('subject/scores/<int:pk>', SubjectScoresDetailView.as_view(), name='subject-scores-detail'),
    url(r'^ajax/load_subjects/$', views.load_subjects, name='ajax_load_subjects'),  # <-- this one here
    #url(r'^subject/select/', views.show_choices, name="career-select"),
    url(r'^subject/scores/new/', SubjectScoresCreateView.as_view(), name="subject-scores-new"),

    path('subject/', SubjectListView.as_view(), name='subject-list'),
    path('subject/new/', SubjectCreateView.as_view(), name='subject-create'),
    path('subject/<int:pk>/', SubjectDetailView.as_view(), name='subject-detail'),
    path('subject/<int:pk>/update/', SubjectUpdateView.as_view(), name='subject-update'),
    path('subject/<int:pk>/delete/', SubjectDeleteView.as_view(), name='subject-delete'),

    path('grading/', views.grades_predictor, name='grades-prediction'),
    url(r'^career/', views.MainView.as_view(), name='career-choices'),
    path('grades/list/', views.grades, name='list-student-grades'),

    path('courses/', views.MainView.as_view(), name="recommend-courses"),
    path('courses/list/', CoursesListView.as_view(), name="list-courses"),
    path('courses/add/', CoursesCreateView.as_view(), name="create-courses"),
    path('courses/<int:pk>/update/', CoursesUpdateView.as_view(), name="course-update"),
    path('courses/<int:pk>/delete/', CoursesDeleteView.as_view(), name="course-delete"),

]