from collectionproject.stage import *


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'carsalesystem',                      # Or path to database file if using sqlite3.
        'USER': 'pcf_user',                      # Not used with sqlite3.
        'PASSWORD': 'StageAardvark12!',                  # Not used with sqlite3.
        'HOST': 'andromeda.crlswk3z6p4a.us-east-1.rds.amazonaws.com',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
        'OPTIONS': { 'init_command': 'SET SESSION TRANSACTION ISOLATION LEVEL READ COMMITTED'},
    }
}

USE_FILE_SERVER = True

COLLECTION_FILE_DIRECTORY = '/tmp'
COOKIE_DIRECTORY = "/tmp/"
DIRECTOR_DATABASE_FILEPATH = '/projects/director/dirdb.sqlite'

DJANGO_PATH = '/projects/%s/bin/django' % SYSTEM_NAME

CEO_API_URL = 'http://ceo.stage.vkspider.com'

FILE_SERVER_IP = '54.225.199.44'
PRIVATE_KEY = '~/.ssh/PCFSTAGE2.pem'
CLIENT_ID = 'u59xrEYEqeKMgROsKW784szhbgArYh2Adv7iNFdO'
CLIENT_SECRET = 'jT6COBeuPY1KKrkNLESq4SvE6qqPFbwy3e5OwDu6cqlLBY8Dhi9bEK4dYBxRp12QRfhsyREKsbCbQEFLZdjcjHgcL6n1B6Yuo0UT'
