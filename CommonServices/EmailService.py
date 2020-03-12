"""
If ever faced with the exception:
"smtplib.SMTPAuthenticationError: (535, b'5.7.8 Username and Password not accepted)",
1. Check Username/Sender's Email and Password.
2. Check google account for if the access to less secure apps is enabled in the account settings.
"""

import smtplib
# the MIMEText class is used to create MIME objects of major type text
from email.mime.text import MIMEText

# A subclass of MIMEBase, this is an intermediate base class for MIME messages that are multipart
from email.mime.multipart import MIMEMultipart


class EmailSender():
    def __init__(self, receiver, subject, body):
        self.email_sender = 'ticketsoftware2020@gmail.com'
        self.password = '9bg8!a41ph'
        self.email_receiver = receiver
        self.subject = subject
        self.body = body

    def sendemail(self):
        try:
            msg = MIMEMultipart()  # used for define multipart message
            msg['From'] = self.email_sender
            msg['To'] = self.email_receiver
            msg['Subject'] = self.subject

            msg.attach(MIMEText(self.body,
                                'plain'))  # attach body to the message, here email is plain so email type plain is used
            text = msg.as_string()  # used for converting object into plain text string

            connection = smtplib.SMTP('smtp.gmail.com', 587)
            connection.starttls()
            connection.login(self.email_sender, self.password)
            connection.sendmail(self.email_sender, self.email_receiver, text)
            connection.quit()
        except Exception as e:
            print(e)
            pass
