import logger
import time
import datetime
import requirements

sql_log = logger.Logger("sql.log", "/var/log/rfid/sql.log")

try:
    import mysql.connector
except ValueError as e:
    requirements.install("mysql-connector-python")
try:
    import sshtunnel
except ValueError as e:
    requirements.install("sshtunnel")


cursor = None
conn = None

db_prefix = "mmo_"

_remote_bind_address = '127.0.0.1'
_local_bind_address = '0.0.0.0'
_remote_mysql_port = 3306
_local_mysql_port = 3306

_host = 'az1-ss14.a2hosting.com'
_ssh_port = 7822
ssh_username = ''
ssh_password = ''


class Database:

    def __init__(self, _db_name, _db_username, _db_password):

        print("Connecting...")
        try:
            sql_log.info("Starting ssh tunnel...")
            self.tunnel = sshtunnel.SSHTunnelForwarder(
                (_host, _ssh_port),
                ssh_username=ssh_username,
                ssh_password=ssh_password,
                remote_bind_address=(_remote_bind_address, _remote_mysql_port),
                local_bind_address=(_local_bind_address, _local_mysql_port))
        except ValueError as e:
            sql_log.error("Failed to start ssh tunnel, see error...")
            sql_log.critical(e)
        try:
            sql_log.info("Started ssh tunnel..")
            self.tunnel.start()
        except ValueError as e:
            sql_log.error("Can not start ssh tunnel, see error....")
            sql_log.critical(e)
        sql_log.info("Connecting to db....")
        try:
            sql_log.info("Connected to db....")
            self.conn = mysql.connector.connect(
                user=_db_username,
                password=_db_password,
                host=_local_bind_address,
                database=_db_name,
                port=_local_mysql_port,
                charset='utf8')
            self.cursor = self.conn.cursor()
        except ValueError as e:
            sql_log.error("Failed to connect to db, see error....")
            sql_log.critical(e)

    def get_user_rfid_number_with_user_login(self, username):
        sql = "SELECT rfid FROM " + db_prefix + "users WHERE user_login = %s"
        try:
            self.cursor.execute(sql, (username,))
        except ValueError as e:
            sql_log.error("Failed to run query... " + sql)
            sql_log.critical(e)
        return self.cursor.fetchone()

    def get_user_id_and_user_name(self, rfid_number):
        sql = "SELECT ID, user_login FROM " + db_prefix + "users WHERE rfid = %s"
        try:
            self.cursor.execute(sql, (rfid_number,))
        except ValueError as e:
            sql_log.error("Failed to run query... " + sql)
            sql_log.critical(e)
        return self.cursor.fetchone()

    def update_user_rfid_number(self, username, rfid_number):
        sql = "UPDATE " + db_prefix + "users SET rfid = %s WHERE user_login = %s"
        try:
            self.cursor.execute(sql, (rfid_number, username,))
        except ValueError as e:
            sql_log.error("Failed to run query... " + sql)
            sql_log.critical(e)

    def delete_user_rfid_number(self, username, rfid_number):
        sql = "UPDATE " + db_prefix + "users SET rfid = 0 WHERE user_login = %s AND rfid = %s"
        try:
            self.cursor.execute(sql, (username, rfid_number,))
        except ValueError as e:
            sql_log.error("Failed to run query... " + sql)
            sql_log.critical(e)

    def insert_tool_data(self, tool_name, elapsed_time, member, member_id):
        sql = "INSERT INTO " + db_prefix + "tool_data (tool_name, elapsed_time, member, user_id) VALUES (%s, %s, %s, %s)"
        print(sql)
        print(tool_name, elapsed_time, member, member_id)
        val = (tool_name, elapsed_time, member, member_id)

        try:
            self.cursor.execute(sql, val)
        except ValueError as e:
            sql_log.error("Failed to run query... " + sql)
            sql_log.critical(e)

    def close(self):
        try:
            self.cursor.close()
            self.conn.close()
        except ValueError as e:
            sql_log.error("Failed to close sql...")
            sql_log.critical(e)

    def commit(self):
        try:
            self.conn.commit()
        except ValueError as e:
            sql_log.error("Failed to commit transaction...")
            sql_log.critical(e)

    def get_server_info(self):
        try:
            return self.conn.get_server_info()
        except ValueError as e:
            sql_log.error("Failed to get server info...")
            sql_log.critical(e)

    def close_ssh(self):
        try:
            return self.tunnel.stop()
        except ValueError as e:
            sql_log.error("Failed to stop ssh tunnel...")
            sql_log.critical(e)
