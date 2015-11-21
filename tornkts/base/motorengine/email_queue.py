import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from motorengine import StringField, BooleanField
from tornkts.base.motorengine.base_document import BaseDocument


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
        settings = app.settings.get('email', {})

        host = settings.get("host")
        port = settings.get("port")
        username = settings.get("username")
        password = settings.get("password")

        smtpserver = smtplib.SMTP(host, port)

        smtpserver.ehlo()
        if settings.get('use_tls'):
            smtpserver.starttls()
        if password:
            smtpserver.login(username, password)

        smtpserver.sendmail(username, self.to, self.message)
        smtpserver.close()
