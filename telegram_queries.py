import json
import sqlite3

DATABASE = 'telegram.db'

conn = sqlite3.connect(DATABASE)
c = conn.cursor()

sql_get_users = "SELECT peer_id FROM tg_user"
sql_get_users_n_name = "SELECT peer_id,first_name FROM tg_user"
sql_get_chats = "SELECT peer_id, title FROM tg_chat"
sql_get_chats_n_title = "SELECT peer_id,title title FROM tg_chat"
sql_get_user_first_name = "SELECT first_name FROM tg_user WHERE peer_id=? LIMIT 1"
sql_get_peer_id_by_username = "SELECT peer_id FROM tg_user WHERE username=?"
sql_get_peer_id_by_first_and_last_name ="SELECT peer_id FROM tg_user WHERE first_name=? AND last_name=?"
sql_get_peer_id_by_first_name = "SELECT peer_id FROM tg_user WHERE first_name=?"
sql_get_peer_id_by_last_name = "SELECT peer_id FROM tg_user WHERE last_name=?"
sql_get_groups_of_user="SELECT tg_chat_peer_id FROM tg_user_tg_chat WHERE tg_user_peer_id=?"
sql_get_groups_in_common="""
SELECT tg_chat_peer_id FROM tg_user_tg_chat WHERE tg_user_peer_id=?
INTERSECT
SELECT tg_chat_peer_id FROM tg_user_tg_chat WHERE tg_user_peer_id=?
"""


def get_users():
    c.execute(sql_get_users)
    users = c.fetchall()
    return list(map(lambda x: x[0], users))

def get_users_n_names():
    c.execute(sql_get_users_n_name)
    users = c.fetchall()
    return users

def get_groups():
    c.execute(sql_get_chats)
    groups = c.fetchall()
    return groups

def get_groups_n_title():
    c.execute(sql_get_chats_n_title)
    groups = c.fetchall()
    return groups

def get_user_first_name(peer_id):
    c.execute(sql_get_user_first_name,(peer_id,))
    response = c.fetchall()
    if len(response > 0):
        return response[0][0]
    return "unknown_first_name"

def get_user_peer_id(username="",first_name="",last_name=""):
    if username != "":
        c.execute(sql_get_peer_id_by_username,(username,))
    elif first_name != "" and last_name != "":
        c.execute(sql_get_peer_id_by_first_and_last_name,(first_name,last_name))
    elif first_name != "":
        c.execute(sql_get_peer_id_by_first_name,(first_name,))
    elif last_name != "":
        c.execute(sql_get_peer_id_by_last_name,(last_name,))
    else:
        return 0
    response = c.fetchall()
    if len(response) > 0:
        return response[0][0]
    return 0

def get_groups_of_user(peer_id):
    c.execute(sql_get_groups_of_user,(peer_id,))
    response = c.fetchall()
    if len(response) > 0:
        return list(map(lambda x: x[0], response))
    return []

def get_groups_in_common(peer_id1,peer_id2):
    c.execute(sql_get_groups_in_common,(peer_id1,peer_id2))
    response = c.fetchall()
    if len(response) > 0:
        return list(map(lambda x: x[0], response))
    return []


