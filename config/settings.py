"""
Django settings for Wasfa Drug Management.
Works for both local development (SQLite) and Render production (PostgreSQL).
"""

from pathlib import Path
import os
import dj_database_url
from decouple import config, Csv

BASE_DIR = Path(__file__).resolve().parent.parent

# ── Security ──────────────────────────────────────────────────
SECRET_KEY = config('SECRET_KEY', default='django-insecure-dev-key-change-in-production')
DEBUG      = config('DEBUG', default=True, cast=bool)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost,127.0.0.1,.onrender.com', cast=Csv())

# ── Application definition ────────────────────────────────────
INSTALLED_APPS = [
    'jazzmin',                          # must be before django.contrib.admin

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'crispy_forms',
    'crispy_bootstrap5',
    'drug_management',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',    # ← static files in production
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
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
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.template.context_processors.i18n',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# ── Database ──────────────────────────────────────────────────
# Render provides DATABASE_URL; fall back to SQLite for local dev
DATABASE_URL = config('DATABASE_URL', default=None)

if DATABASE_URL:
    DATABASES = {
        'default': dj_database_url.parse(DATABASE_URL, conn_max_age=600)
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME':   BASE_DIR / 'db.sqlite3',
        }
    }

# ── Password validators ───────────────────────────────────────
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ── Internationalization ──────────────────────────────────────
LANGUAGE_CODE = 'en'
TIME_ZONE     = 'UTC'
USE_I18N      = True
USE_TZ        = True

LANGUAGES = [
    ('ar', 'العربية'),
    ('en', 'English'),
]

LOCALE_PATHS = [os.path.join(BASE_DIR, 'locale')]

# ── Static & Media files ──────────────────────────────────────
STATIC_URL  = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
_STATIC_DIR = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = [_STATIC_DIR] if os.path.isdir(_STATIC_DIR) else []

# WhiteNoise compression + caching for production
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL  = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# ── Crispy Forms ──────────────────────────────────────────────
CRISPY_ALLOWED_TEMPLATE_PACKS = 'bootstrap5'
CRISPY_TEMPLATE_PACK          = 'bootstrap5'

# ── Default PK ───────────────────────────────────────────────
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ── Security headers (production) ────────────────────────────
if not DEBUG:
    SECURE_PROXY_SSL_HEADER      = ('HTTP_X_FORWARDED_PROTO', 'https')
    SECURE_SSL_REDIRECT          = True
    SESSION_COOKIE_SECURE        = True
    CSRF_COOKIE_SECURE           = True
    SECURE_BROWSER_XSS_FILTER   = True
    SECURE_CONTENT_TYPE_NOSNIFF = True

# ── Logging ───────────────────────────────────────────────────
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {'console': {'class': 'logging.StreamHandler'}},
    'root': {'handlers': ['console'], 'level': 'INFO'},
}

# ════════════════════════════════════════════════════════════════
# Jazzmin Theme
# ════════════════════════════════════════════════════════════════
JAZZMIN_SETTINGS = {
    "site_title":        "Wasfa Admin",
    "site_header":       "Wasfa Drug Management",
    "site_brand":        "💊 Wasfa",
    "welcome_sign":      "Welcome to Wasfa Drug Management",
    "copyright":         "Wasfa Drug Management System",
    "site_icon":         None,
    "site_logo":         None,
    "topmenu_links": [
        {"name": "Home",      "url": "admin:index", "permissions": ["auth.view_user"]},
        {"name": "View Site", "url": "/",           "new_window": True},
    ],
    "usermenu_links": [
        {"name": "View Site", "url": "/", "new_window": True, "icon": "fas fa-globe"},
    ],
    "show_sidebar":        True,
    "navigation_expanded": True,
    "order_with_respect_to": [
        "drug_management",
        "drug_management.PatientGroup",
        "drug_management.DrugCategory",
        "drug_management.DrugFamily",
        "drug_management.GenericMedication",
        "drug_management.DosageRule",
        "drug_management.RangeBasedDose",
        "drug_management.TradeNameProduct",
        "drug_management.TradeNameComposition",
        "drug_management.DrugInteraction",
        "drug_management.MedicationAlternative",
        "drug_management.Manufacturer",
        "drug_management.AgeWeightEstimate",
        "drug_management.Equation",
        "drug_management.EquationInput",
        "drug_management.SearchHistory",
        "auth",
    ],
    "icons": {
        "auth":                                  "fas fa-users-cog",
        "auth.user":                             "fas fa-user",
        "auth.Group":                            "fas fa-users",
        "drug_management.PatientGroup":          "fas fa-user-injured",
        "drug_management.DrugCategory":          "fas fa-folder-open",
        "drug_management.DrugFamily":            "fas fa-sitemap",
        "drug_management.GenericMedication":     "fas fa-pills",
        "drug_management.DosageRule":            "fas fa-calculator",
        "drug_management.RangeBasedDose":        "fas fa-ruler-combined",
        "drug_management.TradeNameProduct":      "fas fa-box",
        "drug_management.TradeNameComposition":  "fas fa-flask",
        "drug_management.DrugInteraction":       "fas fa-exclamation-triangle",
        "drug_management.MedicationAlternative": "fas fa-exchange-alt",
        "drug_management.Manufacturer":          "fas fa-industry",
        "drug_management.AgeWeightEstimate":     "fas fa-weight",
        "drug_management.Equation":              "fas fa-superscript",
        "drug_management.EquationInput":         "fas fa-keyboard",
        "drug_management.SearchHistory":         "fas fa-history",
    },
    "default_icon_parents":  "fas fa-chevron-circle-right",
    "default_icon_children": "fas fa-circle",
    "search_model": [
        "drug_management.GenericMedication",
        "drug_management.TradeNameProduct",
    ],
    "related_modal_active":  True,
    "use_google_fonts_cdn":  True,
    "show_ui_builder":       False,
    "changeform_format":     "horizontal_tabs",
}

JAZZMIN_UI_TWEAKS = {
    "navbar_small_text":      False,
    "brand_colour":           "navbar-purple",
    "accent":                 "accent-purple",
    "navbar":                 "navbar-dark",
    "no_navbar_border":       True,
    "navbar_fixed":           True,
    "sidebar_fixed":          True,
    "sidebar":                "sidebar-dark-purple",
    "theme":                  "flatly",
    "dark_mode_theme":        "darkly",
    "button_classes": {
        "primary":   "btn-primary",
        "secondary": "btn-secondary",
        "info":      "btn-info",
        "warning":   "btn-warning",
        "danger":    "btn-danger",
        "success":   "btn-success",
    },
}
