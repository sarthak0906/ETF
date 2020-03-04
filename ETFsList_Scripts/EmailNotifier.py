import smtplib


class SendEmail(object):

    def __init__(self, subject, body):
        self.subject = subject
        self.body = body

    def sendemail(self):
        gmail_user = 'ticketsoftware2020@gmail.com'
        gmail_password = '9bg8!a41ph'

        sent_from = gmail_user
        to = ['kshitizsharmav@gmail.com', 'piyush888@gmail.com']

        message = 'Subject: {}\n\n{}'.format(self.subject, self.body)

        try:
            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server.ehlo()
            server.login(gmail_user, gmail_password)
            server.sendmail(sent_from, to, message)
            server.close()

            print('Email sent!')
        except Exception as e:
            print(e)
            print('Something went wrong...')

# SendEmail('subject','message').sendemail()
