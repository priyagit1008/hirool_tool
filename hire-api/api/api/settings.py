from .default_settings import *
from .static_files import *
# import raven

DEBUG = bool(int(os.getenv("HIRE_API_DEBUG_FLAG", 1)))
ENV = os.getenv("HIRE_API_ENV", "DEV")
ALLOWED_HOSTS = [os.getenv("HIRE_API_ALLOWED_HOSTS", "*")]
DATADOG_ENABLED = bool(int(os.getenv("HIRE_API_DATADOG_FLAG", 0)))

if DATADOG_ENABLED:
    DATADOG_APP = ['ddtrace.contrib.django']
    INSTALLED_APPS = INSTALLED_APPS + DATADOG_APP

# Database Config
# DATABASES["default"]["ENGINE"] = os.getenv("django.db.backends.postgresql_psycopg2")
DATABASES["default"]["NAME"] = os.getenv("HIRE_API_DATABASE_NAME", "hirool_db")
DATABASES["default"]["USER"] = os.getenv("HIRE_API_DATABASE_USER", "hirool_user")
DATABASES["default"]["PASSWORD"] = os.getenv("HIRE_API_DATABASE_PASSWORD", "hirool@122019")
DATABASES["default"]["HOST"] = os.getenv("HIRE_API_DATABASE_HOST", "127.0.0.1")
DATABASES["default"]["PORT"] = int(os.getenv("HIRE_API_DATABASE_PORT", 5432))




# Elasticsearch service config
# ELASTIC_SEARCH_CONFIG["HOSTS"] = [host for host in os.getenv("HIRE_API_ELASTICSEARCH_HOSTS").split(",")]
ELASTIC_SEARCH_CONFIG["INDEX"] = os.getenv("HIRE_API_ELASTICSEARCH_INDEX", "HIRE-index")

# Sentry Config
RAVEN_CONFIG["dsn"] = os.getenv("HIRE_API_SENTRY_DSN", "")
RAVEN_CONFIG["release"] = os.getenv("HIRE_API_SENTRY_RELEASE", "")
RAVEN_CONFIG["environment"] = os.getenv("HIRE_API_SENTRY_ENV", "")

# Rabbitmq URL
# CELERY_BROKER_URL = os.getenv("HIRE_API_CELERY_BROKER", "")

# Google Map Config
GOOGLE_MAP_CONFIG["KEY"] = os.getenv("HIRE_API_GOOGLE_MAP_KEY", "")

# Redis Config
REDIS_CONFIG["HOST"] = os.getenv("HIRE_API_REDIS_HOST", "localhost")
REDIS_CONFIG["PORT"] = int(os.getenv("HIRE_API_REDIS_PORT", "6379"))
REDIS_CONFIG["DB"] = int(os.getenv("HIRE_API_REDIS_DB", "0"))
REDIS_CONFIG["PASSWORD"] = os.getenv("HIRE_API_REDIS_PASSWORD", "")

#-----------------------------------------#
# ALLOWED_HOSTS = ['localhost','192.168.1.6','127.0.0.1']

# STATIC_URL = '/static/'
# STATIC_ROOT = os.path.join(BASE_DIR,'static/')
STATIC_ROOT = os.path.join(BASE_DIR, "static/")
#------------------------------------------#


