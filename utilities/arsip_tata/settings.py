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

