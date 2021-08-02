import smtplib
from email.mime.text import MIMEText
import conf


def sendEmail(title, content):
    message = MIMEText(content, 'plain', 'utf-8')
    message['Subject'] = title
    message['From'] = conf.sender
    message['To'] = ",".join(conf.receivers)


    try:
        smtpobj = smtplib.SMTP_SSL(conf.mail_host, 465)
        smtpobj.login(conf.mail_user, conf.mail_pass)
        smtpobj.sendmail(conf.sender, conf.receivers, message.as_string())
    except smtplib.SMTPException as e:
        print(f'e')


if __name__ == '__main__':
    sendEmail()
