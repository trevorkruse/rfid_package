import sshtunnel
import mysql.connector

server = "localhost"
_db_user = "minneso5_qubix"
_db_password = "8Ze5S!1-sp"
_db_name = "minneso5_qubix"

_host = 'az1-ss14.a2hosting.com'
_ssh_port = 7822
_username = ''
_password = ''

_remote_bind_address = '127.0.0.1'
_local_bind_address = '0.0.0.0'
_remote_mysql_port = 3306
_local_mysql_port = 3306
# ssh -p 7822 username@example.com -L 3306:localhost:3306
tunnel = sshtunnel.SSHTunnelForwarder(
        (_host, _ssh_port),
        ssh_username=_username,
        ssh_password=_password,
        remote_bind_address=(_remote_bind_address, _remote_mysql_port),
        local_bind_address=(_local_bind_address, _local_mysql_port))
# ) as tunnel:
#     connection = mysql.connector.connect(
#         user=_db_user,
#         password=_db_password,
#         host=_local_bind_address,
#         database=_db_name,
#         port=_local_mysql_port)
#     cursor = connection.cursor()
tunnel.start()
connection = mysql.connector.connect(
        user=_db_user,
        password=_db_password,
        host=_local_bind_address,
        database=_db_name,
        port=_local_mysql_port)
cursor = connection.cursor()
print(connection.get_server_info())

users = cursor.execute("SELECT * FROM qubi_users")
print(users.fetchall())

tunnel.stop()
