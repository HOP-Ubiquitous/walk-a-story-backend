import os

VERSION = '0.5.1'

REST_URL = os.getenv('REST_URL', '0.0.0.0')
REST_PORT = os.getenv('REST_PORT', '8000')

ALLOWED_EXTENSIONS = ['mp4', 'MOV', 'mov']
BUCKET_NAME = os.getenv('BUCKET_NAME', 'co-crew')
# DEBUG_FRONTEND = os.getenv('DEBUG_FRONTEND', 'False')
SECURE_API = os.getenv('SECURE_API', 'True')

REPORT_VALUE = 1
MAX_TIMES_RATING_USER = 1
MAX_COMMENTS_BY_USER = 1
SUPER_ADMIN_USERNAME = 'admin'
MAX_SESSION_TIME_MINUTES = 1440
SECRET_KEY = ''
DEFAULT_ACCEPTED_IMAGES_CONTENT_TYPE = ['image/png', 'image/jpg', 'image/jpeg']
ALLOWED_CONTENT_TYPES = ['video/mp4', 'video/quicktime', 'video/x-flv']

BASE_PATH = os.getenv('BASE_PATH', 'test-co-crew-directory/')

# GUNICORN CONFIG
bind = "{}:{}".format(REST_URL, REST_PORT)
workers = 1
threads = 4
timeout = 120
