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
