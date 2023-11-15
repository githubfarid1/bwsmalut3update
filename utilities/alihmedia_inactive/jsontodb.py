#ok
import json
from sqlalchemy import create_engine, Column, Integer, String, SmallInteger, Text, CHAR
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, Session
from sqlalchemy.orm import mapped_column
# from sqlalchemy.orm import relationship
import argparse
import os
import sys
from settings import *
from dbclass import Doc, Department, Bundle, Base

engine = create_engine('mysql+pymysql://{}:{}@localhost:{}/{}'.format(USER, PASSWORD, PORT, DBNAME) , echo=False)


def main():
    parser = argparse.ArgumentParser(description="Get data from json and save them to database")
    parser.add_argument('-input', '--jsoninput', type=str,help="JSON File Input")
    args = parser.parse_args()
    isExist = os.path.exists(args.jsoninput)
    if not isExist:
        input(args.jsoninput + " does not exist")
        sys.exit()

    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    session = Session(engine)
    irigasi = Department(name="IRIGASI", defcode="IR", link="irigasi")
    ab = Department(name="AIR BAKU", defcode="AB", link="airbaku")
    pantai = Department(name="PANTAI", defcode="P", link="pantai")
    sungai = Department(name="SUNGAI", defcode="S", link="sungai")
    keuangan = Department(name="KEUANGAN", defcode="SPM", link="keuangan")
    session.add(irigasi)
    session.add(ab)
    session.add(pantai)
    session.add(sungai)
    session.add(keuangan)

    session.flush()
    session.commit()

    f = open(args.jsoninput)

    # returns JSON object as a dictionary
    data = json.load(f)
    # Iterating through the json list
    departmentId = irigasi.id
    defconde = irigasi.defcode

    for box in data:
        box_number = box['box']
        for bundle in box['data']:
            bundle_number = bundle['berkas']
            if bundle['ket'] == 'None':
                ket = ''
            else:
                ket = "".join(bundle['ket']).upper()

            if bundle['tahun'] == 'None':
                year = ''
            else:
                year = "".join(bundle['tahun'])

            bundleinsert = Bundle(department_id=departmentId, box_number=box_number, bundle_number=bundle_number, code=bundle['kode'], title=bundle['index'], year=year, orinot=ket)
            session.add(bundleinsert)
            session.flush()
            for doc in bundle['data']:
                if doc['jumlah']  is None:
                    jumlah = 1
                else:
                    jumlah = doc['jumlah']

                docinsert = Doc(bundle_id=bundleinsert.id, doc_number=doc['nourut'], doc_count=jumlah, description=doc['uraian'])
                session.add(docinsert)
                print("Insert record number: ", doc['nourut'])

    session.flush()
    session.commit()

if __name__ == '__main__':
    main()
