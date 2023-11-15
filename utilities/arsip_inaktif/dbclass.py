from sqlalchemy import Column, Integer, String, SmallInteger, Text, CHAR
from sqlalchemy.orm import  DeclarativeBase,  relationship
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from settings import *
import uuid

class Base(DeclarativeBase):
    pass
class Department(Base):
    __tablename__ =  TABLE_PREFIX + DEPARTMENT_TABLE
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    defcode: Mapped[str] = mapped_column(String(20))
    link: Mapped[str] = mapped_column(String(50))
    folder: Mapped[str] = mapped_column(String(50))

class Bundle(Base):
    __tablename__ = TABLE_PREFIX + BUNDLE_TABLE
    id: Mapped[int] = mapped_column(primary_key=True)
    department_id: Mapped[int] = mapped_column(ForeignKey(TABLE_PREFIX + DEPARTMENT_TABLE + ".id"))
    box_number: Mapped[int] = mapped_column(SmallInteger)
    bundle_number: Mapped[int] = mapped_column(SmallInteger)
    code: Mapped[str] = mapped_column(String(20))
    title: Mapped[str] = mapped_column(Text)
    year: Mapped[str] = mapped_column(CHAR(4),  nullable=True)
    orinot: Mapped[str] = mapped_column(String(10), nullable=True)
    description: Mapped[str] = mapped_column(String(255), nullable=True)
    department = relationship("Department")


class Doc(Base):
    __tablename__ = TABLE_PREFIX + DOC_TABLE
    id: Mapped[int] = mapped_column(primary_key=True)
    bundle_id: Mapped[int] = mapped_column(ForeignKey(TABLE_PREFIX + BUNDLE_TABLE + ".id"))
    doc_number: Mapped[int] = mapped_column(SmallInteger)
    doc_count: Mapped[int] = mapped_column(SmallInteger)
    orinot: Mapped[str] = mapped_column(String(10), nullable=True)
    doc_type: Mapped[str] = mapped_column(String(20), nullable=True)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    page_count: Mapped[str] = mapped_column(SmallInteger, nullable=True)
    filesize: Mapped[int] = mapped_column(Integer, nullable=True)
    uuid_id: Mapped[str] = mapped_column(String(36))
    access: Mapped[str] = mapped_column(String(50), nullable=True)

    bundle = relationship("Bundle")
    # comments = relationship("Comment")
