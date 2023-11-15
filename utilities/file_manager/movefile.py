#ok
import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
import fitz
from os.path import exists
from settings import *
# from dbclass import Doc, Department, Bundle
import argparse
import sys
import pathlib
import shutil

# engine = create_engine('mysql+pymysql://{}:{}@localhost:{}/{}'.format(USER, PASSWORD, PORT, DBNAME) , echo=False)
# Session = sessionmaker(bind = engine)
# session = Session()    


tmpfms = pathlib.Path(TMPFM_LOCATION)
for file in list(tmpfms.iterdir()):
    # print(tmp)
    filename = pathlib.Path(file).name
    
    # found = False
    for app in APPS_NAME:
        if filename[:len(app)] != app:
            found = True
            break
    if not found:
        continue

    filepath = str(file).replace("$$", "/")
    filepath = filepath.replace(TMPFM_LOCATION + "/", "")
    if exists(os.path.join(FM_LOCATION, filepath)):
        os.remove(os.path.join(FM_LOCATION, filepath))
    print("File", filename, "Dipindah Ke: " + os.path.join(FM_LOCATION, filepath))
        
    shutil.move(file, os.path.join(FM_LOCATION, filepath))
