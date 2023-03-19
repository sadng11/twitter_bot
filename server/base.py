from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from decouple import config

import logging

logging.basicConfig()
logging.getLogger("sqlalchemy.engine").setLevel(logging.WARN)

connection_string = "mysql://{username}:{password}@{host}/{db}".format(username=config('MYSQL_USERNAME'),
                                                                       password=config('MYSQL_PASSWORD'),
                                                                       host=config('MYSQL_HOST'),
                                                                       db=config('MYSQL_DATABASE'))
engine = create_engine(connection_string)
Session = sessionmaker(bind=engine)

Base = declarative_base()
