from django.shortcuts import render,redirect
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    DeleteView
)
from django.contrib.auth.mixins import LoginRequiredMixin


# def home(request):
#     if request.method == 'POST':
#         return render(request, "teacher/teacher.html", context)
#     return render(request, 'teacher/teacher.html')