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
class Bundlecode(Base):
    __tablename__ =  TABLE_PREFIX + "bundlecode"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255))

