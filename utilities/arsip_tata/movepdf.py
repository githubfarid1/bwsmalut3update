import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
import fitz
from os.path import exists
from settings import *
from dbclass import Box, Item, Bundle
import argparse
import sys
import pathlib
import shutil

engine = create_engine('mysql+pymysql://{}:{}@localhost:{}/{}'.format(USER, PASSWORD, PORT, DBNAME) , echo=False)
Session = sessionmaker(bind = engine)
session = Session()    


tmppdfs = pathlib.Path(TMPPDF_LOCATION)
for pdf in list(tmppdfs.iterdir()):
    filename = pathlib.Path(pdf).name
    if filename[:len(APP_NAME)] != APP_NAME:
        continue
    gencode = filename.replace(".pdf", "").replace(APP_NAME + "$$", "")
    result = session.query(Item).filter(Item.codegen == gencode).first()
    year = gencode.split("-")[0]
    if not exists(os.path.join(PDF_LOCATION, APP_NAME, year)):
        os.mkdir(os.path.join(PDF_LOCATION, APP_NAME, year))

    print("File",pathlib.Path(pdf).name, "Dipindah Ke: " + os.path.join(PDF_LOCATION, APP_NAME, year,  gencode + ".pdf"))
    shutil.move(pdf, os.path.join(PDF_LOCATION, APP_NAME, year, gencode + ".pdf"))
