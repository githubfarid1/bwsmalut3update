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
from dbclass import Bundle, Base, Box, Item, Year
from sqlalchemy import insert

engine = create_engine('mysql+pymysql://{}:{}@localhost:{}/{}'.format(USER, PASSWORD, PORT, DBNAME) , echo=False)

def parse(startbox, endbox, year):
    session = Session(engine)
    
    yearid = session.query(Year).filter(Year.yeardate==year).first().id
    # breakpoint()
    for number in range(startbox, endbox+1):
        stmt = insert(Box).values(year_id=yearid, box_number=number, yeardate=year)
        session.execute(stmt)
    # boxes = session.query(Box).filter(Box.box_number>=startbox).filter(Box.box_number<=endbox).order_by(Box.box_number).all()
    # for box in boxes:
    #     bundles = session.query(Bundle).filter(Bundle.box_id==box.id).order_by(Bundle.bundle_number).all()
    #     for bundle in bundles:
    #         # print("No Box:", box.box_number, "No Bundle:", bundle.bundle_number, "Diupdate ke", genbundlenumber)
    #         # session.query(Bundle).filter(Bundle.id==bundle.id).update({'bundle_number': genbundlenumber})
    #         # genbundlenumber += 1
    #         items = session.query(Item).filter(Item.bundle_id==bundle.id).order_by(Item.item_number).all()
    #         for item in items:
    #             codegen = "-".join([str(box.yeardate) ,str(box.box_number), str(bundle.bundle_number), str(item.item_number)])
    #             print("Codegen:",item.codegen, "Diupdate ke", codegen)
    #             session.query(Item).filter(Item.id==item.id).update({'codegen': codegen})
    jawab = input("Simpan Perubahan (Y/N)?")
    if jawab == 'Y' or jawab == 'y':
        session.flush()
        session.commit()
    else:
        session.rollback()
def main():
    parser = argparse.ArgumentParser(description="Generate Box Number")
    parser.add_argument('-s', '--start', type=str,help="Start Box Number")
    parser.add_argument('-e', '--end', type=str,help="End Box Number")
    parser.add_argument('-y', '--year', type=str,help="Year")


    args = parser.parse_args()
    if not args.start or not args.end or not args.year:
        print("use command python box_numbergen.py -s [start_box] -e [end_box] -y [year]")
        sys.exit()

    parse(int(args.start), int(args.end), int(args.year))
    print("End Process...")    
if __name__ == '__main__':
    main()
