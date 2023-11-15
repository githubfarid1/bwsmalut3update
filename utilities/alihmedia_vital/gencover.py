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

engine = create_engine('mysql+pymysql://{}:{}@localhost:{}/{}'.format(USER, PASSWORD, PORT, DBNAME) , echo=False)

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
    path = os.path.join(COVER_LOCATION, coverfilename)
    print("Membuat cover: " + coverfilename, "...", end="", flush=True)
    doc = fitz.open(pdffile)
    page = doc.load_page(0)
    pix = page.get_pixmap()
    pix.save(path)
    doc.close()
    print("Success")



def main():
    parser = argparse.ArgumentParser(description="Get data from json and save them to database")
    parser.add_argument('-r', '--replace', type=str,help="is replace?")
    args = parser.parse_args()
    if not args.replace:
        print("need -r parameter")
        sys.exit()

    Session = sessionmaker(bind = engine)
    session = Session()    
    result = session.query(Doc).join(Variety).all()
    for row in result:
        path = os.path.join(PDF_LOCATION, APP_NAME, row.variety.folder, str(row.doc_number) + ".pdf")
        # print(path)
        if exists(path):
            coverfilename = "{}{}_{}.png".format(TABLE_PREFIX, row.variety.folder,  row.doc_number)
            
            if args.replace == 'Yes' or args.replace == 'yes':
                generatecover(pdffile=path, coverfilename=coverfilename)
            else:
                if not exists(os.path.join(COVER_LOCATION, coverfilename)):
                    generatecover(pdffile=path, coverfilename=coverfilename)

            filesize = get_size(path, "kb")
            pagecount = get_page_count(pdffile=path)
            session.query(Doc).filter(Doc.id == row.id).update({Doc.filesize: filesize, Doc.page_count: pagecount})
            session.commit()

if __name__ == '__main__':
    main()
