#ok
import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
import fitz
from os.path import exists
from settings import *
from dbclass import Doc, Department, Bundle
import argparse
import sys
import pathlib
import shutil

engine = create_engine('mysql+pymysql://{}:{}@localhost:{}/{}'.format(USER, PASSWORD, PORT, DBNAME) , echo=False)
Session = sessionmaker(bind = engine)
session = Session()    


tmppdfs = pathlib.Path(TMPPDF_LOCATION)
for pdf in list(tmppdfs.iterdir()):
    # print(tmp)
    filename = pathlib.Path(pdf).name
    if filename[:len(APP_NAME)] != APP_NAME:
        continue
    docid = filename.replace(".pdf", "").replace(APP_NAME + "-", "")
    result = session.query(Doc).filter(Doc.id == docid).first()
    box_number = result.bundle.box_number
    doc_number = result.doc_number
    folder = result.bundle.department.folder
    # print(box_number, doc_number, link)
    if not exists(os.path.join(PDF_LOCATION, APP_NAME, folder)):
        os.mkdir(os.path.join(PDF_LOCATION, APP_NAME, folder))

    if not exists(os.path.join(PDF_LOCATION, APP_NAME, folder, str(box_number))):
        os.mkdir(os.path.join(PDF_LOCATION, APP_NAME, folder, str(box_number)))
    print("File",pathlib.Path(pdf).name, "Dipindah Ke: " + os.path.join(PDF_LOCATION, APP_NAME, folder, str(box_number), str(doc_number) + ".pdf"))
    shutil.move(pdf, os.path.join(PDF_LOCATION, APP_NAME, folder, str(box_number), str(doc_number) + ".pdf"))