import os
import sys
import logging
import logging.config
import pandas as pd
import sqlalchemy as sql

from sqlalchemy import create_engine, Column, Integer, String, Text,Float
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

import argparse
import ConnectRDS

logging.basicConfig(level=logging.INFO, filename="logfile")
logger = logging.getLogger('Create_database')


Base = declarative_base()

class appstore(Base):
	""" Defines the data model for the table `appstore`. """

	__tablename__ = 'appstore'

	app_id = Column(String(100), primary_key=True, unique=True, nullable=False)
	track_name = Column(String(100), unique=False, nullable=False)
	size_bytes = Column(String(100), unique=False, nullable=False)
	currency = Column(String(100), unique=False, nullable=False)
	price = Column(Float, unique=False, nullable=False)
	rating_count_tot = Column(String(100), unique=False, nullable=False)
	rating_count_ver = Column(Integer, unique=False, nullable=False)
	user_rating = Column(Float, unique=False, nullable=False)
	user_rating_ver = Column(Float, unique=False, nullable=False)
	ver = Column(String(100), unique=False, nullable=False)
	cont_rating = Column(String(100), unique=False, nullable=False)
	prime_genre = Column(Text, unique=False, nullable=False)
	sup_devices_num = Column(Integer, unique=False, nullable=False)
	ipadSc_urls_num = Column(Integer, unique=False, nullable=False)
	lang_num = Column(Integer, unique=False, nullable=False)
	vpp_lic = Column(Integer, unique=False, nullable=False)

	def __repr__(self):
		appstore_repr = "<appstore(app_id='%s', track_name='%s', size_bytes='%s', currency='%s', price='%s', rating_count_tot='%s', rating_count_ver='%s', user_rating='%s', user_rating_ver='%s', ver='%s', cont_rating='%s', prime_genre='%s', sup_devices_num='%s', ipadSc_urls_num='%s', lang_num='%s', vpp_lic='%s')>"
		return appstore_repr % (self.app_id, self.track_name, self.size_bytes, self.currency, self.price, self.rating_count_tot, self.rating_count_ver, self.user_rating, self.user_rating_ver, self.ver, self.cont_rating, self.prime_genre, self.sup_devices_num, self.ipadSc_urls_num, self.lang_num, self.vpp_lic)


class appStore_description(Base):
	__tablename__ = 'appStore_description'

	app_id = Column(String(100), primary_key=True, unique=True, nullable=False)
	track_name = Column(String(100), unique=False, nullable=False)
	size_bytes = Column(String(100), unique=False, nullable=False)
	app_desc = Column(Text, unique=False, nullable=False)

	def __repr__(self):
		appdesc_repr = "<appStore_description(app_id='%s', track_name='%s', size_bytes='%s', app_desc='%s')>"
		return appdesc_repr % (self.app_id, self.track_name, self.size_bytes, self.app_desc)

class user_input(Base):

	__tablename__ = 'user_input'

	Id = Column(Integer, primary_key=True, unique=True, nullable=False)
	size_bytes = Column(String(100), unique=False, nullable=False)
	price = Column(Float, unique=False, nullable=False)
	sup_devices_num = Column(Integer, unique=False, nullable=False)
	ipadSc_urls_num = Column(Integer, unique=False, nullable=False)
	lang_num = Column(Integer, unique=False, nullable=False)
	rating_count = Column(String(100), unique=False, nullable=False)
	cont_rating = Column(String(100), unique=False, nullable=False)
	prime_genre = Column(Text, unique=False, nullable=False)
	app_desc = Column(Text, unique=False, nullable=False)
	prediction = Column(Float, unique=False, nullable=False)

	def __repr__(self):
		user_repr = "<user_input(Id='%s', size_bytes='%s', price='%s', rating_count='%s', cont_rating='%s', prime_genre='%s', sup_devices_num='%s', ipadSc_urls_num='%s', lang_num='%s', app_desc='%s')>"
		return user_repr % (self.Id, self.size_bytes, self.price, self.rating_count, self.cont_rating, self.prime_genre, self.sup_devices_num, self.ipadSc_urls_num, self.lang_num, self.app_desc)

def get_engine_string(RDS = False):
	if RDS:
		conn_type = "mysql+pymysql"
		user = os.environ.get("MYSQL_USER")
		password = os.environ.get("MYSQL_PASSWORD")
		host = os.environ.get("MYSQL_HOST")
		port = os.environ.get("MYSQL_PORT")
		DATABASE_NAME = 'msia423'
		engine_string = "{}://{}:{}@{}:{}/{}". \
		format(conn_type, user, password, host, port, DATABASE_NAME)
		# print(engine_string)
		logging.debug("engine string: %s"%engine_string)
		return  engine_string
	else:
		return 'sqlite:///user_input.db' # relative path

def create_db(engine=None, engine_string=None):
	if engine is None:
		#RDS = eval(args.RDS) # evaluate string to bool
		#logger.info("RDS:%s"%RDS)
		engine = sql.create_engine(get_engine_string(RDS = RDS))

	Base.metadata.create_all(engine)
	logging.info("database created")

	Session = sessionmaker(bind=engine)  
	session = Session()

	use1 = user_input(size_bytes='28899', price=3.99, rating_count=345, cont_rating='4+', 
		prime_genre='Games', sup_devices_num=4, ipadSc_urls_num=6, lang_num=6, app_desc='Games are fun', prediction = 4.5)
	session.add(use1)

	logger.info("Data added")
	session.commit()


if __name__ == "__main__":
	#parser = argparse.ArgumentParser(description="Create defined tables in database")
	#parser.add_argument("--RDS", default="False",help="True if want to create in RDS else None")
	#args = parser.parse_args()

	create_db()


	



	


