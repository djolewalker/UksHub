from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-g+2e)qgtmq!plc53k9v=k5!-@opb^o5*s5)0tg=+=%*m#a7)2j'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

ADMIN_ENABLED = True

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    # 3rd party
    'compressor', # SCSS
    'easy_thumbnails', # Thumbnail support
    'django_cleanup.apps.CleanupConfig', # Remove unreferenced files
    'crispy_forms', # Format django forms in bootstrap way
    'polymorphic', # ORM polymorphism support
    # Created apps
    'UksHub.apps.hub.apps.HubConfig',
    'UksHub.apps.gitcore.apps.GitCoreConfig',
    'UksHub.apps.events.apps.EventsConfig',
    'UksHub.apps.hubauth.apps.HubAuthConfig',
    'UksHub.apps.backoffice.apps.BackofficeConfig',
    'UksHub.apps.analytics.apps.AnalyticsConfig'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'UksHub.apps.analytics.middleware.AnalyticsMiddleware'
]

ROOT_URLCONF = 'UksHub.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'UksHub' / 'templates'],
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

WSGI_APPLICATION = 'UksHub.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'uks_hub',
        'USER': 'user',
        'PASSWORD': 'user',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}

AUTH_USER_MODEL = 'hubauth.User'

# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = 'static'

MEDIA_ROOT = BASE_DIR / 'user-files'
MEDIA_URL = 'user-files/'

STATICFILES_DIRS = [BASE_DIR / 'UksHub' / 'static']

CRISPY_TEMPLATE_PACK = 'bootstrap4'

# SCSS dependency
STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder'
]
COMPRESS_PRECOMPILERS = (
    ('text/x-scss', 'django_libsass.SassCompiler'),
)

COMPRESS_OFFLINE = True
LIBSASS_OUTPUT_STYLE = 'compressed'
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'


# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_URL = "/login"

GIT_REPOSITORIES = BASE_DIR / 'git-repos'

GIT_ADMIN_SUPERUSER = 'random.user.admin'
GIT_ADMIN = BASE_DIR / 'git-admin-dev'
GIT_ADMIN_CONF_REPO = GIT_ADMIN / 'conf' 
GIT_ADMIN_CONF = GIT_ADMIN_CONF_REPO / 'gitolite.conf'
GIT_ADMIN_KEYS = GIT_ADMIN / 'keydir'
GIT_ADMIN_REMOTE = "D:\git-admin-dev"

THUMBNAIL_ALIASES = {
    '': {
        'avatar-xs': {'size': (38, 38), 'crop': True},
        'avatar-s': {'size': (50, 50), 'crop': True},
        'avatar-m': {'size': (100, 100), 'crop': True},
        'avatar-l': {'size': (150, 150), 'crop': True},
    },
}