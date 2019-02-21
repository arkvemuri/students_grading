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
    args['students'] = Student.objects.all()
    args['teachers'] = Teacher.objects.all()
    args['subjects'] = Subject.objects.all()

    try:
        if User.objects.filter(username=request.user.username).exists():
            user = User.objects.filter(username=request.user.username).first()
            request.session['username'] = request.user.username

            if Student.objects.filter(user=user).exists():
                student=Student.objects.filter(user=user).first()
                args['student'] = student
                args['subjectscores'] = SubjectScores.objects.filter(student_id=student)
                args['student_grades']= Student_Grades.objects.filter(student_id=student)
            else:
                pass

            if Teacher.objects.filter(user=user).exists():
                teacher = Teacher.objects.filter(user=user).first()
                args['teacher'] = teacher
                if Teacher_Students.objects.filter(teacher_id=teacher).exists():
                    teacher_student = Teacher_Students.objects.filter(teacher_id=teacher)
                    args['teacher_students'] = teacher_student
            else:
                pass
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

    response.set_cookie('last_connection', datetime.datetime.now())
    response.set_cookie('username', datetime.datetime.now())

    return response
# GRADES = [85, 92, 96, 67, 73]
def numerical_grade(grades):
    return (sum(grades) / float(len(grades))) / 100

# GRADE = 0.75
def letter_grade(grade):
    grades = 'ABCDFFFFFF'
    if grade > 0:
        return grades[10 - ceil(grade * 10)]
    else:
        return 'F'

def gradeScores(FinalGrade):
    if FinalGrade >= 90 and FinalGrade <= 100:
        return("You received an A")

    elif FinalGrade >= 80 and FinalGrade < 90:
        return("You received a B")

    elif FinalGrade >= 70 and FinalGrade < 80:
        return("You received a C")

    elif FinalGrade >= 60 and FinalGrade < 70:
        return("You received a D")

    else:
        return("Sorry, you received an F")

def about(request):
    return render(request,'grading/about.html',{'title': 'Grading About'})
