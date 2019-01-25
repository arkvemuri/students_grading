"""students_grading URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include

from users import views as user_views
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url, include
#from users.views import UserProfileUpdateView
from django.views.generic import TemplateView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include('grading.urls')),
    url(r'^contacts/', include('contacts.urls')), # new
    url(r'^register/', user_views.register, name='register'),

    path('password-reset/', auth_views.PasswordResetView.as_view(template_name= 'users/password_reset.html'), name='password_reset'),
    path('password-reset-complete/', auth_views.PasswordResetView.as_view(template_name= 'users/password_reset_complete.html'), name='password_reset_complete'),
    path('password-reset/done', auth_views.PasswordResetDoneView.as_view(template_name= 'users/password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name= 'users/password_reset_confirm.html'), name='password_reset_confirm'),

    url(r'^connection/',user_views.formView, name='loginform'),
    url(r'^login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    url(r'^logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    url(r'^profile/', user_views.profile, name='profile'),
    url(r'^oauth/', include('social_django.urls', namespace='social')),
    url(r'^settings/$', user_views.settings, name='settings'),
    url(r'^settings/password/$', user_views.password, name='password'),
    url(r'^student/', include('student.urls')),
    url(r'^teacher/', include('teacher.urls')),
    url(r'^users/', include('users.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)