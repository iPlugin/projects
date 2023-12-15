from sqlalchemy import Column, Integer, String, Boolean, func, Table
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Vacancies(Base):
    __tablename__ = "vacancies"
    id = Column(Integer, primary_key=True)
    company = Column(String(150), nullable=False)
    job_title = Column(String(150), nullable=False)
    job_link = Column(String(150), nullable=False)
    employee = Column(String(150), nullable=False)
    date = Column(String(150), nullable=False)
