"""
Django settings for PlantDBBrowser project.

Generated by 'django-admin startproject' using Django 3.2.8.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-pfayp#-hatr@269za$nntnmn3s583z!-(q_b32-6d4cxh0zy9i"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["dreamweb.azurewebsites.net", "localhost"]


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "corsheaders",
    "crispy_forms",
    "rest_framework",
    "app",
    'background_task',
    'django_extensions',
    'import_export',
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "https://red-cliff-0ae92281e.2.azurestaticapps.net",
]
CSRF_TRUSTED_ORIGINS = ["localhost:3000", "127.0.0.1:3000", "red-cliff-0ae92281e.2.azurestaticapps.net"]
CSRF_COOKIE_NAME = "csrftoken"
CORS_ALLOW_CREDENTIALS = True

ROOT_URLCONF = "PlantDBBrowser.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            BASE_DIR / "templates",
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "PlantDBBrowser.wsgi.application"


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases
if os.getenv("DATABASE_NAME") is not None:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": os.getenv("DATABASE_NAME"),
            "USER": os.getenv("DATABASE_USER"),
            "PASSWORD": os.getenv("DATABASE_PASS"),
            "HOST": os.getenv("DATABASE_HOST"),
            "PORT": 5432,
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "static"

MEDIA_ROOT = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

FILE_UPLOAD_HANDLERS = [
    'django.core.files.uploadhandler.TemporaryFileUploadHandler',
]

EMAIL_CONNECTION_STRING = os.getenv("AZURE_COMMUNICATION_SERVICE_CONNECTION_STRING")
EMAIL_SENDER_ADDRESS = os.getenv("AZURE_COMMUNICATION_SERVICE_SENDER_ADDRESS")

# NCBI_BLAST_SUITE_PATH = os.path.join(BASE_DIR, "utils", "ncbi", "macosx")
NCBI_BLAST_SUITE_PATH = os.path.join(BASE_DIR, "utils", "ncbi", "linux")
NCBI_MAKEBLASTDB_PATH = os.path.join(NCBI_BLAST_SUITE_PATH, "makeblastdb")
NCBI_BLAST_NUCL_PATH = os.path.join(NCBI_BLAST_SUITE_PATH, "blastn")
NCBI_BLAST_PROT_PATH = os.path.join(NCBI_BLAST_SUITE_PATH, "blastp")

NUCL_BLASTDB_PATH = os.path.join(MEDIA_ROOT, "blast_nucl_db", "db")
PROT_BLASTDB_PATH = os.path.join(MEDIA_ROOT, "blast_prot_db", "db")

# Temp TODO: for avoiding race conditions during blast analysis
BACKGROUND_TASK_RUN_ASYNC=False
