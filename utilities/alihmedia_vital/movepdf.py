#ok
import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
import fitz
from os.path import exists
from settings import *
from dbclass import Doc, Variety
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
    docid = filename.replace(".pdf", "").replace(APP_NAME + "-", "")
    result = session.query(Doc).filter(Doc.id == docid).first()
    if result:
        doc_number = result.doc_number
        folder = result.variety.folder
        # print(doc_number, folder)
        # sys.exit()
        # print(box_number, doc_number, link)
        if not exists(os.path.join(PDF_LOCATION, APP_NAME, folder)):
            os.mkdir(os.path.join(PDF_LOCATION, APP_NAME, folder))

        print("File",pathlib.Path(pdf).name, "Dipindah Ke: " + os.path.join(PDF_LOCATION, APP_NAME, folder, str(doc_number) + ".pdf"))
        shutil.move(pdf, os.path.join(PDF_LOCATION, APP_NAME, folder, str(doc_number) + ".pdf"))