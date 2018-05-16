import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):

    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
    'sqlite:///' + os.path.join(basedir,'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    MAIL_SERVER = os.environ.get('MAIL_SERVER') or 'smtp.263.net'
    MAIL_PORT = os.environ.get('MAIL_PORT') or 25
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    FAKE_MAIL_FROM = os.environ.get('FAKE_MAIL_FROM') or 'bravocomtech.com'
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')  or 'wenyongg@bravocomtech.com'
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or 'joyce@2017'
    ADMINS = ['wenyongg@bravocomtech.com']

    POSTS_PER_PAGE = 3

    LANGUAGES = ['en', 'zh_Hans_CN']
