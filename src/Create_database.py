import os
import sys
import logging
import logging.config

from sqlalchemy import create_engine, Column, Integer, String, Text,Float
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

import argparse
import ConnectRDS


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

def create_db(engine=None, engine_string=None):
	if engine is None and engine_string is None:
		return ValueError("`engine` or `engine_string` must be provided")
	elif engine is None:
		engine = create_connection(engine_string=engine_string)

	Base.metadata.create_all(engine)


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Create defined tables in database")
	parser.add_argument("--truncate", "-t", default=False, action="store_true",
	                    help="If given, delete current records from tweet_scores table before create_all "
	                         "so that table can be recreated without unique id issues ")
	args = parser.parse_args()




	create_db(engine=ConnectRDS.engine)




