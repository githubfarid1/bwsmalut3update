import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
import fitz
from os.path import exists
from settings import *
from dbclass import Box, Item, Bundle, Package
import argparse
import sys
import pathlib
import shutil

def get_size(file_path, unit='bytes'):
    file_size = os.path.getsize(file_path)
    exponents_map = {'bytes': 0, 'kb': 1, 'mb': 2, 'gb': 3}
    if unit not in exponents_map:
        raise ValueError("Must select from \
        ['bytes', 'kb', 'mb', 'gb']")
    else:
        size = file_size / 1024 ** exponents_map[unit]
        return round(size, 3)

def get_page_count(pdffile):
    doc = fitz.open(pdffile)
    return doc.page_count

def generatecover(pdffile, coverfilename):
    # coverfilename = str(coverfilename).replace(TABLE_PREFIX, "")
    path = os.path.join(COVER_LOCATION, coverfilename)
    # breakpoint()
    print("Membuat cover: " + coverfilename, "...", end="", flush=True)
    doc = fitz.open(pdffile)
    page = doc.load_page(0)
    pix = page.get_pixmap()
    pix.save(path)
    doc.close()
    print("Success")

engine = create_engine('mysql+pymysql://{}:{}@localhost:{}/{}'.format(USER, PASSWORD, PORT, DBNAME) , echo=False)
Session = sessionmaker(bind = engine)
session = Session()    

tmppdfs = pathlib.Path(TMPPDF_LOCATION)
for pdf in list(tmppdfs.iterdir()):
    filename = pathlib.Path(pdf).name
    if filename[:len(APP_NAME + "_package")] != APP_NAME + "_package":
        continue
    package_id = filename.replace(".pdf", "").replace(APP_NAME + "_package$$", "")
    result = session.get(Package, package_id)
    # year = gencode.split("-")[0]
    if not exists(os.path.join(PDF_LOCATION, APP_NAME)):
        os.mkdir(os.path.join(PDF_LOCATION, APP_NAME))

    if not exists(os.path.join(PDF_LOCATION, APP_NAME, "package_pdf")):
        os.mkdir(os.path.join(PDF_LOCATION, APP_NAME, "package_pdf"))
    path = os.path.join(PDF_LOCATION, APP_NAME, "package_pdf",  result.uuid_id + ".pdf")
    print("File",pathlib.Path(pdf).name, "Dipindah Ke: " + path)
    shutil.move(pdf, path)
