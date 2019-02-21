import django_tables2 as tables
from django_tables2.utils import A

from .models import Student_Grades, Student, Teacher, Teacher_Students,  Subject,SubjectScores

class SubjectTable(tables.Table):
    class Meta:
        model = Subject
        template_name = 'django_tables2/bootstrap4.html'
        attrs = {'class': 'table table-striped table-dark'}

class StudentTable(tables.Table):
    class Meta:
        model = Student
        template_name = 'django_tables2/bootstrap4.html'
        attrs = {'class': 'table table-striped table-dark'}

class SubjectScoresTable(tables.Table):
    class Meta:
        model = SubjectScores
        template_name = 'django_tables2/bootstrap4.html'
        attrs = {'class': 'table table-striped table-dark'}

class StudentGradesTable(tables.Table):
    class Meta:
        model = Student_Grades
        template_name = 'django_tables2/bootstrap4.html'
        attrs = {'class': 'table table-striped table-dark'}
        fields = ("student", "subject", "SA1", "SA2", "SA3")
        empty_text = "There are no student grades matching the search criteria..."

class Student_GradesTable(tables.Table):
    student = tables.LinkColumn('teacher-student-grades-detail', args=[A('pk')])
    subject = tables.LinkColumn('teacher-student-grades-detail', args=[A('pk')])
    SA1 = tables.LinkColumn('teacher-student-grades-detail', args=[A('pk')])
    SA2 = tables.LinkColumn('teacher-student-grades-detail', args=[A('pk')])
    SA3 = tables.LinkColumn('teacher-student-grades-detail', args=[A('pk')])

    class Meta:
        model = Student_Grades
        template_name = 'django_tables2/bootstrap4.html'
        attrs = {"class": "table table-striped table-dark table-bordered"}

        #attrs = {'class': 'table table-striped table-dark'}
        fields = ("student", "subject", "SA1", "SA2", "SA3")
        empty_text = "There are no student grades matching the search criteria..."
        #edit = TemplateColumn(template_name='users/student_grades_list.html')

        #subject = tables.Column(attrs={'tr': {'bgcolor': 'white'}})

