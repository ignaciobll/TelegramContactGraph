import json, sqlite3
import time
from pytg.sender import Sender

DATABASE = 'telegram.db'
LIMIT = 10000

conn = sqlite3.connect(DATABASE)
c = conn.cursor()

sender = Sender(host="localhost", port=4458)

print("Let's request about your dialog...")

def dialog_list(timeout=20):
    try:
        return sender.dialog_list(LIMIT)
    except Exception:
        print("Wooops, dialog_list failed. Just {} more times...".format(timeout))
        time.sleep(1)
        return dialog_list(timeout-1)

def chat_info(name,timeout=10):
    try:
        if timeout == 0:
            print("NOOOOOO, it was impossible to get the info of {}...".format(name))
            return {}
        return sender.chat_info(name)
    except Exception:
        print("Wooops, chat_info failed. Just {} more times...".format(timeout))
        time.sleep(1)
        return chat_info(name,timeout-1)

def channel_get_members(name,timeout=5):
    try:
        if timeout == 0:
            print("NOOOOOO, it was impossible to get the info of {}...".format(name))
            print("Maybe it's because YOU HAVE NO POWER HERE. Tsss. Evil.")
            return []
        return sender.channel_get_members(name,LIMIT)
    except Exception:
        print("Wooops, channel_get_members failed. Just {} more times...".format(timeout))
        time.sleep(1)
        return channel_get_members(name,timeout-1)


j_dialog = json.loads(json.dumps(dialog_list()))

sql_add_user = "INSERT OR IGNORE INTO tg_user (peer_id, print_name, first_name, last_name, username) VALUES (?,?,?,?,?) "
sql_add_chat = "INSERT INTO tg_chat (peer_id, print_name, title) VALUES (?,?,?)"
sql_relation_user_char = "INSERT INTO tg_user_tg_chat (id, tg_user_peer_id, tg_chat_peer_id) VALUES (?,?,?)"

def add_user(entry):
    print_name, peer_id, first_name, last_name, username = "",0,"","",""
    if 'print_name' in entry.keys():
        if not (entry['print_name'] == ""):
            print_name = entry['print_name']
            peer_id = entry['peer_id']
            if 'first_name' in entry.keys():
                first_name = entry['first_name']
            if 'last_name' in entry.keys():
                last_name = entry['last_name']
            if 'username' in entry.keys():
                username = entry['username']
            c.execute(sql_add_user,(peer_id, print_name, first_name, last_name, username))
        else: print("LOG: woops, print name is a void string")
    else: print("LOG: not print_name in keys.")


def add_members(entry):
    members = []
    info = {}
    print_name = entry['print_name']
    print(print_name)
    if entry['peer_type'] == 'channel':
        members = channel_get_members(print_name)
    if entry['peer_type'] == 'chat':
        info = chat_info(print_name)
        if 'members' in info.keys():
            members = info['members']
    for m in range(0,len(members)):
        add_user(members[m])
        chat_id, chat_id, member_id = 0,0,0
        chat_id, member_id = entry['peer_id'], members[m]['peer_id']
        table_id = chat_id*(100000000) +  member_id # 10 ^ 8
        if table_id != 0:
            c.execute(sql_relation_user_char,(table_id, member_id, chat_id))


def add_chat(entry):
    peer_id, print_name, title = 0, "", ""
    if 'peer_id' in entry.keys():
        peer_id = entry['peer_id']
    if 'print_name' in entry.keys():
        print_name = entry['print_name']
    if 'title' in entry.keys():
        title = entry['title']
    if (peer_id != 0): c.execute(sql_add_chat,(peer_id, print_name, title))

for i in range(0,len(j_dialog)):
    if 'peer_type' in j_dialog[i].keys():
        if j_dialog[i]['peer_type'] == 'user':
            add_user(j_dialog[i])
        if j_dialog[i]['peer_type'] == 'chat' or j_dialog[i]['peer_type'] == 'channel':
            add_chat(j_dialog[i])
            add_members(j_dialog[i])

conn.commit()
conn.close()
