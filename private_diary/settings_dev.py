from .settings_common import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False # 本番ではセキュリティの観点でFalseにする必要あり

ALLOWED_HOSTS = []

LOGGING = {
    'version': 1,#固定
    'disable_existing_loggers':False,

    #ロガー設定
    'loggers': {
        #Djangoが使用するロガー
        'django': {
            'handlers':['console'],
            'level':'INFO',
        },
        #diaryアプリが使用するロガー
        'diary': {
            'handlers':['console'],
            'level':'DEBUG',
        }
    },
    #ハンドラの設定
    'handlers': {
        'console': {
            'level':'DEBUG',
            'class':'logging.StreamHandler',
            'formatter':'dev'
        },
    },

    #フォーマッタの設定
    'formatters': {
        'dev': {
            'format':'\t'.join([
                '%(asctime)s',
                '[%(levelname)s]',
                '%(pathname)s(Line:%(lineno)d)',
                '%(message)s'
            ])
        },
    }
}

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(db_from_env)