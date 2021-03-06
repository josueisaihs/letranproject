"""
Django settings for Bartolo project.

Generated by 'django-admin startproject' using Django 3.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '!^jkfhybvxwkbsq$qbj)fxx^!gqqnjf(3g*)*9#(brn5f)3+%e'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["localhost", "bartolo.org",]

INTERNAL_IPS = [
    '127.0.0.1',
]


# Application definition

INSTALLED_APPS = [
    # 'jet.dashboard',
    'jet',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',   
    'django.contrib.sites',
    'django.contrib.sitemaps',
    'django.contrib.humanize',
    'captcha',
    'Docencia',
    'SapereAude',
    'Pagary',
    'Blog',
    'LetranPay',
    'easy_thumbnails',
    'debug_toolbar',
    'background_task',
    'django_ckeditor_5',
    'rest_framework',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

ROOT_URLCONF = 'Bartolo.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'Bartolo.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'es'

# TIME_ZONE = 'UTC'
TIME_ZONE = 'America/Havana'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)

STATIC_URL = '/static/'
# STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/login/'

# gmail_send/settings.py
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'smtp.gmail.com' # 172.16.0.15
# EMAIL_PORT = 587 # 25
# EMAIL_HOST_USER = 'centrofbc@gmail.com' # noreply@bartolo.org
# EMAIL_HOST_PASSWORD = 'wwdkyebpkxwovjkp' # N0r3ply
EMAIL_HOST = '172.16.0.15'
EMAIL_PORT = 25
EMAIL_HOST_USER = 'noreply@bartolo.org'
EMAIL_HOST_PASSWORD = 'N0r3ply'
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

GOOGLE_RECAPTCHA_SECRET_KEY = '6LfFq7cZAAAAALssBIXhs6hTjasdyzOKj4B9_OWn'
GOOGLE_RECAPTCHA_WEB_KEY = '6LfFq7cZAAAAAHiXjtwSz81PheHSXB9WzXauWOh0'

RECAPTCHA_PRIVATE_KEY = GOOGLE_RECAPTCHA_SECRET_KEY
RECAPTCHA_PUBLIC_KEY = GOOGLE_RECAPTCHA_WEB_KEY

WEBMASTER = EMAIL_HOST_USER

# Mensajes Constantes
MESSAGES_INFO = 50

# JET ADMIN
JET_DEFAULT_THEME = 'light-gray'
JET_SIDE_MENU_COMPACT = False
JET_INDEX_DASHBOARD = 'dashboard.CustomIndexDashboard'
JET_APP_INDEX_DASHBOARD = 'jet.dashboard.dashboard.DefaultAppIndexDashboard'
JET_THEMES = [
    {
        'theme': 'default', # theme folder name
        'color': '#47bac1', # color of the theme's button in user menu
        'title': 'Default' # theme title
    },
    {
        'theme': 'green',
        'color': '#44b78b',
        'title': 'Green'
    },
    {
        'theme': 'light-green',
        'color': '#2faa60',
        'title': 'Light Green'
    },
    {
        'theme': 'light-violet',
        'color': '#a464c4',
        'title': 'Light Violet'
    },
    {
        'theme': 'light-blue',
        'color': '#5EADDE',
        'title': 'Light Blue'
    },
    {
        'theme': 'light-gray',
        'color': '#222',
        'title': 'Light Gray'
    }
]


THUMBNAIL_ALIASES = {
    '': {
        'card': {'size': (250, 0),},
        'card-desk': {'size': (500, 0),},

        'img-200': {'size': (0, 200)},
        'img-400': {'size': (0, 400)},
        'img-400x2': {'size': (0, 400)},
        'img-600': {'size': (0, 800)},
        'img-640': {'size': (0, 1000)},
        'img-1100': {'size': (0, 2000)},
    },
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
        'OPTIONS': {
            'server_max_value_length': 1024 * 1024 * 2,
        }
    }
}

SITE_ID = 1

X_FRAME_OPTIONS = 'SAMEORIGIN'

# Ejecucion de las tareas de forma asincornica
# BACKGROUND_TASK_RUN_ASYNC = True
ADMINS =(('josueisaihs','josueisaihs@gmail.com'),)

# LOGGING = { 
#     'version': 1, 
#     'disable_existing_loggers': False, 
#     'handlers': { 
#         'mail_admins': { 
#             'class': 'django.utils.log.AdminEmailHandler', 
#             'level': 'ERROR',
#             'include_html': True, 
#         },
#         'logfile': { 
#             'class': 'logging.handlers.WatchedFileHandler', 
#             'filename': os.path.join(BASE_DIR, "debug.log") 
#         }, 
#     }, 
#     'loggers': { 
#         'django.request': { 
#             'handlers': ['mail_admins'], 
#             'level': 'ERROR', 
#             'propagate': True, 
#         }, 
#         'django': { 
#             'handlers': ['logfile', 'mail_admins'], 
#             'level': 'ERROR', 
#             'propagate': False, 
#         },
#     }, 
# } 

customColorPalette = [
        {
            'color': 'hsl(4, 90%, 58%)',
            'label': 'Red'
        },
        {
            'color': 'hsl(340, 82%, 52%)',
            'label': 'Pink'
        },
        {
            'color': 'hsl(291, 64%, 42%)',
            'label': 'Purple'
        },
        {
            'color': 'hsl(262, 52%, 47%)',
            'label': 'Deep Purple'
        },
        {
            'color': 'hsl(231, 48%, 48%)',
            'label': 'Indigo'
        },
        {
            'color': 'hsl(207, 90%, 54%)',
            'label': 'Blue'
        },
]


CKEDITOR_5_CONFIGS = {
    'default': {
        'toolbar': ['heading', '|', 'bold', 'italic', 'link',
                    'bulletedList', 'numberedList', 'blockQuote', 'imageUpload', ],

    },
    'extends': {
        'blockToolbar': [
            'paragraph', 'heading1', 'heading2', 'heading3', 'heading4', 'heading5', 'heading6',
            '|',
            'bulletedList', 'numberedList',
            '|',
            'blockQuote', 'imageUpload'
        ],
        'toolbar': ['heading', '|', 'outdent', 'indent', 'alignment', '|', 'bold', 'italic', 'link', 'underline', 'strikethrough',
        'code','subscript', 'superscript', 'highlight', '|',
                    'bulletedList', 'numberedList', 'todoList', '|',  'blockQuote', 'imageUpload', '|',
                    'fontSize', 'fontFamily', 'fontColor', 'fontBackgroundColor', 'mediaEmbed', 'removeFormat',
                    'insertTable'],
        'image': {
            'toolbar': ['imageTextAlternative', 'imageTitle', '|', 'imageStyle:alignLeft', 'imageStyle:full',
                        'imageStyle:alignRight', 'imageStyle:alignCenter', 'imageStyle:side'],
            'styles': [
                'full',
                'side',
                'alignLeft',
                'alignRight',
                'alignCenter',
            ]

        },
        'table': {
            'contentToolbar': [ 'tableColumn', 'tableRow', 'mergeTableCells',
            'tableProperties', 'tableCellProperties' ],
            'tableProperties': {
                'borderColors': customColorPalette,
                'backgroundColors': customColorPalette
            },
            'tableCellProperties': {
                'borderColors': customColorPalette,
                'backgroundColors': customColorPalette
            }
        },
        'heading' : {
            'options': [
                { 'model': 'paragraph', 'title': 'Paragraph', 'class': 'ck-heading_paragraph' },
                { 'model': 'heading1', 'view': 'h1', 'title': 'Heading 1', 'class': 'ck-heading_heading1' },
                { 'model': 'heading2', 'view': 'h2', 'title': 'Heading 2', 'class': 'ck-heading_heading2' },
                { 'model': 'heading3', 'view': 'h3', 'title': 'Heading 3', 'class': 'ck-heading_heading3' },
                { 'model': 'heading4', 'view': 'h4', 'title': 'Heading 4', 'class': 'ck-heading_heading4' },
                { 'model': 'heading5', 'view': 'h5', 'title': 'Heading 5', 'class': 'ck-heading_heading5' },
                { 'model': 'heading6', 'view': 'h6', 'title': 'Heading 6', 'class': 'ck-heading_heading6' }
            ]
        },
        'alignment': {
            'options': [ 'left', 'right', 'center', 'justify' ]
        },
    }
}

# AUTHENTICATION_BACKENDS = (
#     'django.contrib.auth.backends.ModelBackend',
#     'social.backends.google.GoogleOAuth2',
#     'social_core.backends.twitter.TwitterOAuth',
# )
# SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '376066366575-fvr53t9j57fqhpbdt4tiplbprjcn62qc.apps.googleusercontent.com'
# SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = 'gKvpCfNxjhxD74FfgHunccA7'
# SOCIAL_AUTH_TWITTER_KEY = 'dNY7kBN9ptV6IUn49lSlkerN0'
# SOCIAL_AUTH_TWITTER_SECRET = 'Gd1SqdmY0tZzD1Rttxusrhm8w5OI2N5pMKHujYCC2dBAT3aRKH'
# SOCIAL_AUTH_URL_NAMESPACE = 'social'
# SOCIAL_AUTH_PIPELINE = (
#     'social_core.pipeline.social_auth.social_details',
#     'social_core.pipeline.social_auth.social_uid',
#     'social_core.pipeline.social_auth.social_user',
#     'social_core.pipeline.user.get_username',
#     'social_core.pipeline.social_auth.associate_by_email',
#     'social_core.pipeline.user.create_user',
#     'social_core.pipeline.social_auth.associate_user',
#     'social_core.pipeline.social_auth.load_extra_data',
#     'social_core.pipeline.user.user_details',
# )

REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ]
}