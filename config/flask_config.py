import os
DEBUG = True
LOGGING_CONFIG = "../config/logging/local.conf"
PORT = 3000
conn_type = "mysql+pymysql"  
user = os.environ.get("MYSQL_USER")  
password = os.environ.get("MYSQL_PASSWORD")  
host = os.environ.get("MYSQL_HOST") 
port = os.environ.get("MYSQL_PORT")  
DATABASE_NAME = 'msia423'  
SQLALCHEMY_DATABASE_URI = "{}://{}:{}@{}:{}/{}".\
        format(conn_type, user, password, host, port, DATABASE_NAME)
APP_NAME = "IOS App Prediction"
PATH_TO_MODEL = '../models/app-prediction.pkl'
SQLALCHEMY_TRACK_MODIFICATIONS = True
HOST = "0.0.0.0"
SQLALCHEMY_ECHO = False  # If true, SQL for queries made will be printed
