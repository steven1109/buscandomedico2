# import mysql.connector
import pymysql
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
    TOKEN = os.getenv("token")


class DBMySql:
    def __init__(self):
        self.config = None
        self.connection = None

    def initialize(self):
        self.config = Config()

    def connect(self):
        # old_connection = mysql.connector.connect(host=self.config.MYSQL_HOST,
        #                                          database=self.config.MYSQL_DB,
        #                                          user=self.config.MYSQL_USER,
        #                                          password=self.config.MYSQL_PASSWORD)

        new_connection = pymysql.connect(host=self.config.MYSQL_HOST,
                                         database=self.config.MYSQL_DB,
                                         user=self.config.MYSQL_USER,
                                         passwd=self.config.MYSQL_PASSWORD)

        return new_connection

    def close(self):
        pymysql.connect.close()
        # mysql.connector.close()
