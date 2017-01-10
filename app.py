import sys
import os

from django.conf import settings
from django.conf.urls import url
from django.core.management import execute_from_command_line
from django.core.wsgi import get_wsgi_application
from django.shortcuts import render

BASE_DIR = os.path.dirname(os.path.abspath(__name__))

settings.configure(
    DEBUG=True,
    ALLOWED_HOSTS=['*'],
    SECRET_KEY='%vdbix7n2satn*a^510q9^(i5$o@ib53p5b0egnwb!-b7**3gx',
    ROOT_URLCONF=sys.modules[__name__],
    SITE_PAGES_DIRECTORY=os.path.join(BASE_DIR, 'pages'),
    LOGGING={
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'verbose': {
                'format': '[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s',
                'datefmt': '%d/%b/%Y %H:%M:%S'
            }
        },
        'handlers': {
            'deploy': {
                'level': 'DEBUG',
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': BASE_DIR + '/deploy.log',
                'maxBytes': 1024 * 1024 * 5,  # 5MB
                'backupCount': 5,
                'formatter': 'verbose'
            },
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
                'formatter': 'verbose'
            }
        },
        'loggers': {
            __name__: {
                'handlers': ['deploy', 'console'],
                'level': 'DEBUG',
                'propagate': True
            },
        }
    },
    TEMPLATES=[
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [
                os.path.join(BASE_DIR, "templates"),
                os.path.join(BASE_DIR, "pages"),
            ],
        },
    ]
)


urlpatterns = [
    url(r'^$', (lambda r:
                render(r,
                       'index.html',
                       context={
                           'pages': list(
                               filter(lambda x: x[-4:] == 'html',
                                      [p for p in os.listdir(settings.SITE_PAGES_DIRECTORY)]))}))),
    url(r'^(?P<page>\S+)$', (lambda r, page: render(r, page))),
]

if __name__ == '__main__':
    execute_from_command_line(sys.argv)
else:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", __name__)
    application = get_wsgi_application()
