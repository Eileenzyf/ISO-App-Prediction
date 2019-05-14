import os
import sqlalchemy as sql
# the engine_string format
# engine_string = "{conn_type}://{user}:{password}@{host}:{port}/{database}" conn_type = "mysql+pymysql"
conn_type = "mysql+pymysql"
user = os.environ.get("MYSQL_USER")
password = os.environ.get("MYSQL_PASSWORD")
host = os.environ.get("MYSQL_HOST")
port = os.environ.get("MYSQL_PORT")
engine_string = "{}://{}:{}@{}:{}/DATABASE_NAME".format(conn_type, user, password, host, port)
print(engine_string)
engine = sql.create_engine(engine_string)