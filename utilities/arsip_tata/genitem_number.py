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
from dbclass import Bundle, Base, Box, Item

engine = create_engine('mysql+pymysql://{}:{}@localhost:{}/{}'.format(USER, PASSWORD, PORT, DBNAME) , echo=False)

def parse(startbox, endbox, firstitem):
    gennumber = firstitem
    session = Session(engine)
    boxes = session.query(Box).filter(Box.box_number>=startbox).filter(Box.box_number<=endbox).order_by(Box.box_number).all()
    for box in boxes:
        bundles = session.query(Bundle).filter(Bundle.box_id==box.id).order_by(Bundle.bundle_number).all()
        for bundle in bundles:
            items = session.query(Item).filter(Item.bundle_id==bundle.id).order_by(Item.item_number).all()
            for item in items:
                print("No Box:", box.box_number, "No Berkas:", bundle.bundle_number, "No Item:", item.item_number, "Diupdate ke", gennumber)
                session.query(Item).filter(Item.id==item.id).update({'item_number': gennumber, 'codegen': "-".join([str(box.yeardate) ,str(box.box_number), str(bundle.bundle_number), str(gennumber)])})
                gennumber += 1
    jawab = input("Simpan Perubahan (Y/N)?")
    if jawab == 'Y' or jawab == 'y':
        session.flush()
        session.commit()

def main():
    parser = argparse.ArgumentParser(description="Generate Item Number")
    parser.add_argument('-s', '--start', type=str,help="Start Box Number")
    parser.add_argument('-e', '--end', type=str,help="End Box Number")
    parser.add_argument('-f', '--firstnumber', type=str,help="First Item Number")

    args = parser.parse_args()
    if not args.start or not args.end or not args.firstnumber:
        print("use command python genitem_number.py -s [start_box] -e [end_box] -f [first_item_number]")
        sys.exit()

    parse(int(args.start), int(args.end), int(args.firstnumber))
    print("End Process...")    
if __name__ == '__main__':
    main()