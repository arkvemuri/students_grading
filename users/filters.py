# filters.py
import django_filters
from .models import Student_Grades


class Student_GradesListFilter(django_filters.FilterSet):
    class Meta:
        model = Student_Grades
        fields = ["student", "subject", "SA1", "SA2", "SA3"]
        order_by = ['pk']