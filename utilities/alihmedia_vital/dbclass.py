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

class Variety(Base):
    __tablename__ =  TABLE_PREFIX + VARIETY_TABLE
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    folder: Mapped[str] = mapped_column(String(100))



class Doc(Base):
    __tablename__ = TABLE_PREFIX + DOC_TABLE
    id: Mapped[int] = mapped_column(primary_key=True)
    variety_id: Mapped[int] = mapped_column(ForeignKey(TABLE_PREFIX + VARIETY_TABLE + ".id"))
    doc_number: Mapped[int] = mapped_column(SmallInteger)
    name: Mapped[str] = mapped_column(Text, nullable=True)
    work_unit: Mapped[str] = mapped_column(String(100), nullable=True)
    period: Mapped[str] = mapped_column(String(4), nullable=True)
    media: Mapped[str] = mapped_column(String(50), nullable=True)
    countstr: Mapped[str] = mapped_column(String(100), nullable=True)
    save_life: Mapped[str] = mapped_column(String(50), nullable=True)
    uuid_id: Mapped[str] = mapped_column(String(36))
    save_location: Mapped[str] = mapped_column(Text, nullable=True)
    protect_method: Mapped[str] = mapped_column(String(100), nullable=True)
    description: Mapped[str] = mapped_column(String(100), nullable=True)
    page_count: Mapped[str] = mapped_column(SmallInteger, nullable=True)
    filesize: Mapped[int] = mapped_column(Integer, nullable=True)
    variety = relationship("Variety")
    