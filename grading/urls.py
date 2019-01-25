from django.urls import path
from . import views


urlpatterns = [
    path('', views.home,name='grading-home'),
    path('about/',views.about,name='grading-about'),
    path('grading/', views.grading, name='grading-grading'),



]