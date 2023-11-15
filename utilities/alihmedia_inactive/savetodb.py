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

engine = create_engine('mysql+pymysql://root:1234@localhost:33061/arsipdb3', echo=False)

class Base(DeclarativeBase):
    pass

class Department(Base):
    __tablename__ = "arsip_department"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    defcode: Mapped[str] = mapped_column(String(20))
    link: Mapped[str] = mapped_column(String(20))

class Bundle(Base):
    __tablename__ = "arsip_bundle"
    id: Mapped[int] = mapped_column(primary_key=True)
    department_id: Mapped[int] = mapped_column(ForeignKey("arsip_department.id"))
    box_number: Mapped[int] = mapped_column(SmallInteger)
    bundle_number: Mapped[int] = mapped_column(SmallInteger)
    code: Mapped[str] = mapped_column(String(20))
    title: Mapped[str] = mapped_column(Text)
    year: Mapped[str] = mapped_column(CHAR(4),  nullable=True)
    orinot: Mapped[str] = mapped_column(String(10), nullable=True)
    description: Mapped[str] = mapped_column(String(255), nullable=True)


class Doc(Base):
    __tablename__ = "arsip_doc"
    id: Mapped[int] = mapped_column(primary_key=True)
    bundle_id: Mapped[int] = mapped_column(ForeignKey("arsip_bundle.id"))
    doc_number: Mapped[int] = mapped_column(SmallInteger)
    doc_count: Mapped[int] = mapped_column(SmallInteger)
    orinot: Mapped[str] = mapped_column(String(10), nullable=True)
    doc_type: Mapped[str] = mapped_column(String(20), nullable=True)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    page_count: Mapped[str] = mapped_column(SmallInteger, nullable=True)
    filesize: Mapped[int] = mapped_column(SmallInteger, nullable=True)


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

f = open('data.json')

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
