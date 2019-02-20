from django_tables2 import  TemplateColumn
import django_tables2 as tables

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

class Student_GradesTable(tables.Table):
    class Meta:
        model = Student_Grades
        template_name = 'django_tables2/bootstrap4.html'
        attrs = {'class': 'table table-striped table-dark'}
        empty_text = "There are no grades yet"
        #student = tables.Column(attrs={'th': {'bgcolor': 'white'}})
        fields = ["student", "subject", "SA1", "SA2", "SA3"]
    #edit = TemplateColumn(template_name='users/student_grades_list.html')

        #subject = tables.Column(attrs={'tr': {'bgcolor': 'white'}})

