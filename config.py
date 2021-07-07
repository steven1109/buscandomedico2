import mysql.connector
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    MYSQL_DB = os.getenv("MYSQL_DB")
    # CREDENTIAL LOCALHOST
    # MYSQL_HOST = os.getenv("MYSQL_HOST")
    # MYSQL_USER = os.getenv("MYSQL_USER")
    # MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
    # CREDENTIAL AWS
    MYSQL_HOST = os.getenv("MYSQL_HOST_AWS")
    MYSQL_USER = os.getenv("MYSQL_USER_AWS")
    MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD_AWS")


# MySQL Connection localhost
db = mysql.connector.connect(host=Config.MYSQL_HOST,
                             database=Config.MYSQL_DB,
                             user=Config.MYSQL_USER,
                             password=Config.MYSQL_PASSWORD)
