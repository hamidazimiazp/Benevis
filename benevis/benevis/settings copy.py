from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-=x%#do&4_@f35g75q@xm2u4(&(p%tikyc2omy_)%++m!zi(puj'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # local apps
    'core.apps.CoreConfig',
    "accounts.apps.AccountsConfig",
    "twitte.apps.TwitteConfig",
    # third-party apps
    "storages",
    'social_django',
    'sorl.thumbnail',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # third-party middlewares
    "social_django.middleware.SocialAuthExceptionMiddleware",
]

ROOT_URLCONF = 'benevis.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                # third-party context processor 
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
            ],
            'libraries':{
                'basefilter': 'accounts.templatetags.basefilter',
            }
        },
    },
]

WSGI_APPLICATION = 'benevis.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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


LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


STATIC_URL = '/static/'


# local configs

STATICFILES_DIRS = [
    (BASE_DIR / 'static'),
]

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = "accounts.User"
LOGIN_URL = "/accounts/login/"


# recaptcha v2 config
NORECAPTCHA_SITE_KEY = "<site-key>"
RECAPTCHA_SECRET_KEY = "<secret-key>"


# social django oauth2 

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '<google-auth-key>'
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = '<google-auth-secret>'
SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE = [
    'https://www.googleapis.com/auth/userinfo.email',
]

# some config
SOCIAL_AUTH_LOGIN_REDIRECT_URL = 'core:home' # /accounts/profile/
SOCIAL_AUTH_LOGIN_ERROR_URL = 'accounts:login'


AUTHENTICATION_BACKENDS = (
    'social_core.backends.google.GoogleOAuth2',
    'django.contrib.auth.backends.ModelBackend',
)


# SOCIAL_AUTH_STORAGE = 'social_django_mongoengine.models.DjangoStorage'


# arvan cloud storage
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
AWS_ACCESS_KEY_ID = "<key-id>"
AWS_SECRET_ACCESS_KEY = "<secret-access>"
AWS_STORAGE_BUCKET_NAME = "<bucket-name>"
AWS_SERVICE_NAME = "s3"
AWS_S3_ENDPOINT_URL = "<url>"
AWS_S3_FILE_OVERWRITE = False
THUMBNAIL_FORCE_OVERWRITE = True