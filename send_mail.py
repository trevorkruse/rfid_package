import smtplib

# Credentials
from_address = 'wpserverdmd@gmail.com'
password = ''


def send(receivers, subject, text):
    message = 'Subject: {}\n\n{}'.format(subject, text)
    # print(message)
    try:

        # The actual mail send
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.starttls()
        server.login(from_address, password)
        server.sendmail(from_address, receivers, message)
        server.quit()
        print("Successfully sent email")
    except ValueError:
        print("Error: unable to send email")
