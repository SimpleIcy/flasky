from flask_mail import Message
from flask import render_template
from ..configuration import config
from . import mail
from threading import Thread
from ..flasky import app


def send_async_email(appname, msg):
    with appname.app_context():
        mail.send(msg)
    

def send_email(to, subject, template, **kwargs):
    msg = Message(config.get('FLASKY_MAIL_SUBJECT_PREFIX') + subject,
                  sender=config.get('FLASKY_MAIL_SENDER'), recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template+'.html', **kwargs)
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return thr
