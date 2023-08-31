from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import DatabaseError
from dotenv import dotenv_values
from sqlalchemy import create_engine


#* settings .env
config = dotenv_values(".env")

SQLALCHEMY_DATABASE_URL = config["ELEPHANTSQL"]
engine = create_engine(SQLALCHEMY_DATABASE_URL)

DBSession = sessionmaker(bind=engine)
session = DBSession()