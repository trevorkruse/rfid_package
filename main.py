import sql
import api
import send_mail
import logger
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import time
import readchar
import getch
import keyboard

# main_log = log.setup_logger('main_log', 'main.log')
# main_log.info('This is just info message from main')
log_api = logger.Logger("main_log", "main2.log")

emailReceivers = ['api@email.com', ]
emailSubject = 'Tool ID Was Not Found for '
emailBody = 'A course ID was not returned for '

server = "localhost"
user = ""
passwd = ""
database = ""

key = ""
secret = ""
url = ""

tool_name = "BandSaw"

start_time = 0
tool_start_time = 0

tool_status = False

user_name = None
user_id = None

power_strip_gpio_pin = 3
GPIO.setmode(GPIO.BOARD)
GPIO.setup(power_strip_gpio_pin, GPIO.OUT)  # GPIO Assign mode


#
#
# user_info = conn.get_user_id_and_user_name("123456")
# print(user_info)
# x = None
# user_id, user_name = user_info
#
# print("User id: " + str(user_id))
# print("User Name:" + str(user_name))
#
def turn_tool_on():
    GPIO.output(power_strip_gpio_pin, GPIO.HIGH)


def turn_tool_off():
    GPIO.output(power_strip_gpio_pin, GPIO.LOW)


def get_rfid():
    id = None
    raw_id = None
    print("Place tag by RFID...")
    raw_id = getch.getch()
    id = raw_id.strip("0")
    print(id)
    return id


while True:
    try:
        rfid_id = get_rfid()
        print("This is the RFID Number:" + rfid_id)
        # Turn off tool and gather tool data
        if tool_status is True:
            try:
                print("Killing power to tool...")
                turn_tool_off()
                tool_elapsed_time = time.time() - tool_start_time
                print("Sending tool data to server...")
                conn = sql.Database(database, user, passwd)
                conn.insert_tool_data(tool_name, tool_elapsed_time, user_name, user_id)
                conn.commit()
                conn.close()
                conn.close_ssh()
                tool_status = False
            except ValueError as e:
                tool_status = False
                print(e)
        else:
            try:
                try:
                    conn = sql.Database(database, user, passwd)
                    user_id, user_name = conn.get_user_id_and_user_name(rfid_id)
                    conn.close()
                    conn.close_ssh()
                except ValueError as e:
                    print("Failed to connect to the database...")
                    print(e)
                print("User id: " + str(user_id))
                print("User Name:" + str(user_name))
                api_call = api.Api(key, secret, url)
                course_id = api_call.get_course_id(tool_name)
                student_progress = api_call.get_student_progress(user_id, course_id)
                print(student_progress)
                if student_progress == "complete":
                    try:
                        turn_tool_on()
                        tool_status = True
                        tool_start_time = time.time()
                        print("Tool time has started...")
                        print("Granting access to tool.")
                        student_progress = None
                    except ValueError as e:
                        print(e)
                else:
                    print("Student hasn't completed the required class for this tool.")
            except ValueError as e:
                print(e)

    finally:
        print("done")
        #



