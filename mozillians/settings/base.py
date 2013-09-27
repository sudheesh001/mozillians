# -*- coding: utf-8 -*-

# Django settings for the mozillians project.
import logging
import os.path
import sys

from funfactory.manage import path
from funfactory.settings_base import *
from urlparse import urljoin

from mozillians.users.helpers import calculate_username
from django.utils.functional import lazy

## Log settings
SYSLOG_TAG = "http_app_mozillians"
LOGGING = {
    'loggers': {
        'landing': {'level': logging.INFO},
        'phonebook': {'level': logging.INFO},
    },
}

## Database settings
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': '',
        'PORT': '',
        'OPTIONS': {
            'init_command': 'SET storage_engine=InnoDB',
            'charset': 'utf8',
            'use_unicode': True,
        },
        'TEST_CHARSET': 'utf8',
        'TEST_COLLATION': 'utf8_general_ci',
    },
}

## L10n
LOCALE_PATHS = [path('locale')]

# Tells the extract script what files to parse for strings and what functions to use.
DOMAIN_METHODS = {
    'messages': [
        ('mozillians/**.py',
            'tower.management.commands.extract.extract_tower_python'),
        ('mozillians/**/templates/**.html',
            'tower.management.commands.extract.extract_tower_template'),
        ('templates/**.html',
            'tower.management.commands.extract.extract_tower_template'),
    ],
}

# Accepted locales
PROD_LANGUAGES = ('ca', 'cs', 'de', 'en-US', 'es', 'hu', 'fr', 'it', 'ko',
                  'nl', 'pl', 'pt-BR', 'ru', 'sk', 'sl', 'sq', 'sv', 'zh-TW',
                  'zh-CN', 'lt', 'ja')

# List of RTL locales known to this project. Subset of LANGUAGES.
RTL_LANGUAGES = ()  # ('ar', 'fa', 'fa-IR', 'he')

# For absoluate urls
PROTOCOL = "https://"
PORT = 443

## Templates.

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'jingo.Loader',
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = get_template_context_processors(
	append=['django_browserid.context_processors.browserid',
                'mozillians.common.context_processors.current_year'])


JINGO_EXCLUDE_APPS = [
    'bootstrapform',
    'admin',
    'autocomplete_light',
    'browserid'
]

MINIFY_BUNDLES = {
    'css': {
        'common': (
            'mozillians/css/main.less',
            'mozillians/css/jquery-ui-1.8.16.custom.css',
            'mozillians/js/libs/tag-it/css/jquery.tagit.css',
        ),
        'api': (
            'mozillians/css/prettify.css',
        ),
        'test': (
            'mozillians/css/qunit.css',
        ),
    },
    'js': {
        'common': (
            'mozillians/js/libs/jquery-1.7.2.js',
            'mozillians/js/libs/jquery-ui-1.8.7.custom.min.js',
            'mozillians/js/libs/jquery.placeholder.min.js',
            'mozillians/js/main.js',
            'mozillians/js/libs/validation/validation.js',
        ),
        'homepage': (
            'mozillians/js/libs/modernizr.custom.26887.js',
            'mozillians/js/libs/jquery.transit.js',
            'mozillians/js/libs/jquery.gridrotator.js',
            'mozillians/js/libs/jquery.smooth-scroll.min.js',
            'mozillians/js/homepage.js'
        ),
        'api': (
            'mozillians/js/libs/prettify.js',
            'mozillians/js/api.js'
        ),
        'edit_profile': (
            'mozillians/js/libs/tag-it/js/tag-it.js',
            'mozillians/js/profile_edit.js',
            'mozillians/js/groups.js'
        ),
        'register': (
            'mozillians/js/libs/tag-it/js/tag-it.js',
            'mozillians/js/register.js',
        ),
        'backbone': (
            'mozillians/js/libs/underscore.js',
            'mozillians/js/libs/backbone.js',
            'mozillians/js/libs/backbone.localStorage.js',
            'mozillians/js/profiles.js',
        ),
        'test': (
            'mozillians/js/libs/qunit.js',
            'mozillians/js/tests/test.js',
        ),
        'profile_view': (
            'mozillians/js/libs/tag-it/js/tag-it.js',
            'mozillians/js/profile_view.js',
        ),
        'google_analytics': (
            'mozillians/js/google-analytics.js',
        ),
        'search': (
            'mozillians/js/search.js',
            'mozillians/js/pagination.js',
        ),
        'groups': (
            'mozillians/js/pagination.js',
        ),
        'logout_view': (
            'mozillians/js/logout_view.js',
        ),
    }
}

LESS_PREPROCESS = False
LESS_BIN = 'lessc'

MIDDLEWARE_CLASSES = get_middleware(append=[
    'commonware.response.middleware.StrictTransportMiddleware',

    'django_statsd.middleware.GraphiteMiddleware',
    'django_statsd.middleware.GraphiteRequestTimingMiddleware',
    'django_statsd.middleware.TastyPieRequestTimingMiddleware',

    'mozillians.common.middleware.StrongholdMiddleware',
    'mozillians.phonebook.middleware.RegisterMiddleware',
    'mozillians.phonebook.middleware.UsernameRedirectionMiddleware',
    'mozillians.groups.middleware.OldGroupRedirectionMiddleware'])

# StrictTransport
STS_SUBDOMAINS = True

# Not all URLs need locale.
SUPPORTED_NONLOCALES = list(SUPPORTED_NONLOCALES) + [
    'csp',
    'api',
    'browserid',
    'admin',
    'autocomplete',
]

AUTHENTICATION_BACKENDS = ('django_browserid.auth.BrowserIDBackend',)

# BrowserID creates a user if one doesn't exist.
BROWSERID_CREATE_USER = True
BROWSERID_USERNAME_ALGO = calculate_username

# On Login, we redirect through register.
LOGIN_URL = '/'
LOGIN_REDIRECT_URL = '/login/'
INSTALLED_APPS = (
    # Local apps
    'funfactory',
    'compressor',

    'tower',
    'cronjobs',

    # Django contrib apps
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.staticfiles',

    'commonware.response.cookies',
    'djcelery',
    'django_nose',
    'session_csrf',

    'product_details',

    'jingo_minify',

    'mozillians',
    'mozillians.users',
    'mozillians.phonebook',
    'mozillians.groups',
    'mozillians.common',
    'mozillians.api',
    'mozillians.mozspaces',
    'mozillians.funfacts',
    'mozillians.announcements',

    'sorl.thumbnail',
    'autocomplete_light',

    'django.contrib.admin',
    'django_browserid',
    'bootstrapform',
    # DB migrations
    'south',
)

## Auth
PWD_ALGORITHM = 'bcrypt'
HMAC_KEYS = {
    '2011-01-01': 'cheesecake',
}

SESSION_COOKIE_HTTPONLY = True
SESSION_ENGINE = 'django.contrib.sessions.backends.signed_cookies'
SESSION_COOKIE_NAME='mozillians_sessionid'
ANON_ALWAYS = True

# Email
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
FROM_NOREPLY = u'Mozillians <no-reply@mozillians.org>'

# Auth
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    }
}

AUTH_PROFILE_MODULE = 'users.UserProfile'

MAX_PHOTO_UPLOAD_SIZE = 8 * (1024 ** 2)

AUTO_VOUCH_DOMAINS = ('mozilla.com', 'mozilla.org', 'mozillafoundation.org')
SOUTH_TESTS_MIGRATE = False

# Django-CSP
CSP_DEFAULT_SRC = ("'self'",)
CSP_FONT_SRC = ("'self'",
                'https://*.mozilla.org',
                'https://*.mozilla.net')
CSP_FRAME_SRC = ("'self'",
                 'https://login.persona.org',)
CSP_IMG_SRC = ("'self'",
               'data:',
               'https://*.mozilla.net',
               'https://*.google-analytics.com',
               'https://*.gravatar.com',
               'https://i1.wp.com')
CSP_SCRIPT_SRC = ("'self'",
                  'https://*.mozilla.org',
                  'https://*.mozilla.net',
                  'https://*.google-analytics.com',
                  'https://login.persona.org',)
CSP_STYLE_SRC = ("'self'",
                 "'unsafe-inline'",
                 'https://*.mozilla.org',
                 'https://*.mozilla.net',)

# Elasticutils settings
ES_DISABLED = True
ES_HOSTS = ['127.0.0.1:9200']
ES_INDEXES = {'default': 'mozillians',
              'public': 'mozillians-public'}
ES_INDEXING_TIMEOUT = 10

# Sorl settings
THUMBNAIL_DUMMY = True
THUMBNAIL_PREFIX = 'uploads/sorl-cache/'

# Statsd Graphite
STATSD_CLIENT = 'django_statsd.clients.normal'

# Basket
# If we're running tests, don't hit the real basket server.
if 'test' in sys.argv:
    BASKET_URL = 'http://127.0.0.1'
else:
    BASKET_URL = 'http://basket.mozilla.com'
BASKET_NEWSLETTER = 'mozilla-phone'

USER_AVATAR_DIR = 'uploads/userprofile'
MOZSPACE_PHOTO_DIR = 'uploads/mozspaces'
ANNOUNCEMENTS_PHOTO_DIR = 'uploads/announcements'

# Google Analytics
GA_ACCOUNT_CODE = 'UA-35433268-19'

# Set ALLOWED_HOSTS based on SITE_URL.
def _allowed_hosts():
    from django.conf import settings
    from urlparse import urlparse

    host = urlparse(settings.SITE_URL).netloc # Remove protocol and path
    host = host.rsplit(':', 1)[0]  # Remove port
    return [host]
ALLOWED_HOSTS = lazy(_allowed_hosts, list)()

STRONGHOLD_EXCEPTIONS = ['^%s' % MEDIA_URL,
                         '^/csp/',
                         '^/admin/',
                         '^/browserid/',
                         '^/jsi18n',
                         '^/api/']

# Set default avatar for user profiles
DEFAULT_AVATAR= 'img/default_avatar.png'
DEFAULT_AVATAR_URL = urljoin(MEDIA_URL, DEFAULT_AVATAR)
DEFAULT_AVATAR_PATH = os.path.join(MEDIA_ROOT, DEFAULT_AVATAR)

CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler'
MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'

SECRET_KEY = ''

def _request_args():
    from django.conf import settings
    from tower import ugettext_lazy as _lazy

    args = {
        'siteName': _lazy('Mozillians'),
    }

    if settings.SITE_URL.startswith('https'):
        args['siteLogo'] = urljoin(STATIC_URL, "mozillians/img/apple-touch-icon-144.png")

    return args
BROWSERID_REQUEST_ARGS = lazy(_request_args, dict)()
BROWSERID_VERIFY_CLASS = 'mozillians.phonebook.views.BrowserIDVerify'

# Pagination: Items per page.
ITEMS_PER_PAGE = 21
