import os
import environ
from os.path import dirname, abspath, join
BASE_DIR = dirname(dirname(dirname(abspath(__file__))))
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

DBNAME =  os.getenv('DB_NAME')
PORT = os.getenv('DB_PORT')
USER = os.getenv('DB_USERNAME')
PASSWORD = os.getenv('DB_PASS')

APPS_NAME = ["fm_pjpa", "fm_pjsa"]
#COVER_LOCATION = os.path.join("/home/farid/dev/python/bwsmalut3/apps", "static", "cover")
FM_LOCATION = r"D:\dataweb\fms"
# EXCEL_FILE = "/home/farid/dev/python/bwsmalut3/utilities/data/Daftar Arsip-asli.xlsx"
# EXCEL_SHEET = ["IRIGASI", "AIR BAKU", "PANTAI", "SUNGAI", "KEUANGAN"]
# EXCEL_SHEET = ["KEUANGAN"]
TMPFM_LOCATION = r"D:\dev\python\bws\bwsmalut3update\media\tmpfiles"
# BACKUP_LOCATION = "/home/farid/backup"
