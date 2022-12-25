'''
configuration for the project
'''

from pathlib import Path

import environ

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

APPS_DIR = BASE_DIR / "apps"

env = environ.Env()
env.read_env(str(BASE_DIR / ".env"))



# Quick-start development settings - unsuitable for production
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env(
    "SECRET_KEY",
    # fallback value if secret is key is not provided
    default="SpiS8STrVjjVkFCr22C1hukiqbaF1CF9CBXF0036HkI3AVbZDvAC91KEAfuH6DHN"
    )

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env('DJANGO_DEBUG')

# ALLOWED_HOSTS = ["localhost", "0.0.0.0", "127.0.0.1"]
ALLOWED_HOSTS = ["*"]


# Application definition

# django apps
DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

# external apps
THIRD_PARTY_APPLICATIONS = [
    "corsheaders",
    "rest_framework",
    "rest_framework_simplejwt.token_blacklist",
    "rest_framework_simplejwt",
    "drf_yasg"
]

# internal apps 
LOCAL_APPS = [
    "apps.users.apps.UsersConfig",
    "apps.environment.apps.EnvironmentConfig",
    "apps.generator.apps.GeneratorConfig",
    "apps.students.apps.StudentsConfig",
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPLICATIONS + LOCAL_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',

    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

# as im using Django as an API, I will not be using the template
# engines
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

WSGI_APPLICATION = 'core.wsgi.application'


# DATABASE

DATABASES = {
    # main postgres data
    'default': env.db(),
    # back up database if the postgres one is unavailable
    'extra':{
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'backup-db.sqlite3',
    }
}


# Password validation

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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True



# Static files (CSS, JavaScript, Images)

STATIC_URL = '/static/'

# Default primary key field type

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Authentication
AUTH_USER_MODEL = "users.User"


# Django Rest Framework

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        # 'rest_framework_simplejwt.authentication.JWTStatelessUserAuthentication',

        'rest_framework_simplejwt.authentication.JWTAuthentication',
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.TokenAuthentication",
    ),
    # WARNING - THIS PERMISSION MUST BE SET TO 'ISUATHENTICATED' DURING PRODUCTION TO PROTECT ENDPOINTS
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.AllowAny",),
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema'
}

SITE_ID = 1

# simple JWT
import datetime

SIMPLE_JWT = {
    # WARNING CHANGE ACCESS TOKEN TO BE SHORTER
    'ACCESS_TOKEN_LIFETIME': datetime.timedelta(minutes=100),
    'REFRESH_TOKEN_LIFETIME': datetime.timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': False,

    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,
    'JWK_URL': None,
    'LEEWAY': 0,

    'AUTH_HEADER_TYPES': ('Bearer','JWT'),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'uuid',
    'USER_ID_CLAIM': 'user_id',
    'USER_AUTHENTICATION_RULE': 'rest_framework_simplejwt.authentication.default_user_authentication_rule',

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
    'TOKEN_USER_CLASS': 'rest_framework_simplejwt.models.TokenUser',

    'JTI_CLAIM': 'jti',

    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': datetime.timedelta(minutes=5),
    'SLIDING_TOKEN_REFRESH_LIFETIME': datetime.timedelta(days=1),
}

# declares that the DRF will use JWT for authentication
REST_USE_JWT = True

# CORS
# crucial to define so that the frontend can communitcate
CORS_ALLOWED_ORIGINS = [
    'http://localhost:8080'
]

BLOCK_GENERATOR_OPTIONS = {
    # use during debugging to read from static file
    "data_and_options_use_static":False,
}

OBG_SETTINGS = {
    "DEBUG":True
}

# option block options
MAX_BLOCKS = 15
DEFAULT_CLASS_SIZE = 24
MAX_CLASS_SIZE = 40
ROOM_CODE_LENGTH = 8

# API Files options
DATA_CSV_LOOKUP = "data"
OPTIONS_CSV_LOOKUP = "options"

# generator settings (DEBUG ONLY)
NODE_DEBUG = True
GENERATOR_DEBUG = True

EBACC_SUBJECTS = {
        "humanities":["Hi","Ge"],
        "languages":["Fr","Sn"],
        "sciences":["Sc","Co"],
        "vocational":["Co","Bs","Eg","Cb", "Hc", "Bb", "Mu", "Pb", "Sb", "Hb", "Mu"]
    }
