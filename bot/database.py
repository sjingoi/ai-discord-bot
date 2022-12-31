import mysql.connector
import os
from dotenv import load_dotenv, find_dotenv

env_dir = find_dotenv('secrets.env', True)
load_dotenv(env_dir)

HOST = os.environ["DB_IP"]
DATABASE = os.environ["DB_NAME"]
USERNAME = os.environ["DB_USER"]
PASSWORD = os.environ["DB_PASSWORD"]

def get_connection():
    mydb = mysql.connector.connect(
        host = HOST,
        user = USERNAME,
        password = PASSWORD,
        database = DATABASE
    )
    return mydb

def add_server(id: int, name: str, cmd_prefix: str = '$', openai_key: str = None) -> None:
    mydb = get_connection()
    dbcursor = mydb.cursor()
    sql = "INSERT INTO dservers (server_id, server_name, cmd_prefix, openai_key) VALUES (%s, %s, %s, %s)"
    val = (id, name, cmd_prefix, openai_key)
    dbcursor.execute(sql, val)
    mydb.commit()
    dbcursor.close()
    mydb.close()


def get_ai_key(server_id: int):
    return get_from_dserver_table(server_id, "openai_key")


def get_cmd_prefix(server_id: int):
    return get_from_dserver_table(server_id, "cmd_prefix")


def get_from_dserver_table(server_id: int, collumn: str):
    mydb = get_connection()
    dbcursor = mydb.cursor()
    dbcursor.execute("SELECT " + collumn + " FROM dservers WHERE server_id = " + str(server_id))
    for key in dbcursor:
        return key[0]
    dbcursor.close()
    mydb.close()


def update_openai_key(server_id: int, key: int):
    update_dserver(server_id, "openai_key", key)


def update_prefix(server_id: int, prefix: str):
    update_dserver(server_id, "cmd_prefix", prefix)


def update_dserver(server_id: int, collumn: str, value: str):
    mydb = get_connection()
    dbcursor = mydb.cursor()
    dbcursor.execute("UPDATE dservers SET " + collumn + " = '" + value + "' WHERE server_id = " + str(server_id))
    mydb.commit()
    dbcursor.close()
    mydb.close()


def server_in_database(server_id: int) -> bool:
    if get_from_dserver_table(server_id, "server_name") is None:
        return False
    return True