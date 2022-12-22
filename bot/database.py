import mysql.connector

mydb = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    password = '12346789',
    database = 'gptbotdb'
)


def add_server(id: int, name: str, cmd_prefix: str = '$', openai_key: str = None) -> None:
    dbcursor = mydb.cursor()
    sql = "INSERT INTO dservers (server_id, server_name, cmd_prefix, openai_key) VALUES (%s, %s, %s, %s)"
    val = (id, name, cmd_prefix, openai_key)
    dbcursor.execute(sql, val)
    mydb.commit()


def get_ai_key(server_id: int):
    return get_from_dserver_table(server_id, "openai_key")


def get_cmd_prefix(server_id: int):
    return get_from_dserver_table(server_id, "cmd_prefix")


def get_from_dserver_table(server_id: int, collumn: str):
    dbcursor = mydb.cursor()
    dbcursor.execute("SELECT " + collumn + " FROM dservers WHERE server_id = " + str(server_id))
    for key in dbcursor:
        return key[0]


def update_openai_key(server_id: int, key: int):
    update_dserver(server_id, "openai_key", key)

def update_prefix(server_id: int, prefix: str):
    update_dserver(server_id, "cmd_prefix", prefix)


def update_dserver(server_id: int, collumn: str, value: str):
    dbcursor = mydb.cursor()
    dbcursor.execute("UPDATE dservers SET " + collumn + " = '" + value + "' WHERE server_id = " + str(server_id))
    mydb.commit()
