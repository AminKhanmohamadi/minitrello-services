from .common import *

DEBUG=True

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'console': {
            'format': '%(name)-12s %(levelname)-8s %(message)s'
        },
        'file': {
            'format': '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'console'
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'formatter': 'file',
            'filename': '/tmp/debug.log'
        }
    },
    'loggers': {
        '': {
            'level': 'DEBUG',
            'handlers': ['console', 'file']
        }
    }
}


# import sentry_sdk
#
# sentry_sdk.init(
#     dsn="https://3ee050fad5c2db425cf4bf5a4a9f8083@o4508450666053632.ingest.de.sentry.io/4508450672017488",
#     # Set traces_sample_rate to 1.0 to capture 100%
#     # of transactions for tracing.
#     traces_sample_rate=1.0,
#     _experiments={
#         # Set continuous_profiling_auto_start to True
#         # to automatically start the profiler on when
#         # possible.
#         "continuous_profiling_auto_start": True,
#     },
# )


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'trello',
        'USER': 'trello',
        'PASSWORD':'123@456',
        'HOST':'db',
        'PORT': 5432
    }
}