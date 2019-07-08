# -*- coding: utf-8 -*-
import os
import datetime
import logging

import ldap
from django_auth_ldap.config import LDAPSearch, GroupOfNamesType


def app_state(env_mode):
    """
    Using OS environment 'mode' arg to detect application state (dev/prod)
    """
    result = {
        'debug': True,
        'allowed_hosts': ['127.0.0.1', '*']
    }
    if env_mode is 'prod':
        result['debug'] = False
        result['allowed_hosts'] = ['*']

    return result


def get_secret_key():
    """Docker Build fails without secret key"""
    env_key = os.environ.get('DJANGO_SECRET_KEY')
    return env_key if env_key else '$%e*q@$aav2r92bwuhj867v_9juy1)90c+cdxux6g_68k45rm+'


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

SECRET_KEY = get_secret_key()

DEBUG = app_state(os.environ.get('MODE'))['debug']

ALLOWED_HOSTS = app_state(os.environ.get('MODE'))['allowed_hosts']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'main.apps.MainConfig',
    'graphene_django',
    'django_filters',
    'graphql_jwt.refresh_token.apps.RefreshTokenConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

AUTHENTICATION_BACKENDS = [
    'django_auth_ldap.backend.LDAPBackend',
    'graphql_jwt.backends.JSONWebTokenBackend',
    'django.contrib.auth.backends.ModelBackend',
]

ROOT_URLCONF = 'backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
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

WSGI_APPLICATION = 'backend.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get('POSTGRES_DB'),
        'USER': os.environ.get('POSTGRES_USER'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD'),
        'HOST': 'django_nginx_secure_link_db',  # <-- IMPORTANT: same name as docker-compose service!
        'PORT': '5432',
    }
}

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

LANGUAGE_CODE = 'ru-ru'

TIME_ZONE = 'Asia/Yekaterinburg'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(os.path.dirname(BASE_DIR), 'static')

MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(os.path.dirname(BASE_DIR), 'media')

GRAPHENE = {
    'SCHEMA': 'main.schema.schema',  # Where your Graphene schema lives
    'MIDDLEWARE': [
        'graphql_jwt.middleware.JSONWebTokenMiddleware',
    ],
}
GRAPHQL_JWT = {
    'JWT_VERIFY_EXPIRATION': True,
    'JWT_LONG_RUNNING_REFRESH_TOKEN': True,
    'JWT_EXPIRATION_DELTA': datetime.timedelta(hours=12),
    'JWT_REFRESH_EXPIRATION_DELTA': datetime.timedelta(days=7),
    'JWT_ALLOW_ARGUMENT': True,
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'main_formatter',
        },
    },
    'loggers': {
        '': {  # 'catch all' loggers by referencing it with the empty string
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    },
    'formatters': {
        'main_formatter': {
            'format': '%(levelname)s:%(name)s: %(message)s '
                      '(%(asctime)s; %(filename)s:%(lineno)d)',
            'datefmt': "%Y-%m-%d %H:%M:%S",
        },
    },
}

EXTENSIONS = {
    'image': ['.jpg', '.jpeg', '.gif', '.png', '.tif', '.tiff', '.gif'],
    'document': ['.pdf', '.doc', '.rtf', '.txt', '.xls', '.csv', '.docx'],
    'video': ['.mov', '.mp4', '.m4v', '.webm', '.wmv', '.mpeg', '.mpg', '.avi', '.rm', '.mkv'],
    'audio': ['.mp3', '.wav', '.aiff', '.midi', '.m4p'],
    'archive': ['.tar', '.rar', '.zip', '.tgz', '']
}

# Время существования линка в секундах по умолчанию
# Может быть изменено через веб-интерфейс в модели User
DEFAULT_PUBLIC_URL_TTL = 86400 * 5  # 5 дней

MIN_PUBLIC_URL_TTL = 86400 * 1  # 1 день

MAX_PUBLIC_URL_TTL = 86400 * 30  # 30 дней

# Пароль для хеша - такой же в nginx.conf
NGINX_SECRET = os.environ.get('NGINX_SECRET')

# Путь до папки которую будет раздавать nginx
SECURE_LINK_PATH = os.path.join(os.path.dirname(BASE_DIR), 'secure')

# LDAP CONFIG

# Baseline configuration.
logger = logging.getLogger('django_auth_ldap')
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)

AUTH_LDAP_SERVER_URI = os.environ.get('AUTH_LDAP_SERVER_URI')
AUTH_LDAP_BIND_DN = os.environ.get('AUTH_LDAP_BIND_DN')
AUTH_LDAP_BIND_PASSWORD = os.environ.get('AUTH_LDAP_BIND_PASSWORD')
AUTH_LDAP_USER_SEARCH = LDAPSearch(os.environ.get('AUTH_LDAP_USER_SEARCH'), ldap.SCOPE_SUBTREE, "(cn=%(user)s)")

# Set up the basic group parameters.
AUTH_LDAP_GROUP_SEARCH = LDAPSearch(
    os.environ.get('AUTH_LDAP_GROUP_SEARCH'),
    ldap.SCOPE_SUBTREE,
    '(objectClass=groupOfNames)',
)
AUTH_LDAP_GROUP_TYPE = GroupOfNamesType(name_attr='cn')

# Simple group restrictions
AUTH_LDAP_REQUIRE_GROUP = os.environ.get('AUTH_LDAP_REQUIRE_GROUP')
# AUTH_LDAP_DENY_GROUP = 'cn=Access_Restrict,ou=groups,dc=example,dc=com'

# Populate the Django user from the LDAP directory.
AUTH_LDAP_USER_ATTR_MAP = {
    'first_name': 'givenName',
    'last_name': 'sn',
    'email': 'mail',
}

AUTH_LDAP_USER_FLAGS_BY_GROUP = {
    'is_active': os.environ.get('AUTH_LDAP_USER_FLAGS_BY_GROUP_IS_ACTIVE'),
    #    'is_staff': 'cn=staff,ou=django,ou=groups,dc=example,dc=com',
    #    'is_superuser': 'cn=superuser,ou=django,ou=groups,dc=example,dc=com',
}

# This is the default, but I like to be explicit.
AUTH_LDAP_ALWAYS_UPDATE_USER = True

# Use LDAP group membership to calculate group permissions.
AUTH_LDAP_FIND_GROUP_PERMS = False

# Cache distinguised names and group memberships for an hour to minimize
# LDAP traffic.
AUTH_LDAP_CACHE_TIMEOUT = int(os.environ.get('AUTH_LDAP_CACHE_TIMEOUT')) if os.environ.get(
    'AUTH_LDAP_CACHE_TIMEOUT') else 3600

if DEBUG:
    logger = logging.getLogger('django_auth_ldap')
    logger.addHandler(logging.StreamHandler())
    logger.setLevel(logging.DEBUG)
