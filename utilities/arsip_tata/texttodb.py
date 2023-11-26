import json
import argparse
import sys
import os
from settings import *
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from dbclass import Bundlecode
import uuid

engine = create_engine('mysql+pymysql://{}:{}@localhost:{}/{}'.format(USER, PASSWORD, PORT, DBNAME) , echo=False)
session = Session(engine)
with open('items.txt') as f:
    contents = f.readlines()
    for txt in contents:
        code = Bundlecode(name=txt.replace("\n", ""))
        session.add(code)
    # line = f.read()
    # code = Bundlecode(name=line)
    # session.add(code)
    # print(line)
    session.flush()
    session.commit()
