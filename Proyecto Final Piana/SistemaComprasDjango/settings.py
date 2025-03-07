"""
Django settings for SistemaComprasDjango project.

Generated by 'django-admin startproject' using Django 5.1.4.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path
import os  # Importar os para manejar rutas y variables de entorno

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-75@_a=vtq1dmo)wejtq=#gp(0wq)*otcco7xatq3-qd8+=*jdy'  # Cambiar en producción

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True  # Cambiar a False en producción

# Lista de hosts permitidos (en producción, agregar los dominios válidos)
ALLOWED_HOSTS = ['*']  # En desarrollo, permite cualquier host. En producción, especificar dominios.

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'compras',  # Aplicación personalizada para compras
    'rest_framework',  # Django REST Framework
    'usuarios',  # Aplicación personalizada para usuarios
    'productos',  # Aplicación personalizada para productos
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'SistemaComprasDjango.urls'  # Archivo principal de URLs

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'Templates'],  # Directorio de plantillas
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

WSGI_APPLICATION = 'SistemaComprasDjango.wsgi.application'  # Configuración WSGI

# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',  # Motor de base de datos (SQLite por defecto)
        'NAME': BASE_DIR / 'db.sqlite3',  # Ruta de la base de datos SQLite
    }
}

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators
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
# https://docs.djangoproject.com/en/5.1/topics/i18n/
LANGUAGE_CODE = 'es-es'  # Cambiar a español
TIME_ZONE = 'America/Argentina/Buenos_Aires'  # Cambiar a tu zona horaria
USE_I18N = True  # Habilitar internacionalización
USE_L10N = True  # Habilitar localización
USE_TZ = True  # Habilitar zonas horarias

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/
STATIC_URL = '/static/'  # URL para archivos estáticos
STATICFILES_DIRS = [BASE_DIR / 'static']  # Directorio de archivos estáticos

# Media files (uploaded images and other user-generated content)
MEDIA_URL = '/media/'  # URL para archivos multimedia
MEDIA_ROOT = BASE_DIR / 'media'  # Directorio de archivos multimedia

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'  # Tipo de campo predeterminado para claves primarias

# URL de inicio de sesión
LOGIN_URL = 'iniciar_sesion'  # Redirige a esta URL si el usuario no está autenticado

# Configuración para producción (opcional)
if not DEBUG:
    # Configuración de seguridad adicional
    SECURE_HSTS_SECONDS = 31536000  # Habilitar HSTS (HTTP Strict Transport Security)
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_SSL_REDIRECT = True  # Redirigir HTTP a HTTPS
    SESSION_COOKIE_SECURE = True  # Cookies de sesión solo en HTTPS
    CSRF_COOKIE_SECURE = True  # Cookies CSRF solo en HTTPS