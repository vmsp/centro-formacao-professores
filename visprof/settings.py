import datetime
from pathlib import Path

import environ

env = environ.Env()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve(strict=True).parent.parent

environ.Env.read_env(str(BASE_DIR / '.env'))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/dev/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env.str('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool('DEBUG', False)

INTERNAL_IPS = ['.localhost', '127.0.0.1', '[::1]'] if DEBUG else []

ALLOWED_HOSTS = ['*']  # TODO(vitor): Isto pode ser má ideia

CRISPY_FAIL_SILENTLY = not DEBUG

# Application definition

INSTALLED_APPS = [
    'whitenoise.runserver_nostatic',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'crispy_forms',
    'django_tables2',
    'compressor',
    'visprof.apps.VisProfConfig',
]

if DEBUG:
    INSTALLED_APPS += ['django_extensions', 'shouty']

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    # 'sesame.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'visprof.urls'

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
            ],
        },
    },
]

SHOUTY_VARIABLE_BLACKLIST = {
    '*': (
        'auth/widgets/read_only_password_hash.html',
        'bootstrap4/display_form.html',
        'bootstrap4/errors.html',
        'bootstrap4/field.html',
        'bootstrap4/uni_form.html',
        'bootstrap4/layout/checkboxselectmultiple.html',
        'bootstrap4/layout/help_text_and_errors.html',
        'bootstrap4/layout/radioselect.html',
        'django_tables2/bootstrap4.html',
        'visprof/layout/radio_with_other.html',
    ),
}

WSGI_APPLICATION = 'visprof.wsgi.application'

# Database
# https://docs.djangoproject.com/en/dev/ref/settings/#databases

DATABASES = {'default': env.db()}

# Email

EMAIL_CONFIG = env.email()
vars().update(EMAIL_CONFIG)

DEFAULT_FROM_EMAIL = env.str('DEFAULT_FROM_EMAIL')

# Password validation
# https://docs.djangoproject.com/en/dev/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME':
            'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',  # pylint: disable=line-too-long
    },
    {
        'NAME':
            'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME':
            'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME':
            'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/dev/topics/i18n/

LANGUAGE_CODE = 'pt-pt'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/dev/howto/static-files/

STATIC_URL = '/static/'

STATIC_ROOT = env.path('STATIC_ROOT', '/static')

STATICFILES_DIRS = ['node_modules']

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
]

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

COMPRESS_OFFLINE = True

# Authentication

AUTH_USER_MODEL = 'visprof.User'

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'visprof.auth_backends.OAuthBackend',
    'sesame.backends.ModelBackend',
]

# TODO(vitor): 1 semana é suficiente?
SESAME_MAX_AGE = datetime.timedelta(weeks=1)

AUTHLIB_OAUTH_CLIENTS = {
    'microsoft': {
        'client_id': 'e0910b82-0fbd-4184-845c-f615b9704a2d',
        'client_secret': '21tIiw5rc03S3A.M_-.l~PyNA3GZLM5sJ0',
    },
    'google': {
        'client_id':
            '766162854093-hs8thauu6okrbevckna0ljeoia2sd9ed.apps.googleusercontent.com',  # pylint: disable=line-too-long
        'client_secret':
            'UCi3jyJo5tKtZOIhzj7kigKO',
    },
}

# Theming

CRISPY_TEMPLATE_PACK = 'bootstrap4'

DJANGO_TABLES2_TEMPLATE = 'django_tables2/bootstrap4.html'
