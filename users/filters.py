# filters.py
import django_filters
from .models import Student_Grades, Teacher_Students

class Teacher_StudentsListFilter(django_filters.FilterSet):
    class Meta:
        model = Teacher_Students
        fields = ["id","date_created","school_id","student_id","teacher_id"]
        order_by = ['pk']

class Student_GradesListFilter(django_filters.FilterSet):
    class Meta:
        model = Student_Grades
        fields = ["student", "subject", "SA1", "SA2", "SA3"]
        order_by = ['pk']