"""
Django settings for students_grading project.

Generated by 'django-admin startproject' using Django 2.1.4.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os
import json

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

with open(os.path.join(BASE_DIR, 'config.json')) as config_file:
    config=json.load(config_file)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config['SECRET_KEY']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['www.studentsgrading.co.in','localhost','studentsgrading.appspot.com']


# Application definition

INSTALLED_APPS = [
    'grading.apps.GradingConfig',
    'users.apps.UsersConfig',
    'student.apps.StudentConfig',
    'teacher.apps.TeacherConfig',
    'school_admin.apps.SchoolAdminConfig',
    'contacts.apps.ContactsConfig',
    'crispy_forms',
    'django.contrib.admin',
    'django.contrib.auth',
    'reset_migrations',
    'django_tables2',
    'django_filters',
    'bootstrap4',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'social_django'  # <--
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'social_django.middleware.SocialAuthExceptionMiddleware',  # <--
]

AUTHENTICATION_BACKENDS = (
    'social_core.backends.github.GithubOAuth2',
    'social_core.backends.twitter.TwitterOAuth',
    'social_core.backends.facebook.FacebookOAuth2',
    'social_core.backends.google.GoogleOpenId',
    'social_core.backends.google.GoogleOAuth2',
    'django.contrib.auth.backends.ModelBackend',
    #'django.db.backends.mysql',
)

ROOT_URLCONF = 'students_grading.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'social_django.context_processors.backends',  # <--
                'social_django.context_processors.login_redirect', # <--
            ],
        },
    },
]

WSGI_APPLICATION = 'students_grading.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases
# [START db_setup]
if os.getenv('GAE_APPLICATION', None):
    # Running on production App Engine, so connect to Google Cloud SQL using
    # the unix socket at /cloudsql/<your-cloudsql-connection string>
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'HOST': '/cloudsql/studentsgrading:asia-south1:students-grading',
            'USER': 'rkvemuri',
            'PASSWORD': 'Ananth@2019',
            'NAME': 'students-grading',
        }
    }

else:
    # Running locally so connect to either a local MySQL instance or connect to
    # Cloud SQL via the proxy. To start the proxy via command line:
    #
    #     $ cloud_sql_proxy -instances=[INSTANCE_CONNECTION_NAME]=tcp:3306
    #
    # See https://cloud.google.com/sql/docs/mysql-connect-proxy
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'HOST': 'localhost',
            'PORT': '3306',
            'NAME': 'students_grading',
            'USER': 'rkvemuri',
            'PASSWORD': 'Ananth@2019',
        }
    }
# [END db_setup]




# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

#STATIC_URL = 'https://storage.googleapis.com/students_grading/static/'
STATIC_URL = '/static/'
STATIC_ROOT= os.path.join(BASE_DIR, 'static')

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

CRISPY_TEMPLATE_PACK = 'bootstrap4'

LOGIN_REDIRECT_URL = 'grading-home'

LOGIN_URL = 'login'
LOGOUT_URL = 'logout'

SOCIAL_AUTH_GITHUB_KEY = config.get('GITHUB_KEY')
SOCIAL_AUTH_GITHUB_SECRET = config.get('GITHUB_SECRET')

SOCIAL_AUTH_TWITTER_KEY = config.get('TWITTER_KEY')
SOCIAL_AUTH_TWITTER_SECRET = config.get('TWITTER_SECRET')

SOCIAL_AUTH_FACEBOOK_KEY = config.get('FACEBOOK_KEY')  # App ID
SOCIAL_AUTH_FACEBOOK_SECRET = config.get('FACEBOOK_SECRET')  # App Secret

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = config.get('GOOGLE_OAUTH2_KEY')   # App ID
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = config.get('GOOGLE_OAUTH2_SECRET')   # App Secret

SOCIAL_AUTH_PIPELINE = (
    'social_core.pipeline.social_auth.social_details',
    'social_core.pipeline.social_auth.social_uid',
    'social_core.pipeline.social_auth.social_user',
    'social_core.pipeline.user.get_username',
    'social_core.pipeline.user.create_user',
    'social_core.pipeline.social_auth.associate_user',
    'social_core.pipeline.social_auth.load_extra_data',
    'social_core.pipeline.user.user_details',
    'social_core.pipeline.social_auth.associate_by_email',
)
#SOCIAL_AUTH_FACEBOOK_SCOPE = ['email']
SOCIAL_AUTH_FACEBOOK_PROFILE_EXTRA_PARAMS = {
    'fields': 'id,name,email',
}
SOCIAL_AUTH_USER_FIELDS = ['email', 'username']
SOCIAL_AUTH_USERNAME_IS_FULL_EMAIL = True

SOCIAL_AUTH_LOGIN_ERROR_URL = '/settings/'
SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/settings/'
SOCIAL_AUTH_RAISE_EXCEPTIONS = False

#EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = config.get('EMAIL_USER')
EMAIL_HOST_PASSWORD = config.get('EMAIL_PASS')

# Use BOOTSTRAP3 if you are using Bootstrap 3
BOOTSTRAP4 = {
    'include_jquery': True,
}
AUTH_USER_MODEL = "users.User"
DJANGO_TABLES2_TEMPLATE = "django_tables2/bootstrap4.html"
