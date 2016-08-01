import os
import dj_database_url
import django_jinja.builtins


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

try:
    from honcho.environ import parse as parse_env
    with open(os.path.join(BASE_DIR, '.env')) as f:
        for name, value in parse_env(f.read()).items():
            os.environ.setdefault(name, value)
except IOError:
    pass


SECRET_KEY = os.environ.get('SECRET_KEY', 'please_change_me')

DEBUG = bool(int(os.environ.get('DEBUG', 0)))

SILENCED_SYSTEM_CHECKS = ['fields.W342']

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'localhost').split(',')


INSTALLED_APPS = [
    # django apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # 3rd party
    'django_jinja',
    'webpack_loader',

    # project apps
    'nav',
    'pages',
    'news',
]

if DEBUG:
    # Debug Toolbar
    import debug_toolbar

    if debug_toolbar.VERSION == '1.5':
        # Fix error "'Template' object has no attribute 'engine'"
        # See: http://stackoverflow.com/q/38569760
        #      https://github.com/niwinz/django-jinja/issues/151
        #      https://github.com/jazzband/django-debug-toolbar/issues/790
        def _patch_debug_toolbar_1_5():
            from debug_toolbar.panels.templates import TemplatesPanel
            orig_store_template_info = TemplatesPanel._store_template_info

            def new_store_template_info(self, *args, **kwargs):
                orig_store_template_info(self, *args, **kwargs)
                template = self.templates[0].get('template')
                if template and not hasattr(template, 'engine'):
                    template.engine = template.backend

            TemplatesPanel._store_template_info = new_store_template_info

        _patch_debug_toolbar_1_5()

    INTERNAL_IPS = os.environ.get('INTERNAL_IPS', '127.0.0.1').split(',')
    INSTALLED_APPS += ['debug_toolbar']

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django_jinja.backend.Jinja2',
        'APP_DIRS': True,
        'OPTIONS': {
            # pyjade preprocesses only .jade files (this is hardcoded),
            # so we must match using the same extension.
            'match_extension': '.jade',
            'globals': {
                'site_menu': 'nav.urls.site_menu',
                'tagadelic_terms': 'nav.urls.tagadelic_terms',
            },
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'extensions': django_jinja.builtins.DEFAULT_EXTENSIONS + [
                'pyjade.ext.jinja.PyJadeExtension',
                'webpack_loader.contrib.jinja2ext.WebpackExtension',
            ],
        }
    },
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

WSGI_APPLICATION = 'project.wsgi.application'


DATABASES = {'default': dj_database_url.config(conn_max_age=600)}


AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Europe/Moscow'
USE_I18N = True
USE_L10N = True
USE_TZ = True


STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'assets')
]

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

if DEBUG:
    WEBPACK_LOADER = {
        'DEFAULT': {
            'BUNDLE_DIR_NAME': 'debug/',
            'STATS_FILE': os.path.join(BASE_DIR, 'webpack/stats-debug.json')
        }
    }
else:
    WEBPACK_LOADER = {
        'DEFAULT': {
            'BUNDLE_DIR_NAME': 'prod/',
            'STATS_FILE': os.path.join(BASE_DIR, 'webpack/stats-prod.json')
        }
    }
