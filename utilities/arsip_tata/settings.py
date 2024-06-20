import os
import environ
from os.path import dirname, abspath, join
BASE_DIR = dirname(dirname(dirname(abspath(__file__))))
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

DBNAME =  os.getenv('DB_NAME')
PORT = os.getenv('DB_PORT')
USER = os.getenv('DB_USERNAME')
PASSWORD = os.getenv('DB_PASS')
TABLE_PREFIX = "arsip_tata_"
APP_NAME = "arsip_tata"
COVER_LOCATION = os.path.join("/home/arsip/dev/bwsmalut3", "staticfiles", "cover")
PDF_LOCATION = "/home/farid/pdfs/"
COVER_LOCATION = os.path.join("/home/arsip/dev/bwsmalut3", "staticfiles", "cover")
PDF_LOCATION = "/home/arsip/nas-media/"

TMPPDF_LOCATION = "/home/arsip/dev/bwsmalut3/media/tmpfiles"
BACKUP_LOCATION = "/home/arsip/backup"

