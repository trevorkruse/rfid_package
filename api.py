import requirements
import logger
import requests
from termcolor import colored

log_api = logger.Logger("api.log", "/var/log/rfid/api.log")

try:
    import requests
except ValueError as e:
    requirements.install("requests")


class Api:

    def __init__(self, key, secret, domain_url):
        self.key = key
        self.secret = secret
        self.domain_url = domain_url
        self.api_path = "/wp-json/llms/v1"

    def get_api_keys(self):
        path = "/api-keys"
        url = self.domain_url + self.api_path + path

        try:
            log_api.info("Getting API keys at " + url)
            request = requests.get(url=url, auth=(self.key, self.secret))
            return request.json()
        except ValueError as e:
            log_api.error(e)

    def get_courses(self):
        path = "/courses"
        url = self.domain_url + self.api_path + path

        try:
            log_api.info("Getting Courses at " + url)
            request = requests.get(url=url, auth=(self.key, self.secret))
            return request.json()
        except ValueError as e:
            log_api.error(e)

    def get_course_id(self, tool_name):
        path = "/courses"
        url = self.domain_url + self.api_path + path
        try:
            log_api.info("Getting Course ID at " + url + " With tool: " + tool_name)
            request = requests.get(url=url, auth=(self.key, self.secret))
            data = request.json()
            x = 0
            while x < len(data):
                if data[x]['title']['rendered'] == tool_name:
                    log_api.info("Course ID: " + str(data[x]['id']))
                    return data[x]['id']
                else:
                    x = x + 1
        except ValueError as e:
            log_api.error(e)

    def get_student_progress(self, student_id, course_id):
        path = "/students/"
        path2 = "/progress/"
        url = self.domain_url + self.api_path + path + str(student_id) + path2 + str(course_id)
        try:
            log_api.info("Getting Student Progress at " + url)
            request = requests.get(url=url, auth=(self.key, self.secret))
            log_api.info("Student Progress: " + str(request.json()['status']))
            return request.json()['status']
        except ValueError as e:
            log_api.error(e)
