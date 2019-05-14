import os
import sys
import json
from json import JSONDecodeError

import config
import logging
import logging.config
import sqlite3

from Create_database import appscore
from Create_database import appStore_description
from Create_database import user_input

engine = sql.create_engine(engine_string) 
Base.metadata.create_all(engine)

