import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir,'.env'))


class Config(object):

    SECRET_KEY = os.environ.get('SECRET_KEY')
    print('SECRET_KEY:',SECRET_KEY)
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
    'sqlite:///' + os.path.join(basedir,'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = os.environ.get('MAIL_PORT')
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    FAKE_MAIL_FROM = os.environ.get('FAKE_MAIL_FROM') or 'bravocomtech.com'
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')  or 'wenyongg@bravocomtech.com'
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')     
    ADMINS = ['wenyongg@bravocomtech.com']

    POSTS_PER_PAGE = 3

    LANGUAGES = ['zh_CN', 'en']

    YOUDAO_TRANSLATOR_KEY = os.environ.get('YOUDAO_TRANSLATOR_KEY')
    print('YOUDAO_TRANSLATOR_KEY:',YOUDAO_TRANSLATOR_KEY)
    YOUDAO_SECRET_KEY = os.environ.get('YOUDAO_SECRET_KEY')
    print('YOUDAO_SECRET_KEY',YOUDAO_SECRET_KEY)
