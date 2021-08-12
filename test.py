from cryptography.fernet import Fernet
from config import Config
import mysql.connector


def encrypt_decryption():
    # message = "hello geeks"
    message = input('new password: ')

    key = Config.TOKEN.encode()  # Fernet.generate_key()
    fernet = Fernet(key)
    encMessage = fernet.encrypt(message.encode())
    print("original string: ", message)
    print("encrypted string: ", encMessage)
    decMessage = fernet.decrypt(encMessage).decode()
    print("decrypted string: ", decMessage)

    # convert bytes to strings
    string_encMessage = encMessage.decode("utf-8")
    print("convert string encrypted: ", string_encMessage)

    # decrypted string
    print(fernet.decrypt(string_encMessage.encode()).decode())

    dd = 'gAAAAABhFOuLHtx23jN5IZgutfWceYYTEhjFOaXwHXtBwIcN4_UaNLsWgCP7_NIWIeKxLxSn2dSua0SFU6UUHlb-BvXuOAbuWg=='.encode()
    print(fernet.decrypt(dd).decode())


def decrypt(encMessage):
    key = Config.TOKEN.encode()  # Fernet.generate_key()
    fernet = Fernet(key)
    return fernet.decrypt(encMessage.encode()).decode()


def getUsersDB():
    config = Config()

    connection = mysql.connector.connect(host=config.MYSQL_HOST,
                                         database=config.MYSQL_DB,
                                         user=config.MYSQL_USER,
                                         password=config.MYSQL_PASSWORD)

    cur = connection.cursor()
    cur.execute("select * from usuario;")
    usuarios = cur.fetchall()

    for usuario in usuarios:
        print(usuario[3], usuario[4], decrypt(usuario[4]))


if __name__ == "__main__":
    getUsersDB()
