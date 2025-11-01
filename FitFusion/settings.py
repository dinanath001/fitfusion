from pathlib import Path
import os
from django.utils.translation import gettext_lazy as _
from dotenv import load_dotenv

# Load environment variables (optional, if you make a .env file)
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

LANGUAGES = [
    ('en', _('English')),
    ('hi', _('Hindi')),
    ('fr', _('French')),
]

LOCALE_PATHS = [os.path.join(BASE_DIR, 'locale')]

# ---------------- Security ----------------
SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-local-key')
DEBUG = os.getenv('DEBUG', 'True') == 'True'   # ✅ Default True for local
ALLOWED_HOSTS = ['*']  # ✅ Safe for dev; change to ['.onrender.com'] for deployment

# ---------------- Apps ----------------
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'gym',
]

# ---------------- Middleware ----------------
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # ✅ Works both local & Render
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'gym.middleware.no_cache_middleware.NoCacheMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'FitFusion.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],  # ✅ optional if you have custom HTMLs
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

WSGI_APPLICATION = 'FitFusion.wsgi.application'

# ---------------- Database ----------------
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# ---------------- Password ----------------
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ---------------- Internationalization ----------------
LANGUAGE_CODE = 'en'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# ---------------- Static & Media ----------------
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]  # ✅ for development
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')    # ✅ for Render (after collectstatic)
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# ---------------- Email ----------------
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER', 'dinumishra725@gmail.com')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD', 'gyhp rugk kihb with')
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# ---------------- Default PK ----------------
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
