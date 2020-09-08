import subprocess
import sys
import logger

log_req = logger.Logger("req.log", "/var/log/rfid/req.log")


def install(package):

    if sys.version_info < (3, 6):
        print("You can only run rfid_packet with python3.6 and up...")
        log_req.error("You can only run rfid_packet with python3.6 and up...")
    if sys.version_info == (3, 6):
        try:
            log_req.info("Installing " + package)
            subprocess.call([sys.executable, "-m", "pip3.6", "install", package])
        except ValueError as e:
            log.req.error("Failed to install " + package)
            log.req.critical(e)
            print(e)

    if sys.version_info == (3, 7):
        try:
            log.req.info("Installing " + package)
            subprocess.call([sys.executable, "-m", "pip3.7", "install", package])
        except ValueError as e:
            log.req.error("Failed to install " + package)
            log.req.critical(e)
            print(e)
    if sys.version_info == (3, 8):
        try:
            log.req.info("Installing " + package)
            subprocess.call([sys.executable, "-m", "pip3.8", "install", package])
        except ValueError as e:
            log.req.error("Failed to install " + package)
            log.req.critical(e)
            print(e)