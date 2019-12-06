"""
Django settings for mandal project.

Generated by 'django-admin startproject' using Django 2.2.5.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MEDIA_ROOT = os.path.join(BASE_DIR, "media")
FILES_ROOT = os.path.join(BASE_DIR, "files")
BIOIMAGE_ROOT = os.path.join(MEDIA_ROOT, "bioimages")
H5FILES_ROOT = os.path.join(MEDIA_ROOT, "h5files")
PANDAS_ROOT = os.path.join(MEDIA_ROOT, "pandas")
NIFTI_ROOT = os.path.join(MEDIA_ROOT, "nifti")
PROFILES_ROOT = os.path.join(MEDIA_ROOT, "profiles")
EXCELS_ROOT = os.path.join(MEDIA_ROOT, "excels")
UPLOAD_ROOT = os.path.join(MEDIA_ROOT, "_upload")
MEDIA_URL = "/images/"
DOCKER = False
DEBUG = True
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'e+uck-nbb+_%(d@%s-@l@*o!xp__p7rssglb74xr*6=m5lh=vx'

# SECURITY WARNING: don't run with debug turned on in production!
ALLOWED_HOSTS = ['129.206.5.200','127.0.0.1',"localhost",'johannesroos.de','129.206.173.171',"192.168.0.116","192.168.137.1","192.168.99.100"]

#Cors Settings
CORS_ORIGIN_ALLOW_ALL = True

# Application definition
INSTALLED_APPS = [
    'registration',
    'dal',
    'dal_select2',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'oauth2_provider',
    'graphene_django',
    'rest_framework',
    'django_filters',
    'django_extensions',
    'channels',
    'corsheaders',
    'taggit',
    'chat',
    'social',
    'metamorphers',
    'transformers',
    'evaluators',
    'mutaters',
    'filterbank',
    'bioconverter',
    'biouploader',
    'drawing',
    'elements',
    'revamper',
    'flow',
    'answers',
    'visualizers',
    'importer',
]

# Taggit Settings
TAGGIT_CASE_INSENSITIVE = True # for the tags system

# Registration Settings
ACCOUNT_ACTIVATION_DAYS = 7 # One-week activation window; you may, of course, use a different value.
REGISTRATION_AUTO_LOGIN = True # Automatically log the user in.

redis_host = os.environ.get('REDIS_HOST', 'localhost')

# Channel layer definitions
# http://channels.readthedocs.io/en/latest/topics/channel_layers.html
CHANNEL_LAYERS = {
    "default": {
        # This example app uses the Redis channel layer implementation channels_redis
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [(redis_host, 6379)],
        },
    },
}

# ASGI_APPLICATION should be set to your outermost router
ASGI_APPLICATION = 'mandal.routing.application'

OAUTH2_PROVIDER = {
    # this is the list of available scopes
    'SCOPES': {
        'read': 'Reading all of your Data ',
        'read_starred': "Reading your shared Data",
        'write': 'Modifying all of your Data',
        'profile': 'Access to your Profile (including Email, Name and Address'}

}
# Rest Framework settings
REST_FRAMEWORK = {

    'DEFAULT_PERMISSION_CLASSES': (
       'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'oauth2_provider.contrib.rest_framework.OAuth2Authentication',
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    )
}

GRAPHENE = {
    'SCHEMA': 'gql.schema.schema', # Where your Graphene schema lives
    'MIDDLEWARE': [
            'graphene_django_extras.ExtraGraphQLDirectiveMiddleware'
        ]
}

GRAPHENE_DJANGO_EXTRAS = {
    'DEFAULT_PAGINATION_CLASS': 'graphene_django_extras.paginations.LimitOffsetGraphqlPagination',
    'DEFAULT_PAGE_SIZE': 20,
    'MAX_PAGE_SIZE': 50,
    'CACHE_ACTIVE': True,
    'CACHE_TIMEOUT': 300  # seconds
}

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'mandal.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
                os.path.join(BASE_DIR, 'templates'),
        ],
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

WSGI_APPLICATION = 'mandal.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases
if DOCKER:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'postgres',
            'USER': 'postgres',
            'HOST': 'db',
            'PORT': 5432,
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db/db.sqlite3'),
        }
    }


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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

LOGIN_REDIRECT_URL = "/"
# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LOGPIPE = {
    # Required Settings
    'OFFSET_BACKEND': 'logpipe.backend.kafka.ModelOffsetStore',
    'CONSUMER_BACKEND': 'logpipe.backend.kafka.Consumer',
    'PRODUCER_BACKEND': 'logpipe.backend.kafka.Producer',
    'KAFKA_BOOTSTRAP_SERVERS': [
        'kafka:9092'
    ],
    'KAFKA_CONSUMER_KWARGS': {
        'group_id': 'django-logpipe',
    },

    # Optional Settings
    # 'KAFKA_SEND_TIMEOUT': 10,
    # 'KAFKA_MAX_SEND_RETRIES': 0,
    # 'MIN_MESSAGE_LAG_MS': 0,
    # 'DEFAULT_FORMAT': 'json',
}
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
        },
    },
}
# Internationalization
# https://docs.djangoproject.com/en/dev/topics/i18n/
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/
STATIC_ROOT =  os.path.join(BASE_DIR, "static_collected")
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
    os.path.join(BASE_DIR, "build/static")
]


FIXTURE_DIRS =  [ "fixtures"]


TRANSFORMATION_DTYPE = None
TRANSFORMATION_COMPRESSION = None
PANDAS_COMPRESSION = None
REPRESENTATION_DTYPE = None
REPRESENTATION_COMPRESSION = None