import os
import sys
import logging
import logging.config
import pandas as pd
import sqlalchemy as sql


from sqlalchemy import create_engine, Column, Integer, String, Text,Float
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, MetaData

import argparse

#get logger
logging.basicConfig(level=logging.INFO, filename="logfile")
logger = logging.getLogger('Create_database')

#define base
Base = declarative_base()

class user_input(Base):
	""" Defines the data model for the table `user_input. """
	__tablename__ = 'user_input'

	#define each column name and variable type
	Id = Column(Integer, primary_key=True, unique=True, nullable=False)
	size_bytes = Column(String(100), unique=False, nullable=False)
	price = Column(Float, unique=False, nullable=False)
	sup_devices_num = Column(Integer, unique=False, nullable=False)
	ipadSc_urls_num = Column(Integer, unique=False, nullable=False)
	lang_num = Column(Integer, unique=False, nullable=False)
	rating_count_tot = Column(String(100), unique=False, nullable=False)
	rating_count_ver = Column(String(100), unique=False, nullable=False)
	cont_rating = Column(String(100), unique=False, nullable=False)
	prime_genre = Column(Text, unique=False, nullable=False)
	app_desc = Column(Text, unique=False, nullable=False)
	prediction = Column(Float, unique=False, nullable=False)

	def __repr__(self):
		user_repr = "<user_input(Id='%s', size_bytes='%s', price='%s', rating_count='%s', cont_rating_tot='%s', cont_rating_ver='%s', prime_genre='%s', sup_devices_num='%s', ipadSc_urls_num='%s', lang_num='%s', app_desc='%s')>"
		return user_repr % (self.Id, self.size_bytes, self.price, self.rating_count, self.cont_rating_tot, self.cont_rating_ver, self.prime_genre, self.sup_devices_num, self.ipadSc_urls_num, self.lang_num, self.app_desc)

def get_engine_string(RDS = False):
	"""Get database engine path."""
	if RDS:
		conn_type = "mysql+pymysql"
		user = os.environ.get("MYSQL_USER")
		password = os.environ.get("MYSQL_PASSWORD")
		host = os.environ.get("MYSQL_HOST")
		port = os.environ.get("MYSQL_PORT")
		DATABASE_NAME = 'msia423'
		engine_string = "{}://{}:{}@{}:{}/{}". \
		format(conn_type, user, password, host, port, DATABASE_NAME)
		logging.debug("engine string: %s"%engine_string)
		return  engine_string
	else:
		return 'sqlite:///data/user_input.db' # relative path


def create_db(args, engine=None):
	"""Creates a database with the data models inherited from `Base`.

    Args:
        engine (:py:class:`sqlalchemy.engine.Engine`, default None): SQLAlchemy connection engine.
            If None, `engine_string` must be provided.
        engine_string (`str`, default None): String defining SQLAlchemy connection URI in the form of
            `dialect+driver://username:password@host:port/database`. If None, `engine` must be provided.

    Returns:
        None
    """
    #if running on RDS
	if args.RDS:
		engine = sql.create_engine(get_engine_string(RDS = True))
	#if running a local
	else:
		engine = sql.create_engine(get_engine_string(RDS = False))
	logger.info("RDS:%s"%args.RDS)


	Base.metadata.create_all(engine)
	logging.info("database created")

	#create a db session
	Session = sessionmaker(bind=engine)  
	session = Session()

	#test unit for the user_input table
	user1 = user_input(size_bytes='100788224', price=3.99, rating_count_tot=21292, rating_count_ver=26, cont_rating='4+', 
						prime_genre='Games', sup_devices_num=38, ipadSc_urls_num=5, lang_num=10, app_desc='SAVE 20%, now only $3.99 for a limited time! One of the most popular video games in arcade history! 2015 World Video Game Hall of Fame Inductee', prediction = 4)
	session.add(user1)

	logger.info("Data added")
	session.commit()

	return engine


if __name__ == "__main__":
	#user input
	parser = argparse.ArgumentParser(description="Create Database")
	parser.add_argument('--RDS', default = False, help='Whether connect to RDS')
	

	args = parser.parse_args()

	engine = create_db(args)

	query = "SELECT * FROM user_input"
	df = pd.read_sql(query, con=engine)
	print(df)


	



	


