import os
from pathlib import Path
from datetime import timedelta
import environ #  Gestión de variables de entorno

# Inicializar gestor de variables de entorno
env = environ.Env(
    DEBUG=(bool, False)
)

BASE_DIR = Path(__file__).resolve().parent.parent

#  Leer archivo .env desde la raíz del proyecto
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

#  SECRET_KEY protegida en variable de entorno
SECRET_KEY = env('SECRET_KEY')

DEBUG = env('DEBUG')

ALLOWED_HOSTS = []

# [cite: 14, 16] Definición de aplicaciones
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # [cite: 14] Frameworks requeridos para la API
    'rest_framework',
    'rest_framework_simplejwt',
    # [cite: 16] Aplicación del núcleo del sistema
    'core',
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

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

#  Configuración de Base de Datos MySQL (XAMPP)
# Se mapean las variables individuales para evitar errores de DATABASE_URL
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': env('DB_NAME'),
        'USER': env('DB_USER'),
        'PASSWORD': env('DB_PASSWORD', default=''),
        'HOST': env('DB_HOST'),
        'PORT': env('DB_PORT'),
    }
}

# Validadores de seguridad para contraseñas
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Configuración regional (Chile)
LANGUAGE_CODE = 'es-cl'
TIME_ZONE = 'America/Santiago'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# [cite: 10, 48, 85, 114] Configuración de Django Rest Framework
REST_FRAMEWORK = {
    #  Sistema de autenticación JWT
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    # [cite: 48, 123] Restricción global: Solo usuarios autenticados
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    # [cite: 85] Paginación de resultados (Requerimiento avanzado)
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
}

# [cite: 46, 101, 104] Configuración de Simple JWT
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'AUTH_HEADER_TYPES': ('Bearer',), # Formato: Bearer <token>
}

# PARCHE DE COMPATIBILIDAD TOTAL PARA XAMPP (MariaDB 10.4)
from django.db.backends.base.base import BaseDatabaseWrapper
from django.db.backends.mysql.features import DatabaseFeatures

# 1. Saltamos la verificación de versión mínima (requerimiento 3.1.1)
BaseDatabaseWrapper.check_database_version_supported = lambda self: None

# 2. Desactivamos 'can_return_rows_from_bulk_insert' para evitar el error 'RETURNING'
DatabaseFeatures.can_return_rows_from_bulk_insert = property(lambda self: False)
DatabaseFeatures.can_return_columns_from_insert = property(lambda self: False)