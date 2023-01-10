import mysql.connector
import os
from dotenv import load_dotenv, find_dotenv

env_dir = find_dotenv('secrets.env', True)
load_dotenv(env_dir)

# MYSQL CREDENTIALS
HOST = os.environ["DB_IP"]
DATABASE = os.environ["DB_NAME"]
USERNAME = os.environ["DB_USER"]
PASSWORD = os.environ["DB_PASSWORD"]

# TABLES
SERVERS_TABLE = "dservers"
SERVER_ID_COL = "server_id"
SERVER_NAME_COL = "server_name"
SERVER_CMD_PFX_COL = "cmd_prefix"
SERVER_AI_KEY_COL = "openai_key"
SERVER_OWNER_COL = "owner_id"
USERS_TABLE = "users"
USER_ID_COL = "user_id"
USER_NAME_COL = "user_name"
USER_NUM_OF_REQ_COL = "num_of_req"


def get_connection():
    mydb = mysql.connector.connect(
        host = HOST,
        user = USERNAME,
        password = PASSWORD,
        database = DATABASE
    )
    return mydb


def add_server(server_id: int, name: str, owner_id: int) -> None:
    mydb = get_connection()
    dbcursor = mydb.cursor()
    sql = "INSERT INTO dservers (server_id, server_name, cmd_prefix, openai_key, owner_id) VALUES (%s, %s, %s, %s, %s)"
    val = (server_id, name, cmd_prefix, openai_key, owner_id)
    dbcursor.execute(sql, val)
    mydb.commit()
    dbcursor.close()
    mydb.close()


def add_user(user_id: int, user_name: str):
    print("Hello")
    mydb = get_connection()
    dbcursor = mydb.cursor()
    sql = "INSERT INTO users (user_id, user_name) VALUES (%s, %s)"
    val = (user_id, user_name)
    dbcursor.execute(sql, val)
    mydb.commit()
    dbcursor.close()
    mydb.close()


def in_table(table: str, key_col: str, key: int) -> bool:
    return not get_from_table(table, key_col, key, key_col) is None


def increment(table: str, key_col: str, key: int, collumn: str, ammount: int = 1):
    mydb = get_connection()
    dbcursor = mydb.cursor()
    dbcursor.execute("UPDATE " + table + " SET " + collumn + " = " +  collumn + " + " + str(ammount) + " WHERE " + key_col + " = " + str(key))
    mydb.commit()
    dbcursor.close()
    mydb.close()


def update_table(table: str, key_col: str, key: int, collumn: str, value):
    mydb = get_connection()
    dbcursor = mydb.cursor()
    dbcursor.execute("UPDATE " + table + " SET " + collumn + " = '" + str(value) + "' WHERE " + key_col + " = " + str(key))
    mydb.commit()
    dbcursor.close()
    mydb.close()


def get_from_table(table: str, key_col: str, key: int, collumn: str):
    mydb = get_connection()
    dbcursor = mydb.cursor()
    dbcursor.execute("SELECT " + collumn + " FROM " + table + " WHERE " + key_col + " = " + str(key))
    for key in dbcursor:
        return key[0]
    dbcursor.close()
    mydb.close()
