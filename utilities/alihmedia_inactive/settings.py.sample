import os
import environ
from os.path import dirname, abspath, join
BASE_DIR = dirname(dirname(dirname(abspath(__file__))))
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

DBNAME =  os.getenv('DB_NAME')
PORT = os.getenv('DB_PORT')
USER = os.getenv('DB_USERNAME')
PASSWORD = os.getenv('DB_PASS')

DEPARTMENT_TABLE = "department"
BUNDLE_TABLE = "bundle"
DOC_TABLE = "doc"
TABLE_PREFIX = "alihmedia_inactive_"
APP_NAME = "alihmedia_inactive"
COVER_LOCATION = os.path.join("/home/farid/dev/python/bwsmalut3/apps", "static", "cover")
PDF_LOCATION = "/home/farid/pdfs/"
EXCEL_FILE = "Daftar Arsip-asli.xlsx"
EXCEL_SHEET = ["IRIGASI", "AIR BAKU", "PANTAI", "SUNGAI", "KEUANGAN"]
# EXCEL_SHEET = ["KEUANGAN"]
TMPPDF_LOCATION = "/home/farid/dev/python/bwsmalut3/media/tmpfiles"

BACKUP_LOCATION = "/home/farid/backup"
