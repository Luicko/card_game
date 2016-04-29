import os

_basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = True

SQLALCHEMY_TRACK_MODIFICATIONS = False

SECRET_KEY = 'just-a-normal-key'

WTF_CSRF_ENABLED = True