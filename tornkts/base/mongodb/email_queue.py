import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from mongoengine import StringField, BooleanField
from tornkts.base.mongodb.base_document import BaseDocument


class EmailQueue(BaseDocument):
    message = StringField(required=True)
    to = StringField(required=True)
    from_email = StringField(required=False)
    sended = BooleanField(default=False)

    @staticmethod
    def add(username, to, subject, msg, msg_type="text"):
        if type(to) != list:
            to = [to, ]

        message = MIMEMultipart('alternative')
        message['From'] = username
        message['Subject'] = subject
        if msg_type == "text":
                msg = MIMEText(msg, 'plain', 'utf-8')
        elif msg_type == "html":
            msg = MIMEText(msg, 'html', 'utf-8')
        message.attach(msg)

        for email in to:
            message['To'] = email
            message_str = message.as_string()
            EmailQueue(message=message_str, from_email=username, to=email).save()

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

        if self.from_email is not None and isinstance(self.from_email, (str, unicode)):
            username = self.from_email

        smtpserver.sendmail(username, self.to, self.message)
        smtpserver.close()
