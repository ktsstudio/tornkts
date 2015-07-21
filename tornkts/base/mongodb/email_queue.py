from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

from mongoengine import StringField, BooleanField

from tornkts.base.mongodb.base_document import BaseDocument


class EmailQueue(BaseDocument):

    message = StringField(required=True)
    to = StringField(required=True)
    sended = BooleanField(default=False)

    @staticmethod
    def add(username, to, subject, msg, type="text"):

        message = MIMEMultipart('alternative')
        message['From'] = username
        message['To'] = to
        message['Subject'] = subject

        if type == "text":
            msg = MIMEText(msg, 'plain', 'utf-8')
        elif type == "html":
            msg = MIMEText(msg, 'html', 'utf-8')

        message.attach(msg)
        message = message.as_string()

        EmailQueue(message=message, to=to).save()

    @staticmethod
    def send(application):
        emails = EmailQueue.objects(sended=False)
        for email in emails:
            email._send_mail(application)
            email.delete()

    def _send_mail(self, app):
        username = app.settings["email_username"]
        password = app.settings["email_password"]

        smtpserver = smtplib.SMTP("smtp.gmail.com", 587)

        smtpserver.ehlo()
        smtpserver.starttls()
        smtpserver.login(username, password)

        smtpserver.sendmail(username, self.to, self.message)
        smtpserver.close()