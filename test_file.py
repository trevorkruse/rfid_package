import sql
import time




_host = 'az1-ss14.a2hosting.com'
_ssh_port = 7822
_username = 'minneso5'
_password = 'y]m7nZw!BJ59Z2'
_db_name = "minneso5_qubix"

conn = sql.Database(_host, _db_name, _username, _password, _ssh_port)

user_info = conn.get_user_id_and_user_name("123456")
print(user_info)

# print(conn.get_server_info())
# time.sleep(5)
# print(conn.get_all_users())
conn.close()
conn.close_ssh()