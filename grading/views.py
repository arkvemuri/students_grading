from django.shortcuts import render, get_object_or_404
import pandas as pd
import os
from django.shortcuts import render_to_response
from django.core import serializers
from json2html import *
import json
from django.http import HttpResponse
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

from users.models import User, Student, Teacher, Student_Grades, Teacher_Students, Subject,SubjectScores
from django.template import RequestContext
import datetime
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

basedir = os.path.abspath(os.path.dirname(__file__))

def grading(request):
    if request.method == 'POST':
        csvfile = request.FILES['csv_file']
        data = pd.read_csv(os.path.join(basedir, csvfile.name))

        data_html = data.to_html()
        context = {'loaded_data': data_html}
        return render(request, "grading/grading_results.html", context)
    return render(request, 'grading/grading.html')


@login_required
def home(request):
    args = {}
    students_list=Student.objects.all()
    teachers_list=Teacher.objects.all()
    subjects_list=Subject.objects.all().order_by('id')
    #ordering = ['-id']
    paginate_by = 4
    paginator = Paginator(subjects_list, paginate_by)

    #paginator1=Paginator(students_list, paginate_by)
    page = request.GET.get('page')
    try:
        subjects = paginator.page(page)
        #students = paginator1.page(page)
    except PageNotAnInteger:
        subjects = paginator.page(1)
        #students = paginator1.page(1)
    except EmptyPage:
        subjects = paginator.page(paginator.num_pages)
        #students = paginator1.page(paginator.num_pages)

    args['subjects'] = subjects
    args['students'] = students_list

    args['teachers'] = teachers_list
    try:
        if User.objects.filter(username=request.user.username).exists():
            user = User.objects.filter(username=request.user.username).first()
            request.session['username'] = request.user.username

            if Student.objects.filter(user=user).exists():
                student=Student.objects.filter(user=user).first()
                args['student'] = student
                args['subjectscores'] = SubjectScores.objects.all()
                args['student_grades']= Student_Grades.objects.filter(student_id=student)
            else:
                pass

            if Teacher.objects.filter(user=user).exists():
                teacher = Teacher.objects.filter(user=user).first()
                args['teacher'] = teacher
                args['subject'] = Subject.objects.filter(pk=teacher.subject_id.id).first()
                if Teacher_Students.objects.filter(teacher_id=teacher).exists():
                    teacher_students = Teacher_Students.objects.filter(teacher_id=teacher)
                    args['teacher_students'] = teacher_students
            else:
                if Teacher_Students.objects.all().exists():
                    teacher_students = Teacher_Students.objects.all()
                    args['teacher_students'] = teacher_students
        else:
            pass
    except Student.DoesNotExist:
        raise TypeError('Student Doesnt exist')
    except Teacher.DoesNotExist:
        raise TypeError('Teacher doesnt exist')
    except User.DoesNotExist:
        raise TypeError('User doesnt exist')


    if request.user.is_authenticated:
        if request.user.is_student:
            response= render(request, 'student/home.html', args,{"username": request.user.username})
        elif request.user.is_teacher:
            response= render(request, 'teacher/home.html', args,{"username": request.user.username})
        else:
            response= render(request, 'users/home.html', args,{"username": request.user.username})
    else:
        response= render(request, 'users/login.html', args)

    return response


def about(request):
    return render(request,'grading/about.html',{'title': 'Grading About'})
